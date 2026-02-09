# src/agents.py

import logging
from pathlib import Path
from typing import List, Dict, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer

from src.rag_pipeline import retrieve_job_context
from src.config import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Global model and tokenizer (lazy-loaded)
_model: Optional[AutoModelForCausalLM] = None
_tokenizer: Optional[AutoTokenizer] = None


def _load_model():
    """Lazy load LLM model and tokenizer on first use."""
    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    try:
        logger.info(f"Loading LLM model: {settings.LLM_MODEL_NAME}...")
        _tokenizer = AutoTokenizer.from_pretrained(settings.LLM_MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL_NAME,
            device_map=settings.LLM_DEVICE
        )
        logger.info("✅ Model loaded successfully.")
        return _model, _tokenizer
    except Exception as e:
        logger.error(f"Failed to load LLM model: {e}")
        raise


def get_model_and_tokenizer():
    """Get model and tokenizer, loading if necessary."""
    return _load_model()

# ------------------------------
# Core Agent Functions
# ------------------------------


def explain_skill_gap(
    candidate_skills: List[str],
    missing_skills: List[str],
    target_job: str
) -> str:
    """
    Generate LLM explanation of missing skills and learning recommendations.

    Args:
        candidate_skills: List of candidate's current skills
        missing_skills: List of missing skills for the target job
        target_job: Target job title

    Returns:
        explanation string
    """

    if not missing_skills:
        return "✅ You already have all required skills for this role!"

    prompt = f"""You are a career guidance AI assistant.
Candidate current skills: {', '.join(candidate_skills)}
Target job role: {target_job}
Missing skills: {', '.join(missing_skills)}

For each missing skill, explain why it is important for the target job,
and give actionable recommendations on how to learn it efficiently.
Provide concise, practical advice suitable for a candidate.
"""

    try:
        model, tokenizer = get_model_and_tokenizer()
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=settings.LLM_MAX_TOKENS,
            temperature=0.7,
            top_p=0.95
        )
        explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return explanation
    except Exception as e:
        logger.error(f"Error generating LLM explanation: {e}")
        return f"⚠️ LLM reasoning encountered an error: {str(e)}. Please try again."


def get_rag_explanation(
    candidate_skills: List[str],
    target_job: str,
    top_k: int = 3
) -> Dict:
    """
    Retrieve RAG context from job descriptions and combine with LLM reasoning.

    Args:
        candidate_skills: List of candidate's skills
        target_job: Target job title or job description
        top_k: Number of relevant job contexts to retrieve

    Returns:
        Dictionary containing retrieved context and AI explanation

    Raises:
        Exception: If RAG retrieval or LLM generation fails
    """
    try:
        # Use top_k from settings if not provided
        if top_k is None:
            top_k = settings.TOP_K_RETRIEVALS

        # Retrieve relevant job context (RAG)
        context_docs = retrieve_job_context(target_job, top_k=top_k)

        if not context_docs:
            logger.warning(f"No job context retrieved for: {target_job}")
            return {
                "retrieved_context": [],
                "missing_skills": [],
                "llm_explanation": "⚠️ No matching job descriptions found for this role."
            }

        retrieved_texts = [
            doc.get("job_description_clean", doc.get("job_description", ""))
            for doc in context_docs
        ]

        # Identify missing skills from RAG context
        all_required_skills = set()
        for doc in context_docs:
            skills = doc.get("skills_required_list",
                             doc.get("skills_required", []))
            if isinstance(skills, list):
                all_required_skills.update([s.lower() for s in skills])

        candidate_skills_lower = [s.lower() for s in candidate_skills]
        missing_skills = [
            s for s in all_required_skills
            if s not in candidate_skills_lower
        ]

        # Generate explanation with LLM
        explanation = explain_skill_gap(
            candidate_skills, list(missing_skills), target_job
        )

        return {
            "retrieved_context": retrieved_texts,
            "missing_skills": list(missing_skills),
            "llm_explanation": explanation
        }

    except Exception as e:
        logger.error(f"Error in get_rag_explanation: {e}")
        return {
            "retrieved_context": [],
            "missing_skills": [],
            "llm_explanation": f"❌ Error processing request: {str(e)}"
        }


# ------------------------------
# Example standalone test
# ------------------------------
if __name__ == "__main__":
    candidate = ["Python", "Pandas", "SQL"]
    target = "Machine Learning Engineer"

    result = get_rag_explanation(candidate, target)
    print("=== RETRIEVED CONTEXT ===")
    for idx, ctx in enumerate(result["retrieved_context"], 1):
        print(f"{idx}. {ctx}\n")

    print("=== MISSING SKILLS ===")
    print(result["missing_skills"])

    print("=== LLM EXPLANATION ===")
    print(result["llm_explanation"])
