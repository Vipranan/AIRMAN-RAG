"""
ingest_with_ocr.py - Document ingestion with OCR support for scanned PDFs
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

# For OCR support
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("OCR libraries not available. Install with: pip install pdf2image pytesseract pillow")

import config


class OCRDocumentProcessor:
    """Document processor with OCR fallback for scanned PDFs"""
    
    def __init__(self):
        self.logger = logger
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1600,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            is_separator_regex=False
        )
    
    def extract_text_with_ocr(self, pdf_path: str) -> List[Document]:
        """Extract text from scanned PDF using OCR"""
        if not OCR_AVAILABLE:
            self.logger.error("OCR not available. Cannot process scanned PDF.")
            return []
        
        self.logger.info(f"Using OCR for: {pdf_path}")
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=300)
            
            documents = []
            doc_name = Path(pdf_path).name
            
            for page_num, image in enumerate(images, start=1):
                # Extract text using Tesseract OCR
                text = pytesseract.image_to_string(image)
                
                if text.strip():
                    doc = Document(
                        page_content=text,
                        metadata={
                            'source': pdf_path,
                            'page': page_num,
                            'doc_name': doc_name
                        }
                    )
                    documents.append(doc)
                
                if page_num % 10 == 0:
                    self.logger.info(f"  OCR processed {page_num}/{len(images)} pages")
            
            self.logger.info(f"  OCR extracted text from {len(documents)} pages")
            return documents
            
        except Exception as e:
            self.logger.error(f"OCR failed: {e}")
            return []
