# Evaluation System Guide

## How `evaluate.py` Works

The evaluation script tests your AIRMAN RAG system by running questions through the API and measuring performance metrics.

### Overview

```
questions.json → evaluate.py → API (/ask endpoint) → Results + Metrics
```

### Step-by-Step Process

#### 1. Load Questions
```python
def load_questions(self, require_ground_truth: bool = False)
```
- Reads questions from `questions.json`
- By default: Loads ALL 50 questions
- With `--require-ground-truth` flag: Only loads questions with filled `ground_truth` field
- Currently: All 50 questions have empty `ground_truth`, so it runs in "system test mode"

#### 2. Ask Each Question
```python
def ask_question(self, question: str, debug: bool = True)
```
- Sends POST request to `http://localhost:8000/ask`
- Measures response time (latency)
- Gets back: answer, citations, faithfulness_score, retrieved_chunks

#### 3. Compute Metrics

For each question, it calculates:

**a) Retrieval Hit Rate**
```python
def compute_retrieval_hit(self, retrieved_chunks, expected_keywords)
```
- Checks if ANY of the `expected_keywords` appear in retrieved chunks
- Example: For "What are cloud types?", keywords = ["stratiform", "cumuliform", "cirriform"]
- Returns: True if found, False if not

**b) Answer Match Score** (only if ground_truth exists)
```python
def compute_answer_match_score(self, answer, ground_truth)
```
- Compares answer words with ground truth words
- Calculates overlap percentage
- Currently NOT used (no ground truth filled in)

**c) Faithfulness Score**
- Comes from the RAG pipeline
- Measures how well the answer matches the retrieved context
- Range: 0.0 to 1.0 (higher is better)

**d) Hallucination Detection**
```python
hallucinated = (faithfulness_score < FAITHFULNESS_THRESHOLD and not no_answer_returned)
```
- Flags answers with low faithfulness that aren't "not available"
- Threshold: 0.50 (configurable in config.py)

**e) No-Answer Rate**
- Counts how often system returns "This information is not available in the provided document(s)."
- High rate = conservative (good for preventing hallucinations)
- Low rate = answering more questions (but risk of hallucinations)

**f) Latency**
- Time taken to answer each question (in milliseconds)
- Includes: embedding query, retrieval, LLM generation

#### 4. Group by Category

Questions are organized into 3 categories:

```json
{
  "category": "factual",    // 20 questions - direct facts
  "category": "applied",    // 20 questions - practical scenarios  
  "category": "reasoning"   // 10 questions - explanations
}
```

#### 5. Generate Summary

Calculates averages per category and overall:
- Retrieval Hit Rate
- Average Faithfulness
- Hallucination Rate
- No-Answer Rate
- Average Latency

#### 6. Save Results

Saves detailed results to `data/eval_results.json`:
```json
{
  "results": [
    {
      "id": 1,
      "category": "factual",
      "question": "What does VFR stand for?",
      "answer": "This information is not available...",
      "citations": [...],
      "faithfulness_score": 1.0,
      "retrieval_hit": true,
      "hallucinated": false,
      "no_answer_returned": true,
      "latency_ms": 4523
    },
    ...
  ]
}
```

---

## Question Selection

### Source: `questions.json`

The evaluation uses ALL questions from `questions.json` by default. The file contains:

**Structure:**
```json
{
  "questions": [
    {
      "id": 1,
      "category": "factual",
      "question": "What does VFR stand for?",
      "ground_truth": "",
      "expected_keywords": ["Visual Flight Rules", "visibility"],
      "source_hint": "PPL Textbook — Air Law"
    }
  ]
}
```

**Fields:**
- `id`: Unique question number (1-50)
- `category`: Type of question (factual/applied/reasoning)
- `question`: The actual question text
- `ground_truth`: Expected answer (currently empty for all)
- `expected_keywords`: Words that should appear in retrieved chunks
- `source_hint`: Which document should contain the answer

### Question Categories

#### 1. Factual Questions (20 questions, IDs 1-20)
**Purpose:** Test basic knowledge retrieval

**Examples:**
- "What does VFR stand for?"
- "What is the standard atmospheric pressure at sea level?"
- "What are the main types of clouds?"

**Expected Behavior:**
- Should find direct answers in documents
- High retrieval hit rate
- Clear citations

#### 2. Applied Questions (20 questions, IDs 21-40)
**Purpose:** Test practical application of knowledge

**Examples:**
- "If outside air temperature is higher than standard, how does it affect density altitude?"
- "During pre-flight inspection, you notice a dent on the wing. What should you do?"
- "How do you calculate weight and balance for a flight?"

**Expected Behavior:**
- May require synthesizing information from multiple chunks
- Needs reasoning based on principles in documents
- More challenging than factual questions

#### 3. Reasoning Questions (10 questions, IDs 41-50)
**Purpose:** Test explanation and understanding

**Examples:**
- "Why is it dangerous to fly through a thunderstorm?"
- "Explain the relationship between angle of attack, lift, and stall"
- "Why does an aircraft require more runway on a hot day?"

**Expected Behavior:**
- Requires combining multiple concepts
- Needs clear explanations
- Most challenging category

---

## Running Evaluation

### Basic Usage
```bash
python evaluate.py
```
- Tests all 50 questions
- No ground truth required
- Measures: faithfulness, latency, retrieval, citations

### With Ground Truth (if you fill it in)
```bash
python evaluate.py --require-ground-truth
```
- Only tests questions with filled `ground_truth` field
- Calculates answer match scores
- More accurate evaluation

### Custom Port
```bash
python evaluate.py --port 8080
```
- If your API runs on different port

---

## Understanding Results

### Sample Output
```
====================================================================================================
EVALUATION SUMMARY
(System Test Mode - No Ground Truth Available)
====================================================================================================
+------------------+----------------------+--------------------+----------------------+------------------+--------------------+
| Category         |   Retrieval Hit Rate |   Avg Faithfulness |   Hallucination Rate |   No-Answer Rate |   Avg Latency (ms) |
+==================+======================+====================+======================+==================+====================+
| Factual (n=20)   |                 0.70 |               0.71 |                 0.00 |             0.90 |               4746 |
+------------------+----------------------+--------------------+----------------------+------------------+--------------------+
| Applied (n=20)   |                 0.55 |               0.76 |                 0.00 |             0.85 |               8043 |
+------------------+----------------------+--------------------+----------------------+------------------+--------------------+
| Reasoning (n=10) |                 0.60 |               0.81 |                 0.00 |             0.90 |               5509 |
+------------------+----------------------+--------------------+----------------------+------------------+--------------------+
| Overall (n=50)   |                 0.62 |               0.75 |                 0.00 |             0.88 |               6218 |
+------------------+----------------------+--------------------+----------------------+------------------+--------------------+
====================================================================================================
```

### Interpreting Metrics

**Retrieval Hit Rate: 0.62 (62%)**
- 62% of questions had expected keywords in retrieved chunks
- Good: System is finding relevant information
- Could improve: Increase TOP_K or lower similarity threshold

**Avg Faithfulness: 0.75 (75%)**
- Answers match retrieved context well
- Above threshold (0.50), so answers are grounded
- Higher is better (max 1.0)

**Hallucination Rate: 0.00 (0%)**
- No hallucinations detected! ✅
- System never made up information
- This is excellent

**No-Answer Rate: 0.88 (88%)**
- 88% of questions got "not available" response
- High rate = very conservative
- Could be improved by:
  - Lowering faithfulness threshold
  - Improving prompt
  - Adding more documents
  - Better chunk retrieval

**Avg Latency: 6218ms (~6 seconds)**
- Time per question
- Includes: embedding (GPU), retrieval, LLM generation
- Reasonable for complex questions

---

## Improving Performance

### If No-Answer Rate is Too High (>80%)

1. **Lower faithfulness threshold**
   ```python
   # config.py
   FAITHFULNESS_THRESHOLD = 0.40  # from 0.50
   ```

2. **Increase retrieved chunks**
   ```python
   # config.py
   TOP_K = 10  # from 7
   ```

3. **Lower similarity threshold**
   ```python
   # config.py
   SIMILARITY_THRESHOLD = 0.25  # from 0.30
   ```

4. **Improve prompt** (allow more synthesis)
   - Edit `rag.py` prompt template
   - Allow reasonable inferences

### If Hallucination Rate is High (>5%)

1. **Increase faithfulness threshold**
   ```python
   # config.py
   FAITHFULNESS_THRESHOLD = 0.65  # from 0.50
   ```

2. **Stricter prompt**
   - Emphasize staying grounded in context
   - Reduce inference allowance

3. **Better faithfulness checking**
   - Improve algorithm in `rag.py`
   - Add more sophisticated matching

### If Latency is Too High (>10s)

1. **Verify GPU usage**
   ```bash
   nvidia-smi  # Check if GPU is being used
   ```

2. **Reduce chunks**
   ```python
   # config.py
   TOP_K = 5  # from 7
   ```

3. **Reduce max tokens**
   ```python
   # config.py
   OLLAMA_MAX_TOKENS = 512  # from 768
   ```

---

## Adding Ground Truth

To enable answer match scoring, fill in the `ground_truth` field:

```json
{
  "id": 1,
  "category": "factual",
  "question": "What are the main types of clouds?",
  "ground_truth": "The three basic forms of cloud are stratiform, cumuliform, and cirriform.",
  "expected_keywords": ["stratiform", "cumuliform", "cirriform"],
  "source_hint": "Meteorology full book.pdf"
}
```

Then run:
```bash
python evaluate.py --require-ground-truth
```

This will add an "Avg Answer Match" column showing how well answers match expected answers.

---

## Files Generated

1. **`data/eval_results.json`**
   - Detailed results for each question
   - Includes: question, answer, citations, scores
   - Use for debugging specific questions

2. **Console output**
   - Summary table with metrics
   - Quick overview of performance

---

## Best Practices

1. **Run evaluation after changes**
   - Changed config? Run eval
   - Updated prompt? Run eval
   - Added documents? Run eval

2. **Track metrics over time**
   - Save eval results with timestamps
   - Compare before/after changes

3. **Focus on zero hallucinations**
   - Better to say "not available" than hallucinate
   - High no-answer rate is acceptable if accurate

4. **Balance coverage vs accuracy**
   - Lower thresholds = more answers (but risk hallucinations)
   - Higher thresholds = fewer answers (but more accurate)

---

**Last Updated:** February 12, 2026
**Evaluation Version:** 1.0.0
