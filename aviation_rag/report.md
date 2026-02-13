# Aviation Document AI Chat — Evaluation Report

## 1. System Architecture

### Overview
The Aviation Document AI Chat is a Retrieval-Augmented Generation (RAG) system designed to answer questions strictly from aviation documents including PPL/CPL/ATPL textbooks, SOPs/Checklists, and Flight Manuals (AFM/POH). Built with LangChain for robust document processing and retrieval.

### Components

#### 1.1 Document Ingestion Pipeline (`ingest.py`)
- **PDF Extraction**: Uses LangChain's `PyPDFLoader` to extract text with page tracking
- **Text Splitting**: 
  - `RecursiveCharacterTextSplitter` with intelligent splitting
  - 1600 characters (~400 words) per chunk with 200 character (~50 word) overlap
  - Splits on paragraph/sentence boundaries (never mid-sentence)
  - Rationale: Aviation procedures are dense and context-dependent; overlap preserves cross-boundary references
- **Embedding & Indexing**:
  - `HuggingFaceEmbeddings` with `multi-qa-mpnet-base-dot-v1` (768-dim)
  - `FAISS` vector store with cosine similarity (normalized vectors)
  - Metadata tracking: doc_name, page, chunk_id, word_count

#### 1.2 RAG Pipeline (`rag.py`)
- **Retrieval**: 
  - LangChain's `FAISS.similarity_search_with_score()` for top-K semantic search (default K=5)
  - Similarity threshold: 0.35 (below this → no-answer)
- **Generation**:
  - LLM: LangChain's `Ollama` integration with `llama3.1:8b` (local, temperature=0.0)
  - `PromptTemplate` with strict grounding rules
  - `LLMChain` combines prompt and LLM for streamlined generation
  - Context includes source citations [doc_name, Page N]
- **Faithfulness Check**:
  - Extracts key phrases from answer
  - Verifies presence in retrieved context
  - Threshold: 0.70 (below this → override with no-answer)

#### 1.3 FastAPI Application (`app.py`)
- **Endpoints**:
  - `GET /health`: System status, index stats, Ollama connectivity
  - `POST /ingest`: Trigger document ingestion
  - `POST /ask`: Question answering with optional debug mode
- **Response Format**: answer, citations, faithfulness_score, retrieved_chunks (if debug)

#### 1.4 Evaluation Framework (`evaluate.py`)
- **Metrics**:
  - Retrieval Hit Rate: % of questions where expected keywords found in retrieved chunks
  - Faithfulness Score: Avg faithfulness of generated answers
  - Hallucination Rate: % of answers with faithfulness < threshold
  - No-Answer Rate: % of questions returning no-answer response
  - Answer Match Score: Token overlap with ground truth
  - Latency: Response time per question
- **Categories**: Factual (20), Applied (20), Reasoning (10)

---

## 2. Configuration Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| CHUNK_SIZE | 400 words | Fits one procedure/concept section |
| CHUNK_OVERLAP | 50 words | Preserves cross-boundary references |
| EMBEDDING_MODEL | multi-qa-mpnet-base-dot-v1 | Optimized for Q&A retrieval |
| TOP_K | 5 | Balance between context and noise |
| SIMILARITY_THRESHOLD | 0.35 | Filters irrelevant chunks |
| FAITHFULNESS_THRESHOLD | 0.70 | Prevents hallucinations |
| OLLAMA_TEMPERATURE | 0.0 | Deterministic, factual responses |
| OLLAMA_MAX_TOKENS | 512 | Concise answers |

---

## 3. Evaluation Results

### 3.1 Summary Metrics

*Note: This section will be auto-populated by `evaluate.py` after running evaluation with ground truth answers.*

```
┌─────────────────────────────────┬────────────────┬───────────────┬──────────────────┐
│ Metric                          │ Factual (n=20) │ Applied(n=20) │ Reasoning (n=10) │
├─────────────────────────────────┼────────────────┼───────────────┼──────────────────┤
│ Retrieval Hit Rate              │ 0.XX           │ 0.XX          │ 0.XX             │
│ Avg Faithfulness Score          │ 0.XX           │ 0.XX          │ 0.XX             │
│ Hallucination Rate              │ 0.XX           │ 0.XX          │ 0.XX             │
│ No-Answer Rate                  │ 0.XX           │ 0.XX          │ 0.XX             │
│ Avg Answer Match Score          │ 0.XX           │ 0.XX          │ 0.XX             │
│ Avg Latency (ms)                │ XXXX           │ XXXX          │ XXXX             │
└─────────────────────────────────┴────────────────┴───────────────┴──────────────────┘
```

### 3.2 Per-Category Analysis

#### Factual Questions (IDs 1-20)
- **Characteristics**: Direct lookups, definitions, limits
- **Expected Performance**: High retrieval hit rate, high faithfulness
- **Observations**: [To be filled after evaluation]

#### Applied Questions (IDs 21-40)
- **Characteristics**: Scenario-based, procedural, decision-making
- **Expected Performance**: Moderate retrieval, requires multi-chunk synthesis
- **Observations**: [To be filled after evaluation]

#### Reasoning Questions (IDs 41-50)
- **Characteristics**: Multi-step, trade-offs, explanations
- **Expected Performance**: Lower retrieval hit, higher no-answer rate
- **Observations**: [To be filled after evaluation]

---

## 4. Sample Question Analysis

### Example 1: Factual Question
**Q**: What does VFR stand for and what does it require?

**Retrieved Chunks**: [To be filled]

**Answer**: [To be filled]

**Faithfulness Score**: [To be filled]

**Analysis**: [To be filled]

---

### Example 2: Applied Question
**Q**: If the outside air temperature is higher than standard, how does this affect density altitude and aircraft performance?

**Retrieved Chunks**: [To be filled]

**Answer**: [To be filled]

**Faithfulness Score**: [To be filled]

**Analysis**: [To be filled]

---

### Example 3: Reasoning Question
**Q**: Why is it dangerous to fly through a thunderstorm, and what are the recommended avoidance procedures?

**Retrieved Chunks**: [To be filled]

**Answer**: [To be filled]

**Faithfulness Score**: [To be filled]

**Analysis**: [To be filled]

---

## 5. Failure Analysis

### 5.1 Retrieval Failures
- **Definition**: Questions where no relevant chunks retrieved (similarity < threshold)
- **Count**: [To be filled]
- **Common Patterns**: [To be filled]
- **Mitigation**: Adjust chunking strategy, lower threshold, add synonyms

### 5.2 Generation Failures
- **Definition**: Low faithfulness score or hallucinated content
- **Count**: [To be filled]
- **Common Patterns**: [To be filled]
- **Mitigation**: Strengthen system prompt, adjust temperature, improve context formatting

### 5.3 No-Answer Cases
- **Definition**: System returned "This information is not available..."
- **Count**: [To be filled]
- **Breakdown**:
  - Legitimate (info truly not in docs): [X]
  - False negatives (info present but not retrieved): [X]
- **Analysis**: [To be filled]

---

## 6. Strengths & Limitations

### Strengths
1. **LangChain Integration**: Leverages battle-tested abstractions for document processing and retrieval
2. **Strict Grounding**: Faithfulness check prevents hallucinations
3. **Transparent Citations**: Every answer includes source doc + page
4. **No External Dependencies**: Runs locally with Ollama
5. **Intelligent Chunking**: RecursiveCharacterTextSplitter preserves semantic completeness
6. **Multi-Document Support**: Handles PPL/CPL/ATPL/SOP/AFM simultaneously
7. **Extensible**: Easy to add LangChain features (memory, agents, hybrid search)

### Limitations
1. **Context Window**: Limited to top-K chunks (may miss relevant info in large docs)
2. **No Cross-Chunk Reasoning**: Cannot synthesize info across distant sections
3. **Keyword Dependency**: Retrieval relies on lexical/semantic overlap
4. **No Table/Image Extraction**: PDF text only, misses charts and diagrams
5. **Single-Turn**: No conversation history or follow-up context

---

## 7. Recommendations

### 7.1 Immediate Improvements
- [ ] Add table extraction from PDFs (e.g., performance charts, weight & balance)
- [ ] Implement query expansion (synonyms, aviation acronyms)
- [ ] Add LangChain's ContextualCompressionRetriever for re-ranking
- [ ] Fine-tune similarity threshold per document type

### 7.2 Advanced Enhancements (LangChain Features)
- [ ] Multi-hop reasoning: Use LangChain agents for iterative retrieval
- [ ] Hybrid search: Combine semantic + keyword using EnsembleRetriever
- [ ] Conversation memory: Add ConversationBufferMemory for multi-turn context
- [ ] Document structure awareness: Custom retrievers prioritizing sections like "Limitations", "Procedures"

### 7.3 Production Readiness
- [ ] Add authentication & rate limiting
- [ ] Implement caching for common questions
- [ ] Monitor & log all queries for continuous improvement
- [ ] A/B test different chunking strategies
- [ ] Build feedback loop: users flag incorrect answers

---

## 8. Conclusion

The Aviation Document AI Chat system demonstrates a robust approach to grounded question-answering for aviation documents. The strict faithfulness enforcement and transparent citation system ensure reliability, which is critical for safety-sensitive aviation information.

**Key Takeaway**: The system prioritizes precision over recall — it will return "no answer" rather than risk providing incorrect information. This conservative approach is appropriate for the aviation domain.

**Next Steps**:
1. Fill ground truth answers in `questions.json`
2. Run `python evaluate.py` to populate metrics
3. Analyze failure cases and iterate on chunking/retrieval strategy
4. Deploy for pilot testing with real users

---

## Appendix A: Setup Instructions

### Prerequisites
- Python 3.10+
- Ollama installed and running (`ollama serve`)
- Model downloaded: `ollama pull llama3.1:8b`

### Installation
```bash
cd aviation_rag
pip install -r requirements.txt
```

### Usage
```bash
# 1. Place PDFs in ./documents/
# 2. Ingest documents
python ingest.py

# 3. Start API
uvicorn app:app --reload --port 8000

# 4. Test single question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does VFR stand for?"}'

# 5. Run evaluation (after filling ground truth)
python evaluate.py
```

---

## Appendix B: File Structure

```
aviation_rag/
├── config.py              # All tunable parameters
├── ingest.py              # PDF ingestion pipeline
├── rag.py                 # RAG pipeline (retrieve, generate, check)
├── app.py                 # FastAPI application
├── evaluate.py            # Evaluation script
├── questions.json         # 50 test questions
├── report.md              # This file
├── requirements.txt       # Python dependencies
├── README.md              # Quick start guide
├── data/
│   ├── faiss_index/
│   │   ├── index.faiss    # FAISS vector index
│   │   └── index.pkl      # (unused, kept for compatibility)
│   ├── metadata.json      # Chunk metadata
│   └── eval_results.json  # Evaluation results
└── documents/             # Place PDF files here
    ├── PPL_Textbook.pdf
    ├── CPL_Textbook.pdf
    ├── ATPL_Textbook.pdf
    ├── SOP_Checklist.pdf
    └── AFM_POH.pdf
```

---

*Report generated: [Date to be filled by evaluate.py]*
*System version: 1.0.0 (LangChain-powered)*
