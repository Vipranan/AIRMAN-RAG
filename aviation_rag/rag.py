"""
rag.py - RAG Pipeline for aviation document Q&A using LangChain
Handles retrieval, generation, and faithfulness checking
"""

import os
import json
import re
from typing import List, Dict
import requests
from loguru import logger

# LangChain imports
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama

import config


class RAGPipeline:
    """Complete RAG pipeline for aviation document Q&A using LangChain"""
    
    def __init__(self):
        self.logger = logger
        self._load_vectorstore()
        self._load_metadata()
        self._setup_llm()
        self._verify_ollama()
    
    def _load_vectorstore(self):
        """Load FAISS vector store using LangChain"""
        index_path = config.FAISS_INDEX_DIR
        
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}. Run ingest.py first.")
        
        # Check for GPU availability
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Initialize embeddings with GPU support
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Load FAISS vector store
        self.vectorstore = FAISS.load_local(
            index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        self.logger.info(f"Loaded FAISS vector store from {index_path} (device: {device})")
    
    def _load_metadata(self):
        """Load metadata from disk"""
        with open(config.METADATA_PATH, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        self.logger.info(f"Loaded {len(self.metadata)} metadata entries")
    
    def _setup_llm(self):
        """Setup Ollama LLM using LangChain"""
        self.llm = Ollama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=config.OLLAMA_TEMPERATURE,
            num_predict=config.OLLAMA_MAX_TOKENS
        )
        
        # Define prompt template
        template = """You are an aviation document assistant. Your knowledge source is the
context provided below from official aviation documents including PPL/CPL/ATPL textbooks,
SOPs, and Flight Manuals.

INSTRUCTIONS:
1. Answer questions using the information in the provided context.
2. For factual questions: Provide direct information from the context.
3. For applied/reasoning questions: You may synthesize and combine information from
   multiple parts of the context to provide a complete answer.
4. You may make reasonable inferences based on the context, but clearly indicate when
   you are doing so (e.g., "Based on the principles described...").
5. If the context lacks sufficient information to answer the question adequately,
   respond with: "This information is not available in the provided document(s)."
6. Always cite which source document and page your answer comes from.
7. Be concise but thorough in your explanations.

<context>
{context}
</context>

<question>
{question}
</question>

Answer:"""
        
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.logger.info("LLM configured with Ollama")
    
    def _verify_ollama(self):
        """Verify Ollama is reachable"""
        try:
            response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5)
            response.raise_for_status()
            self.logger.info("Ollama connection verified")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Cannot reach Ollama at {config.OLLAMA_BASE_URL}. "
                f"Make sure Ollama is running. Error: {e}"
            )
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Retrieve relevant chunks for a query using LangChain
        
        Args:
            query: User question
            top_k: Number of results to return (default from config)
        
        Returns:
            List of dicts with chunk_id, doc_name, page, text, similarity_score
        """
        if top_k is None:
            top_k = config.TOP_K
        
        # Use LangChain's similarity search with scores
        docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=top_k)
        
        # Filter by similarity threshold and build results
        results = []
        for doc, score in docs_with_scores:
            # FAISS returns distance, convert to similarity (for normalized vectors, distance = 2 - 2*similarity)
            # But with IndexFlatIP on normalized vectors, score IS the cosine similarity
            similarity = float(score)
            
            if similarity >= config.SIMILARITY_THRESHOLD:
                results.append({
                    "chunk_id": doc.metadata.get('chunk_id', 'unknown'),
                    "doc_name": doc.metadata.get('doc_name', 'unknown'),
                    "page": doc.metadata.get('page', 0),
                    "text": doc.page_content,
                    "similarity_score": similarity
                })
        
        self.logger.debug(f"Retrieved {len(results)} chunks above threshold {config.SIMILARITY_THRESHOLD}")
        return results
    
    def check_faithfulness(self, answer: str, chunks: List[Dict]) -> float:
        """
        Check if answer is faithful to retrieved context
        Uses improved algorithm with better word matching
        
        Args:
            answer: Generated answer
            chunks: Retrieved chunks
        
        Returns:
            Faithfulness score (0.0-1.0)
        """
        if answer == config.NO_ANSWER_RESPONSE:
            return 1.0  # No-answer is always faithful
        
        # Concatenate all chunk texts
        context = " ".join([chunk["text"] for chunk in chunks])
        context_lower = context.lower()
        answer_lower = answer.lower()
        
        # Remove common words and punctuation for better matching
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                      'this', 'that', 'these', 'those', 'it', 'its', 'as', 'which', 'what'}
        
        # Extract meaningful words from answer (3+ chars, not stop words)
        answer_words = [w.strip('.,!?;:()[]{}') for w in answer_lower.split()]
        answer_words = [w for w in answer_words if len(w) >= 3 and w not in stop_words]
        
        if not answer_words:
            return 0.5  # Neutral score if no meaningful words
        
        # Check how many answer words appear in context
        matched = 0
        for word in answer_words:
            if word in context_lower:
                matched += 1
        
        # Calculate base score
        base_score = matched / len(answer_words) if answer_words else 0.0
        
        # Bonus: Check for exact phrase matches (3+ word sequences)
        answer_phrases = []
        words = answer_lower.split()
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 10:  # Only meaningful phrases
                answer_phrases.append(phrase)
        
        phrase_matches = sum(1 for phrase in answer_phrases if phrase in context_lower)
        phrase_bonus = 0.2 * (phrase_matches / len(answer_phrases)) if answer_phrases else 0.0
        
        # Final score with phrase bonus
        final_score = min(1.0, base_score + phrase_bonus)
        
        self.logger.debug(f"Faithfulness: {matched}/{len(answer_words)} words matched, "
                         f"{phrase_matches}/{len(answer_phrases) if answer_phrases else 0} phrases = {final_score:.2f}")
        
        return final_score
    
    def generate_answer(self, question: str, chunks: List[Dict]) -> str:
        """
        Generate answer using LangChain and Ollama
        
        Args:
            question: User question
            chunks: Retrieved chunks
        
        Returns:
            Generated answer
        """
        # Build context string with citations
        context_parts = []
        for chunk in chunks:
            context_parts.append(
                f"[Source: {chunk['doc_name']}, Page: {chunk['page']}]\n{chunk['text']}"
            )
        context = "\n\n".join(context_parts)
        
        # Generate answer using LangChain prompt
        try:
            # Format the prompt
            formatted_prompt = self.prompt.format(context=context, question=question)
            # Invoke the LLM directly
            answer = self.llm.invoke(formatted_prompt)
            return answer.strip()
        
        except Exception as e:
            self.logger.error(f"LLM generation error: {e}")
            raise
    
    def ask(self, question: str, top_k: int = None, debug: bool = False) -> Dict:
        """
        Complete RAG pipeline: retrieve, generate, check faithfulness
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            debug: Include retrieved chunks in response
        
        Returns:
            Dict with answer, citations, faithfulness_score, and optionally retrieved_chunks
        """
        # Retrieve
        chunks = self.retrieve(question, top_k)
        
        # If no chunks retrieved, return no-answer immediately
        if not chunks:
            self.logger.info("No chunks above similarity threshold")
            return {
                "answer": config.NO_ANSWER_RESPONSE,
                "citations": [],
                "faithfulness_score": 1.0,
                "retrieved_chunks": [] if debug else None
            }
        
        # Generate answer
        answer = self.generate_answer(question, chunks)
        
        # Check faithfulness
        faithfulness_score = self.check_faithfulness(answer, chunks)
        
        # Override with no-answer if faithfulness too low
        if faithfulness_score < config.FAITHFULNESS_THRESHOLD and answer != config.NO_ANSWER_RESPONSE:
            self.logger.warning(f"Low faithfulness ({faithfulness_score:.2f}), overriding with no-answer")
            answer = config.NO_ANSWER_RESPONSE
        
        # Build citations
        citations = [
            {
                "doc_name": chunk["doc_name"],
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"]
            }
            for chunk in chunks
        ]
        
        # Build response
        response = {
            "answer": answer,
            "citations": citations,
            "faithfulness_score": faithfulness_score,
            "retrieved_chunks": chunks if debug else None
        }
        
        return response


if __name__ == "__main__":
    # Simple CLI test
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python rag.py 'Your question here'")
        sys.exit(1)
    
    question = sys.argv[1]
    
    rag = RAGPipeline()
    result = rag.ask(question, debug=True)
    
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {result['answer']}")
    print(f"\nFaithfulness: {result['faithfulness_score']:.2f}")
    print(f"\nCitations:")
    for cite in result['citations']:
        print(f"  - {cite['doc_name']}, Page {cite['page']}")
