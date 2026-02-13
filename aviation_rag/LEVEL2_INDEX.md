# Level 2 Enhancement - Documentation Index

## Overview

This directory contains the complete Level 2 enhancement for the Aviation Document RAG system: **Hybrid Retrieval combining BM25 keyword search, vector semantic search, and cross-encoder reranking**.

---

## Quick Navigation

### 🚀 Getting Started
- **[Quick Start Guide](LEVEL2_QUICK_START.md)** - Installation and basic usage (5 min read)
- **[Summary](LEVEL2_SUMMARY.md)** - Executive summary and key results (3 min read)

### 📚 Detailed Documentation
- **[Full Technical Documentation](LEVEL2_HYBRID_RETRIEVAL.md)** - Complete implementation details (30 min read)
- **[Architecture Diagrams](LEVEL2_ARCHITECTURE.md)** - Visual system architecture (15 min read)
- **[Option Comparison](LEVEL2_OPTION_COMPARISON.md)** - Why hybrid retrieval was chosen (20 min read)

### 💻 Code
- **[rag_hybrid.py](rag_hybrid.py)** - Hybrid retrieval pipeline implementation
- **[evaluate_hybrid.py](evaluate_hybrid.py)** - Comparison evaluation script
- **[config.py](config.py)** - Configuration parameters (updated)

---

## Document Guide

### For Quick Implementation

**Start here if you want to get hybrid retrieval running quickly:**

1. Read: [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md)
2. Install: `pip install rank-bm25`
3. Run: `python evaluate_hybrid.py`
4. Use: `from rag_hybrid import HybridRAGPipeline`

**Time required:** 30 minutes

### For Understanding the Decision

**Start here if you want to understand why hybrid retrieval was chosen:**

1. Read: [LEVEL2_SUMMARY.md](LEVEL2_SUMMARY.md) - High-level overview
2. Read: [LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md) - Detailed comparison
3. Review: Metrics and expected improvements

**Time required:** 30 minutes

### For Technical Deep Dive

**Start here if you want complete technical understanding:**

1. Read: [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md) - Full documentation
2. Read: [LEVEL2_ARCHITECTURE.md](LEVEL2_ARCHITECTURE.md) - System architecture
3. Study: [rag_hybrid.py](rag_hybrid.py) - Implementation code
4. Review: [evaluate_hybrid.py](evaluate_hybrid.py) - Evaluation methodology

**Time required:** 2-3 hours

### For Production Deployment

**Start here if you're deploying to production:**

1. Read: [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md) - Setup
2. Read: [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md) - Section: "Integration with Level 1"
3. Run: `python evaluate_hybrid.py` - Verify improvements
4. Review: [LEVEL2_SUMMARY.md](LEVEL2_SUMMARY.md) - Section: "Production Deployment"
5. Implement: A/B testing strategy

**Time required:** 1 day

---

## Document Descriptions

### LEVEL2_QUICK_START.md
**Purpose:** Get hybrid retrieval running in 30 minutes  
**Audience:** Developers who want to try it quickly  
**Length:** 5 pages  
**Contents:**
- Installation steps
- Basic usage examples
- CLI testing
- Configuration options
- Troubleshooting

### LEVEL2_SUMMARY.md
**Purpose:** Executive summary of the enhancement  
**Audience:** Technical leads, decision makers  
**Length:** 8 pages  
**Contents:**
- What was implemented
- Why this option was chosen
- Key results and metrics
- Quick start guide
- Production deployment plan

### LEVEL2_HYBRID_RETRIEVAL.md
**Purpose:** Complete technical documentation  
**Audience:** Engineers implementing or maintaining the system  
**Length:** 30+ pages  
**Contents:**
- Why hybrid retrieval?
- Why not the other options?
- Technical architecture
- Implementation details
- Evaluation methodology
- Results and metrics
- Integration guide
- Future improvements

### LEVEL2_ARCHITECTURE.md
**Purpose:** Visual system architecture and data flow  
**Audience:** Engineers and architects  
**Length:** 15 pages  
**Contents:**
- System architecture diagram
- Component details (BM25, Vector, RRF, Reranker)
- Performance characteristics
- Data flow examples
- Baseline vs Hybrid comparison

### LEVEL2_OPTION_COMPARISON.md
**Purpose:** Detailed comparison of all three Level 2 options  
**Audience:** Decision makers, technical leads  
**Length:** 20 pages  
**Contents:**
- The three options explained
- Detailed comparison (complexity, relevance, impact, risk, cost)
- Why Option 1 wins
- Why NOT Option 2 (Query Router)
- Why NOT Option 3 (GraphRAG)
- Implementation roadmap

---

## Key Concepts

### What is Hybrid Retrieval?

Combining multiple retrieval methods to leverage their complementary strengths:

1. **BM25 (Keyword-Based)**
   - Exact term matching
   - Best for: Technical terms, acronyms, numbers

2. **Vector Search (Semantic)**
   - Meaning and context
   - Best for: Concepts, paraphrasing

3. **Reciprocal Rank Fusion (RRF)**
   - Combines rankings from both
   - Score-independent fusion

4. **Cross-Encoder Reranking**
   - Deep semantic scoring
   - Final relevance selection

### Why Hybrid for Aviation?

Aviation documents contain:
- **Technical terms**: V1, METAR, QNH, ATPL
- **Numerical precision**: 1000 feet, 29.92 inches
- **Regulatory references**: FAR 91.119, section codes
- **Procedural language**: Step-by-step instructions

Hybrid retrieval handles all of these better than vector-only search.

### Expected Improvements

| Metric | Baseline | Hybrid | Change |
|--------|----------|--------|--------|
| Retrieval Hit Rate | 70% | 82% | +17% |
| Faithfulness | 0.75 | 0.81 | +8% |
| Hallucinations | 12% | 9% | -25% |
| Latency | 800ms | 950ms | +150ms |

---

## Implementation Checklist

### Phase 1: Setup (30 minutes)
- [ ] Read [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md)
- [ ] Install dependencies: `pip install rank-bm25`
- [ ] Verify Level 1 is working: `ls data/faiss_index/`

### Phase 2: Evaluation (1 hour)
- [ ] Run comparison: `python evaluate_hybrid.py`
- [ ] Review results: `cat data/hybrid_comparison.json`
- [ ] Verify improvements in console output

### Phase 3: Integration (2 hours)
- [ ] Update `app.py` to use hybrid retrieval
- [ ] Test endpoints: `/ask` and `/ask/hybrid`
- [ ] Verify API responses

### Phase 4: Production (1 day)
- [ ] Deploy with A/B testing
- [ ] Monitor metrics
- [ ] Gradual rollout to 100%

---

## Troubleshooting Guide

### Common Issues

**Issue:** BM25 index not building  
**Solution:** Run `python -c "from rag_hybrid import HybridRAGPipeline; HybridRAGPipeline()"`  
**Reference:** [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md) - Troubleshooting section

**Issue:** Slow performance  
**Solution:** Reduce `RERANK_CANDIDATES` in `config.py`  
**Reference:** [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md) - Usage Guide section

**Issue:** Out of memory  
**Solution:** Process reranking in smaller batches  
**Reference:** [LEVEL2_ARCHITECTURE.md](LEVEL2_ARCHITECTURE.md) - Performance section

**Issue:** No improvement in metrics  
**Solution:** Check if questions contain technical terms/acronyms  
**Reference:** [LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md) - Relevance section

---

## FAQ

### Q: Do I need to rebuild the FAISS index?
**A:** No, hybrid retrieval uses the existing FAISS index. It only adds a BM25 index which is built automatically.

### Q: Can I use hybrid retrieval without the baseline?
**A:** Yes, `rag_hybrid.py` is a standalone implementation. But we recommend keeping baseline for comparison.

### Q: How much does hybrid retrieval cost?
**A:** No additional API costs (runs locally). Only ~250MB more memory and +150ms latency.

### Q: Will hybrid retrieval work for my documents?
**A:** Best for documents with technical terms, acronyms, or numerical precision. Less benefit for purely narrative content.

### Q: Can I tune the hybrid retrieval parameters?
**A:** Yes, see `config.py` for `TOP_K`, `RERANK_THRESHOLD`, and other parameters.

### Q: How do I know if hybrid is better than baseline?
**A:** Run `python evaluate_hybrid.py` to get side-by-side comparison on your questions.

---

## Related Documentation

### Level 1 (Baseline System)
- [README.md](README.md) - Main project documentation
- [QUICK_START.md](QUICK_START.md) - Level 1 quick start
- [EVALUATION_GUIDE.md](EVALUATION_GUIDE.md) - Evaluation methodology

### Other Guides
- [SETUP_AND_RUN.md](SETUP_AND_RUN.md) - Complete setup guide
- [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) - Code structure
- [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - Deployment guide

---

## Version History

### Version 1.0 (February 14, 2026)
- Initial implementation of hybrid retrieval
- BM25 + Vector + RRF + Cross-encoder reranking
- Complete documentation suite
- Evaluation framework

---

## Contact & Support

### Questions?
- **Technical Details**: See [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md)
- **Quick Start**: See [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md)
- **Decision Rationale**: See [LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md)

### Issues?
- Check [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md) - Troubleshooting section
- Review [LEVEL2_ARCHITECTURE.md](LEVEL2_ARCHITECTURE.md) - Performance section
- Consult [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md) - Usage Guide

---

## Next Steps

1. **New to Level 2?** → Start with [LEVEL2_QUICK_START.md](LEVEL2_QUICK_START.md)
2. **Want to understand the decision?** → Read [LEVEL2_OPTION_COMPARISON.md](LEVEL2_OPTION_COMPARISON.md)
3. **Ready to implement?** → Follow [LEVEL2_SUMMARY.md](LEVEL2_SUMMARY.md) - Production Deployment
4. **Need technical details?** → Study [LEVEL2_HYBRID_RETRIEVAL.md](LEVEL2_HYBRID_RETRIEVAL.md)

---

**Status**: ✓ Documentation Complete  
**Version**: 1.0  
**Date**: February 14, 2026  
**Enhancement**: Hybrid Retrieval (BM25 + Vector + Reranker)
