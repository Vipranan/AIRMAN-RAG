"""
rag_hybrid.py - Enhanced RAG Pipeline with Hybrid Retrieval (BM25 + Vector + Reranker)
Level 2 Enhancement: Combines keyword-based and semantic search with cross-encoder reranking
"""

import os
import json
import pickle
from typing import List, Dict, Tuple
import requests
from loguru import logger

# LangChain imports
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama

# BM25 and Reranker
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

import config


class HybridRAGPipeline:
    """
    Enhanced RAG pipeline with hybrid retrieval:
    1. BM25 keyword-based retrieval
    2. Vector semantic retrieval
    3. Reciprocal Rank Fusion (RRF) to combine results
    4. Cross-encoder reranking for final selection
    """
    
    def __init__(self):
        self.logger = logger
        self._load_vectorstore()
        self._load_metadata()
        self._load_bm25_index()
        self._setup_reranker()
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
    
    def _load_bm25_index(self):
        """Load or build BM25 index for keyword-based retrieval"""
        bm25_path = os.path.join(config.FAISS_INDEX_DIR, "bm25_index.pkl")
        
        if os.path.exists(bm25_path):
            # Load existing BM25 index
            with open(bm25_path, 'rb') as f:
                bm25_data = pickle.load(f)
                self.bm25 = bm25_data['bm25']
                self.bm25_chunk_ids = bm25_data['chunk_ids']
            self.logger.info(f"Loaded BM25 index with {len(self.bm25_chunk_ids)} documents")
        else:
            # Build BM25 index from metadata
            self.logger.info("Building BM25 index from metadata...")
            corpus = []
            self.bm25_chunk_ids = []
            
            # Metadata is a list of dictionaries
            for meta in self.metadata:
                # Tokenize text for BM25
                tokens = meta['text'].lower().split()
                corpus.append(tokens)
                self.bm25_chunk_ids.append(meta['chunk_id'])
            
            self.bm25 = BM25Okapi(corpus)
            
            # Save BM25 index
            with open(bm25_path, 'wb') as f:
                pickle.dump({
                    'bm25': self.bm25,
                    'chunk_ids': self.bm25_chunk_ids
                }, f)
            
            self.logger.info(f"Built and saved BM25 index with {len(self.bm25_chunk_ids)} documents")
    
    def _setup_reranker(self):
        """Setup cross-encoder reranker"""
        # Use a lightweight but effective cross-encoder
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.logger.info("Loaded cross-encoder reranker")
    
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
    
    def retrieve_bm25(self, query: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Retrieve using BM25 keyword-based search
        
        Args:
            query: User question
            top_k: Number of results to return
        
        Returns:
            List of (chunk_id, score) tuples
        """
        # Tokenize query
        query_tokens = query.lower().split()
        
        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)
        
        # Get top-k indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        # Return chunk_ids with scores
        results = [(self.bm25_chunk_ids[i], float(scores[i])) for i in top_indices]
        
        self.logger.debug(f"BM25 retrieved {len(results)} chunks")
        return results
    
    def retrieve_vector(self, query: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Retrieve using vector semantic search
        
        Args:
            query: User question
            top_k: Number of results to return
        
        Returns:
            List of (chunk_id, similarity_score) tuples
        """
        # Use LangChain's similarity search with scores
        docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=top_k)
        
        # Extract chunk_ids and scores
        results = []
        for doc, score in docs_with_scores:
            chunk_id = doc.metadata.get('chunk_id', 'unknown')
            similarity = float(score)
            results.append((chunk_id, similarity))
        
        self.logger.debug(f"Vector search retrieved {len(results)} chunks")
        return results
    
    def reciprocal_rank_fusion(
        self,
        bm25_results: List[Tuple[str, float]],
        vector_results: List[Tuple[str, float]],
        k: int = 60
    ) -> List[Tuple[str, float]]:
        """
        Combine BM25 and vector results using Reciprocal Rank Fusion (RRF)
        
        RRF formula: score(d) = sum(1 / (k + rank(d)))
        
        Args:
            bm25_results: List of (chunk_id, score) from BM25
            vector_results: List of (chunk_id, score) from vector search
            k: Constant for RRF (default 60)
        
        Returns:
            List of (chunk_id, rrf_score) sorted by score
        """
        rrf_scores = {}
        
        # Add BM25 ranks
        for rank, (chunk_id, _) in enumerate(bm25_results, start=1):
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k + rank))
        
        # Add vector ranks
        for rank, (chunk_id, _) in enumerate(vector_results, start=1):
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k + rank))
        
        # Sort by RRF score
        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        self.logger.debug(f"RRF combined to {len(sorted_results)} unique chunks")
        return sorted_results
    
    def rerank(self, query: str, chunk_ids: List[str], top_k: int = None) -> List[Dict]:
        """
        Rerank chunks using cross-encoder
        
        Args:
            query: User question
            chunk_ids: List of chunk IDs to rerank
            top_k: Number of results to return (default from config)
        
        Returns:
            List of dicts with chunk_id, doc_name, page, text, rerank_score
        """
        if top_k is None:
            top_k = config.TOP_K
        
        # Create a lookup dictionary for faster access
        metadata_dict = {meta['chunk_id']: meta for meta in self.metadata}
        
        # Prepare query-document pairs for reranker
        pairs = []
        chunk_data = []
        
        for chunk_id in chunk_ids:
            if chunk_id in metadata_dict:
                meta = metadata_dict[chunk_id]
                pairs.append([query, meta['text']])
                chunk_data.append({
                    'chunk_id': chunk_id,
                    'doc_name': meta['doc_name'],
                    'page': meta['page'],
                    'text': meta['text']
                })
        
        # Get reranker scores
        scores = self.reranker.predict(pairs)
        
        # Combine with chunk data and sort
        results = []
        for i, score in enumerate(scores):
            chunk_data[i]['rerank_score'] = float(score)
            results.append(chunk_data[i])
        
        # Sort by rerank score and take top-k
        results.sort(key=lambda x: x['rerank_score'], reverse=True)
        results = results[:top_k]
        
        # Filter by threshold
        results = [r for r in results if r['rerank_score'] >= config.RERANK_THRESHOLD]
        
        self.logger.debug(f"Reranked to {len(results)} chunks above threshold {config.RERANK_THRESHOLD}")
        return results
    
    def retrieve_hybrid(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Complete hybrid retrieval pipeline:
        1. BM25 retrieval
        2. Vector retrieval
        3. RRF fusion
        4. Cross-encoder reranking
        
        Args:
            query: User question
            top_k: Number of final results to return
        
        Returns:
            List of dicts with chunk_id, doc_name, page, text, rerank_score
        """
        # Step 1: BM25 retrieval
        bm25_results = self.retrieve_bm25(query, top_k=20)
        
        # Step 2: Vector retrieval
        vector_results = self.retrieve_vector(query, top_k=20)
        
        # Step 3: RRF fusion
        fused_results = self.reciprocal_rank_fusion(bm25_results, vector_results)
        
        # Take top candidates for reranking (more than final top_k to allow reranker to choose)
        rerank_candidates = [chunk_id for chunk_id, _ in fused_results[:30]]
        
        # Step 4: Rerank
        final_results = self.rerank(query, rerank_candidates, top_k=top_k)
        
        return final_results
    
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
        Complete hybrid RAG pipeline: retrieve, generate, check faithfulness
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            debug: Include retrieved chunks in response
        
        Returns:
            Dict with answer, citations, faithfulness_score, and optionally retrieved_chunks
        """
        # Hybrid retrieval
        chunks = self.retrieve_hybrid(question, top_k)
        
        # If no chunks retrieved, return no-answer immediately
        if not chunks:
            self.logger.info("No chunks above rerank threshold")
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
        print("Usage: python rag_hybrid.py 'Your question here'")
        sys.exit(1)
    
    question = sys.argv[1]
    
    rag = HybridRAGPipeline()
    result = rag.ask(question, debug=True)
    
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {result['answer']}")
    print(f"\nFaithfulness: {result['faithfulness_score']:.2f}")
    print(f"\nCitations:")
    for cite in result['citations']:
        print(f"  - {cite['doc_name']}, Page {cite['page']}")
