# Contributing to AIRMAN

Thank you for your interest in contributing to AIRMAN Aviation RAG System! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)
9. [Release Process](#release-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Enforcement

Instances of unacceptable behavior may be reported to the project maintainers.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Git
- Ollama
- Basic understanding of RAG systems

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/airman-rag.git
cd airman-rag

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/airman-rag.git
```

---

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Install Pre-commit Hooks

```bash
pre-commit install
```

### 4. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

### 5. Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

---

## Making Changes

### 1. Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates
- `chore/` - Maintenance tasks

### 2. Make Your Changes

- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add hybrid retrieval support"
```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/updates
- `chore`: Maintenance tasks

**Examples:**
```
feat(rag): add BM25 retrieval support
fix(api): resolve CORS issue
docs(readme): update installation instructions
```

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these specifics:

#### Formatting

```python
# Line length: 100 characters max
# Indentation: 4 spaces (no tabs)
# Quotes: Double quotes for strings

def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    result = some_operation(param1, param2)
    return result
```

#### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional

def process_chunks(
    chunks: List[Dict],
    threshold: float = 0.5
) -> Optional[str]:
    """Process chunks and return result."""
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve relevant chunks for a query.
    
    Args:
        query: User question
        top_k: Number of results to return
    
    Returns:
        List of retrieved chunks with metadata
    
    Raises:
        ValueError: If query is empty
    """
    pass
```

#### Imports

Organize imports in this order:

```python
# Standard library
import os
import json
from typing import List, Dict

# Third-party
import numpy as np
from langchain_community.vectorstores import FAISS

# Local
from config import TOP_K
from rag import RAGPipeline
```

### Code Quality Tools

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

---

## Testing

### Writing Tests

```python
# tests/test_rag.py
import pytest
from rag import RAGPipeline

def test_retrieve():
    """Test retrieval functionality."""
    rag = RAGPipeline()
    results = rag.retrieve("test query", top_k=5)
    
    assert len(results) <= 5
    assert all("chunk_id" in r for r in results)

def test_faithfulness_check():
    """Test faithfulness checking."""
    rag = RAGPipeline()
    score = rag.check_faithfulness("answer", [{"text": "context"}])
    
    assert 0.0 <= score <= 1.0
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_rag.py

# Run specific test
pytest tests/test_rag.py::test_retrieve

# Run with coverage
pytest --cov=. --cov-report=html tests/

# Run with verbose output
pytest -v tests/
```

### Test Coverage

Aim for >80% code coverage:

```bash
# Generate coverage report
pytest --cov=. --cov-report=term-missing tests/

# View HTML report
open htmlcov/index.html
```

---

## Documentation

### Updating Documentation

When making changes, update relevant documentation:

1. **Code Comments**: Explain complex logic
2. **Docstrings**: Update function/class documentation
3. **README.md**: Update if adding features
4. **CHANGELOG.md**: Add entry for your changes
5. **API Docs**: Update if changing API

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep formatting consistent

### Building Documentation

```bash
# If using Sphinx
cd docs/
make html
open _build/html/index.html
```

---

## Pull Request Process

### 1. Prepare Your PR

```bash
# Update your branch
git fetch upstream
git rebase upstream/main

# Run tests
pytest tests/

# Run linting
flake8 .
black --check .
isort --check .

# Push to your fork
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### 3. Review Process

- Maintainers will review your PR
- Address feedback and comments
- Make requested changes
- Push updates to your branch

### 4. Merge

Once approved:
- PR will be merged by maintainers
- Your branch can be deleted
- Changes will be in next release

---

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- MAJOR.MINOR.PATCH (e.g., 2.0.0)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Creating a Release

1. Update version in `__version__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Build and publish

```bash
# Tag release
git tag -a v2.0.0 -m "Release version 2.0.0"
git push upstream v2.0.0

# Build package
python setup.py sdist bdist_wheel

# Publish to PyPI
twine upload dist/*
```

---

## Questions?

- Check [Documentation](INDEX.md)
- Open an [Issue](https://github.com/OWNER/airman-rag/issues)
- Join our [Discord](https://discord.gg/airman) (if available)

---

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- Release notes
- Project README

Thank you for contributing to AIRMAN! 🚁
