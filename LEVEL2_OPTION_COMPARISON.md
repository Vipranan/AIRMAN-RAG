# Level 2 Option Comparison: Why Hybrid Retrieval?

## Executive Summary

For the aviation document RAG system, **Option 1: Hybrid Retrieval (BM25 + Vector + Reranker)** was selected as the Level 2 enhancement. This document provides a detailed comparison of all three options and justifies the selection.

---

## The Three Options

### Option 1: Hybrid Retrieval (BM25 + Vector + Reranker)
**Goal:** Improve retrieval quality by combining keyword and semantic search

**Components:**
- BM25 keyword-based retrieval
- Vector semantic retrieval (existing)
- Reciprocal Rank Fusion (RRF) to combine results
- Cross-encoder reranking for final selection

**Metrics to Measure:**
- Retrieval hit rate improvement
- Faithfulness score improvement
- Hallucination rate reduction
- Latency impact

### Option 2: Query Router + Confidence Thresholding
**Goal:** Route queries to appropriate models and refuse low-confidence answers

**Components:**
- Query classifier (simple vs. complex)
- Multiple LLM endpoints (cheap vs. expensive)
- Confidence scoring mechanism
- Refusal/clarification logic

**Metrics to Measure:**
- Cost reduction
- Answer quality by query type
- Refusal accuracy
- User satisfaction

### Option 3: GraphRAG (Mini Prototype)
**Goal:** Add graph-based reasoning for regulatory cross-references

**Components:**
- Entity extraction from documents
- Relationship extraction
- Graph database (Neo4j or in-memory)
- Graph traversal + vector retrieval

**Metrics to Measure:**
- Multi-hop reasoning accuracy
- Graph coverage
- Query types benefiting from graph
- Reasoning path quality

---

## Detailed Comparison

### 1. Implementation Complexity

| Aspect | Option 1 (Hybrid) | Option 2 (Router) | Option 3 (GraphRAG) |
|--------|-------------------|-------------------|---------------------|
| **New Dependencies** | rank-bm25 (1 package) | None (logic only) | Neo4j, spaCy, graph libs (5+ packages) |
| **Code Changes** | New retrieval pipeline | Query classification + routing | Entity extraction + graph building |
| **Infrastructure** | None (uses existing) | None | Neo4j database or custom graph |
| **Lines of Code** | ~300 lines | ~200 lines | ~800+ lines |
| **Testing Complexity** | Medium | Low | High |
| **Maintenance Burden** | Low | Low | High |

**Winner: Option 2** (simplest), but Option 1 is close second

### 2. Relevance to Aviation Use Case

| Aspect | Option 1 (Hybrid) | Option 2 (Router) | Option 3 (GraphRAG) |
|--------|-------------------|-------------------|---------------------|
| **Technical Terms** | ✓✓✓ BM25 excels | ✗ Doesn't help | ✓ Could help |
| **Acronyms (VFR, METAR)** | ✓✓✓ Exact matching | ✗ Doesn't help | ✓ Could help |
| **Numerical Precision** | ✓✓✓ Keyword matching | ✗ Doesn't help | ✗ Not relevant |
| **Procedural Questions** | ✓✓ Better context | ✓ Better model selection | ✗ Not graph-like |
| **Regulatory Cross-refs** | ✓ Some improvement | ✗ Doesn't help | ✓✓✓ Designed for this |
| **Conceptual Questions** | ✓✓ Vector still works | ✓ Better model selection | ✓ Could help |

**Winner: Option 1** (helps most question types)

### 3. Measurable Impact

| Metric | Option 1 (Hybrid) | Option 2 (Router) | Option 3 (GraphRAG) |
|--------|-------------------|-------------------|---------------------|
| **Retrieval Quality** | ✓✓✓ Direct improvement | ✗ No change | ✓✓ Potential improvement |
| **Answer Quality** | ✓✓ Better context | ✓ Better model match | ✓ Better reasoning |
| **Hallucination Reduction** | ✓✓✓ Better grounding | ✗ No direct impact | ✓ Better context |
| **Clear Baseline** | ✓✓✓ Vector-only | ✓✓ Single model | ✓✓ Vector-only |
| **Quantifiable Metrics** | ✓✓✓ Hit rate, faithfulness | ✓ Cost, refusal rate | ✓ Graph coverage |
| **Easy to Demonstrate** | ✓✓✓ Side-by-side comparison | ✓✓ A/B testing | ✓ Case studies |

**Winner: Option 1** (clearest, most measurable improvement)

### 4. Risk Assessment

| Risk Factor | Option 1 (Hybrid) | Option 2 (Router) | Option 3 (GraphRAG) |
|-------------|-------------------|-------------------|---------------------|
| **Implementation Failure** | Low | Low | High |
| **No Improvement** | Low (proven technique) | Medium (subjective) | High (uncertain fit) |
| **Performance Degradation** | Low (+150ms) | None | High (graph queries) |
| **Maintenance Issues** | Low | Low | High (graph updates) |
| **Scope Creep** | Low (well-defined) | Medium (confidence tuning) | High (entity extraction) |

**Winner: Option 1** (lowest risk)

### 5. Production Readiness

| Aspect | Option 1 (Hybrid) | Option 2 (Router) | Option 3 (GraphRAG) |
|--------|-------------------|-------------------|---------------------|
| **Deployment Complexity** | Low | Low | High (Neo4j) |
| **Scalability** | Good | Good | Medium (graph size) |
| **Monitoring** | Easy (metrics) | Medium (confidence) | Hard (graph quality) |
| **Debugging** | Easy (compare retrievers) | Medium (routing logic) | Hard (graph traversal) |
| **Rollback** | Easy (switch back) | Easy (remove router) | Hard (remove graph) |

**Winner: Option 1** (most production-ready)

### 6. Cost-Benefit Analysis

| Factor | Option 1 (Hybrid) | Option 2 (Router) | Option 3 (GraphRAG) |
|--------|-------------------|-------------------|---------------------|
| **Development Time** | 2-3 days | 1-2 days | 5-7 days |
| **Expected Improvement** | 15-20% retrieval | 10-15% cost savings | 5-10% reasoning |
| **Maintenance Cost** | Low | Low | High |
| **User Impact** | High (better answers) | Low (cost invisible) | Medium (some queries) |
| **ROI** | High | Medium | Low |

**Winner: Option 1** (best ROI)

---

## Why Option 1 (Hybrid Retrieval) Wins

### Quantitative Reasons

1. **Proven Technique**: Hybrid retrieval is well-established in IR research
   - BM25 + Dense retrieval is industry standard
   - Cross-encoder reranking shows consistent 10-20% improvements
   - Used by major search engines (Bing, Google)

2. **Clear Metrics**: Easy to measure improvement
   - Retrieval hit rate: % of queries finding expected keywords
   - Faithfulness: Grounding quality
   - Hallucination rate: Safety metric
   - All measurable with existing evaluation framework

3. **Low Risk**: Builds on existing infrastructure
   - Uses same FAISS index
   - Same metadata
   - Same LLM pipeline
   - Just adds BM25 + reranker

4. **Fast Implementation**: 2-3 days vs. 5-7 for GraphRAG
   - BM25: 1 day (index building + retrieval)
   - RRF: 2 hours (simple algorithm)
   - Reranker: 1 day (integration + tuning)
   - Evaluation: 4 hours (comparison script)

### Qualitative Reasons

1. **Aviation-Specific Benefits**
   - Technical terms: "V1", "METAR", "QNH" need exact matching
   - Acronyms: BM25 treats them as single tokens
   - Numbers: "1000 feet" vs "2000 feet" - precision matters
   - Procedures: Keyword matching finds specific steps

2. **User Experience**
   - Better answers for factual questions (40% of queries)
   - More reliable for applied questions (40% of queries)
   - Still good for reasoning questions (20% of queries)
   - Reduced "information not available" responses

3. **Maintainability**
   - No new infrastructure (Neo4j, entity extractors)
   - No complex tuning (confidence thresholds, routing rules)
   - Easy to debug (inspect BM25 vs vector results)
   - Simple to explain to stakeholders

---

## Why NOT Option 2 (Query Router)

### Doesn't Address Core Problem

The bottleneck in our system is **retrieval quality**, not generation quality:
- If wrong documents are retrieved, even GPT-4 can't help
- Routing to a better model doesn't fix poor context
- Our Ollama model (llama3.1:8b) is already good enough

### Hard to Measure Improvement

- Confidence scoring is subjective and model-dependent
- No ground truth for "this query is complex"
- Difficult to validate routing decisions
- Refusal accuracy is hard to measure

### Limited Benefit for Aviation

- Aviation questions are consistently complex (safety-critical)
- No clear "simple vs. complex" distinction
- All questions deserve high-quality answers
- Cost savings not relevant (local Ollama)

### When Option 2 Would Be Better

- **Production systems with API costs**: Routing to cheaper models saves money
- **Clear query complexity distinction**: E.g., "What is X?" vs. "Explain the relationship between X, Y, and Z"
- **Generation bottleneck**: When retrieval is good but answers are poor
- **User feedback available**: To tune confidence thresholds

---

## Why NOT Option 3 (GraphRAG)

### High Implementation Complexity

1. **Entity Extraction**: Challenging for aviation documents
   - Technical terms: "V1", "METAR", "QNH" - are these entities?
   - Procedures: "short field takeoff" - entity or concept?
   - Regulations: "FAR 91.119" - how to extract and link?
   - Requires domain-specific NER model

2. **Relationship Extraction**: Even harder
   - "V1 is used during takeoff" - what relationship?
   - "VFR requires visibility of 5km" - requirement relationship?
   - "METAR reports weather" - reporting relationship?
   - Requires custom relationship ontology

3. **Graph Maintenance**: Ongoing burden
   - Must re-extract when documents change
   - Graph schema must be updated
   - Relationships must be validated
   - Neo4j or custom graph storage

### Uncertain ROI

1. **Limited Applicable Questions**: Only ~10-15 of 50 questions benefit
   - Factual questions (40%): Don't need graph traversal
   - Applied questions (40%): Procedural, not relational
   - Reasoning questions (20%): Some might benefit

2. **Vector Search Already Handles Connections**
   - Semantic similarity captures conceptual relationships
   - Chunks contain cross-references naturally
   - LLM can synthesize across chunks

3. **Aviation Documents Not Graph-Heavy**
   - Textbooks are narrative/procedural
   - SOPs are sequential
   - Regulations have some cross-refs, but not extensive
   - Not like legal documents or knowledge bases

### When Option 3 Would Be Better

- **Highly interconnected documents**: Legal codes, regulations with extensive cross-references
- **Multi-hop reasoning required**: "How does regulation A affect procedure B which impacts system C?"
- **Explicit entity relationships**: Organizational charts, system diagrams
- **Domain-specific entity extraction available**: Pre-trained aviation NER models

---

## Conclusion

**Option 1: Hybrid Retrieval** is the clear winner because it:

1. ✓ **Directly addresses the core problem**: Retrieval quality
2. ✓ **Fits the aviation use case**: Technical terms, acronyms, numbers
3. ✓ **Has clear, measurable metrics**: Retrieval hit rate, faithfulness
4. ✓ **Low implementation risk**: Proven technique, simple integration
5. ✓ **Production-ready**: Minimal latency, easy to deploy
6. ✓ **High ROI**: 2-3 days work for 15-20% improvement

**Option 2** would be better for cost optimization in production systems with API costs.

**Option 3** would be better for highly interconnected regulatory documents requiring multi-hop reasoning.

For this aviation RAG system, **hybrid retrieval provides the best balance of impact, risk, and effort**.

---

## Implementation Roadmap

### Phase 1: Core Implementation (Day 1-2)
- [ ] Add BM25 indexing to ingestion pipeline
- [ ] Implement BM25 retrieval function
- [ ] Implement RRF fusion
- [ ] Add cross-encoder reranking
- [ ] Test on sample queries

### Phase 2: Evaluation (Day 2-3)
- [ ] Create comparison evaluation script
- [ ] Run baseline vs hybrid on 50 questions
- [ ] Analyze results by category
- [ ] Generate comparison report

### Phase 3: Documentation (Day 3)
- [ ] Write technical documentation
- [ ] Create quick start guide
- [ ] Update README
- [ ] Document configuration options

### Phase 4: Integration (Day 4)
- [ ] Integrate with FastAPI app
- [ ] Add hybrid endpoint
- [ ] Update health check
- [ ] Deploy and test

**Total Time: 3-4 days**

---

**Document Version:** 1.0  
**Last Updated:** February 14, 2026  
**Decision:** Option 1 - Hybrid Retrieval Selected
