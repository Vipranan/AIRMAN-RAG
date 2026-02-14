# Complete Evaluation Guide

This guide walks you through generating ground truth answers, running the evaluation, and generating a complete report with qualitative analysis.

## Prerequisites

1. **Documents ingested**: Run `python ingest.py` first
2. **API running**: Start the API with `python app.py`
3. **Ollama running**: Make sure Ollama is serving the model

## Quick Start (Automated)

Run the complete pipeline with one command:

```bash
cd aviation_rag
python run_complete_evaluation.py
```

This will:
1. Generate ground truth answers for all 50 questions (~2-3 minutes)
2. Run evaluation with all metrics (~2-3 minutes)
3. Generate a complete report with qualitative analysis

**Total time:** ~5-6 minutes

## Manual Steps (If you prefer step-by-step)

### Step 1: Generate Ground Truth Answers

```bash
cd aviation_rag
python generate_ground_truth.py
```

This queries the RAG system for all 50 questions and saves the answers as ground truth in `questions.json`.

**Output:** Updated `questions.json` with `ground_truth` field filled

### Step 2: Run Evaluation

```bash
python evaluate_with_analysis.py
```

This re-runs all questions, computes metrics, and generates a detailed report.

**Outputs:**
- `data/eval_results.json` - Detailed metrics for each question
- `evaluation_report.md` - Complete report with qualitative analysis

## What Gets Generated

### 1. Updated questions.json
```json
{
  "id": 1,
  "question": "What does VFR stand for?",
  "ground_truth": "VFR stands for Visual Flight Rules...",  // ← Added
  "expected_keywords": ["Visual Flight Rules", "visibility"]
}
```

### 2. eval_results.json
Contains detailed metrics for each question:
- Retrieval hit rate
- Faithfulness score
- Answer match score
- Hallucination detection
- Latency
- Retrieved chunks

### 3. evaluation_report.md
Complete report with:
- Summary metrics table
- Key findings
- **5 best answers** with explanations
- **5 worst answers** with explanations
- Recommendations for improvement

## Evaluation Metrics Explained

| Metric | Description | Good Value |
|--------|-------------|------------|
| **Retrieval Hit Rate** | % of questions where expected keywords found in retrieved chunks | > 80% |
| **Faithfulness Score** | How well the answer is grounded in retrieved context | > 0.70 |
| **Hallucination Rate** | % of answers with unsupported claims | < 10% |
| **No-Answer Rate** | % of questions where system returned "not available" | 10-20% |
| **Answer Match Score** | Token overlap with ground truth | > 60% |
| **Latency** | Response time per question | < 3000ms |

## Interpreting Results

### Good Performance Indicators
- ✓ High retrieval hit rate (>80%)
- ✓ High faithfulness (>0.70)
- ✓ Low hallucination (<10%)
- ✓ Reasonable no-answer rate (10-20%)

### Warning Signs
- ⚠ Low retrieval hit rate → Improve chunking or embeddings
- ⚠ Low faithfulness → Strengthen system prompt
- ⚠ High hallucination → Increase faithfulness threshold
- ⚠ High no-answer rate → Lower similarity threshold

## Troubleshooting

### "API is not running"
```bash
# Start the API in another terminal
cd aviation_rag
python app.py
```

### "Ollama connection failed"
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, verify model is available
ollama list
```

### "No questions found"
Make sure `questions.json` exists in the `aviation_rag/` directory.

### "Ground truth generation is slow"
This is normal. Each question takes 2-5 seconds to process. Total time for 50 questions: 2-3 minutes.

## Next Steps After Evaluation

1. **Review the report**: Check `evaluation_report.md`
2. **Analyze failures**: Look at the "5 worst answers" section
3. **Implement improvements**: Follow recommendations in the report
4. **Re-run evaluation**: Test if improvements helped
5. **Iterate**: Keep improving until metrics are satisfactory

## Example Output

```
[Step 1/3] Generating ground truth answers...
[1/50] Generating answer for Q1: What does VFR stand for?
  ✓ Generated (245 chars, faithfulness: 0.92)
[2/50] Generating answer for Q2: What is the minimum safe altitude?
  ✓ Generated (198 chars, faithfulness: 0.88)
...
✓ Generated ground truth for 50/50 questions

[Step 2/3] Running evaluation with metrics...
Evaluating Q1: What does VFR stand for?
Evaluating Q2: What is the minimum safe altitude?
...
✓ Evaluation complete

✓ COMPLETE EVALUATION PIPELINE FINISHED

Generated files:
  1. aviation_rag/questions.json (updated with ground truth)
  2. aviation_rag/data/eval_results.json (detailed metrics)
  3. aviation_rag/evaluation_report.md (qualitative analysis)
```

## Files Overview

| File | Purpose |
|------|---------|
| `generate_ground_truth.py` | Queries RAG system to generate answers |
| `evaluate_with_analysis.py` | Runs evaluation and generates report |
| `run_complete_evaluation.py` | Automated pipeline (runs both above) |
| `questions.json` | 50 test questions (updated with ground truth) |
| `data/eval_results.json` | Detailed evaluation results |
| `evaluation_report.md` | Final report with analysis |

## Tips

- **First run**: Use the automated script (`run_complete_evaluation.py`)
- **Subsequent runs**: Use `evaluate_with_analysis.py` directly (ground truth already exists)
- **Update questions**: Edit `questions.json` and re-run evaluation
- **Compare versions**: Save `evaluation_report.md` with different names to compare improvements
