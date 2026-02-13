# AIRMAN - Command Reference

Quick reference for all common commands in the AIRMAN Aviation RAG System.

---

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama
ollama serve

# Ingest documents
python ingest_fast.py

# Start API server
python app.py

# Open browser
# http://localhost:8000
```

---

## 📦 Installation

### Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Level 2 dependencies
pip install rank-bm25
```

### Ollama Setup

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Start server
ollama serve

# Check status
curl http://localhost:11434/api/tags
```

---

## 📄 Document Ingestion

### Standard Ingestion

```bash
# Ingest all documents
python ingest.py

# Ingest specific file
python ingest.py --file documents/sample.pdf
```

### Fast Ingestion (GPU)

```bash
# Ingest with GPU acceleration
python ingest_fast.py

# Ingest specific file
python ingest_fast.py --file documents/sample.pdf
```

### OCR Ingestion

```bash
# Ingest with OCR for scanned PDFs
python ingest_with_ocr.py

# Ingest specific file
python ingest_with_ocr.py --file documents/scanned.pdf
```

---

## 🎮 Running the System

### API Server

```bash
# Start server (default port 8000)
python app.py

# Start with custom port
uvicorn app:app --port 8080

# Start with reload (development)
uvicorn app:app --reload

# Start with multiple workers (production)
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Direct RAG Usage

```bash
# Baseline RAG
python rag.py "What are the main types of clouds?"

# Hybrid RAG (Level 2)
python rag_hybrid.py "What are the main types of clouds?"
```

---

## 🧪 Testing & Evaluation

### Evaluation

```bash
# Run baseline evaluation
python evaluate.py

# Run with custom port
python evaluate.py --port 8080

# Run hybrid comparison
python evaluate_hybrid.py
```

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_rag.py

# Run with verbose output
pytest -v tests/
```

---

## 🔍 Health Checks

### System Health

```bash
# Check API health
curl http://localhost:8000/health

# Check Ollama
curl http://localhost:11434/api/tags

# Check FAISS index
ls -lh data/faiss_index/

# Check metadata
wc -l data/metadata.json
```

### Logs

```bash
# View ingestion logs
tail -f ingestion_fast.log

# View last 50 lines
tail -n 50 ingestion_fast.log

# Search logs
grep "ERROR" ingestion_fast.log
```

---

## 🌐 API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

### Ask Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the main types of clouds?",
    "top_k": 7,
    "debug": false
  }'
```

### Ingest Documents

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_paths": ["./documents/sample.pdf"]
  }'
```

---

## 🔧 Configuration

### View Configuration

```bash
# View all settings
cat config.py

# View specific setting
grep "TOP_K" config.py
```

### Update Configuration

```bash
# Edit configuration
nano config.py
# or
vim config.py
```

---

## 📊 Data Management

### Check Data

```bash
# List FAISS index files
ls -lh data/faiss_index/

# Check metadata size
du -h data/metadata.json

# Count chunks
jq '. | length' data/metadata.json

# View evaluation results
cat data/eval_results.json | jq .

# View hybrid comparison
cat data/hybrid_comparison.json | jq .
```

### Backup Data

```bash
# Backup all data
tar -czf backup_$(date +%Y%m%d).tar.gz data/

# Backup specific files
tar -czf faiss_backup.tar.gz data/faiss_index/

# Restore backup
tar -xzf backup_20260214.tar.gz
```

### Clean Data

```bash
# Remove generated files
rm data/eval_results.json
rm data/hybrid_comparison.json

# Remove indices (will need to re-ingest)
rm -rf data/faiss_index/*

# Remove logs
rm *.log
```

---

## 🐙 Git Commands

### Initial Setup

```bash
# Initialize repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: AIRMAN v2.0.0"

# Add remote
git remote add origin https://github.com/USERNAME/repo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Daily Workflow

```bash
# Check status
git status

# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Stage changes
git add .

# Commit changes
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature
```

### Branch Management

```bash
# List branches
git branch -a

# Switch branch
git checkout main

# Create and switch
git checkout -b develop

# Delete branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

---

## 🐳 Docker Commands

### Build and Run

```bash
# Build image
docker build -t airman-rag .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/documents:/app/documents \
  --name airman \
  airman-rag

# View logs
docker logs -f airman

# Stop container
docker stop airman

# Remove container
docker rm airman
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

## 🔍 Debugging

### Check Processes

```bash
# Check if Ollama is running
ps aux | grep ollama

# Check if API is running
ps aux | grep python

# Check port usage
lsof -i :8000
lsof -i :11434
```

### Kill Processes

```bash
# Kill by port
kill $(lsof -t -i:8000)

# Kill by name
pkill -f "python app.py"
pkill ollama
```

### GPU Check

```bash
# Check GPU availability
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Monitor GPU usage
watch -n 1 nvidia-smi
```

---

## 📦 Package Management

### Update Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade langchain

# Check outdated packages
pip list --outdated

# Freeze current versions
pip freeze > requirements.txt
```

### Virtual Environment

```bash
# Create new environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Deactivate
deactivate

# Remove environment
rm -rf venv
```

---

## 🧹 Cleanup

### Clean Python Cache

```bash
# Remove __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +

# Remove .pyc files
find . -type f -name "*.pyc" -delete

# Remove .pyo files
find . -type f -name "*.pyo" -delete
```

### Clean Logs

```bash
# Remove all logs
rm *.log

# Archive old logs
mkdir -p logs/archive
mv *.log logs/archive/
```

### Clean Data

```bash
# Remove generated files only
rm data/eval_results.json
rm data/hybrid_comparison.json

# Keep indices and metadata
```

---

## 📈 Monitoring

### System Resources

```bash
# CPU usage
top

# Memory usage
free -h

# Disk usage
df -h

# Disk usage by directory
du -sh *
```

### Application Metrics

```bash
# Request count
grep "POST /ask" logs/app.log | wc -l

# Average response time
grep "latency" logs/app.log | awk '{sum+=$NF; count++} END {print sum/count}'

# Error count
grep "ERROR" logs/app.log | wc -l
```

---

## 🔐 Security

### Check for Secrets

```bash
# Search for potential secrets
grep -r "password" . --exclude-dir=.git
grep -r "api_key" . --exclude-dir=.git
grep -r "secret" . --exclude-dir=.git

# Check .env is ignored
git status | grep .env
```

### File Permissions

```bash
# Secure .env file
chmod 600 .env

# Secure private keys
chmod 600 *.key

# Make scripts executable
chmod +x *.sh
```

---

## 📚 Documentation

### Generate Documentation

```bash
# Generate API docs (if using Sphinx)
cd docs/
make html
open _build/html/index.html
```

### View Documentation

```bash
# View README
cat README.md

# View specific guide
cat QUICK_START.md

# Search documentation
grep -r "hybrid retrieval" *.md
```

---

## 🆘 Troubleshooting

### Common Issues

```bash
# Port already in use
lsof -i :8000
kill $(lsof -t -i:8000)

# Ollama not responding
curl http://localhost:11434/api/tags
ollama serve

# FAISS index not found
ls data/faiss_index/
python ingest_fast.py

# Module not found
pip install -r requirements.txt

# Permission denied
chmod +x script.sh
```

---

## 📞 Quick Reference

### Most Used Commands

```bash
# Start system
ollama serve &
python app.py

# Run evaluation
python evaluate_hybrid.py

# Check health
curl http://localhost:8000/health

# View logs
tail -f ingestion_fast.log

# Git push
git add . && git commit -m "update" && git push
```

---

**For more details, see:**
- [SETUP_AND_RUN.md](SETUP_AND_RUN.md) - Complete setup guide
- [GIT_SETUP.md](GIT_SETUP.md) - Git setup guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
