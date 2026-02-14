"""
run_complete_evaluation.py - Complete evaluation pipeline
1. Generate ground truth answers
2. Run evaluation with metrics
3. Generate report with qualitative analysis
"""

import sys
import subprocess
import requests
from loguru import logger


def check_api_running(port: int = 8000) -> bool:
    """Check if the API is running"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    port = 8000
    
    logger.info("="*80)
    logger.info("COMPLETE EVALUATION PIPELINE")
    logger.info("="*80)
    
    # Step 0: Check if API is running
    logger.info("\n[Step 0/3] Checking if API is running...")
    
    if not check_api_running(port):
        logger.error(f"✗ API is not running on port {port}")
        logger.error("Please start the API first:")
        logger.error("  python app.py")
        logger.error("\nOr in another terminal:")
        logger.error("  cd aviation_rag")
        logger.error("  python app.py")
        sys.exit(1)
    
    logger.success(f"✓ API is running on port {port}")
    
    # Step 1: Generate ground truth
    logger.info("\n[Step 1/3] Generating ground truth answers...")
    logger.info("This will query the RAG system for all 50 questions...")
    logger.info("Estimated time: 2-3 minutes")
    
    try:
        result = subprocess.run(
            [sys.executable, "generate_ground_truth.py", "--port", str(port)],
            check=True,
            capture_output=False
        )
        logger.success("✓ Ground truth generation complete")
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Ground truth generation failed: {e}")
        sys.exit(1)
    
    # Step 2: Run evaluation
    logger.info("\n[Step 2/3] Running evaluation with metrics...")
    logger.info("This will re-query all questions and compute metrics...")
    logger.info("Estimated time: 2-3 minutes")
    
    try:
        result = subprocess.run(
            [sys.executable, "evaluate_with_analysis.py", "--port", str(port)],
            check=True,
            capture_output=False
        )
        logger.success("✓ Evaluation complete")
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Evaluation failed: {e}")
        sys.exit(1)
    
    # Done
    logger.info("\n" + "="*80)
    logger.success("✓ COMPLETE EVALUATION PIPELINE FINISHED")
    logger.info("="*80)
    logger.info("\nGenerated files:")
    logger.info("  1. questions.json (updated with ground truth)")
    logger.info("  2. data/eval_results.json (detailed metrics)")
    logger.info("  3. evaluation_report.md (qualitative analysis)")
    logger.info("\nNext steps:")
    logger.info("  - Review evaluation_report.md for insights")
    logger.info("  - Check best/worst answers section")
    logger.info("  - Implement recommended improvements")
    logger.info("")


if __name__ == "__main__":
    main()
