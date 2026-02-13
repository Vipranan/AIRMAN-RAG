"""
app.py - FastAPI application for Aviation Document AI Chat
"""

import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from loguru import logger
import config
# from rag import RAGPipeline
from rag_hybrid import HybridRAGPipeline as RAGPipeline

from ingest import ingest_documents


# Pydantic models
class AskRequest(BaseModel):
    question: str
    top_k: Optional[int] = config.TOP_K
    debug: Optional[bool] = False


class IngestRequest(BaseModel):
    pdf_paths: Optional[List[str]] = None


class AskResponse(BaseModel):
    answer: str
    citations: List[dict]
    faithfulness_score: float
    retrieved_chunks: Optional[List[dict]] = None


class HealthResponse(BaseModel):
    status: str
    index_loaded: bool
    total_chunks: int
    documents: List[str]
    ollama_reachable: bool
    model: str


class IngestResponse(BaseModel):
    status: str
    documents_processed: int
    total_chunks: int


# FastAPI app
app = FastAPI(
    title="AIRMAN - Aviation Document AI Chat",
    description="RAG system for aviation documents (PPL/CPL/ATPL textbooks, SOPs, Flight Manuals)",
    version="1.0.0"
)

# Setup templates - use absolute path relative to this file
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Global RAG pipeline instance
rag_pipeline: Optional[RAGPipeline] = None


@app.on_event("startup")
async def startup_event():
    """Load RAG pipeline on startup"""
    global rag_pipeline
    
    logger.info("Starting AIRMAN Aviation Document AI Chat API (LangChain-powered)...")
    
    # Check if FAISS index exists
    index_path = config.FAISS_INDEX_DIR
    
    if not os.path.exists(index_path):
        logger.warning(
            f"FAISS index not found at {index_path}. "
            "Run ingest.py or use POST /ingest to create index."
        )
        rag_pipeline = None
    else:
        try:
            rag_pipeline = RAGPipeline()
            logger.success("RAG pipeline loaded successfully with LangChain")
        except Exception as e:
            logger.error(f"Failed to load RAG pipeline: {e}")
            rag_pipeline = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main chat interface"""
    logger.info(f"Template directory: {TEMPLATE_DIR}")
    logger.info(f"Template exists: {os.path.exists(os.path.join(TEMPLATE_DIR, 'index.html'))}")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    
    index_loaded = rag_pipeline is not None
    total_chunks = 0
    documents = []
    
    if index_loaded:
        # Get total chunks from vectorstore
        total_chunks = rag_pipeline.vectorstore.index.ntotal
        # Extract unique document names from metadata
        documents = list(set(chunk["doc_name"] for chunk in rag_pipeline.metadata))
    
    # Check Ollama
    ollama_reachable = False
    try:
        response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        ollama_reachable = response.status_code == 200
    except:
        pass
    
    return HealthResponse(
        status="ok",
        index_loaded=index_loaded,
        total_chunks=total_chunks,
        documents=sorted(documents),
        ollama_reachable=ollama_reachable,
        model=config.OLLAMA_MODEL
    )


@app.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest):
    """
    Ingest PDF documents and build FAISS index using LangChain
    
    If pdf_paths is None, scans ./documents/ directory
    """
    global rag_pipeline
    
    try:
        logger.info("Starting ingestion via API with LangChain...")
        
        # Run ingestion
        ingest_documents(request.pdf_paths)
        
        # Reload RAG pipeline
        rag_pipeline = RAGPipeline()
        
        total_chunks = rag_pipeline.vectorstore.index.ntotal
        documents = list(set(chunk["doc_name"] for chunk in rag_pipeline.metadata))
        
        return IngestResponse(
            status="success",
            documents_processed=len(documents),
            total_chunks=total_chunks
        )
    
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: AskRequest):
    """
    Ask a question about aviation documents
    """
    
    # Check if index is loaded
    if rag_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="FAISS index not loaded. Run POST /ingest first or check logs."
        )
    
    try:
        # Call RAG pipeline
        result = rag_pipeline.ask(
            question=request.question,
            top_k=request.top_k,
            debug=request.debug
        )
        
        return AskResponse(**result)
    
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
