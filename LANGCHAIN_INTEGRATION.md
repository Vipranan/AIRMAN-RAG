# LangChain Integration Guide

This document explains how LangChain is integrated into the Aviation Document AI Chat system.

## Overview

The system uses LangChain for:
1. **Document Loading**: `PyPDFLoader` for PDF extraction
2. **Text Splitting**: `RecursiveCharacterTextSplitter` for intelligent chunking
3. **Embeddings**: `HuggingFaceEmbeddings` wrapper
4. **Vector Store**: `FAISS` for similarity search
5. **LLM Integration**: `Ollama` LLM wrapper
6. **Prompt Management**: `PromptTemplate` for structured prompts
7. **Chain Orchestration**: `LLMChain` for combining prompts and LLMs

## Component Breakdown

### 1. Document Ingestion (`ingest.py`)

#### PyPDFLoader
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(pdf_path)
pages = loader.load()  # Returns List[Document] with page metadata
```

**Benefits**:
- Automatic page tracking
- Returns LangChain `Document` objects with metadata
- Handles various PDF formats robustly

#### RecursiveCharacterTextSplitter
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1600,        # ~400 words
    chunk_overlap=200,      # ~50 words
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(pages)
```

**Benefits**:
- Intelligent splitting on natural boundaries (paragraphs, sentences)
- Preserves context with overlap
- Never splits mid-sentence
- Works directly with LangChain Documents

#### HuggingFaceEmbeddings
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="multi-qa-mpnet-base-dot-v1",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

**Benefits**:
- Consistent interface with other LangChain embeddings
- Automatic normalization for cosine similarity
- Easy to swap models

#### FAISS VectorStore
```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(config.FAISS_INDEX_DIR)
```

**Benefits**:
- One-line vector store creation
- Built-in persistence
- Efficient similarity search
- Easy to switch to other vector stores (Chroma, Pinecone, etc.)

---

### 2. RAG Pipeline (`rag.py`)

#### Loading VectorStore
```python
vectorstore = FAISS.load_local(
    index_path,
    embeddings,
    allow_dangerous_deserialization=True
)
```

#### Retrieval
```python
docs_with_scores = vectorstore.similarity_search_with_score(query, k=top_k)

for doc, score in docs_with_scores:
    # doc is a LangChain Document with metadata
    # score is cosine similarity
    if score >= threshold:
        results.append({
            "chunk_id": doc.metadata['chunk_id'],
            "doc_name": doc.metadata['doc_name'],
            "page": doc.metadata['page'],
            "text": doc.page_content,
            "similarity_score": score
        })
```

**Benefits**:
- Returns both documents and similarity scores
- Metadata automatically preserved
- Easy filtering and post-processing

#### Ollama LLM Integration
```python
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.0,
    num_predict=512
)
```

**Benefits**:
- Consistent interface with other LangChain LLMs
- Easy to switch to OpenAI, Anthropic, etc.
- Automatic error handling

#### PromptTemplate
```python
from langchain.prompts import PromptTemplate

template = """You are an aviation document assistant...

<context>
{context}
</context>

<question>
{question}
</question>

Answer:"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)
```

**Benefits**:
- Structured prompt management
- Easy to version and test different prompts
- Clear separation of prompt logic from code

#### LLMChain
```python
from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)
answer = chain.run(context=context, question=question)
```

**Benefits**:
- Combines prompt and LLM in one object
- Automatic prompt formatting
- Easy to extend with memory, callbacks, etc.

---

## Advantages of LangChain Integration

### 1. Modularity
- Each component (loader, splitter, embeddings, vectorstore, LLM) is swappable
- Easy to experiment with different models and configurations

### 2. Standardization
- Consistent interfaces across all components
- Well-documented patterns and best practices
- Large community and ecosystem

### 3. Extensibility
- Easy to add advanced features:
  - **Conversation Memory**: `ConversationBufferMemory`
  - **Agents**: Multi-step reasoning with tools
  - **Hybrid Search**: `EnsembleRetriever` (semantic + keyword)
  - **Re-ranking**: `ContextualCompressionRetriever`
  - **Callbacks**: Logging, monitoring, debugging

### 4. Production-Ready
- Battle-tested components
- Error handling and retries built-in
- Performance optimizations

### 5. Future-Proof
- Easy to migrate to new models (GPT-4, Claude, etc.)
- Easy to switch vector stores (Pinecone, Weaviate, etc.)
- Easy to add new features as LangChain evolves

---

## Migration from Custom Implementation

### Before (Custom)
```python
# Custom PDF extraction
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # Manual cleaning, chunking, etc.

# Custom FAISS index
embeddings = model.encode(texts)
faiss.normalize_L2(embeddings)
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

# Custom Ollama API call
response = requests.post(
    f"{OLLAMA_BASE_URL}/api/generate",
    json={"model": "llama3.1:8b", "prompt": prompt}
)
```

### After (LangChain)
```python
# LangChain PDF loading
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# LangChain text splitting
chunks = text_splitter.split_documents(pages)

# LangChain vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# LangChain LLM chain
chain = LLMChain(llm=llm, prompt=prompt)
answer = chain.run(context=context, question=question)
```

**Result**: Cleaner, more maintainable, and extensible code.

---

## Future Enhancements with LangChain

### 1. Conversation Memory
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
```

### 2. Multi-Hop Reasoning (Agents)
```python
from langchain.agents import initialize_agent, Tool

tools = [
    Tool(name="Search", func=vectorstore.similarity_search),
    Tool(name="Calculator", func=calculator)
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
```

### 3. Hybrid Search
```python
from langchain.retrievers import EnsembleRetriever, BM25Retriever

bm25_retriever = BM25Retriever.from_documents(chunks)
faiss_retriever = vectorstore.as_retriever()

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.5, 0.5]
)
```

### 4. Re-Ranking
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)
```

---

## Conclusion

LangChain provides a robust, extensible foundation for the Aviation Document AI Chat system. The integration enables:
- Cleaner, more maintainable code
- Easy experimentation with different models and configurations
- Straightforward path to advanced features (memory, agents, hybrid search)
- Production-ready components with built-in error handling

The system is now well-positioned for future enhancements and scaling.
