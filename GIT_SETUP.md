# Git Setup Guide for AIRMAN

This guide will help you prepare the AIRMAN project for Git and push it to a remote repository.

---

## 📋 Pre-Push Checklist

Before pushing to Git, ensure:

- [ ] All sensitive data is removed
- [ ] Large files are excluded (.gitignore)
- [ ] Documentation is complete
- [ ] Code is tested and working
- [ ] Environment template is created
- [ ] License is added

---

## 🚀 Quick Setup (5 Minutes)

### 1. Initialize Git Repository

```bash
# Navigate to project directory
cd /mnt/c/Users/vipra/kact/AIRMAN-RAG/Document-Drive--RAG-Chat/aviation_rag

# Initialize Git
git init

# Check status
git status
```

### 2. Review What Will Be Committed

```bash
# See what files will be tracked
git status

# Files that WILL be committed:
# ✅ All .py files (code)
# ✅ All .md files (documentation)
# ✅ requirements.txt
# ✅ questions.json
# ✅ templates/
# ✅ .gitkeep files

# Files that WON'T be committed (in .gitignore):
# ❌ data/faiss_index/*.faiss, *.pkl (large binary files)
# ❌ data/*.json (generated files)
# ❌ documents/**/*.pdf (large PDF files)
# ❌ *.log (log files)
# ❌ __pycache__/ (Python cache)
# ❌ .env (secrets)
```

### 3. Stage All Files

```bash
# Add all files (respecting .gitignore)
git add .

# Verify what's staged
git status
```

### 4. Create Initial Commit

```bash
# Commit with descriptive message
git commit -m "Initial commit: AIRMAN Aviation RAG System v2.0.0

- Core RAG pipeline with LangChain integration
- Level 2: Hybrid Retrieval (BM25 + Vector + Reranker)
- FastAPI web application with chat interface
- Comprehensive documentation (90+ pages)
- Evaluation framework with 50 test questions
- Production-ready deployment configuration"
```

### 5. Create Remote Repository

**On GitHub:**
1. Go to https://github.com/new
2. Repository name: `airman-aviation-rag`
3. Description: `Production-grade RAG system for aviation documentation with hybrid retrieval`
4. Choose: Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 6. Connect to Remote

```bash
# Add remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/airman-aviation-rag.git

# Verify remote
git remote -v
```

### 7. Push to Remote

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

---

## 📦 What Gets Pushed

### ✅ Included in Git

```
aviation_rag/
├── *.py                    # All Python code
├── *.md                    # All documentation
├── requirements.txt        # Dependencies
├── questions.json          # Test questions
├── report.md              # Report template
├── templates/             # Web templates
├── .gitignore             # Git ignore rules
├── .env.example           # Environment template
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guide
├── CHANGELOG.md           # Version history
└── data/
    └── .gitkeep           # Directory placeholder
```

### ❌ Excluded from Git

```
aviation_rag/
├── data/
│   ├── faiss_index/
│   │   ├── index.faiss         # ~250 MB (too large)
│   │   ├── index.pkl           # ~50 MB (too large)
│   │   └── bm25_index.pkl      # ~50 MB (too large)
│   ├── metadata.json           # Generated file
│   ├── eval_results.json       # Generated file
│   └── hybrid_comparison.json  # Generated file
├── documents/
│   └── **/*.pdf                # PDF files (too large)
├── *.log                       # Log files
├── __pycache__/                # Python cache
└── .env                        # Secrets
```

---

## 🔒 Security Checklist

### Before Pushing

1. **Check for Secrets**
   ```bash
   # Search for potential secrets
   grep -r "password" .
   grep -r "api_key" .
   grep -r "secret" .
   grep -r "token" .
   ```

2. **Verify .env is Ignored**
   ```bash
   # This should show nothing
   git status | grep .env
   
   # This should show .env.example
   git status | grep .env.example
   ```

3. **Check File Sizes**
   ```bash
   # Find large files (>10MB)
   find . -type f -size +10M
   
   # These should all be in .gitignore
   ```

4. **Review Staged Files**
   ```bash
   # List all files to be committed
   git diff --cached --name-only
   ```

---

## 📝 Repository Setup

### GitHub Repository Settings

After pushing, configure your repository:

#### 1. About Section
- Description: `Production-grade RAG system for aviation documentation with hybrid retrieval`
- Website: Your deployment URL (if any)
- Topics: `rag`, `llm`, `aviation`, `langchain`, `faiss`, `ollama`, `fastapi`, `python`

#### 2. Branch Protection
```
Settings → Branches → Add rule
- Branch name pattern: main
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
```

#### 3. Issues
```
Settings → Features
- ✅ Enable Issues
- Add issue templates (optional)
```

#### 4. Wiki (Optional)
```
Settings → Features
- ✅ Enable Wiki
- Add detailed documentation
```

---

## 🌿 Branch Strategy

### Recommended Branches

```
main                    # Production-ready code
├── develop            # Development branch
├── feature/*          # New features
├── fix/*             # Bug fixes
└── docs/*            # Documentation updates
```

### Creating Branches

```bash
# Create and switch to develop branch
git checkout -b develop
git push -u origin develop

# Create feature branch
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```

---

## 📊 Repository Structure on GitHub

After pushing, your repository will look like:

```
airman-aviation-rag/
├── 📄 README.md (or MASTER_README.md)
├── 📄 LICENSE
├── 📄 CONTRIBUTING.md
├── 📄 CHANGELOG.md
├── 📁 Core Application
│   ├── app.py
│   ├── rag.py
│   ├── rag_hybrid.py
│   └── config.py
├── 📁 Documentation (20+ files)
│   ├── QUICK_START.md
│   ├── SETUP_AND_RUN.md
│   ├── PROJECT_STRUCTURE.md
│   └── LEVEL2_*.md
├── 📁 Scripts
│   ├── ingest*.py
│   └── evaluate*.py
└── 📁 Data (empty, with .gitkeep)
```

---

## 🔄 Keeping Repository Updated

### Daily Workflow

```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/my-feature

# Make changes
# ...

# Stage and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature

# Create Pull Request on GitHub
```

### Syncing Fork (If Contributing)

```bash
# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/airman-rag.git

# Fetch upstream changes
git fetch upstream

# Merge upstream changes
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

---

## 📦 Large Files (Git LFS)

If you need to track large files (PDFs, models):

### Setup Git LFS

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pdf"
git lfs track "*.faiss"
git lfs track "*.pkl"

# Add .gitattributes
git add .gitattributes

# Commit and push
git commit -m "chore: add Git LFS tracking"
git push
```

### Note
- Git LFS has storage limits on free plans
- Consider alternative storage for large files:
  - Cloud storage (S3, Google Drive)
  - Separate data repository
  - Download scripts

---

## 🚨 Common Issues

### Issue 1: Large Files Rejected

```bash
# Error: file is too large
# Solution: Add to .gitignore

echo "large_file.pdf" >> .gitignore
git rm --cached large_file.pdf
git commit -m "chore: remove large file"
```

### Issue 2: Sensitive Data Committed

```bash
# Remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (DANGEROUS - only if repository is private)
git push origin --force --all
```

### Issue 3: Wrong Remote URL

```bash
# Check current remote
git remote -v

# Change remote URL
git remote set-url origin https://github.com/NEW_URL/repo.git

# Verify
git remote -v
```

---

## ✅ Post-Push Checklist

After pushing to GitHub:

- [ ] Repository is accessible
- [ ] README displays correctly
- [ ] All documentation is visible
- [ ] No sensitive data exposed
- [ ] .gitignore is working
- [ ] Branch protection is set up
- [ ] Issues are enabled
- [ ] Topics/tags are added
- [ ] Description is set
- [ ] License is visible

---

## 📚 Additional Resources

### Git Documentation
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Guides](https://guides.github.com/)
- [Git LFS](https://git-lfs.github.com/)

### Best Practices
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

## 🆘 Need Help?

- Check [CONTRIBUTING.md](CONTRIBUTING.md)
- Review [GitHub Docs](https://docs.github.com/)
- Ask in project discussions

---

**Ready to push?** Follow the Quick Setup section above! 🚀
