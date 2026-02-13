"""
evaluate_hybrid.py - Compare baseline (vector-only) vs hybrid retrieval
Runs the same questions through both pipelines and compares metrics
"""

import json
import time
from typing import List, Dict
from loguru import logger
from tabulate import tabulate

from rag import RAGPipeline
from rag_hybrid import HybridRAGPipeline
import config


class HybridEvaluator:
    """Compare baseline and hybrid RAG pipelines"""
    
    def __init__(self):
        self.logger = logger
        self.logger.info("Initializing baseline (vector-only) pipeline...")
        self.baseline_rag = RAGPipeline()
        
        self.logger.info("Initializing hybrid (BM25 + Vector + Reranker) pipeline...")
        self.hybrid_rag = HybridRAGPipeline()
    
    def load_questions(self) -> List[Dict]:
        """Load questions from JSON file"""
        with open(config.QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data["questions"]
        self.logger.info(f"Loaded {len(questions)} questions")
        return questions
    
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
    
    def evaluate_single_question(
        self,
        question_data: Dict,
        pipeline_name: str,
        pipeline
    ) -> Dict:
        """Evaluate a single question on one pipeline"""
        question = question_data["question"]
        expected_keywords = question_data.get("expected_keywords", [])
        
        self.logger.debug(f"[{pipeline_name}] Q{question_data['id']}: {question[:60]}...")
        
        # Call pipeline
        start_time = time.time()
        result = pipeline.ask(question, debug=True)
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Compute metrics
        retrieval_hit = self.compute_retrieval_hit(
            result.get("retrieved_chunks", []),
            expected_keywords
        ) if expected_keywords else None
        
        no_answer_returned = (result["answer"] == config.NO_ANSWER_RESPONSE)
        
        hallucinated = (
            result["faithfulness_score"] < config.FAITHFULNESS_THRESHOLD
            and not no_answer_returned
        )
        
        num_chunks_retrieved = len(result.get("retrieved_chunks", []))
        
        # Build result
        eval_result = {
            "id": question_data["id"],
            "category": question_data["category"],
            "question": question,
            "answer": result["answer"],
            "citations": result["citations"],
            "faithfulness_score": result["faithfulness_score"],
            "retrieval_hit": retrieval_hit,
            "hallucinated": hallucinated,
            "no_answer_returned": no_answer_returned,
            "num_chunks_retrieved": num_chunks_retrieved,
            "latency_ms": latency_ms
        }
        
        return eval_result
    
    def run_comparison(self) -> Dict:
        """Run evaluation on both pipelines and compare"""
        questions = self.load_questions()
        
        if not questions:
            self.logger.warning("No questions found in questions.json")
            return {}
        
        baseline_results = []
        hybrid_results = []
        
        for q in questions:
            try:
                # Evaluate on baseline
                baseline_result = self.evaluate_single_question(q, "Baseline", self.baseline_rag)
                baseline_results.append(baseline_result)
                
                # Evaluate on hybrid
                hybrid_result = self.evaluate_single_question(q, "Hybrid", self.hybrid_rag)
                hybrid_results.append(hybrid_result)
                
            except Exception as e:
                self.logger.error(f"Failed to evaluate Q{q['id']}: {e}")
                continue
        
        return {
            "baseline": baseline_results,
            "hybrid": hybrid_results
        }
    
    def save_results(self, results: Dict):
        """Save comparison results to JSON file"""
        output_path = "./data/hybrid_comparison.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.logger.success(f"Comparison results saved to {output_path}")
    
    def print_comparison_summary(self, results: Dict):
        """Print side-by-side comparison table"""
        baseline_results = results["baseline"]
        hybrid_results = results["hybrid"]
        
        if not baseline_results or not hybrid_results:
            print("No results to compare.")
            return
        
        # Group by category
        categories = ["factual", "applied", "reasoning"]
        
        table_data = []
        
        for cat_name in categories:
            baseline_cat = [r for r in baseline_results if r["category"] == cat_name]
            hybrid_cat = [r for r in hybrid_results if r["category"] == cat_name]
            
            if not baseline_cat or not hybrid_cat:
                continue
            
            n = len(baseline_cat)
            
            # Baseline metrics
            b_retrieval_hit = sum(r["retrieval_hit"] for r in baseline_cat if r["retrieval_hit"] is not None) / n if any(r["retrieval_hit"] is not None for r in baseline_cat) else None
            b_faithfulness = sum(r["faithfulness_score"] for r in baseline_cat) / n
            b_hallucination = sum(r["hallucinated"] for r in baseline_cat) / n
            b_no_answer = sum(r["no_answer_returned"] for r in baseline_cat) / n
            b_latency = sum(r["latency_ms"] for r in baseline_cat) / n
            
            # Hybrid metrics
            h_retrieval_hit = sum(r["retrieval_hit"] for r in hybrid_cat if r["retrieval_hit"] is not None) / n if any(r["retrieval_hit"] is not None for r in hybrid_cat) else None
            h_faithfulness = sum(r["faithfulness_score"] for r in hybrid_cat) / n
            h_hallucination = sum(r["hallucinated"] for r in hybrid_cat) / n
            h_no_answer = sum(r["no_answer_returned"] for r in hybrid_cat) / n
            h_latency = sum(r["latency_ms"] for r in hybrid_cat) / n
            
            # Calculate improvements
            retrieval_improvement = ((h_retrieval_hit - b_retrieval_hit) / b_retrieval_hit * 100) if b_retrieval_hit and h_retrieval_hit else None
            faithfulness_improvement = ((h_faithfulness - b_faithfulness) / b_faithfulness * 100) if b_faithfulness else None
            
            row = [
                f"{cat_name.capitalize()} (n={n})",
                f"{b_retrieval_hit:.3f}" if b_retrieval_hit is not None else "N/A",
                f"{h_retrieval_hit:.3f}" if h_retrieval_hit is not None else "N/A",
                f"{retrieval_improvement:+.1f}%" if retrieval_improvement is not None else "N/A",
                f"{b_faithfulness:.3f}",
                f"{h_faithfulness:.3f}",
                f"{faithfulness_improvement:+.1f}%" if faithfulness_improvement is not None else "N/A",
                f"{b_hallucination:.3f}",
                f"{h_hallucination:.3f}",
                f"{b_no_answer:.3f}",
                f"{h_no_answer:.3f}",
                f"{int(b_latency)}",
                f"{int(h_latency)}"
            ]
            table_data.append(row)
        
        # Overall
        n_total = len(baseline_results)
        
        # Baseline overall
        b_retrieval_hits = [r for r in baseline_results if r["retrieval_hit"] is not None]
        b_overall_retrieval = sum(r["retrieval_hit"] for r in b_retrieval_hits) / len(b_retrieval_hits) if b_retrieval_hits else None
        b_overall_faithfulness = sum(r["faithfulness_score"] for r in baseline_results) / n_total
        b_overall_hallucination = sum(r["hallucinated"] for r in baseline_results) / n_total
        b_overall_no_answer = sum(r["no_answer_returned"] for r in baseline_results) / n_total
        b_overall_latency = sum(r["latency_ms"] for r in baseline_results) / n_total
        
        # Hybrid overall
        h_retrieval_hits = [r for r in hybrid_results if r["retrieval_hit"] is not None]
        h_overall_retrieval = sum(r["retrieval_hit"] for r in h_retrieval_hits) / len(h_retrieval_hits) if h_retrieval_hits else None
        h_overall_faithfulness = sum(r["faithfulness_score"] for r in hybrid_results) / n_total
        h_overall_hallucination = sum(r["hallucinated"] for r in hybrid_results) / n_total
        h_overall_no_answer = sum(r["no_answer_returned"] for r in hybrid_results) / n_total
        h_overall_latency = sum(r["latency_ms"] for r in hybrid_results) / n_total
        
        # Overall improvements
        overall_retrieval_improvement = ((h_overall_retrieval - b_overall_retrieval) / b_overall_retrieval * 100) if b_overall_retrieval and h_overall_retrieval else None
        overall_faithfulness_improvement = ((h_overall_faithfulness - b_overall_faithfulness) / b_overall_faithfulness * 100) if b_overall_faithfulness else None
        
        overall_row = [
            f"Overall (n={n_total})",
            f"{b_overall_retrieval:.3f}" if b_overall_retrieval is not None else "N/A",
            f"{h_overall_retrieval:.3f}" if h_overall_retrieval is not None else "N/A",
            f"{overall_retrieval_improvement:+.1f}%" if overall_retrieval_improvement is not None else "N/A",
            f"{b_overall_faithfulness:.3f}",
            f"{h_overall_faithfulness:.3f}",
            f"{overall_faithfulness_improvement:+.1f}%" if overall_faithfulness_improvement is not None else "N/A",
            f"{b_overall_hallucination:.3f}",
            f"{h_overall_hallucination:.3f}",
            f"{b_overall_no_answer:.3f}",
            f"{h_overall_no_answer:.3f}",
            f"{int(b_overall_latency)}",
            f"{int(h_overall_latency)}"
        ]
        table_data.append(overall_row)
        
        headers = [
            "Category",
            "Baseline\nRetrieval Hit",
            "Hybrid\nRetrieval Hit",
            "Improvement",
            "Baseline\nFaithfulness",
            "Hybrid\nFaithfulness",
            "Improvement",
            "Baseline\nHallucination",
            "Hybrid\nHallucination",
            "Baseline\nNo-Answer",
            "Hybrid\nNo-Answer",
            "Baseline\nLatency (ms)",
            "Hybrid\nLatency (ms)"
        ]
        
        print("\n" + "="*150)
        print("BASELINE vs HYBRID RETRIEVAL COMPARISON")
        print("Baseline: Vector-only retrieval (FAISS)")
        print("Hybrid: BM25 + Vector + Reciprocal Rank Fusion + Cross-Encoder Reranking")
        print("="*150)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print("="*150 + "\n")
        
        # Print key insights
        print("KEY INSIGHTS:")
        if overall_retrieval_improvement and overall_retrieval_improvement > 0:
            print(f"✓ Hybrid retrieval improved retrieval hit rate by {overall_retrieval_improvement:.1f}%")
        if overall_faithfulness_improvement and overall_faithfulness_improvement > 0:
            print(f"✓ Hybrid retrieval improved faithfulness by {overall_faithfulness_improvement:.1f}%")
        if h_overall_hallucination < b_overall_hallucination:
            reduction = ((b_overall_hallucination - h_overall_hallucination) / b_overall_hallucination * 100)
            print(f"✓ Hybrid retrieval reduced hallucinations by {reduction:.1f}%")
        print()


def main():
    logger.info("Starting hybrid retrieval comparison evaluation...")
    
    evaluator = HybridEvaluator()
    results = evaluator.run_comparison()
    
    if results:
        evaluator.save_results(results)
        evaluator.print_comparison_summary(results)
    else:
        logger.warning("No evaluation results generated.")


if __name__ == "__main__":
    main()
