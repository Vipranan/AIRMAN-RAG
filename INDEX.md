# Aviation Document AI Chat - Documentation Index

## Quick Navigation

### Getting Started
1. **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
2. **[README.md](README.md)** - Complete documentation
3. **[SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md)** - High-level overview

### Level 2 Enhancement (Hybrid Retrieval) ⭐ NEW
4. **[LEVEL2_INDEX.md](LEVEL2_INDEX.md)** - Level 2 documentation index
5. **[LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md)** - Quick start for hybrid retrieval
6. **[LEVEL2_SUMMARY.md](LEVEL2_SUMMARY.md)** - Executive summary
7. **[LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md)** - Full technical documentation
8. **[LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md)** - Why hybrid retrieval?
9. **[LEVEL2_ARCHITECTURE.md](LEVEL2_ARCHITECTURE.md)** - Architecture diagrams

### Technical Documentation
10. **[LANGCHAIN_INTEGRATION.md](LANGCHAIN_INTEGRATION.md)** - LangChain integration details
11. **[COMPARISON.md](COMPARISON.md)** - LangChain vs Custom implementation
12. **[report.md](report.md)** - Evaluation report template

### Code Files
13. **[config.py](config.py)** - All tunable parameters
14. **[ingest.py](ingest.py)** - Document ingestion pipeline
15. **[rag.py](rag.py)** - Baseline RAG pipeline (vector-only)
16. **[rag_hybrid.py](rag_hybrid.py)** - Level 2: Hybrid RAG pipeline ⭐
17. **[app.py](app.py)** - FastAPI application
18. **[evaluate.py](evaluate.py)** - Baseline evaluation script
19. **[evaluate_hybrid.py](evaluate_hybrid.py)** - Level 2: Comparison evaluation ⭐

### Data Files
20. **[questions.json](questions.json)** - 50 test questions
21. **[requirements.txt](requirements.txt)** - Python dependencies

---

## Document Descriptions

### QUICK_START.md
**Purpose**: Get up and running in 5 minutes  
**Audience**: New users, developers  
**Contents**:
- Installation steps
- Basic usage (3 steps)
- Testing examples
- Troubleshooting

**Start here if**: You want to quickly test the system

---

### README.md
**Purpose**: Complete system documentation  
**Audience**: All users  
**Contents**:
- Features and architecture
- Prerequisites and installation
- Detailed usage instructions
- API endpoints
- Configuration options
- Troubleshooting
- CLI usage

**Start here if**: You want comprehensive documentation

---

### SYSTEM_SUMMARY.md
**Purpose**: High-level system overview  
**Audience**: Managers, architects, reviewers  
**Contents**:
- Tech stack
- Architecture diagram
- Key features
- Configuration parameters
- Performance characteristics
- Strengths and limitations

**Start here if**: You want a quick overview without diving into code

---

### LEVEL2_INDEX.md ⭐ NEW
**Purpose**: Navigation hub for Level 2 documentation  
**Audience**: All users interested in hybrid retrieval  
**Contents**:
- Quick navigation to all Level 2 docs
- Document guide (quick implementation, understanding decision, technical deep dive)
- Implementation checklist
- FAQ
- Troubleshooting guide

**Start here if**: You want to explore Level 2 hybrid retrieval enhancement

---

### LEVEL2_QUICK_START.md ⭐ NEW
**Purpose**: Get hybrid retrieval running in 30 minutes  
**Audience**: Developers  
**Contents**:
- Installation steps
- Usage examples (direct Python, comparison, CLI)
- Configuration options
- Integration with FastAPI
- Troubleshooting

**Start here if**: You want to quickly try hybrid retrieval

---

### LEVEL2_SUMMARY.md ⭐ NEW
**Purpose**: Executive summary of Level 2 enhancement  
**Audience**: Technical leads, decision makers  
**Contents**:
- What was implemented
- Why this option was chosen
- Key results and metrics
- Architecture overview
- Production deployment plan

**Start here if**: You want a high-level overview of Level 2

---

### LEVEL2_HYBRID_RETRIEVAL.md ⭐ NEW
**Purpose**: Complete technical documentation for hybrid retrieval  
**Audience**: Engineers implementing or maintaining the system  
**Contents**:
- Why hybrid retrieval? (30+ pages)
- Why not the other options?
- Technical architecture (BM25, Vector, RRF, Reranker)
- Implementation details
- Evaluation methodology
- Results and metrics
- Integration guide
- Future improvements

**Start here if**: You want complete technical understanding

---

### LEVEL2_OPTION_COMPARISON.md ⭐ NEW
**Purpose**: Detailed comparison of all three Level 2 options  
**Audience**: Decision makers, technical leads  
**Contents**:
- The three options explained
- Detailed comparison (complexity, relevance, impact, risk, cost)
- Why Option 1 (Hybrid Retrieval) wins
- Why NOT Option 2 (Query Router)
- Why NOT Option 3 (GraphRAG)
- Implementation roadmap

**Start here if**: You want to understand the decision rationale

---

### LEVEL2_ARCHITECTURE.md ⭐ NEW
**Purpose**: Visual system architecture and data flow  
**Audience**: Engineers and architects  
**Contents**:
- System architecture diagram
- Component details (BM25, Vector, RRF, Reranker)
- Performance characteristics
- Data flow examples
- Baseline vs Hybrid comparison

**Start here if**: You want to understand the system architecture visually

---

### LANGCHAIN_INTEGRATION.md
**Purpose**: Explain LangChain integration  
**Audience**: Developers, architects  
**Contents**:
- Component breakdown (PyPDFLoader, TextSplitter, FAISS, etc.)
- Code examples for each component
- Benefits of LangChain
- Migration guide (custom → LangChain)
- Future enhancements with LangChain

**Start here if**: You want to understand how LangChain is used

---

### COMPARISON.md
**Purpose**: Compare LangChain vs Custom implementation  
**Audience**: Developers, decision makers  
**Contents**:
- Side-by-side code comparisons
- Feature comparison table
- Advantages of each approach
- When to use each
- Migration paths

**Start here if**: You're deciding between LangChain and custom implementation

---

### report.md
**Purpose**: Evaluation report template  
**Audience**: Evaluators, QA, stakeholders  
**Contents**:
- System architecture details
- Configuration parameters
- Evaluation results (to be filled)
- Per-category analysis
- Sample question analysis
- Failure analysis
- Recommendations

**Start here if**: You're evaluating system performance

---

### config.py
**Purpose**: Central configuration  
**Audience**: Developers, operators  
**Contents**:
- All tunable parameters
- Paths, chunking, embeddings, retrieval, LLM, evaluation settings

**Edit this if**: You want to tune system behavior

---

### ingest.py
**Purpose**: Document ingestion pipeline  
**Audience**: Developers  
**Contents**:
- PyPDFLoader integration
- RecursiveCharacterTextSplitter usage
- FAISS vector store creation
- Metadata management

**Run this to**: Ingest PDFs into the system

---

### rag.py
**Purpose**: RAG pipeline implementation  
**Audience**: Developers  
**Contents**:
- FAISS retrieval
- Ollama LLM integration
- PromptTemplate and LLMChain
- Faithfulness checking

**Use this to**: Understand retrieval and generation logic

---

### app.py
**Purpose**: FastAPI REST API  
**Audience**: Developers, API users  
**Contents**:
- /health endpoint
- /ingest endpoint
- /ask endpoint
- Request/response models

**Run this to**: Start the API server

---

### evaluate.py
**Purpose**: Evaluation script  
**Audience**: QA, evaluators  
**Contents**:
- Question loading
- API calling
- Metrics computation
- Results saving and reporting

**Run this to**: Evaluate system performance

---

### questions.json
**Purpose**: Test questions with ground truth  
**Audience**: QA, evaluators  
**Contents**:
- 50 questions across 3 categories
- Ground truth answers (to be filled)
- Expected keywords
- Source hints

**Edit this to**: Add ground truth answers for evaluation

---

### requirements.txt
**Purpose**: Python dependencies  
**Audience**: Developers, operators  
**Contents**:
- LangChain packages
- FastAPI and Uvicorn
- FAISS, sentence-transformers
- Other dependencies

**Use this to**: Install required packages

---

## Reading Paths

### Path 1: Quick Start (15 minutes)
1. QUICK_START.md
2. Run installation and basic test
3. README.md (skim API section)

### Path 2: Level 2 Hybrid Retrieval (30 minutes) ⭐ NEW
1. LEVEL2_QUICK_START.md
2. Install: `pip install rank-bm25`
3. Run: `python evaluate_hybrid.py`
4. Review: LEVEL2_SUMMARY.md

### Path 3: Full Understanding (1 hour)
1. SYSTEM_SUMMARY.md
2. README.md
3. LANGCHAIN_INTEGRATION.md
4. Code files (config.py → ingest.py → rag.py → app.py)

### Path 4: Level 2 Deep Dive (2 hours) ⭐ NEW
1. LEVEL2_SUMMARY.md
2. LEVEL2_OPTION_COMPARISON.md
3. LEVEL2_HYBRID_RETRIEVAL.md
4. LEVEL2_ARCHITECTURE.md
5. Code: rag_hybrid.py, evaluate_hybrid.py

### Path 5: Evaluation (30 minutes)
1. QUICK_START.md (setup)
2. questions.json (fill ground truth)
3. evaluate.py (run evaluation)
4. report.md (review results)

### Path 6: Decision Making (30 minutes)
1. SYSTEM_SUMMARY.md
2. COMPARISON.md
3. LANGCHAIN_INTEGRATION.md (benefits section)
4. LEVEL2_OPTION_COMPARISON.md (for Level 2 decision) ⭐

### Path 7: Development (2 hours)
1. README.md
2. LANGCHAIN_INTEGRATION.md
3. All code files
4. COMPARISON.md (for context)

---

## File Dependencies

```
QUICK_START.md
    ↓
README.md ←→ SYSTEM_SUMMARY.md
    ↓
LANGCHAIN_INTEGRATION.md ←→ COMPARISON.md
    ↓
Code Files (config.py, ingest.py, rag.py, app.py, evaluate.py)
    ↓
Data Files (questions.json, requirements.txt)
    ↓
report.md (evaluation results)
```

---

## Maintenance

### When to Update Each Document

**QUICK_START.md**: When installation steps or basic usage changes  
**README.md**: When features, API, or configuration changes  
**SYSTEM_SUMMARY.md**: When architecture or tech stack changes  
**LANGCHAIN_INTEGRATION.md**: When LangChain components change  
**COMPARISON.md**: When implementation approach changes  
**report.md**: After each evaluation run  
**config.py**: When adding/removing parameters  
**Code files**: During development  
**questions.json**: When adding/modifying test questions  
**requirements.txt**: When dependencies change

---

## Support

For questions or issues:
1. Check relevant documentation above
2. Review code comments
3. Check logs (loguru output)
4. Consult LangChain documentation: https://python.langchain.com/

---

**Last Updated**: 2026-02-13  
**Version**: 1.0.0 (LangChain-powered)
