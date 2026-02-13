"""
evaluate.py - Evaluation script for Aviation Document AI Chat
Runs questions against the API and computes metrics
"""

import json
import time
import argparse
from typing import List, Dict
import requests
from loguru import logger
from tabulate import tabulate
import config


class Evaluator:
    """Evaluate RAG system against ground truth questions"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.logger = logger
    
    def load_questions(self, require_ground_truth: bool = False) -> List[Dict]:
        """Load questions from JSON file"""
        with open(config.QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if require_ground_truth:
            # Filter only questions with non-empty ground truth
            questions = [q for q in data["questions"] if q.get("ground_truth", "").strip()]
            self.logger.info(f"Loaded {len(questions)} questions with ground truth")
        else:
            # Load all questions
            questions = data["questions"]
            self.logger.info(f"Loaded {len(questions)} questions (no ground truth required)")
        
        return questions
    
    def ask_question(self, question: str, debug: bool = True) -> Dict:
        """Call the /ask API endpoint"""
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/ask",
                json={"question": question, "debug": debug},
                timeout=120
            )
            latency_ms = int((time.time() - start_time) * 1000)
            
            response.raise_for_status()
            result = response.json()
            result["latency_ms"] = latency_ms
            return result
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API error: {e}")
            raise
    
    def compute_retrieval_hit(self, retrieved_chunks: List[Dict], expected_keywords: List[str]) -> bool:
        """Check if any retrieved chunk contains expected keywords"""
        if not retrieved_chunks:
            return False
        
        # Concatenate all chunk texts
        all_text = " ".join([chunk["text"].lower() for chunk in retrieved_chunks])
        
        # Check if any keyword appears
        for keyword in expected_keywords:
            if keyword.lower() in all_text:
                return True
        
        return False
    
    def compute_answer_match_score(self, answer: str, ground_truth: str) -> float:
        """Compute token overlap between answer and ground truth"""
        if answer == config.NO_ANSWER_RESPONSE:
            return 0.0
        
        # Tokenize (simple word split)
        answer_tokens = set(answer.lower().split())
        gt_tokens = set(ground_truth.lower().split())
        
        if not gt_tokens:
            return 0.0
        
        # Compute overlap
        overlap = len(answer_tokens & gt_tokens)
        score = overlap / len(gt_tokens)
        
        return score
    
    def evaluate_question(self, question_data: Dict, has_ground_truth: bool = False) -> Dict:
        """Evaluate a single question"""
        question = question_data["question"]
        ground_truth = question_data.get("ground_truth", "")
        expected_keywords = question_data.get("expected_keywords", [])
        
        self.logger.info(f"Evaluating Q{question_data['id']}: {question[:60]}...")
        
        # Call API
        result = self.ask_question(question, debug=True)
        
        # Compute metrics
        retrieval_hit = self.compute_retrieval_hit(
            result.get("retrieved_chunks", []),
            expected_keywords
        ) if expected_keywords else None
        
        answer_match_score = self.compute_answer_match_score(
            result["answer"],
            ground_truth
        ) if has_ground_truth and ground_truth else None
        
        no_answer_returned = (result["answer"] == config.NO_ANSWER_RESPONSE)
        
        hallucinated = (
            result["faithfulness_score"] < config.FAITHFULNESS_THRESHOLD
            and not no_answer_returned
        )
        
        # Build result
        eval_result = {
            "id": question_data["id"],
            "category": question_data["category"],
            "question": question,
            "ground_truth": ground_truth if has_ground_truth else None,
            "answer": result["answer"],
            "citations": result["citations"],
            "faithfulness_score": result["faithfulness_score"],
            "retrieval_hit": retrieval_hit,
            "answer_match_score": answer_match_score,
            "hallucinated": hallucinated,
            "no_answer_returned": no_answer_returned,
            "latency_ms": result["latency_ms"]
        }
        
        return eval_result
    
    def run_evaluation(self, require_ground_truth: bool = False) -> List[Dict]:
        """Run evaluation on all questions"""
        questions = self.load_questions(require_ground_truth=require_ground_truth)
        
        if not questions:
            self.logger.warning("No questions found in questions.json")
            return []
        
        has_ground_truth = any(q.get("ground_truth", "").strip() for q in questions)
        
        if not has_ground_truth and not require_ground_truth:
            self.logger.info("Running system test without ground truth (will measure faithfulness, latency, citations)")
        
        results = []
        
        for q in questions:
            try:
                result = self.evaluate_question(q, has_ground_truth=has_ground_truth)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to evaluate Q{q['id']}: {e}")
                continue
        
        return results
    
    def save_results(self, results: List[Dict]):
        """Save results to JSON file"""
        output = {"results": results}
        
        with open(config.RESULTS_PATH, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self.logger.success(f"Results saved to {config.RESULTS_PATH}")
    
    def print_summary(self, results: List[Dict]):
        """Print summary table to stdout"""
        if not results:
            print("No results to summarize.")
            return
        
        # Check if we have ground truth
        has_ground_truth = any(r.get("answer_match_score") is not None for r in results)
        
        # Group by category
        categories = {}
        for r in results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)
        
        # Compute metrics per category
        table_data = []
        
        for cat_name in ["factual", "applied", "reasoning"]:
            cat_results = categories.get(cat_name, [])
            
            if not cat_results:
                continue
            
            n = len(cat_results)
            
            retrieval_hit_rate = sum(r["retrieval_hit"] for r in cat_results if r["retrieval_hit"] is not None) / n if any(r["retrieval_hit"] is not None for r in cat_results) else None
            avg_faithfulness = sum(r["faithfulness_score"] for r in cat_results) / n
            hallucination_rate = sum(r["hallucinated"] for r in cat_results) / n
            no_answer_rate = sum(r["no_answer_returned"] for r in cat_results) / n
            avg_answer_match = sum(r["answer_match_score"] for r in cat_results if r["answer_match_score"] is not None) / n if has_ground_truth else None
            avg_latency = sum(r["latency_ms"] for r in cat_results) / n
            
            row = [
                f"{cat_name.capitalize()} (n={n})",
                f"{retrieval_hit_rate:.2f}" if retrieval_hit_rate is not None else "N/A",
                f"{avg_faithfulness:.2f}",
                f"{hallucination_rate:.2f}",
                f"{no_answer_rate:.2f}",
            ]
            
            if has_ground_truth:
                row.append(f"{avg_answer_match:.2f}" if avg_answer_match is not None else "N/A")
            
            row.append(f"{int(avg_latency)}")
            table_data.append(row)
        
        # Overall
        n_total = len(results)
        retrieval_hits = [r for r in results if r["retrieval_hit"] is not None]
        answer_matches = [r for r in results if r["answer_match_score"] is not None]
        
        overall_row = [
            f"Overall (n={n_total})",
            f"{sum(r['retrieval_hit'] for r in retrieval_hits) / len(retrieval_hits):.2f}" if retrieval_hits else "N/A",
            f"{sum(r['faithfulness_score'] for r in results) / n_total:.2f}",
            f"{sum(r['hallucinated'] for r in results) / n_total:.2f}",
            f"{sum(r['no_answer_returned'] for r in results) / n_total:.2f}",
        ]
        
        if has_ground_truth:
            overall_row.append(f"{sum(r['answer_match_score'] for r in answer_matches) / len(answer_matches):.2f}" if answer_matches else "N/A")
        
        overall_row.append(f"{int(sum(r['latency_ms'] for r in results) / n_total)}")
        table_data.append(overall_row)
        
        headers = [
            "Category",
            "Retrieval Hit Rate",
            "Avg Faithfulness",
            "Hallucination Rate",
            "No-Answer Rate",
        ]
        
        if has_ground_truth:
            headers.append("Avg Answer Match")
        
        headers.append("Avg Latency (ms)")
        
        print("\n" + "="*100)
        print("EVALUATION SUMMARY")
        if not has_ground_truth:
            print("(System Test Mode - No Ground Truth Available)")
        print("="*100)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("="*100 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Evaluate Aviation Document AI Chat")
    parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    parser.add_argument("--require-ground-truth", action="store_true", help="Only evaluate questions with ground truth")
    args = parser.parse_args()
    
    api_url = f"http://localhost:{args.port}"
    
    # Check if API is reachable
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        response.raise_for_status()
        logger.info(f"API is reachable at {api_url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot reach API at {api_url}. Make sure the app is running.")
        logger.error(f"Start with: uvicorn app:app --port {args.port}")
        return
    
    # Run evaluation
    evaluator = Evaluator(api_url)
    results = evaluator.run_evaluation(require_ground_truth=args.require_ground_truth)
    
    if results:
        evaluator.save_results(results)
        evaluator.print_summary(results)
    else:
        logger.warning("No evaluation results generated.")


if __name__ == "__main__":
    main()
