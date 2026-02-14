# Quick Evaluation Commands

## One-Command Complete Evaluation

```bash
# Make sure API is running first
python app.py

# In another terminal, run complete evaluation
cd aviation_rag
python run_complete_evaluation.py
```

This generates:
1. Ground truth answers (in `questions.json`)
2. Evaluation metrics (in `data/eval_results.json`)
3. Complete report with best/worst analysis (in `evaluation_report.md`)

**Time:** ~5-6 minutes for 50 questions

---

## Step-by-Step Commands

### 1. Start the API
```bash
cd aviation_rag
python app.py
```

### 2. Generate Ground Truth (in another terminal)
```bash
cd aviation_rag
python generate_ground_truth.py
```

### 3. Run Evaluation
```bash
python evaluate_with_analysis.py
```

---

## Check Results

```bash
# View the complete report
cat evaluation_report.md

# Or open in your editor
code evaluation_report.md

# Check raw metrics
cat data/eval_results.json
```

---

## Re-run After Changes

If you modify the system (chunking, prompts, etc.), re-evaluate:

```bash
# No need to regenerate ground truth, just re-evaluate
python evaluate_with_analysis.py
```

---

## Troubleshooting

**API not running?**
```bash
python app.py
```

**Ollama not running?**
```bash
ollama serve
```

**Want to see what's happening?**
```bash
# Check API logs
tail -f app.log

# Check Ollama logs
ollama logs
```
