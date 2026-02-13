# AIRMAN Aviation RAG System - Project Structure

## Overview

This document provides a complete overview of the project structure, file organization, and navigation guide for the AIRMAN Aviation Document AI Chat system.

**Version:** 2.0.0 (with Level 2 Hybrid Retrieval)  
**Last Updated:** February 14, 2026  
**Status:** Production Ready

---

## Table of Contents

1. [Project Organization](#project-organization)
2. [Directory Structure](#directory-structure)
3. [Documentation Index](#documentation-index)
4. [Code Organization](#code-organization)
5. [Data Management](#data-management)
6. [Quick Navigation](#quick-navigation)

---

## Project Organization

### Core Components

```
aviation_rag/
├── Core System (Level 1)
│   ├── Document Ingestion
│   ├── Vector Storage (FAISS)
│   ├── RAG Pipeline
│   └── FastAPI Application
│
├── Enhanced System (Level 2)
│   ├── Hybrid Retrieval
│   ├── BM25 Indexing
│   ├── Cross-Encoder Reranking
│   └── Comparison Evaluation
│
└── Documentation & Configuration
    ├── Setup Guides
    ├── Technical Documentation
    ├── API Documentation
    └── Evaluation Reports
```

---

## Directory Structure

### Root Directory

```
aviation_rag/
│
├── 📁 Core Application Files
│   ├── app.py                          # FastAPI web application
│   ├── rag.py                          # Baseline RAG pipeline (Level 1)
│   ├── rag_hybrid.py                   # Hybrid RAG pipeline (Level 2)
│   ├── config.py                       # Configuration parameters
│   └── requirements.txt                # Python dependencies
│
├── 📁 Ingestion Scripts
│   ├── ingest.py                       # Standard ingestion
│   ├── ingest_fast.py                  # GPU-accelerated ingestion
│   └── ingest_with_ocr.py              # OCR-enabled ingestion
│
├── 📁 Evaluation Scripts
│   ├── evaluate.py                     # Baseline evaluation
│   └── evaluate_hybrid.py              # Hybrid comparison evaluation
│
├── 📁 Data Directory
│   ├── data/
│   │   ├── faiss_index/                # Vector indices
│   │   │   ├── index.faiss             # FAISS vector index
│   │   │   ├── index.pkl               # FAISS metadata
│   │   │   └── bm25_index.pkl          # BM25 index (Level 2)
│   │   ├── metadata.json               # Chunk metadata
│   │   ├── eval_results.json           # Baseline evaluation results
│   │   └── hybrid_comparison.json      # Level 2 comparison results
│
├── 📁 Documents Directory
│   ├── documents/
│   │   ├── Air Navigation/             # Navigation textbooks
│   │   ├── Meteorology/                # Meteorology textbooks
│   │   ├── Air-Regulation-RK-BALI.pdf  # Regulations (scanned)
│   │   └── Sample test questions.pdf   # Test questions
│
├── 📁 Templates
│   └── templates/
│       └── index.html                  # Web interface template
│
├── 📁 Documentation - Getting Started
│   ├── README.md                       # Main project documentation
│   ├── QUICK_START.md                  # 5-minute quick start
│   ├── SETUP_AND_RUN.md                # Complete setup guide
│   └── PROJECT_STRUCTURE.md            # This file
│
├── 📁 Documentation - Level 1 (Core System)
│   ├── SYSTEM_SUMMARY.md               # System overview
│   ├── CODEBASE_GUIDE.md               # Code structure guide
│   ├── LANGCHAIN_INTEGRATION.md        # LangChain details
│   ├── COMPARISON.md                   # LangChain vs Custom
│   ├── EVALUATION_GUIDE.md             # Evaluation methodology
│   ├── SCANNED_PDF_GUIDE.md            # OCR handling
│   └── TEST_QUESTIONS.md               # Test question examples
│
├── 📁 Documentation - Level 2 (Hybrid Retrieval)
│   ├── LEVEL2_INDEX.md                 # Level 2 navigation hub
│   ├── LEVEL2_QUICK_START.md           # Quick start for Level 2
│   ├── LEVEL2_SUMMARY.md               # Executive summary
│   ├── LEVEL2_HYBRID_RETRIEVAL.md      # Complete technical docs
│   ├── LEVEL2_OPTION_COMPARISON.md     # Decision rationale
│   ├── LEVEL2_ARCHITECTURE.md          # Architecture diagrams
│   └── LEVEL2_IMPLEMENTATION_COMPLETE.md # Implementation summary
│
├── 📁 Documentation - Deployment
│   ├── DEPLOYMENT_SUMMARY.md           # Deployment guide
│   ├── ASSESSMENT.md                   # System assessment
│   └── INDEX.md                        # Documentation index
│
├── 📁 Configuration & Data Files
│   ├── questions.json                  # Test questions dataset
│   ├── ingestion.log                   # Ingestion logs
│   ├── ingestion_fast.log              # Fast ingestion logs
│   └── report.md                       # Evaluation report template
│
└── 📁 Cache & Build
    └── __pycache__/                    # Python cache files
```

---

## Documentation Index

### 🚀 Quick Start (5-15 minutes)

| Document | Purpose | Time | Audience |
|----------|---------|------|----------|
| [QUICK_START.md](QUICK_START.md) | Get system running | 5 min | All users |
| [SETUP_AND_RUN.md](SETUP_AND_RUN.md) | Complete setup guide | 15 min | Developers |
| [README.md](README.md) | Full documentation | 30 min | All users |

### 📚 Level 1: Core System

| Document | Purpose | Pages | Audience |
|----------|---------|-------|----------|
| [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md) | High-level overview | 5 | Managers, Architects |
| [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) | Code structure | 15 | Developers |
| [LANGCHAIN_INTEGRATION.md](LANGCHAIN_INTEGRATION.md) | LangChain details | 20 | Developers |
| [EVALUATION_GUIDE.md](EVALUATION_GUIDE.md) | Testing methodology | 10 | QA, Developers |
| [SCANNED_PDF_GUIDE.md](SCANNED_PDF_GUIDE.md) | OCR handling | 8 | Operators |

### ⭐ Level 2: Hybrid Retrieval

| Document | Purpose | Pages | Audience |
|----------|---------|-------|----------|
| [LEVEL2_INDEX.md](LEVEL2_INDEX.md) | Navigation hub | 10 | All users |
| [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md) | Quick start | 6 | Developers |
| [LEVEL2_SUMMARY.md](LEVEL2_SUMMARY.md) | Executive summary | 8 | Decision makers |
| [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md) | Complete technical docs | 30+ | Engineers |
| [LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md) | Decision rationale | 20 | Technical leads |
| [LEVEL2_ARCHITECTURE.md](LEVEL2_ARCHITECTURE.md) | Architecture diagrams | 15 | Architects |

### 🚀 Deployment & Operations

| Document | Purpose | Pages | Audience |
|----------|---------|-------|----------|
| [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) | Deployment guide | 12 | DevOps |
| [ASSESSMENT.md](ASSESSMENT.md) | System assessment | 8 | Evaluators |

---

## Code Organization

### Core Application (`app.py`)

```python
# FastAPI Application Structure
├── Imports & Configuration
├── RAGPipeline Initialization
├── API Endpoints
│   ├── GET  /              # Web interface
│   ├── GET  /health        # Health check
│   ├── POST /ingest        # Document ingestion
│   └── POST /ask           # Question answering
└── Server Startup
```

### RAG Pipeline (`rag.py` - Baseline)

```python
# Baseline RAG Pipeline
├── RAGPipeline Class
│   ├── __init__()          # Initialize components
│   ├── _load_vectorstore() # Load FAISS index
│   ├── _load_metadata()    # Load chunk metadata
│   ├── _setup_llm()        # Configure Ollama
│   ├── retrieve()          # Vector retrieval
│   ├── generate_answer()   # LLM generation
│   ├── check_faithfulness()# Grounding check
│   └── ask()               # Complete pipeline
```

### Hybrid RAG Pipeline (`rag_hybrid.py` - Level 2)

```python
# Hybrid RAG Pipeline
├── HybridRAGPipeline Class
│   ├── __init__()              # Initialize components
│   ├── _load_vectorstore()     # Load FAISS index
│   ├── _load_metadata()        # Load chunk metadata
│   ├── _load_bm25_index()      # Load/build BM25 index
│   ├── _setup_reranker()       # Load cross-encoder
│   ├── _setup_llm()            # Configure Ollama
│   ├── retrieve_bm25()         # Keyword retrieval
│   ├── retrieve_vector()       # Semantic retrieval
│   ├── reciprocal_rank_fusion()# Combine rankings
│   ├── rerank()                # Cross-encoder reranking
│   ├── retrieve_hybrid()       # Complete hybrid retrieval
│   ├── generate_answer()       # LLM generation
│   ├── check_faithfulness()    # Grounding check
│   └── ask()                   # Complete pipeline
```

### Configuration (`config.py`)

```python
# Configuration Parameters
├── Paths
│   ├── DOCUMENTS_DIR
│   ├── FAISS_INDEX_DIR
│   └── METADATA_PATH
│
├── Chunking
│   ├── CHUNK_SIZE
│   ├── CHUNK_OVERLAP
│   └── MIN_CHUNK_WORDS
│
├── Embeddings
│   ├── EMBEDDING_MODEL
│   └── EMBEDDING_DIM
│
├── Retrieval
│   ├── TOP_K
│   ├── SIMILARITY_THRESHOLD
│   └── RERANK_THRESHOLD (Level 2)
│
├── LLM
│   ├── OLLAMA_BASE_URL
│   ├── OLLAMA_MODEL
│   ├── OLLAMA_TEMPERATURE
│   └── OLLAMA_MAX_TOKENS
│
└── Evaluation
    ├── QUESTIONS_PATH
    ├── RESULTS_PATH
    └── FAITHFULNESS_THRESHOLD
```

---

## Data Management

### Data Flow

```
Documents (PDF)
    ↓
Ingestion Pipeline
    ↓
Chunks + Metadata
    ↓
Embedding Generation
    ↓
FAISS Index + BM25 Index
    ↓
RAG Pipeline
    ↓
Answers + Citations
```

### Data Files

| File | Size | Purpose | Generated By |
|------|------|---------|--------------|
| `data/faiss_index/index.faiss` | ~250 MB | Vector index | ingest_fast.py |
| `data/faiss_index/index.pkl` | ~50 MB | FAISS metadata | ingest_fast.py |
| `data/faiss_index/bm25_index.pkl` | ~50 MB | BM25 index | rag_hybrid.py |
| `data/metadata.json` | ~15 MB | Chunk metadata | ingest_fast.py |
| `data/eval_results.json` | ~100 KB | Evaluation results | evaluate.py |
| `data/hybrid_comparison.json` | ~200 KB | Comparison results | evaluate_hybrid.py |

### Data Lifecycle

1. **Ingestion** (One-time)
   ```bash
   python ingest_fast.py
   # Creates: index.faiss, index.pkl, metadata.json
   ```

2. **BM25 Index** (Auto-generated on first hybrid use)
   ```bash
   python rag_hybrid.py "test question"
   # Creates: bm25_index.pkl
   ```

3. **Evaluation** (On-demand)
   ```bash
   python evaluate.py              # Creates: eval_results.json
   python evaluate_hybrid.py       # Creates: hybrid_comparison.json
   ```

---

## Quick Navigation

### By User Role

#### 👨‍💼 Project Manager / Stakeholder
1. Start: [LEVEL2_SUMMARY.md](LEVEL2_SUMMARY.md)
2. Then: [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)
3. Finally: [ASSESSMENT.md](ASSESSMENT.md)

#### 👨‍💻 Developer (New to Project)
1. Start: [QUICK_START.md](QUICK_START.md)
2. Then: [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md)
3. Then: [LANGCHAIN_INTEGRATION.md](LANGCHAIN_INTEGRATION.md)
4. Finally: [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md)

#### 🏗️ System Architect
1. Start: [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)
2. Then: [LEVEL2_ARCHITECTURE.md](LEVEL2_ARCHITECTURE.md)
3. Finally: [LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md)

#### 🧪 QA / Tester
1. Start: [EVALUATION_GUIDE.md](EVALUATION_GUIDE.md)
2. Then: [TEST_QUESTIONS.md](TEST_QUESTIONS.md)
3. Finally: Run evaluations

#### 🚀 DevOps / Deployment
1. Start: [SETUP_AND_RUN.md](SETUP_AND_RUN.md)
2. Then: [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)
3. Finally: Deploy system

### By Task

#### 🎯 Getting Started
```
QUICK_START.md → SETUP_AND_RUN.md → README.md
```

#### 🔧 Understanding Code
```
CODEBASE_GUIDE.md → LANGCHAIN_INTEGRATION.md → Code files
```

#### ⭐ Implementing Level 2
```
LEVEL2_QUICK_START.md → LEVEL2_HYBRID_RETRIEVAL.md → rag_hybrid.py
```

#### 📊 Running Evaluation
```
EVALUATION_GUIDE.md → evaluate.py → evaluate_hybrid.py
```

#### 🚀 Deploying System
```
SETUP_AND_RUN.md → DEPLOYMENT_SUMMARY.md → Production
```

---

## File Naming Conventions

### Documentation Files

| Prefix | Purpose | Example |
|--------|---------|---------|
| None | Core documentation | README.md, QUICK_START.md |
| LEVEL2_ | Level 2 specific | LEVEL2_SUMMARY.md |
| None (CAPS) | General guides | SETUP_AND_RUN.md |

### Code Files

| Pattern | Purpose | Example |
|---------|---------|---------|
| `*.py` | Python scripts | app.py, rag.py |
| `*_hybrid.py` | Level 2 files | rag_hybrid.py, evaluate_hybrid.py |
| `ingest_*.py` | Ingestion variants | ingest_fast.py, ingest_with_ocr.py |

### Data Files

| Pattern | Purpose | Example |
|---------|---------|---------|
| `*.json` | JSON data | metadata.json, questions.json |
| `*.pkl` | Pickle files | index.pkl, bm25_index.pkl |
| `*.faiss` | FAISS indices | index.faiss |
| `*.log` | Log files | ingestion.log |

---

## Version Control

### Git Structure (Recommended)

```
.gitignore should include:
├── __pycache__/
├── *.pyc
├── data/faiss_index/
├── data/*.json (except questions.json)
├── *.log
└── .env
```

### Branches

```
main                    # Production-ready code
├── develop            # Development branch
├── feature/level2     # Level 2 implementation
└── hotfix/*          # Bug fixes
```

---

## Maintenance

### Regular Tasks

| Task | Frequency | Command |
|------|-----------|---------|
| Update dependencies | Monthly | `pip install --upgrade -r requirements.txt` |
| Re-ingest documents | When docs change | `python ingest_fast.py` |
| Run evaluation | Weekly | `python evaluate_hybrid.py` |
| Check logs | Daily | `tail -f ingestion.log` |
| Backup data | Weekly | `tar -czf backup.tar.gz data/` |

### Health Checks

```bash
# Check system health
curl http://localhost:8000/health

# Check Ollama
curl http://localhost:11434/api/tags

# Check indices
ls -lh data/faiss_index/

# Check logs
tail -n 50 ingestion_fast.log
```

---

## Support & Resources

### Internal Documentation
- [INDEX.md](INDEX.md) - Complete documentation index
- [LEVEL2_INDEX.md](LEVEL2_INDEX.md) - Level 2 navigation
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - This file

### External Resources
- Ollama: https://ollama.com/docs
- LangChain: https://python.langchain.com/
- FAISS: https://github.com/facebookresearch/faiss
- FastAPI: https://fastapi.tiangolo.com/

### Contact
- Technical Issues: Check troubleshooting in SETUP_AND_RUN.md
- Documentation: Refer to INDEX.md
- Level 2 Questions: See LEVEL2_INDEX.md

---

**Document Version:** 1.0  
**Last Updated:** February 14, 2026  
**Maintained By:** AIRMAN Development Team  
**Status:** Production Ready ✅
