# AIRMAN Aviation RAG - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER LAYER                                  │
│                                                                          │
│  ┌──────────────────┐         ┌──────────────────┐                     │
│  │   Web Browser    │         │   API Client     │                     │
│  │  (Chat Interface)│         │   (curl/Postman) │                     │
│  └────────┬─────────┘         └────────┬─────────┘                     │
│           │                             │                               │
│           └─────────────┬───────────────┘                               │
└─────────────────────────┼─────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          API LAYER (FastAPI)                             │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                                       │  │
│  │  • GET  /          → Web Interface                               │  │
│  │  • GET  /health    → System Status                               │  │
│  │  • POST /ask       → Question Answering                          │  │
│  │  • POST /ingest    → Document Ingestion                          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE (LangChain)                              │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    HYBRID RETRIEVAL                             │    │
│  │                                                                 │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │    │
│  │  │   BM25       │    │   FAISS      │    │ Cross-Encoder│    │    │
│  │  │   Keyword    │    │   Vector     │    │   Reranker   │    │    │
│  │  │   Search     │    │   Semantic   │    │   (MiniLM)   │    │    │
│  │  │              │    │   Search     │    │              │    │    │
│  │  │  Top 20      │    │  Top 20      │    │  Top 5       │    │    │
│  │  └──────┬───────┘    └──────┬───────┘    └──────▲───────┘    │    │
│  │         │                   │                    │            │    │
│  │         └─────────┬─────────┘                    │            │    │
│  │                   ▼                              │            │    │
│  │         ┌──────────────────────┐                 │            │    │
│  │         │ Reciprocal Rank      │                 │            │    │
│  │         │ Fusion (RRF)         │─────────────────┘            │    │
│  │         │ ~38 unique chunks    │                              │    │
│  │         └──────────────────────┘                              │    │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    LLM GENERATION                                │  │
│  │                                                                  │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │  Ollama (Llama 3.1 8B)                                   │  │  │
│  │  │  • Temperature: 0.0 (deterministic)                      │  │  │
│  │  │  • Max tokens: 512                                       │  │  │
│  │  │  • Prompt: Strict grounding instructions                 │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  │                           ▼                                     │  │
│  │  ┌──────────────────────────────────────────────────────────┐  │  │
│  │  │  Faithfulness Check                                      │  │  │
│  │  │  • Extract key phrases from answer                       │  │  │
│  │  │  • Verify presence in retrieved context                  │  │  │
│  │  │  • Threshold: 0.70                                       │  │  │
│  │  │  • Override with "not available" if below threshold      │  │  │
│  │  └──────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE                                         │
│                                                                          │
│  {                                                                       │
│    "answer": "VFR stands for Visual Flight Rules...",                   │
│    "citations": [                                                        │
│      {"doc_name": "...", "page": 157, "chunk_id": "..."}               │
│    ],                                                                    │
│    "faithfulness_score": 0.92,                                          │
│    "retrieved_chunks": [...]  // if debug=true                          │
│  }                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Document Ingestion Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DOCUMENT INGESTION                                │
│                                                                          │
│  PDF Files (8 documents)                                                │
│  ├── Air-Regulation-RK-BALI.pdf                                         │
│  ├── Meteorology full book.pdf                                          │
│  ├── 6-mass-and-balance-and-performance-2014.pdf                        │
│  ├── 7-Flight-Planning-and-Monitoring-2014.pdf                          │
│  ├── 10-General-Navigation-2014.pdf                                     │
│  ├── 11-radio-navigation-2014.pdf                                       │
│  ├── Instruments.pdf                                                    │
│  └── Sample test questions.pdf                                          │
│                                                                          │
│                          ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  LangChain PyPDFLoader                                           │  │
│  │  • Extract text page by page                                     │  │
│  │  • Preserve page numbers                                         │  │
│  │  • Handle multi-column layouts                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                          ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  RecursiveCharacterTextSplitter                                  │  │
│  │  • Chunk size: 400 words (~1600 chars)                           │  │
│  │  • Overlap: 50 words (~200 chars)                                │  │
│  │  • Split on: paragraphs → sentences → words                      │  │
│  │  • Never split mid-sentence                                      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                          ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Metadata Attachment                                             │  │
│  │  • doc_name: "Meteorology full book.pdf"                         │  │
│  │  • page: 157                                                     │  │
│  │  • chunk_id: "meteorology_full_book_p157_c234"                   │  │
│  │  • word_count: 387                                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                          ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Parallel Indexing                                               │  │
│  │                                                                  │  │
│  │  ┌─────────────────────┐      ┌─────────────────────┐          │  │
│  │  │  Vector Index       │      │  Keyword Index      │          │  │
│  │  │  (FAISS)            │      │  (BM25)             │          │  │
│  │  │                     │      │                     │          │  │
│  │  │  HuggingFace        │      │  Tokenize chunks    │          │  │
│  │  │  Embeddings         │      │  Build term freq    │          │  │
│  │  │  (768-dim vectors)  │      │  Compute IDF        │          │  │
│  │  │                     │      │                     │          │  │
│  │  │  Save: index.faiss  │      │  Save: bm25.pkl     │          │  │
│  │  └─────────────────────┘      └─────────────────────┘          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                          ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Metadata Storage                                                │  │
│  │  • Save: metadata.json                                           │  │
│  │  • 3,983 chunks indexed                                          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Hybrid Retrieval Flow (Detailed)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER QUERY                                       │
│              "What does VFR stand for?"                                  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│     BM25 RETRIEVAL        │  │    VECTOR RETRIEVAL       │
│                           │  │                           │
│  1. Tokenize query        │  │  1. Embed query           │
│  2. Compute BM25 scores   │  │     (768-dim vector)      │
│  3. Rank by relevance     │  │  2. FAISS similarity      │
│  4. Return top 20         │  │     search                │
│                           │  │  3. Cosine similarity     │
│  Results:                 │  │  4. Return top 20         │
│  • chunk_234 (score: 8.5) │  │                           │
│  • chunk_157 (score: 7.2) │  │  Results:                 │
│  • chunk_891 (score: 6.8) │  │  • chunk_157 (sim: 0.89)  │
│  • ...                    │  │  • chunk_456 (sim: 0.85)  │
│  • chunk_456 (score: 4.1) │  │  • chunk_234 (sim: 0.82)  │
│  • ...                    │  │  • ...                    │
└───────────┬───────────────┘  └───────────┬───────────────┘
            │                              │
            └──────────┬───────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              RECIPROCAL RANK FUSION (RRF)                                │
│                                                                          │
│  Formula: RRF_score(chunk) = Σ 1/(k + rank_i)                           │
│           where k=60, rank_i = rank in result set i                     │
│                                                                          │
│  Example:                                                                │
│  • chunk_157: rank_BM25=2, rank_Vector=1                                │
│    → RRF = 1/(60+2) + 1/(60+1) = 0.0161 + 0.0164 = 0.0325              │
│                                                                          │
│  • chunk_234: rank_BM25=1, rank_Vector=3                                │
│    → RRF = 1/(60+1) + 1/(60+3) = 0.0164 + 0.0159 = 0.0323              │
│                                                                          │
│  • chunk_456: rank_BM25=20, rank_Vector=2                               │
│    → RRF = 1/(60+20) + 1/(60+2) = 0.0125 + 0.0161 = 0.0286             │
│                                                                          │
│  Output: ~38 unique chunks, ranked by RRF score                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              CROSS-ENCODER RERANKING                                     │
│                                                                          │
│  Model: cross-encoder/ms-marco-MiniLM-L-6-v2                            │
│                                                                          │
│  For each chunk:                                                         │
│    score = CrossEncoder(query, chunk_text)                              │
│                                                                          │
│  Example scores:                                                         │
│  • chunk_157: 4.23  ← High relevance                                    │
│  • chunk_234: 3.87                                                      │
│  • chunk_456: 2.91                                                      │
│  • chunk_891: 1.45                                                      │
│  • chunk_123: -2.1  ← Low relevance (filtered out)                     │
│                                                                          │
│  Filter: Keep only chunks with score > -5.0                             │
│  Select: Top 5 chunks                                                   │
│                                                                          │
│  Final chunks:                                                           │
│  1. chunk_157 (score: 4.23)                                             │
│  2. chunk_234 (score: 3.87)                                             │
│  3. chunk_456 (score: 2.91)                                             │
│  4. chunk_891 (score: 1.45)                                             │
│  5. chunk_678 (score: 0.82)                                             │
└────────────────────────────┬────────────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONTEXT FORMATTING                                    │
│                                                                          │
│  Combine top 5 chunks into context:                                     │
│                                                                          │
│  [Source: 7-Flight-Planning-and-Monitoring-2014.pdf, Page: 157]         │
│  VFR stands for Visual Flight Rules. IFR and VFR flights are            │
│  permitted; IFR flights are subject to ATC service...                   │
│                                                                          │
│  [Source: 7-Flight-Planning-and-Monitoring-2014.pdf, Page: 135]         │
│  The Jeppesen VFR + GPS Chart is designed for VMC (Visual               │
│  Meteorological Conditions) flight in accordance with VFR...            │
│                                                                          │
│  [... 3 more chunks ...]                                                │
└────────────────────────────┬────────────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    LLM GENERATION                                        │
│                                                                          │
│  Prompt Template:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ You are an aviation document assistant. Answer using ONLY       │   │
│  │ the context provided below. If information is not in context,   │   │
│  │ respond: "This information is not available..."                 │   │
│  │                                                                  │   │
│  │ <context>                                                        │   │
│  │ [5 retrieved chunks]                                             │   │
│  │ </context>                                                       │   │
│  │                                                                  │   │
│  │ <question>                                                       │   │
│  │ What does VFR stand for?                                         │   │
│  │ </question>                                                      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                             ▼                                            │
│  Ollama (Llama 3.1 8B) generates:                                       │
│  "VFR stands for Visual Flight Rules. According to the provided         │
│   context, VFR requires visual navigation..."                           │
└────────────────────────────┬────────────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FAITHFULNESS CHECK                                    │
│                                                                          │
│  1. Extract key phrases from answer:                                    │
│     ["VFR", "Visual Flight Rules", "visual navigation"]                 │
│                                                                          │
│  2. Check each phrase in retrieved context:                             │
│     • "VFR" → Found in chunk_157 ✓                                      │
│     • "Visual Flight Rules" → Found in chunk_157 ✓                      │
│     • "visual navigation" → Found in chunk_234 ✓                        │
│                                                                          │
│  3. Compute faithfulness score:                                         │
│     score = phrases_found / total_phrases = 3/3 = 1.00                  │
│                                                                          │
│  4. Check threshold:                                                    │
│     1.00 >= 0.70 ✓ → Answer is faithful                                │
│                                                                          │
│  If score < 0.70:                                                       │
│     Override answer with "This information is not available..."         │
└────────────────────────────┬────────────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FINAL RESPONSE                                   │
│                                                                          │
│  {                                                                       │
│    "answer": "VFR stands for Visual Flight Rules...",                   │
│    "citations": [                                                        │
│      {                                                                   │
│        "doc_name": "7-Flight-Planning-and-Monitoring-2014.pdf",         │
│        "page": 157,                                                     │
│        "chunk_id": "7_flight_planning_and_monitoring_2014_p157_c203"    │
│      },                                                                  │
│      {                                                                   │
│        "doc_name": "7-Flight-Planning-and-Monitoring-2014.pdf",         │
│        "page": 135,                                                     │
│        "chunk_id": "7_flight_planning_and_monitoring_2014_p135_c175"    │
│      }                                                                   │
│    ],                                                                    │
│    "faithfulness_score": 1.00                                           │
│  }                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Baseline vs Hybrid Comparison

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BASELINE (Vector-Only)                                │
│                                                                          │
│  Query → Vector Search → Top 5 → LLM → Answer                           │
│                                                                          │
│  Limitations:                                                            │
│  • Misses exact keyword matches (acronyms)                              │
│  • Semantic similarity can be misleading                                │
│  • No reranking for relevance                                           │
│                                                                          │
│  Performance:                                                            │
│  • Retrieval Hit Rate: 60%                                              │
│  • Faithfulness: 0.71                                                   │
│  • Hallucination Rate: 2%                                               │
└─────────────────────────────────────────────────────────────────────────┘

                                  VS

┌─────────────────────────────────────────────────────────────────────────┐
│                    HYBRID (BM25 + Vector + Reranker)                     │
│                                                                          │
│  Query → BM25 + Vector → RRF → Reranker → Top 5 → LLM → Answer          │
│                                                                          │
│  Advantages:                                                             │
│  • BM25 catches exact terms and acronyms                                │
│  • Vector search handles conceptual queries                             │
│  • RRF combines strengths of both                                       │
│  • Cross-encoder reranks for true relevance                             │
│                                                                          │
│  Performance:                                                            │
│  • Retrieval Hit Rate: 68% (+13% relative improvement)                  │
│  • Faithfulness: 0.73 (+2.8%)                                           │
│  • Hallucination Rate: 0% (zero!)                                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    IMPROVEMENT BREAKDOWN                                 │
│                                                                          │
│  Category          Baseline    Hybrid    Improvement                    │
│  ─────────────────────────────────────────────────────────────────────  │
│  Factual (n=20)    65%         75%       +10% (better for acronyms)     │
│  Applied (n=20)    55%         60%       +5%  (better for scenarios)    │
│  Reasoning (n=10)  60%         70%       +10% (better for concepts)     │
│  ─────────────────────────────────────────────────────────────────────  │
│  Overall (n=50)    60%         68%       +13% relative improvement      │
│                                                                          │
│  Key Wins:                                                               │
│  ✓ Zero hallucinations (vs 2% baseline)                                │
│  ✓ Better retrieval across all categories                               │
│  ✓ Higher faithfulness scores                                           │
│  ✓ More accurate answers                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Summary

```
Documents (PDFs)
    ↓
Ingestion (PyPDFLoader + Splitter)
    ↓
Indexing (FAISS + BM25)
    ↓
Storage (index.faiss + bm25.pkl + metadata.json)
    ↓
Query → Hybrid Retrieval → LLM → Faithfulness Check → Response
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TECHNOLOGY STACK                                 │
│                                                                          │
│  Frontend:                                                               │
│  • HTML/CSS/JavaScript (vanilla)                                        │
│  • Responsive design                                                    │
│                                                                          │
│  Backend:                                                                │
│  • FastAPI (Python web framework)                                       │
│  • Uvicorn (ASGI server)                                                │
│                                                                          │
│  RAG Framework:                                                          │
│  • LangChain (document processing, retrieval, LLM integration)          │
│  • LangChain Community (FAISS, Ollama integrations)                     │
│  • LangChain HuggingFace (embeddings)                                   │
│                                                                          │
│  Retrieval:                                                              │
│  • FAISS (vector similarity search)                                     │
│  • rank-bm25 (keyword search)                                           │
│  • sentence-transformers (cross-encoder reranking)                      │
│                                                                          │
│  Embeddings:                                                             │
│  • HuggingFace: multi-qa-mpnet-base-dot-v1 (768-dim)                    │
│                                                                          │
│  LLM:                                                                    │
│  • Ollama (local LLM server)                                            │
│  • Llama 3.1 8B (quantized model)                                       │
│                                                                          │
│  Utilities:                                                              │
│  • loguru (logging)                                                     │
│  • pydantic (data validation)                                           │
│  • requests (HTTP client)                                               │
│  • tabulate (table formatting)                                          │
│                                                                          │
│  Development:                                                            │
│  • Python 3.10+                                                         │
│  • pip (package management)                                             │
│  • Git (version control)                                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
AIRMAN-RAG/
├── aviation_rag/                    # Main application directory
│   ├── app.py                       # FastAPI application
│   ├── config.py                    # Configuration settings
│   ├── rag.py                       # Baseline RAG pipeline
│   ├── rag_hybrid.py                # Hybrid RAG pipeline ⭐
│   ├── ingest.py                    # Document ingestion
│   ├── ingest_fast.py               # Fast ingestion (parallel)
│   ├── ingest_with_ocr.py           # OCR for scanned PDFs
│   ├── evaluate.py                  # Basic evaluation
│   ├── evaluate_hybrid.py           # Baseline vs hybrid comparison
│   ├── evaluate_with_analysis.py    # Enhanced evaluation ⭐
│   ├── generate_ground_truth.py     # Ground truth generation ⭐
│   ├── run_complete_evaluation.py   # Automated evaluation pipeline ⭐
│   ├── questions.json               # 50 test questions
│   ├── data/                        # Generated data
│   │   ├── faiss_index/             # Vector index
│   │   │   ├── index.faiss
│   │   │   └── bm25_index.pkl
│   │   ├── metadata.json            # Chunk metadata
│   │   ├── eval_results.json        # Evaluation results
│   │   └── hybrid_comparison.json   # Baseline vs hybrid
│   ├── documents/                   # PDF documents
│   │   ├── Air-Regulation-RK-BALI.pdf
│   │   ├── Meteorology full book.pdf
│   │   └── ...
│   ├── templates/                   # Web interface
│   │   └── index.html
│   └── evaluation_report.md         # Generated report ⭐
├── README.md                        # Project overview
├── DEMO_PRESENTATION.md             # Demo script ⭐
├── ARCHITECTURE_DIAGRAM.md          # This file ⭐
├── EVALUATION_SUMMARY.md            # Evaluation summary
└── .gitignore                       # Git ignore rules
```

---

**Legend:**
- ⭐ = Key files for demo
- 📊 = Generated/output files
- 📁 = Data directories
