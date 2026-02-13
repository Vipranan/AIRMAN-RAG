# Changelog

All notable changes to the AIRMAN Aviation RAG System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-02-14

### Added - Level 2: Hybrid Retrieval

- **Hybrid Retrieval Pipeline** (`rag_hybrid.py`)
  - BM25 keyword-based retrieval
  - Vector semantic retrieval
  - Reciprocal Rank Fusion (RRF) for combining results
  - Cross-encoder reranking for final selection
  
- **Evaluation Framework**
  - `evaluate_hybrid.py` for baseline vs hybrid comparison
  - Side-by-side metrics comparison
  - Category-based analysis (factual, applied, reasoning)
  
- **Documentation**
  - `LEVEL2_INDEX.md` - Navigation hub for Level 2
  - `LEVEL2_QUICK_START.md` - Quick start guide
  - `LEVEL2_SUMMARY.md` - Executive summary
  - `LEVEL2_HYBRID_RETRIEVAL.md` - Complete technical documentation (30+ pages)
  - `LEVEL2_OPTION_COMPARISON.md` - Decision rationale (20 pages)
  - `LEVEL2_ARCHITECTURE.md` - Architecture diagrams (15 pages)
  - `LEVEL2_IMPLEMENTATION_COMPLETE.md` - Implementation summary
  
- **Project Organization**
  - `PROJECT_STRUCTURE.md` - Complete project structure guide
  - `MASTER_README.md` - Professional project overview
  - `.gitignore` - Comprehensive Git ignore rules
  - `.env.example` - Environment configuration template
  - `LICENSE` - MIT License
  - `CONTRIBUTING.md` - Contribution guidelines
  - `CHANGELOG.md` - This file

- **Dependencies**
  - `rank-bm25` for BM25 retrieval
  - `sentence-transformers` cross-encoder for reranking

### Changed

- **Configuration** (`config.py`)
  - Added `RERANK_THRESHOLD` parameter for Level 2
  - Updated documentation for all parameters
  
- **Documentation Updates**
  - Updated `README.md` with Level 2 features
  - Updated `SETUP_AND_RUN.md` with Level 2 setup
  - Updated `INDEX.md` with Level 2 navigation
  
- **Performance Improvements**
  - Hybrid retrieval: +9.0% faithfulness improvement
  - Hybrid retrieval: -15.4% latency reduction
  - Better context selection through reranking

### Fixed

- **Metadata Handling** (`rag_hybrid.py`)
  - Fixed metadata access to work with list structure
  - Improved BM25 index building
  - Enhanced reranker integration

---

## [1.0.0] - 2026-02-12

### Added - Initial Release

- **Core RAG Pipeline** (`rag.py`)
  - FAISS vector store integration
  - LangChain-powered document processing
  - Ollama LLM integration
  - Faithfulness checking
  - Citation tracking
  
- **Document Ingestion**
  - `ingest.py` - Standard ingestion
  - `ingest_fast.py` - GPU-accelerated ingestion
  - `ingest_with_ocr.py` - OCR support for scanned PDFs
  - Recursive text splitting with overlap
  - Metadata tracking (document, page, chunk)
  
- **FastAPI Application** (`app.py`)
  - Web interface with chat UI
  - REST API endpoints
  - Health monitoring
  - CORS support
  - Dark/Light theme toggle
  
- **Evaluation Framework** (`evaluate.py`)
  - 50 test questions across 3 categories
  - Retrieval hit rate measurement
  - Faithfulness scoring
  - Hallucination detection
  - Latency tracking
  - Category-based analysis
  
- **Documentation**
  - `README.md` - Main documentation
  - `QUICK_START.md` - 5-minute setup guide
  - `SETUP_AND_RUN.md` - Complete setup guide
  - `SYSTEM_SUMMARY.md` - System overview
  - `CODEBASE_GUIDE.md` - Code structure guide
  - `LANGCHAIN_INTEGRATION.md` - LangChain details
  - `COMPARISON.md` - LangChain vs Custom
  - `EVALUATION_GUIDE.md` - Evaluation methodology
  - `SCANNED_PDF_GUIDE.md` - OCR handling
  - `TEST_QUESTIONS.md` - Test question examples
  - `DEPLOYMENT_SUMMARY.md` - Deployment guide
  - `ASSESSMENT.md` - System assessment
  - `INDEX.md` - Documentation index
  
- **Configuration** (`config.py`)
  - Centralized parameter management
  - Chunking configuration
  - Embedding configuration
  - Retrieval configuration
  - LLM configuration
  - Evaluation configuration
  
- **Web Interface** (`templates/index.html`)
  - Interactive chat interface
  - Real-time responses
  - Citation display
  - Sample questions
  - Theme toggle
  
- **Test Data**
  - `questions.json` - 50 test questions
  - Expected keywords for evaluation
  - Category labels (factual, applied, reasoning)

### Dependencies

- `fastapi>=0.109.0` - Web framework
- `uvicorn[standard]>=0.27.0` - ASGI server
- `langchain>=0.3.0` - RAG orchestration
- `langchain-community>=0.3.0` - Community integrations
- `langchain-huggingface>=0.1.0` - HuggingFace embeddings
- `sentence-transformers>=2.3.0` - Embedding models
- `faiss-cpu>=1.8.0` - Vector search
- `pypdf>=3.17.0` - PDF processing
- `torch>=2.0.0` - PyTorch for GPU support
- `loguru>=0.7.0` - Logging
- `tabulate>=0.9.0` - Table formatting

### Performance

- Document ingestion: ~13 minutes (GPU) / ~45 minutes (CPU)
- Query latency: ~800ms average
- Retrieval hit rate: 70%
- Faithfulness score: 0.685
- Zero hallucinations with faithfulness checking

---

## [Unreleased]

### Planned

- Multi-language support
- Conversation history
- Fine-tuned embeddings on aviation corpus
- GraphRAG for regulatory cross-references
- Mobile application
- Cloud deployment templates
- Docker Compose setup
- Kubernetes manifests
- CI/CD pipeline
- Automated testing
- Performance monitoring
- User authentication
- Rate limiting
- Caching layer

---

## Version History

- **2.0.0** (2026-02-14) - Level 2: Hybrid Retrieval
- **1.0.0** (2026-02-12) - Initial Release

---

## Migration Guides

### Upgrading from 1.0.0 to 2.0.0

1. **Install new dependencies:**
   ```bash
   pip install rank-bm25
   ```

2. **Update configuration:**
   ```python
   # Add to config.py
   RERANK_THRESHOLD = -5.0
   ```

3. **Use hybrid retrieval:**
   ```python
   # Option 1: Direct usage
   from rag_hybrid import HybridRAGPipeline
   rag = HybridRAGPipeline()
   
   # Option 2: Update app.py
   from rag_hybrid import HybridRAGPipeline as RAGPipeline
   ```

4. **Run comparison evaluation:**
   ```bash
   python evaluate_hybrid.py
   ```

5. **Review documentation:**
   - See `LEVEL2_QUICK_START.md` for details
   - Check `LEVEL2_SUMMARY.md` for overview

---

## Support

For questions or issues:
- Check [Documentation](INDEX.md)
- Review [Troubleshooting](SETUP_AND_RUN.md#troubleshooting)
- Open an [Issue](https://github.com/OWNER/airman-rag/issues)

---

**Maintained by:** AIRMAN Development Team  
**License:** MIT  
**Repository:** https://github.com/OWNER/airman-rag
