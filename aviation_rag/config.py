# config.py
# All tunable parameters in one place

# Paths
DOCUMENTS_DIR = "./documents"
FAISS_INDEX_DIR = "./data/faiss_index"
METADATA_PATH = "./data/metadata.json"

# Chunking
CHUNK_SIZE = 400          # words per chunk
CHUNK_OVERLAP = 50        # words of overlap between chunks
MIN_CHUNK_WORDS = 30      # discard chunks shorter than this

# Embeddings
EMBEDDING_MODEL = "multi-qa-mpnet-base-dot-v1"  # via sentence-transformers
EMBEDDING_DIM = 768

# Retrieval
TOP_K = 7  # Increased from 5 for better context
SIMILARITY_THRESHOLD = 0.30   # Lowered from 0.35 for broader retrieval

# Hybrid Retrieval (Level 2)
RERANK_THRESHOLD = -5.0  # Cross-encoder score threshold (lower = more permissive)

# Ollama / LLM
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_TEMPERATURE = 0.0
OLLAMA_MAX_TOKENS = 768  # Increased from 512 for more detailed answers

# Faithfulness
FAITHFULNESS_THRESHOLD = 0.50  # below this → override with no-answer (lowered for better coverage)

# Evaluation
QUESTIONS_PATH = "./questions.json"
RESULTS_PATH = "./data/eval_results.json"
REPORT_PATH = "./report.md"

# Grounding
NO_ANSWER_RESPONSE = "This information is not available in the provided document(s)."
