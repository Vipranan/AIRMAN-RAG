# AIRMAN - Aviation Document AI Chat

A RAG (Retrieval-Augmented Generation) system for aviation documents including PPL/CPL/ATPL textbooks, SOPs, and Flight Manuals.

## Features

- Hybrid retrieval combining FAISS vector search and BM25
- Cross-encoder reranking for improved accuracy
- LangChain-powered LLM integration with Ollama
- FastAPI web interface
- Support for scanned PDFs with OCR
- Citation tracking and faithfulness scoring

## Quick Start

### Prerequisites

- Python 3.8+
- Ollama (for LLM inference)
- CUDA-capable GPU (optional, for faster inference)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AIRMAN-RAG
```

2. Install dependencies:
```bash
cd aviation_rag
pip install -r requirements.txt
```

3. Install and start Ollama:
```bash
# Download from https://ollama.com/download
# Pull the model
ollama pull llama3.1:8b
```

4. Ingest documents:
```bash
python ingest.py
```

5. Start the API server:
```bash
python app.py
```

6. Open your browser to `http://127.0.0.1:8000`

## Project Structure

```
AIRMAN-RAG/
├── aviation_rag/          # Main application code
│   ├── app.py            # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── rag_hybrid.py     # Hybrid RAG pipeline
│   ├── ingest.py         # Document ingestion
│   ├── data/             # Generated indexes and metadata
│   ├── documents/        # PDF documents
│   └── templates/        # Web UI templates
├── .gitignore
└── README.md
```

## Documentation

See the `aviation_rag/` directory for detailed documentation:
- `QUICK_START.md` - Getting started guide
- `SETUP_AND_RUN.md` - Detailed setup instructions
- `EVALUATION_GUIDE.md` - Evaluation methodology
- `LANGCHAIN_INTEGRATION.md` - LangChain integration details

## GPU Acceleration

For faster inference, use GPU acceleration:
- Windows: Install Ollama for Windows (auto-detects GPU)
- Linux: Ensure CUDA toolkit is installed

See `enable_gpu_ollama.md` for detailed instructions.

## License

See LICENSE file for details.
