"""
ingest_fast.py - Faster ingestion with optimized batch processing
"""

import os
import json
from pathlib import Path
from typing import List
from loguru import logger
import torch

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

import config


class FastDocumentProcessor:
    """Fast document processing with optimized settings"""
    
    def __init__(self):
        self.logger = logger
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1600,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            is_separator_regex=False
        )
    
    def load_and_split_pdf(self, pdf_path: str) -> List[Document]:
        """Load PDF and split into chunks"""
        self.logger.info(f"Loading PDF: {pdf_path}")
        
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        self.logger.info(f"  Loaded {len(pages)} pages")
        
        chunks = self.text_splitter.split_documents(pages)
        
        doc_name = Path(pdf_path).name
        doc_stem = Path(pdf_path).stem.lower().replace(' ', '_').replace('-', '_')
        
        for i, chunk in enumerate(chunks):
            page_num = chunk.metadata.get('page', 0) + 1
            chunk_id = f"{doc_stem}_p{page_num:03d}_c{i:03d}"
            
            chunk.metadata.update({
                'chunk_id': chunk_id,
                'doc_name': doc_name,
                'page': page_num,
                'chunk_index': i,
                'word_count': len(chunk.page_content.split())
            })
        
        chunks = [c for c in chunks if c.metadata['word_count'] >= config.MIN_CHUNK_WORDS]
        
        avg_chunk_len = sum(c.metadata['word_count'] for c in chunks) / len(chunks) if chunks else 0
        self.logger.info(f"  Created {len(chunks)} chunks (avg {avg_chunk_len:.1f} words)")
        
        return chunks


def ingest_documents_fast():
    """Fast ingestion with GPU support and larger batches"""
    logger.info("Starting FAST ingestion pipeline...")
    
    # Find all PDFs
    pdf_dir = Path(config.DOCUMENTS_DIR)
    pdf_paths = list(pdf_dir.rglob("*.pdf"))
    
    if not pdf_paths:
        logger.warning(f"No PDF files found in {config.DOCUMENTS_DIR}")
        return
    
    logger.info(f"Found {len(pdf_paths)} PDF(s) to process")
    
    # Process documents
    processor = FastDocumentProcessor()
    all_chunks = []
    
    for pdf_path in pdf_paths:
        logger.info(f"Processing: {pdf_path.name}")
        try:
            chunks = processor.load_and_split_pdf(str(pdf_path))
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"Failed to process {pdf_path.name}: {e}")
            continue
    
    if not all_chunks:
        logger.error("No chunks created. Aborting.")
        return
    
    logger.info(f"\nTotal chunks: {len(all_chunks)}")
    
    # Check for GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {device}")
    
    # Initialize embeddings with optimized settings
    logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={'device': device},  # Use GPU if available
        encode_kwargs={
            'normalize_embeddings': True,
            'batch_size': 128  # Larger batch size for GPU
        }
    )
    
    # Create FAISS vector store with progress
    logger.info("Creating FAISS vector store (this may take 5-15 minutes)...")
    logger.info(f"Processing {len(all_chunks)} chunks in batches of 128...")
    
    vectorstore = FAISS.from_documents(all_chunks, embeddings)
    
    # Save
    os.makedirs(config.FAISS_INDEX_DIR, exist_ok=True)
    vectorstore.save_local(config.FAISS_INDEX_DIR)
    logger.info(f"FAISS vector store saved to {config.FAISS_INDEX_DIR}")
    
    # Save metadata
    metadata = [
        {
            "chunk_id": chunk.metadata['chunk_id'],
            "doc_name": chunk.metadata['doc_name'],
            "page": chunk.metadata['page'],
            "chunk_index": chunk.metadata['chunk_index'],
            "word_count": chunk.metadata['word_count'],
            "text": chunk.page_content
        }
        for chunk in all_chunks
    ]
    
    with open(config.METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    logger.info(f"Metadata saved to {config.METADATA_PATH}")
    
    logger.success(f"Ingestion complete! Total chunks: {len(all_chunks)}")


if __name__ == "__main__":
    ingest_documents_fast()
