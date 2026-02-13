# AIRMAN Codebase Guide

Complete technical documentation explaining how the Aviation Document AI Chat system works.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Configuration](#configuration)
7. [API Endpoints](#api-endpoints)
8. [Web Interface](#web-interface)
9. [Evaluation System](#evaluation-system)
10. [Deployment](#deployment)

---

## System Overview

AIRMAN is a Retrieval-Augmented Generation (RAG) system that answers aviation questions using official documents.

**Technology Stack:**
- **Backend**: FastAPI (Python web framework)
- **LLM**: Ollama (llama3.1:8b model)
- **Embeddings**: sentence-transformers (multi-qa-mpnet-base-dot-v1)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Frontend**: HTML/CSS/JavaScript with Jinja2 templates
- **Framework**: LangChain (orchestration)

**Key Features:**
- Document ingestion from PDFs
- Semantic search with vector embeddings
- GPU-accelerated processing
- Faithfulness checking (prevents hallucinations)
- Citation tracking
- Dark/Light theme UI
- Evaluation framework

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEB INTERFACE                             │
│              (templates/index.html)                          │
│         - Chat UI with theme toggle                          │
│         - Real-time status indicator                         │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP POST /ask
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI SERVER                             │
│                    (app.py)                                  │
│         - Routes: /, /health, /ask, /ingest                  │
│         - Request validation                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   RAG PIPELINE                               │
│                    (rag.py)                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. QUERY EMBEDDING                                  │   │
│  │     - Convert question to 768-dim vector            │   │
│  │     - Uses GPU-accelerated embeddings               │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐   │
│  │  2. RETRIEVAL                                        │   │
│  │     - FAISS similarity search                        │   │
│  │     - Get top-k most relevant chunks                 │   │
│  │     - Filter by similarity threshold                 │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐   │
│  │  3. GENERATION                                       │   │
│  │     - Build context from retrieved chunks            │   │
│  │     - Format prompt with context + question          │   │
│  │     - Call Ollama LLM                                │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
│  ┌──────────────▼───────────────────────────────────────┐   │
│  │  4. FAITHFULNESS CHECK                               │   │
│  │     - Compare answer to retrieved context            │   │
│  │     - Calculate faithfulness score                   │   │
│  │     - Override with "not available" if too low       │   │
│  └──────────────┬───────────────────────────────────────┘   │
│                 │                                            │
└─────────────────┼────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      RESPONSE                                │
│  - Answer text                                               │
│  - Citations (doc name + page)                               │
│  - Faithfulness score                                        │
└─────────────────────────────────────────────────────────────┘
```



---

## File Structure

```
aviation_rag/
├── app.py                      # FastAPI application (main entry point)
├── rag.py                      # RAG pipeline implementation
├── config.py                   # All configuration parameters
├── ingest.py                   # Document ingestion (original)
├── ingest_fast.py              # Optimized GPU ingestion
├── evaluate.py                 # Evaluation script
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── index.html              # Web UI (Jinja2 template)
│
├── documents/                  # PDF documents (input)
│   ├── Air-Regulation-RK-BALI.pdf
│   ├── Sample test questions.pdf
│   ├── Air Navigation/
│   │   ├── 10-General-Navigation-2014.pdf
│   │   ├── 11-radio-navigation-2014.pdf
│   │   ├── 6-mass-and-balance-and-performance-2014.pdf
│   │   ├── 7-Flight-Planning-and-Monitoring-2014.pdf
│   │   └── Instruments.pdf
│   └── Meteorology/
│       └── Meteorology full book.pdf
│
├── data/                       # Generated data
│   ├── faiss_index/            # Vector store
│   │   ├── index.faiss         # FAISS index file
│   │   └── index.pkl           # Metadata pickle
│   ├── metadata.json           # Chunk metadata
│   └── eval_results.json       # Evaluation results
│
├── questions.json              # Test questions (50)
│
└── Documentation/
    ├── README.md               # Project overview
    ├── QUICK_START.md          # Getting started guide
    ├── SYSTEM_SUMMARY.md       # Architecture details
    ├── DEPLOYMENT_SUMMARY.md   # Deployment guide
    ├── LANGCHAIN_INTEGRATION.md # LangChain usage
    ├── TEST_QUESTIONS.md       # Test questions list
    ├── EVALUATION_GUIDE.md     # Evaluation explanation
    └── CODEBASE_GUIDE.md       # This file
```

---

## Core Components

### 1. config.py - Configuration Hub

**Purpose:** Central location for all tunable parameters

**Key Parameters:**
```python
# Chunking
CHUNK_SIZE = 400              # Words per chunk
CHUNK_OVERLAP = 50            # Overlap between chunks
MIN_CHUNK_WORDS = 30          # Minimum chunk size

# Embeddings
EMBEDDING_MODEL = "multi-qa-mpnet-base-dot-v1"
EMBEDDING_DIM = 768           # Vector dimensions

# Retrieval
TOP_K = 7                     # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.30   # Minimum similarity score

# LLM
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_TEMPERATURE = 0.0      # Deterministic output
OLLAMA_MAX_TOKENS = 768       # Max response length

# Faithfulness
FAITHFULNESS_THRESHOLD = 0.50 # Minimum faithfulness score
```

**Why it matters:**
- Single place to tune system behavior
- Easy experimentation
- No hardcoded values in code



### 2. ingest_fast.py - Document Processing

**Purpose:** Convert PDF documents into searchable vector embeddings

**Process:**
```python
class FastDocumentProcessor:
    def load_and_split_pdf(self, pdf_path):
        # 1. Load PDF using PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # 2. Split into chunks
        chunks = text_splitter.split_documents(pages)
        
        # 3. Add metadata to each chunk
        for chunk in chunks:
            chunk.metadata.update({
                'chunk_id': f"{doc_name}_p{page}_c{index}",
                'doc_name': doc_name,
                'page': page_number,
                'word_count': len(chunk.page_content.split())
            })
        
        # 4. Filter out tiny chunks
        chunks = [c for c in chunks if c.metadata['word_count'] >= MIN_CHUNK_WORDS]
        
        return chunks
```

**Key Features:**
- GPU acceleration for embeddings
- Batch processing (128 chunks at a time)
- Progress logging
- Metadata tracking

**Output:**
- `data/faiss_index/index.faiss` - Vector index
- `data/faiss_index/index.pkl` - FAISS metadata
- `data/metadata.json` - Human-readable metadata

**Performance:**
- 8 PDFs (2,738 pages) → 3,983 chunks
- Processing time: ~13 minutes with GPU
- Embedding model: 768-dimensional vectors

**Important Note - Scanned PDFs:**
- Text-based PDFs work perfectly
- Scanned/image PDFs produce 0 chunks
- Example: Air-Regulation-RK-BALI.pdf (348 pages → 0 chunks)
- Solution: Use OCR or get text-based version
- See `SCANNED_PDF_GUIDE.md` for details

**Current Working Documents:**
1. Sample test questions.pdf (12 chunks)
2. 10-General-Navigation-2014.pdf (716 chunks)
3. 11-radio-navigation-2014.pdf (469 chunks)
4. 6-mass-and-balance-and-performance-2014.pdf (759 chunks)
5. 7-Flight-Planning-and-Monitoring-2014.pdf (386 chunks)
6. Instruments.pdf (878 chunks)
7. Meteorology full book.pdf (763 chunks)

**Total: 3,983 chunks from 7 documents**



### 3. rag.py - RAG Pipeline

**Purpose:** Core question-answering logic

**Class Structure:**
```python
class RAGPipeline:
    def __init__(self):
        self._load_vectorstore()    # Load FAISS index
        self._load_metadata()       # Load chunk metadata
        self._setup_llm()           # Initialize Ollama
        self._verify_ollama()       # Check connection
    
    def retrieve(self, query, top_k):
        # Semantic search in FAISS
        
    def generate_answer(self, question, chunks):
        # Call LLM with context
        
    def check_faithfulness(self, answer, chunks):
        # Verify answer matches context
        
    def ask(self, question, top_k, debug):
        # Complete pipeline
```

**Detailed Flow:**

#### Step 1: Retrieve
```python
def retrieve(self, query: str, top_k: int = 7):
    # 1. Embed the query using same model as documents
    # 2. Search FAISS index for similar vectors
    docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=top_k)
    
    # 3. Filter by similarity threshold
    results = []
    for doc, score in docs_with_scores:
        if score >= SIMILARITY_THRESHOLD:
            results.append({
                "chunk_id": doc.metadata['chunk_id'],
                "doc_name": doc.metadata['doc_name'],
                "page": doc.metadata['page'],
                "text": doc.page_content,
                "similarity_score": score
            })
    
    return results
```

#### Step 2: Generate Answer
```python
def generate_answer(self, question: str, chunks: List[Dict]):
    # 1. Build context with citations
    context_parts = []
    for chunk in chunks:
        context_parts.append(
            f"[Source: {chunk['doc_name']}, Page: {chunk['page']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_parts)
    
    # 2. Format prompt
    formatted_prompt = self.prompt.format(
        context=context,
        question=question
    )
    
    # 3. Call LLM
    answer = self.llm.invoke(formatted_prompt)
    
    return answer.strip()
```

#### Step 3: Check Faithfulness
```python
def check_faithfulness(self, answer: str, chunks: List[Dict]):
    # 1. Extract meaningful words from answer
    answer_words = [w for w in answer.lower().split() 
                    if len(w) >= 3 and w not in stop_words]
    
    # 2. Check how many appear in context
    context = " ".join([chunk["text"] for chunk in chunks])
    matched = sum(1 for word in answer_words if word in context.lower())
    
    # 3. Calculate score
    base_score = matched / len(answer_words)
    
    # 4. Bonus for phrase matches
    # (checks for 3+ word sequences)
    
    return final_score
```

#### Step 4: Complete Pipeline
```python
def ask(self, question: str, top_k: int = 7, debug: bool = False):
    # 1. Retrieve relevant chunks
    chunks = self.retrieve(question, top_k)
    
    # 2. If no chunks, return "not available"
    if not chunks:
        return {
            "answer": NO_ANSWER_RESPONSE,
            "citations": [],
            "faithfulness_score": 1.0
        }
    
    # 3. Generate answer
    answer = self.generate_answer(question, chunks)
    
    # 4. Check faithfulness
    faithfulness_score = self.check_faithfulness(answer, chunks)
    
    # 5. Override if faithfulness too low
    if faithfulness_score < FAITHFULNESS_THRESHOLD:
        answer = NO_ANSWER_RESPONSE
    
    # 6. Build response
    return {
        "answer": answer,
        "citations": [...],
        "faithfulness_score": faithfulness_score,
        "retrieved_chunks": chunks if debug else None
    }
```

**Prompt Template:**
```
You are an aviation document assistant. Your knowledge source is the
context provided below from official aviation documents.

INSTRUCTIONS:
1. Answer questions using the information in the provided context.
2. For factual questions: Provide direct information from the context.
3. For applied/reasoning questions: You may synthesize and combine 
   information from multiple parts of the context.
4. You may make reasonable inferences based on the context, but 
   clearly indicate when you are doing so.
5. If the context lacks sufficient information, respond with: 
   "This information is not available in the provided document(s)."
6. Always cite which source document and page your answer comes from.

<context>
{context}
</context>

<question>
{question}
</question>

Answer:
```



### 4. app.py - FastAPI Server

**Purpose:** HTTP API for the RAG system

**Key Components:**

#### Pydantic Models (Request/Response validation)
```python
class AskRequest(BaseModel):
    question: str
    top_k: Optional[int] = 7
    debug: Optional[bool] = False

class AskResponse(BaseModel):
    answer: str
    citations: List[dict]
    faithfulness_score: float
    retrieved_chunks: Optional[List[dict]] = None
```

#### Startup Event
```python
@app.on_event("startup")
async def startup_event():
    global rag_pipeline
    
    # Check if FAISS index exists
    if os.path.exists(FAISS_INDEX_DIR):
        rag_pipeline = RAGPipeline()  # Load pipeline
    else:
        rag_pipeline = None  # Need to run ingestion first
```

#### Routes

**1. Home Route - Web UI**
```python
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

**2. Health Check**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "index_loaded": rag_pipeline is not None,
        "total_chunks": 3983,
        "documents": ["10-General-Navigation-2014.pdf", ...],
        "ollama_reachable": True,
        "model": "llama3.1:8b"
    }
```

**3. Ask Question**
```python
@app.post("/ask")
async def ask_endpoint(request: AskRequest):
    # Validate pipeline is loaded
    if rag_pipeline is None:
        raise HTTPException(503, "Index not loaded")
    
    # Call RAG pipeline
    result = rag_pipeline.ask(
        question=request.question,
        top_k=request.top_k,
        debug=request.debug
    )
    
    return AskResponse(**result)
```

**4. Ingest Documents**
```python
@app.post("/ingest")
async def ingest_endpoint(request: IngestRequest):
    # Run ingestion
    ingest_documents(request.pdf_paths)
    
    # Reload pipeline
    rag_pipeline = RAGPipeline()
    
    return {
        "status": "success",
        "documents_processed": 7,
        "total_chunks": 3983
    }
```



### 5. templates/index.html - Web Interface

**Purpose:** User-friendly chat interface

**Key Features:**

#### Theme Management
```javascript
// Load saved theme from localStorage
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);

// Toggle theme
themeToggle.addEventListener('click', () => {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});
```

#### Status Checking
```javascript
async function checkStatus() {
    const response = await fetch('/health');
    const data = await response.json();
    
    if (data.index_loaded && data.ollama_reachable) {
        statusBadge.className = 'status-badge online';
        statusText.textContent = `Online (${data.total_chunks} chunks)`;
    } else {
        statusBadge.className = 'status-badge offline';
        statusText.textContent = 'Offline';
    }
}

// Check every 30 seconds
setInterval(checkStatus, 30000);
```

#### Ask Question
```javascript
async function askQuestion() {
    const question = input.value.trim();
    
    // Add user message to chat
    addMessage(question, 'user');
    
    // Call API
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question, top_k: 5 })
    });
    
    const data = await response.json();
    
    // Add bot response with citations
    addMessage(data.answer, 'bot', data.citations, data.faithfulness_score);
}
```

#### Message Display
```javascript
function addMessage(text, type, citations, faithfulness) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    
    let content = `<div class="message-content">${text}`;
    
    // Add citations if present
    if (citations && citations.length > 0) {
        content += '<div class="citations">';
        content += '<div class="citations-title">📚 Sources:</div>';
        citations.forEach(cite => {
            content += `<div class="citation-item">• ${cite.doc_name}, Page ${cite.page}</div>`;
        });
        content += `<div class="faithfulness-score">Faithfulness: ${(faithfulness * 100).toFixed(0)}%</div>`;
        content += '</div>';
    }
    
    content += '</div>';
    messageDiv.innerHTML = content;
    messages.appendChild(messageDiv);
}
```

**CSS Theming:**
```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #1a1a1a;
    --accent-primary: #0066cc;
}

[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --text-primary: #e0e0e0;
    --accent-primary: #3399ff;
}
```



### 6. evaluate.py - Evaluation System

**Purpose:** Automated testing and metrics

**Process:**
```python
class Evaluator:
    def run_evaluation(self):
        # 1. Load questions from questions.json
        questions = self.load_questions()
        
        # 2. For each question
        for q in questions:
            # 3. Call API
            result = self.ask_question(q["question"])
            
            # 4. Compute metrics
            eval_result = {
                "retrieval_hit": self.compute_retrieval_hit(...),
                "faithfulness_score": result["faithfulness_score"],
                "hallucinated": faithfulness < threshold,
                "no_answer_returned": answer == NO_ANSWER_RESPONSE,
                "latency_ms": response_time
            }
            
            results.append(eval_result)
        
        # 5. Generate summary by category
        self.print_summary(results)
        
        # 6. Save to JSON
        self.save_results(results)
```

**Metrics Calculated:**
- Retrieval Hit Rate: % of questions where expected keywords found
- Avg Faithfulness: How well answers match context
- Hallucination Rate: % of unfaithful answers
- No-Answer Rate: % of "not available" responses
- Avg Latency: Response time per question

---

## Data Flow

### Complete Request Flow

```
1. USER TYPES QUESTION
   "What are the main types of clouds?"
   
2. BROWSER SENDS REQUEST
   POST /ask
   {
     "question": "What are the main types of clouds?",
     "top_k": 7
   }
   
3. FASTAPI RECEIVES REQUEST
   - Validates request (Pydantic)
   - Checks if rag_pipeline loaded
   
4. RAG PIPELINE: RETRIEVE
   - Embed query: "What are the main types of clouds?"
     → [0.123, -0.456, 0.789, ...] (768 dimensions)
   
   - FAISS search for similar vectors
   - Returns top 7 chunks with scores:
     * Chunk 249 (Meteorology p203): score 0.92
     * Chunk 244 (Meteorology p199): score 0.89
     * Chunk 248 (Meteorology p202): score 0.87
     * ...
   
   - Filter by threshold (0.30)
   - All 7 chunks pass
   
5. RAG PIPELINE: GENERATE
   - Build context from 7 chunks
   - Format prompt:
     """
     You are an aviation document assistant...
     
     <context>
     [Source: Meteorology full book.pdf, Page: 203]
     The three basic forms of cloud are stratiform...
     
     [Source: Meteorology full book.pdf, Page: 199]
     Clouds are classified into different types...
     </context>
     
     <question>
     What are the main types of clouds?
     </question>
     
     Answer:
     """
   
   - Send to Ollama LLM
   - Receive answer:
     "The three basic forms of cloud are:
      1. Stratiform (layered type)
      2. Cumuliform (heaped cloud)
      3. Cirriform (fibrous, wispy)
      [Source: Meteorology full book.pdf, Page: 202]"
   
6. RAG PIPELINE: CHECK FAITHFULNESS
   - Extract words: ["three", "basic", "forms", "cloud", "stratiform", ...]
   - Check against context
   - Matched: 15/18 words = 0.83
   - Phrase bonus: +0.05
   - Final score: 0.88
   
   - Score 0.88 > threshold 0.50 ✓
   - Answer is faithful!
   
7. RAG PIPELINE: BUILD RESPONSE
   {
     "answer": "The three basic forms of cloud are...",
     "citations": [
       {"doc_name": "Meteorology full book.pdf", "page": 203},
       {"doc_name": "Meteorology full book.pdf", "page": 199},
       ...
     ],
     "faithfulness_score": 0.88,
     "retrieved_chunks": null  // debug=false
   }
   
8. FASTAPI RETURNS RESPONSE
   HTTP 200 OK
   Content-Type: application/json
   
9. BROWSER RECEIVES RESPONSE
   - Parses JSON
   - Adds bot message to chat
   - Displays citations
   - Shows faithfulness: 88%
   
10. USER SEES ANSWER
    ✓ Answer displayed
    ✓ Sources cited
    ✓ Faithfulness score shown
```



---

## Configuration

### Tuning Parameters

#### Chunk Size (CHUNK_SIZE = 400 words)
**Effect:**
- Larger chunks: More context per chunk, but less precise retrieval
- Smaller chunks: More precise, but may miss context

**When to adjust:**
- Increase if answers lack context
- Decrease if retrieval is too broad

#### Top-K (TOP_K = 7)
**Effect:**
- More chunks: Better context, slower, more noise
- Fewer chunks: Faster, but may miss information

**When to adjust:**
- Increase if "not available" rate is high
- Decrease if responses are slow

#### Similarity Threshold (SIMILARITY_THRESHOLD = 0.30)
**Effect:**
- Higher threshold: Only very relevant chunks
- Lower threshold: More chunks, but less relevant

**When to adjust:**
- Increase if getting irrelevant information
- Decrease if not finding relevant chunks

#### Faithfulness Threshold (FAITHFULNESS_THRESHOLD = 0.50)
**Effect:**
- Higher threshold: More conservative, fewer answers
- Lower threshold: More answers, risk of hallucinations

**When to adjust:**
- Increase if hallucinations occur
- Decrease if too many "not available" responses

#### Temperature (OLLAMA_TEMPERATURE = 0.0)
**Effect:**
- 0.0: Deterministic, same answer every time
- Higher: More creative, but less predictable

**When to adjust:**
- Keep at 0.0 for factual questions
- Increase slightly (0.1-0.3) for creative tasks

---

## API Endpoints

### GET /
**Purpose:** Serve web interface

**Response:** HTML page

**Example:**
```bash
curl http://localhost:8000/
```

### GET /health
**Purpose:** Check system status

**Response:**
```json
{
  "status": "ok",
  "index_loaded": true,
  "total_chunks": 3983,
  "documents": [
    "10-General-Navigation-2014.pdf",
    "11-radio-navigation-2014.pdf",
    ...
  ],
  "ollama_reachable": true,
  "model": "llama3.1:8b"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

### POST /ask
**Purpose:** Ask a question

**Request:**
```json
{
  "question": "What are the main types of clouds?",
  "top_k": 7,
  "debug": false
}
```

**Response:**
```json
{
  "answer": "The three basic forms of cloud are...",
  "citations": [
    {
      "doc_name": "Meteorology full book.pdf",
      "page": 203,
      "chunk_id": "meteorology_full_book_p203_c249"
    }
  ],
  "faithfulness_score": 0.88,
  "retrieved_chunks": null
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are cloud types?", "top_k": 5}'
```

### POST /ingest
**Purpose:** Ingest new documents

**Request:**
```json
{
  "pdf_paths": null  // null = scan documents/ directory
}
```

**Response:**
```json
{
  "status": "success",
  "documents_processed": 7,
  "total_chunks": 3983
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## Web Interface

### Features

1. **Chat Interface**
   - Message bubbles (user: blue, bot: gray)
   - Smooth animations
   - Auto-scroll to latest message

2. **Theme Toggle**
   - Light/Dark mode
   - Persists in localStorage
   - Smooth transitions

3. **Status Indicator**
   - Online/Offline badge
   - Shows chunk count
   - Auto-updates every 30s

4. **Citations Display**
   - Source document name
   - Page number
   - Faithfulness score

5. **Sample Questions**
   - Quick-start examples
   - Click to ask

### User Flow

```
1. User opens http://localhost:8000
2. Page loads with welcome message
3. Status badge shows "Online (3983 chunks)"
4. User clicks sample question OR types own
5. Question appears in chat (blue bubble)
6. Loading indicator shows
7. Bot response appears (gray bubble)
8. Citations shown below answer
9. User can ask follow-up questions
```



---

## Evaluation System

### Running Evaluation

```bash
# Test all 50 questions
python evaluate.py

# Only questions with ground truth
python evaluate.py --require-ground-truth

# Custom port
python evaluate.py --port 8080
```

### Metrics Explained

**Retrieval Hit Rate**
- Measures: Did we find relevant chunks?
- Calculation: % of questions where expected keywords found in retrieved chunks
- Good: >70%
- Acceptable: 50-70%
- Poor: <50%

**Average Faithfulness**
- Measures: Do answers match retrieved context?
- Calculation: Average faithfulness score across all questions
- Good: >0.75
- Acceptable: 0.65-0.75
- Poor: <0.65

**Hallucination Rate**
- Measures: How often does system make up information?
- Calculation: % of answers with faithfulness < threshold
- Good: <5%
- Acceptable: 5-10%
- Poor: >10%

**No-Answer Rate**
- Measures: How often does system say "not available"?
- Calculation: % of questions returning NO_ANSWER_RESPONSE
- Note: High rate isn't necessarily bad - shows conservative behavior
- Target: 10-30% (depends on document coverage)

**Average Latency**
- Measures: Response time
- Calculation: Average milliseconds per question
- Good: <5s
- Acceptable: 5-10s
- Poor: >10s

### Output Files

**data/eval_results.json**
```json
{
  "results": [
    {
      "id": 1,
      "category": "factual",
      "question": "What are cloud types?",
      "answer": "The three basic forms...",
      "citations": [...],
      "faithfulness_score": 0.88,
      "retrieval_hit": true,
      "hallucinated": false,
      "no_answer_returned": false,
      "latency_ms": 4523
    }
  ]
}
```

---

## Deployment

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Ollama
ollama serve

# 3. Pull model
ollama pull llama3.1:8b

# 4. Ingest documents (one-time)
python ingest_fast.py

# 5. Start API server
python app.py

# 6. Open browser
# http://localhost:8000
```

### Production Deployment

#### Option 1: Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t airman:latest .

# Run
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/documents:/app/documents \
  airman:latest
```

#### Option 2: Cloud (AWS/Azure/GCP)

1. **Package application**
   ```bash
   zip -r airman.zip . -x "*.git*" "*.pyc" "__pycache__/*"
   ```

2. **Upload to cloud storage**
   - AWS S3
   - Azure Blob Storage
   - GCP Cloud Storage

3. **Deploy to compute service**
   - AWS EC2 / ECS / Lambda
   - Azure App Service / Container Instances
   - GCP Compute Engine / Cloud Run

4. **Configure environment**
   - Set OLLAMA_BASE_URL
   - Mount data volumes
   - Configure networking

5. **Set up monitoring**
   - Health check endpoint: /health
   - Logs: Use loguru output
   - Metrics: Response times, error rates

### Environment Variables

```bash
# Optional overrides
export OLLAMA_BASE_URL="http://ollama-server:11434"
export FAISS_INDEX_DIR="/data/faiss_index"
export DOCUMENTS_DIR="/data/documents"
```

### Performance Optimization

**GPU Acceleration**
- Ensure CUDA available
- Check with: `nvidia-smi`
- Embeddings use GPU automatically

**Caching**
- FAISS index loaded once at startup
- Embeddings model loaded once
- Metadata cached in memory

**Scaling**
- Use multiple workers: `uvicorn app:app --workers 4`
- Load balance across instances
- Cache frequent queries (Redis)

---

## Troubleshooting

### Common Issues

**1. "FAISS index not found"**
```bash
# Solution: Run ingestion
python ingest_fast.py
```

**2. "Cannot reach Ollama"**
```bash
# Solution: Start Ollama
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

**3. "Template not found"**
```bash
# Solution: Check templates directory exists
ls templates/index.html

# Restart server
python app.py
```

**4. "Slow responses"**
```bash
# Check GPU usage
nvidia-smi

# Verify GPU being used
# Look for "device: cuda" in logs
```

**5. "Too many 'not available' responses"**
```python
# Solution: Lower thresholds in config.py
FAITHFULNESS_THRESHOLD = 0.40  # from 0.50
SIMILARITY_THRESHOLD = 0.25    # from 0.30
TOP_K = 10                     # from 7
```

**6. "Hallucinations occurring"**
```python
# Solution: Increase faithfulness threshold
FAITHFULNESS_THRESHOLD = 0.65  # from 0.50

# Make prompt stricter in rag.py
```

**7. "PDF produces 0 chunks" (Scanned PDF Issue)**

**Problem:** Some PDFs are scanned images, not text-based documents.

**Example from logs:**
```
Processing: Air-Regulation-RK-BALI.pdf
Loaded 348 pages
Created 0 chunks (avg 0.0 words)  ← Problem!
```

**Diagnosis:**
```bash
# Check if PDF is scanned
# Try to select text in PDF viewer
# If you can't select text → Scanned PDF

# Or use pdftotext
pdftotext documents/Air-Regulation-RK-BALI.pdf test.txt
wc -w test.txt  # If 0 words → Scanned PDF
```

**Solutions:**

**Option A: Use OCR (Optical Character Recognition)**
```bash
# Install OCR dependencies
# Ubuntu/WSL:
sudo apt-get install tesseract-ocr poppler-utils
pip install pdf2image pytesseract pillow

# Windows: Download Tesseract from
# https://github.com/UB-Mannheim/tesseract/wiki

# macOS:
brew install tesseract poppler
pip install pdf2image pytesseract pillow

# Extract text with OCR (slow, 30-60 min for 348 pages)
python -c "
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path('documents/Air-Regulation-RK-BALI.pdf', dpi=300)
text = []
for i, img in enumerate(images, 1):
    text.append(pytesseract.image_to_string(img))
    if i % 10 == 0: print(f'Processed {i}/{len(images)}')

with open('documents/Air-Regulation-RK-BALI-OCR.txt', 'w') as f:
    f.write('\n\n'.join(text))
"

# Then re-run ingestion
python ingest_fast.py
```

**Option B: Get Text-Based Version (Recommended)**
- Contact document source
- Request digital/born-digital PDF
- Much faster and more accurate than OCR

**Option C: Skip Document**
- Remove from documents/ folder
- System works with remaining documents
- Current system: 3,983 chunks from 7 working PDFs

**Prevention:**
```bash
# Before adding new PDFs, verify they're text-based
pdftotext new_document.pdf test.txt
wc -w test.txt  # Should show word count > 0

# If scanned, process with OCR first
```

**Impact:**
- Questions about content in scanned PDF will return "not available"
- System remains functional with other documents
- See `SCANNED_PDF_GUIDE.md` for detailed instructions

### Debug Mode

Enable debug output:
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check retrieved chunks:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are clouds?", "debug": true}'
```

---

## Development Workflow

### Adding New Documents

1. **Verify PDF is text-based (not scanned):**
   ```bash
   # Test if text can be extracted
   pdftotext new_document.pdf test.txt
   wc -w test.txt  # Should show word count > 0
   
   # If 0 words → Scanned PDF (needs OCR)
   # See SCANNED_PDF_GUIDE.md for OCR instructions
   ```

2. Place PDF in `documents/` directory

3. Run ingestion:
   ```bash
   python ingest_fast.py
   ```

4. Check ingestion logs for chunk count:
   ```bash
   tail -20 ingestion_fast.log
   # Look for: "Created X chunks (avg Y words)"
   # If X = 0 → Scanned PDF issue
   ```

5. Restart API server:
   ```bash
   python app.py
   ```

6. Verify with health check:
   ```bash
   curl http://localhost:8000/health
   # Check total_chunks increased
   ```

**Note:** If a PDF produces 0 chunks, it's likely a scanned image PDF. See troubleshooting section #7 for solutions.

### Modifying Prompt

1. Edit `rag.py` → `_setup_llm()` → `template`
2. Restart server
3. Test with sample questions
4. Run evaluation:
   ```bash
   python evaluate.py
   ```

### Tuning Parameters

1. Edit `config.py`
2. Restart server (no re-ingestion needed)
3. Test changes
4. Compare evaluation results

### Adding Features

1. **New API endpoint:**
   - Add route in `app.py`
   - Define Pydantic models
   - Implement logic

2. **New UI feature:**
   - Edit `templates/index.html`
   - Add JavaScript function
   - Update CSS if needed

3. **New metric:**
   - Add calculation in `evaluate.py`
   - Update summary table
   - Document in EVALUATION_GUIDE.md

---

## Code Quality

### Best Practices

1. **Type hints**
   ```python
   def retrieve(self, query: str, top_k: int) -> List[Dict]:
   ```

2. **Docstrings**
   ```python
   def check_faithfulness(self, answer: str, chunks: List[Dict]) -> float:
       """
       Check if answer is faithful to retrieved context
       
       Args:
           answer: Generated answer
           chunks: Retrieved chunks
       
       Returns:
           Faithfulness score (0.0-1.0)
       """
   ```

3. **Logging**
   ```python
   self.logger.info(f"Retrieved {len(chunks)} chunks")
   self.logger.debug(f"Faithfulness: {score:.2f}")
   self.logger.error(f"Failed to process: {e}")
   ```

4. **Error handling**
   ```python
   try:
       result = self.ask_question(question)
   except Exception as e:
       self.logger.error(f"Error: {e}")
       raise HTTPException(500, detail=str(e))
   ```

### Testing

**Manual testing:**
```bash
# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ask -d '{"question": "test"}'

# Test UI
# Open http://localhost:8000 in browser
```

**Automated testing:**
```bash
# Run evaluation
python evaluate.py

# Check results
cat data/eval_results.json
```

---

## Summary

AIRMAN is a production-ready RAG system with:

✅ **Robust architecture** - Modular, maintainable code
✅ **GPU acceleration** - Fast embeddings and retrieval
✅ **Faithfulness checking** - Prevents hallucinations
✅ **User-friendly UI** - Dark/light theme, citations
✅ **Evaluation framework** - Automated testing
✅ **Comprehensive docs** - Easy to understand and extend

**Key Files:**
- `config.py` - Tune parameters
- `rag.py` - Core RAG logic
- `app.py` - API server
- `ingest_fast.py` - Document processing
- `evaluate.py` - Testing

**Key Concepts:**
- Retrieval-Augmented Generation (RAG)
- Vector embeddings (768-dim)
- Semantic search (FAISS)
- Faithfulness checking
- Citation tracking

---

**Version:** 1.0.0  
**Last Updated:** February 12, 2026  
**Author:** AIRMAN Development Team
