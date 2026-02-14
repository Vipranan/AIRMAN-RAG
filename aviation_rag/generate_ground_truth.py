"""
generate_ground_truth.py - Generate ground truth answers using the RAG system
This script queries the RAG system for all questions and saves answers as ground truth
"""

import json
import time
import requests
from loguru import logger
import config


def generate_ground_truth(api_url: str = "http://localhost:8000"):
    """Generate ground truth answers by querying the RAG system"""
    
    # Load questions
    logger.info(f"Loading questions from {config.QUESTIONS_PATH}")
    with open(config.QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data["questions"]
    logger.info(f"Loaded {len(questions)} questions")
    
    # Check API health
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        response.raise_for_status()
        logger.success(f"API is reachable at {api_url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot reach API at {api_url}. Make sure app.py is running.")
        logger.error(f"Start with: python app.py")
        return
    
    # Generate answers
    updated_count = 0
    
    for i, q in enumerate(questions, 1):
        question_text = q["question"]
        logger.info(f"[{i}/{len(questions)}] Generating answer for Q{q['id']}: {question_text[:60]}...")
        
        try:
            # Query the RAG system
            response = requests.post(
                f"{api_url}/ask",
                json={"question": question_text, "debug": False},
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            
            # Save answer as ground truth
            answer = result["answer"]
            q["ground_truth"] = answer
            
            logger.success(f"  ✓ Generated ({len(answer)} chars, faithfulness: {result['faithfulness_score']:.2f})")
            updated_count += 1
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.5)
            
        except Exception as e:
            logger.error(f"  ✗ Failed: {e}")
            q["ground_truth"] = ""
    
    # Save updated questions
    logger.info(f"Saving updated questions to {config.QUESTIONS_PATH}")
    with open(config.QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logger.success(f"✓ Generated ground truth for {updated_count}/{len(questions)} questions")
    logger.info(f"Next step: Run 'python evaluate.py' to generate evaluation report")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate ground truth answers using RAG system")
    parser.add_argument("--port", type=int, default=8000, help="API port (default: 8000)")
    args = parser.parse_args()
    
    api_url = f"http://localhost:{args.port}"
    generate_ground_truth(api_url)
