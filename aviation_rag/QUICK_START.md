# Quick Start Guide - Aviation Document AI Chat (LangChain)

## Installation (5 minutes)

### 1. Install Python Dependencies
```bash
cd aviation_rag
pip install -r requirements.txt
```

### 2. Install and Setup Ollama
```bash
# Download from https://ollama.ai or use package manager
# Windows: Download installer from ollama.ai
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# In another terminal, pull the model
ollama pull llama3.1:8b
```

## Usage (3 steps)

### Step 1: Add Your PDFs
Place aviation PDF files in the `documents/` folder:
```
aviation_rag/documents/
├── PPL_Textbook.pdf
├── CPL_Textbook.pdf
├── ATPL_Textbook.pdf
├── SOP_Checklist.pdf
└── AFM_POH.pdf
```

### Step 2: Ingest Documents
```bash
python ingest.py
```

Expected output:
```
[INFO] Starting ingestion pipeline with LangChain...
[INFO] Found 5 PDF(s) to process
[INFO] Processing: PPL_Textbook.pdf
[INFO]   Loaded 342 pages
[INFO]   Created 856 chunks (avg 387.2 words)
...
[SUCCESS] Ingestion complete! Total chunks: 4821
```

### Step 3: Start API Server
```bash
uvicorn app:app --reload --port 8000
```

Or:
```bash
python app.py
```

## Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Ask a Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does VFR stand for?",
    "top_k": 5,
    "debug": false
  }'
```

### Response
```json
{
  "answer": "VFR stands for Visual Flight Rules. It requires the pilot to maintain visual reference to the ground and maintain specific visibility and cloud clearance minimums. [Source: PPL_Textbook.pdf, Page: 42]",
  "citations": [
    {
      "doc_name": "PPL_Textbook.pdf",
      "page": 42,
      "chunk_id": "ppl_textbook_pdf_p042_c003"
    }
  ],
  "faithfulness_score": 0.91,
  "retrieved_chunks": null
}
```

## CLI Testing

### Test RAG Pipeline Directly
```bash
python rag.py "What is the minimum safe altitude over a congested area?"
```

### Ingest Single File
```bash
python ingest.py --file documents/PPL_Textbook.pdf
```

## Evaluation

### 1. Fill Ground Truth
Edit `questions.json` and fill in the `ground_truth` field for each question:
```json
{
  "id": 1,
  "category": "factual",
  "question": "What does VFR stand for and what does it require?",
  "ground_truth": "VFR stands for Visual Flight Rules. It requires maintaining visual reference to the ground, specific visibility minimums (typically 5km), and cloud clearance requirements.",
  "expected_keywords": ["Visual Flight Rules", "visibility", "cloud clearance"],
  "source_hint": "PPL Textbook — Air Law / Meteorology chapter"
}
```

### 2. Run Evaluation
```bash
# Make sure API is running first
python evaluate.py
```

### 3. View Results
- Console: Summary table with metrics per category
- File: `data/eval_results.json` with detailed per-question results

## Troubleshooting

### "Cannot reach Ollama"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### "FAISS index not found"
```bash
# Run ingestion first
python ingest.py
```

### "No chunks above similarity threshold"
- Question may be out of scope for your documents
- Try lowering `SIMILARITY_THRESHOLD` in `config.py` (default: 0.35)
- Check if documents were ingested correctly

### Low Faithfulness Scores
- Increase `CHUNK_SIZE` in `config.py` for more context per chunk
- Increase `TOP_K` to retrieve more chunks
- Adjust `FAITHFULNESS_THRESHOLD` if too strict (default: 0.70)

## Configuration

Edit `config.py` to tune parameters:

```python
# Chunking
CHUNK_SIZE = 400          # words per chunk (1600 chars)
CHUNK_OVERLAP = 50        # words of overlap (200 chars)

# Retrieval
TOP_K = 5                 # number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.35  # minimum similarity score

# Faithfulness
FAITHFULNESS_THRESHOLD = 0.70  # minimum faithfulness to accept answer

# LLM
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_TEMPERATURE = 0.0
```

## API Endpoints

### GET /health
System status and statistics

### POST /ingest
Trigger document ingestion
```json
{
  "pdf_paths": ["./documents/PPL.pdf"]  // optional
}
```

### POST /ask
Ask a question
```json
{
  "question": "What is V1 speed?",
  "top_k": 5,      // optional
  "debug": false   // optional, includes retrieved chunks if true
}
```

## Next Steps

1. **Add your aviation PDFs** to `documents/`
2. **Run ingestion**: `python ingest.py`
3. **Start API**: `uvicorn app:app --port 8000`
4. **Test questions** via API or CLI
5. **Fill ground truth** in `questions.json`
6. **Run evaluation**: `python evaluate.py`
7. **Review report**: Check `report.md` and `data/eval_results.json`

## LangChain Features

This system uses LangChain for:
- **PyPDFLoader**: PDF extraction
- **RecursiveCharacterTextSplitter**: Intelligent chunking
- **HuggingFaceEmbeddings**: Embedding generation
- **FAISS**: Vector store
- **Ollama**: LLM integration
- **PromptTemplate**: Structured prompts
- **LLMChain**: Chain orchestration

See `LANGCHAIN_INTEGRATION.md` for detailed integration guide.

## Support

- **README.md**: Full documentation
- **LANGCHAIN_INTEGRATION.md**: LangChain integration details
- **report.md**: Architecture and evaluation details
- **Code comments**: Inline documentation in each module
