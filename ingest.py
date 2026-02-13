"""
ingest.py - Full ingestion pipeline for aviation documents using LangChain
Extracts text from PDFs, chunks intelligently, embeds, and builds FAISS index
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict
from loguru import logger

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

import config


class DocumentProcessor:
    """
    Process aviation documents using LangChain.
    
    Aviation documents (AFM procedures, ATPL meteorology, SOP checklists) contain
    dense, context-dependent content. A 400-word chunk (~1600 chars) fits roughly 
    one procedure or one concept section. 50-word overlap (~200 chars) ensures that 
    cross-boundary references (e.g., a limitation mentioned at the end of one chunk 
    that is referenced at the start of the next) are preserved for retrieval.
    
    Multi-doc aware: each chunk carries doc_name + page so citations are exact.
    """
    
    def __init__(self):
        self.logger = logger
        
        # Initialize text splitter with character-based splitting
        # 400 words ≈ 1600 characters (avg 4 chars/word)
        # 50 words overlap ≈ 200 characters
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1600,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            is_separator_regex=False
        )
    
    def load_and_split_pdf(self, pdf_path: str) -> List[Document]:
        """
        Load PDF and split into chunks using LangChain
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of LangChain Document objects with metadata
        """
        self.logger.info(f"Loading PDF: {pdf_path}")
        
        # Load PDF using LangChain's PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        self.logger.info(f"  Loaded {len(pages)} pages")
        
        # Split pages into chunks
        chunks = self.text_splitter.split_documents(pages)
        
        # Enhance metadata with chunk IDs and doc name
        doc_name = Path(pdf_path).name
        doc_stem = Path(pdf_path).stem.lower().replace(' ', '_').replace('-', '_')
        
        for i, chunk in enumerate(chunks):
            page_num = chunk.metadata.get('page', 0) + 1  # PyPDF uses 0-indexed pages
            chunk_id = f"{doc_stem}_p{page_num:03d}_c{i:03d}"
            
            chunk.metadata.update({
                'chunk_id': chunk_id,
                'doc_name': doc_name,
                'page': page_num,
                'chunk_index': i,
                'word_count': len(chunk.page_content.split())
            })
        
        # Filter out very short chunks
        chunks = [c for c in chunks if c.metadata['word_count'] >= config.MIN_CHUNK_WORDS]
        
        avg_chunk_len = sum(c.metadata['word_count'] for c in chunks) / len(chunks) if chunks else 0
        self.logger.info(f"  Created {len(chunks)} chunks (avg {avg_chunk_len:.1f} words)")
        
        return chunks


def ingest_documents(pdf_paths: List[str] = None):
    """Main ingestion pipeline using LangChain"""
    logger.info("Starting ingestion pipeline with LangChain...")
    
    # Determine which PDFs to process
    if pdf_paths is None:
        pdf_dir = Path(config.DOCUMENTS_DIR)
        if not pdf_dir.exists():
            logger.error(f"Documents directory not found: {config.DOCUMENTS_DIR}")
            return
        
        # Find all PDFs recursively including subdirectories
        pdf_paths = list(pdf_dir.rglob("*.pdf"))
        if not pdf_paths:
            logger.warning(f"No PDF files found in {config.DOCUMENTS_DIR}")
            return
    else:
        pdf_paths = [Path(p) for p in pdf_paths]
    
    logger.info(f"Found {len(pdf_paths)} PDF(s) to process")
    
    # Initialize components
    processor = DocumentProcessor()
    
    # Process all documents
    all_chunks = []
    total_pages = 0
    
    for pdf_path in pdf_paths:
        logger.info(f"Processing: {pdf_path.name}")
        
        try:
            # Load and split PDF
            chunks = processor.load_and_split_pdf(str(pdf_path))
            all_chunks.extend(chunks)
            
            # Count unique pages
            unique_pages = len(set(c.metadata['page'] for c in chunks))
            total_pages += unique_pages
            
        except Exception as e:
            logger.error(f"Failed to process {pdf_path.name}: {e}")
            continue
    
    if not all_chunks:
        logger.error("No chunks created. Aborting.")
        return
    
    logger.info(f"\nTotal: {len(pdf_paths)} documents, {total_pages} pages, {len(all_chunks)} chunks")
    
    # Initialize embeddings using LangChain
    logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Create FAISS vector store from documents
    logger.info("Creating FAISS vector store...")
    vectorstore = FAISS.from_documents(all_chunks, embeddings)
    
    # Save vector store
    os.makedirs(config.FAISS_INDEX_DIR, exist_ok=True)
    vectorstore.save_local(config.FAISS_INDEX_DIR)
    logger.info(f"FAISS vector store saved to {config.FAISS_INDEX_DIR}")
    
    # Save metadata separately for easy access
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
    parser = argparse.ArgumentParser(description="Ingest aviation PDFs into FAISS index using LangChain")
    parser.add_argument("--file", type=str, help="Process single PDF file")
    args = parser.parse_args()
    
    if args.file:
        ingest_documents([args.file])
    else:
        ingest_documents()
