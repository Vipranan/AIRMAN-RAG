"""
evaluate_with_analysis.py - Enhanced evaluation with qualitative analysis
Runs evaluation and generates a complete report with best/worst examples
"""

import json
import time
import argparse
from typing import List, Dict, Tuple
import requests
from loguru import logger
from tabulate import tabulate
from datetime import datetime
import config


class EnhancedEvaluator:
    """Evaluate RAG system with qualitative analysis"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.logger = logger
    
    def load_questions(self) -> List[Dict]:
        """Load questions from JSON file"""
        with open(config.QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data["questions"]
        self.logger.info(f"Loaded {len(questions)} questions")
        
        # Check if ground truth exists
        has_gt = sum(1 for q in questions if q.get("ground_truth", "").strip())
        self.logger.info(f"Questions with ground truth: {has_gt}/{len(questions)}")
        
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
        
        all_text = " ".join([chunk["text"].lower() for chunk in retrieved_chunks])
        
        for keyword in expected_keywords:
            if keyword.lower() in all_text:
                return True
        
        return False
    
    def compute_answer_match_score(self, answer: str, ground_truth: str) -> float:
        """Compute token overlap between answer and ground truth"""
        if answer == config.NO_ANSWER_RESPONSE or not ground_truth:
            return 0.0
        
        answer_tokens = set(answer.lower().split())
        gt_tokens = set(ground_truth.lower().split())
        
        if not gt_tokens:
            return 0.0
        
        overlap = len(answer_tokens & gt_tokens)
        score = overlap / len(gt_tokens)
        
        return score
    
    def evaluate_question(self, question_data: Dict) -> Dict:
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
        ) if ground_truth else None
        
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
            "ground_truth": ground_truth,
            "answer": result["answer"],
            "citations": result["citations"],
            "faithfulness_score": result["faithfulness_score"],
            "retrieval_hit": retrieval_hit,
            "answer_match_score": answer_match_score,
            "hallucinated": hallucinated,
            "no_answer_returned": no_answer_returned,
            "latency_ms": result["latency_ms"],
            "retrieved_chunks": result.get("retrieved_chunks", [])
        }
        
        return eval_result
    
    def run_evaluation(self) -> List[Dict]:
        """Run evaluation on all questions"""
        questions = self.load_questions()
        
        if not questions:
            self.logger.warning("No questions found in questions.json")
            return []
        
        results = []
        
        for q in questions:
            try:
                result = self.evaluate_question(q)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Failed to evaluate Q{q['id']}: {e}")
                continue
        
        return results
    
    def get_best_worst_answers(self, results: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Identify 5 best and 5 worst answers"""
        
        # Filter out no-answer responses for best/worst analysis
        answered = [r for r in results if not r["no_answer_returned"]]
        
        if not answered:
            return [], []
        
        # Score each answer (higher is better)
        for r in answered:
            score = 0.0
            
            # Faithfulness (40%)
            score += r["faithfulness_score"] * 0.4
            
            # Retrieval hit (30%)
            if r["retrieval_hit"] is not None:
                score += (1.0 if r["retrieval_hit"] else 0.0) * 0.3
            
            # Answer match (30%)
            if r["answer_match_score"] is not None:
                score += r["answer_match_score"] * 0.3
            
            r["overall_score"] = score
        
        # Sort by score
        sorted_results = sorted(answered, key=lambda x: x["overall_score"], reverse=True)
        
        best_5 = sorted_results[:5]
        worst_5 = sorted_results[-5:]
        
        return best_5, worst_5
    
    def generate_markdown_report(self, results: List[Dict]) -> str:
        """Generate markdown report with qualitative analysis"""
        
        report = []
        report.append("# Aviation Document AI Chat — Evaluation Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Total Questions:** {len(results)}")
        report.append("\n---\n")
        
        # Summary metrics
        report.append("## 1. Summary Metrics\n")
        
        categories = {}
        for r in results:
            cat = r["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)
        
        table_data = []
        
        for cat_name in ["factual", "applied", "reasoning"]:
            cat_results = categories.get(cat_name, [])
            
            if not cat_results:
                continue
            
            n = len(cat_results)
            
            retrieval_hits = [r for r in cat_results if r["retrieval_hit"] is not None]
            retrieval_hit_rate = sum(r["retrieval_hit"] for r in retrieval_hits) / len(retrieval_hits) if retrieval_hits else 0
            
            avg_faithfulness = sum(r["faithfulness_score"] for r in cat_results) / n
            hallucination_rate = sum(r["hallucinated"] for r in cat_results) / n
            no_answer_rate = sum(r["no_answer_returned"] for r in cat_results) / n
            
            answer_matches = [r for r in cat_results if r["answer_match_score"] is not None]
            avg_answer_match = sum(r["answer_match_score"] for r in answer_matches) / len(answer_matches) if answer_matches else 0
            
            avg_latency = sum(r["latency_ms"] for r in cat_results) / n
            
            table_data.append([
                f"{cat_name.capitalize()} (n={n})",
                f"{retrieval_hit_rate:.2%}",
                f"{avg_faithfulness:.2f}",
                f"{hallucination_rate:.2%}",
                f"{no_answer_rate:.2%}",
                f"{avg_answer_match:.2%}",
                f"{int(avg_latency)}ms"
            ])
        
        # Overall
        n_total = len(results)
        retrieval_hits = [r for r in results if r["retrieval_hit"] is not None]
        answer_matches = [r for r in results if r["answer_match_score"] is not None]
        
        table_data.append([
            f"**Overall (n={n_total})**",
            f"**{sum(r['retrieval_hit'] for r in retrieval_hits) / len(retrieval_hits):.2%}**" if retrieval_hits else "N/A",
            f"**{sum(r['faithfulness_score'] for r in results) / n_total:.2f}**",
            f"**{sum(r['hallucinated'] for r in results) / n_total:.2%}**",
            f"**{sum(r['no_answer_returned'] for r in results) / n_total:.2%}**",
            f"**{sum(r['answer_match_score'] for r in answer_matches) / len(answer_matches):.2%}**" if answer_matches else "N/A",
            f"**{int(sum(r['latency_ms'] for r in results) / n_total)}ms**"
        ])
        
        headers = ["Category", "Retrieval Hit", "Faithfulness", "Hallucination", "No-Answer", "Answer Match", "Latency"]
        report.append(tabulate(table_data, headers=headers, tablefmt="github"))
        report.append("\n")
        
        # Key findings
        report.append("## 2. Key Findings\n")
        
        overall_faithfulness = sum(r['faithfulness_score'] for r in results) / len(results)
        overall_hallucination = sum(r['hallucinated'] for r in results) / len(results)
        overall_no_answer = sum(r['no_answer_returned'] for r in results) / len(results)
        
        report.append(f"- **Average Faithfulness:** {overall_faithfulness:.2f} - {'✓ Good' if overall_faithfulness >= 0.7 else '⚠ Needs improvement'}")
        report.append(f"- **Hallucination Rate:** {overall_hallucination:.2%} - {'✓ Low' if overall_hallucination < 0.1 else '⚠ High'}")
        report.append(f"- **No-Answer Rate:** {overall_no_answer:.2%} - {'✓ Conservative' if overall_no_answer < 0.2 else '⚠ Too conservative'}")
        report.append("\n")
        
        # Best and worst answers
        best_5, worst_5 = self.get_best_worst_answers(results)
        
        report.append("## 3. Qualitative Analysis\n")
        
        report.append("### 3.1 Five Best Answers\n")
        for i, r in enumerate(best_5, 1):
            report.append(f"#### Best #{i}: Q{r['id']} (Score: {r['overall_score']:.2f})\n")
            report.append(f"**Question:** {r['question']}\n")
            report.append(f"**Answer:** {r['answer'][:300]}{'...' if len(r['answer']) > 300 else ''}\n")
            report.append(f"**Metrics:**")
            report.append(f"- Faithfulness: {r['faithfulness_score']:.2f}")
            report.append(f"- Retrieval Hit: {'✓' if r['retrieval_hit'] else '✗'}")
            if r['answer_match_score'] is not None:
                report.append(f"- Answer Match: {r['answer_match_score']:.2%}")
            report.append(f"- Citations: {len(r['citations'])} sources")
            report.append(f"\n**Why it's good:** High faithfulness score, relevant retrieval, and comprehensive answer with proper citations.\n")
        
        report.append("### 3.2 Five Worst Answers\n")
        for i, r in enumerate(worst_5, 1):
            report.append(f"#### Worst #{i}: Q{r['id']} (Score: {r['overall_score']:.2f})\n")
            report.append(f"**Question:** {r['question']}\n")
            report.append(f"**Answer:** {r['answer'][:300]}{'...' if len(r['answer']) > 300 else ''}\n")
            report.append(f"**Metrics:**")
            report.append(f"- Faithfulness: {r['faithfulness_score']:.2f}")
            report.append(f"- Retrieval Hit: {'✓' if r['retrieval_hit'] else '✗'}")
            if r['answer_match_score'] is not None:
                report.append(f"- Answer Match: {r['answer_match_score']:.2%}")
            report.append(f"- Hallucinated: {'Yes' if r['hallucinated'] else 'No'}")
            
            # Diagnose the issue
            issues = []
            if r['faithfulness_score'] < 0.5:
                issues.append("Low faithfulness - answer not well grounded in context")
            if not r['retrieval_hit']:
                issues.append("Retrieval failure - relevant chunks not found")
            if r['answer_match_score'] is not None and r['answer_match_score'] < 0.3:
                issues.append("Poor answer quality - low overlap with ground truth")
            
            report.append(f"\n**Issues:** {', '.join(issues) if issues else 'Multiple factors'}\n")
        
        # Recommendations
        report.append("## 4. Recommendations\n")
        report.append("### Immediate Actions\n")
        
        if overall_hallucination > 0.1:
            report.append("- ⚠ **High hallucination rate** - Consider increasing faithfulness threshold or improving prompt")
        
        if overall_no_answer > 0.3:
            report.append("- ⚠ **High no-answer rate** - Consider lowering similarity threshold or improving chunking")
        
        retrieval_failures = sum(1 for r in results if r['retrieval_hit'] is False)
        if retrieval_failures > len(results) * 0.2:
            report.append(f"- ⚠ **{retrieval_failures} retrieval failures** - Review chunking strategy and embedding model")
        
        report.append("\n### Long-term Improvements\n")
        report.append("- Implement hybrid search (BM25 + semantic)")
        report.append("- Add query expansion for aviation acronyms")
        report.append("- Extract tables and charts from PDFs")
        report.append("- Fine-tune embedding model on aviation corpus")
        report.append("\n")
        
        return "\n".join(report)
    
    def save_results(self, results: List[Dict]):
        """Save results to JSON file"""
        output = {
            "generated_at": datetime.now().isoformat(),
            "total_questions": len(results),
            "results": results
        }
        
        with open(config.RESULTS_PATH, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        self.logger.success(f"Results saved to {config.RESULTS_PATH}")
    
    def save_report(self, report_text: str):
        """Save markdown report"""
        report_path = "aviation_rag/evaluation_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        self.logger.success(f"Report saved to {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Enhanced evaluation with qualitative analysis")
    parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    args = parser.parse_args()
    
    api_url = f"http://localhost:{args.port}"
    
    # Check if API is reachable
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        response.raise_for_status()
        logger.info(f"API is reachable at {api_url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot reach API at {api_url}. Make sure the app is running.")
        logger.error(f"Start with: python app.py")
        return
    
    # Run evaluation
    evaluator = EnhancedEvaluator(api_url)
    
    logger.info("Starting evaluation...")
    results = evaluator.run_evaluation()
    
    if results:
        logger.info("Saving results...")
        evaluator.save_results(results)
        
        logger.info("Generating report with qualitative analysis...")
        report = evaluator.generate_markdown_report(results)
        evaluator.save_report(report)
        
        logger.success("✓ Evaluation complete!")
        logger.info("Check evaluation_report.md for detailed analysis")
    else:
        logger.warning("No evaluation results generated.")


if __name__ == "__main__":
    main()
