# src/preprocessing.py

import pandas as pd
import re
import logging
from pathlib import Path
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Lowercase, remove special characters, extra spaces.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s,]", "", text)  # Keep letters, numbers, commas
    text = re.sub(r"\s+", " ", text)          # Remove extra spaces
    return text.strip()


def extract_skills(text: str) -> list:
    """
    Extract skills from text. Assumes skills are comma-separated in text.
    Handles None/NaN values gracefully.
    """
    if pd.isna(text) or not isinstance(text, str):
        return []
    return [s.strip() for s in text.split(",") if s.strip()]


def calculate_job_fit(resume_skills: list, jd_skills: list) -> float:
    """
    Calculate job-fit score: (# matching skills) / (# JD skills)
    """
    if not jd_skills:
        return 0.0
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])
    match = len(resume_set & jd_set)
    return round(match / len(jd_set), 2)


def preprocess_resumes(resume_path: str, output_path: str) -> pd.DataFrame:
    """
    Read raw resumes, clean text, extract skills.
    Save processed CSV.

    Args:
        resume_path: Path to raw resumes CSV
        output_path: Path to save processed resumes CSV

    Returns:
        Processed DataFrame

    Raises:
        FileNotFoundError: If resume file doesn't exist
        ValueError: If required columns are missing
    """
    try:
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"Resume file not found: {resume_path}")

        logger.info(f"Loading resumes from {resume_path}")
        resumes = pd.read_csv(resume_path)

        # Validate required columns
        required_cols = {"resume_text", "skills", "candidate_name"}
        missing_cols = required_cols - set(resumes.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        if resumes.empty:
            raise ValueError("Resume CSV is empty")

        resumes["resume_text_clean"] = resumes["resume_text"].apply(clean_text)
        resumes["skills_list"] = resumes["skills"].apply(extract_skills)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        resumes.to_csv(output_path, index=False)
        logger.info(
            f"Processed {len(resumes)} resumes and saved to {output_path}")
        return resumes

    except Exception as e:
        logger.error(f"Error processing resumes: {str(e)}")
        raise


def preprocess_job_descriptions(jd_path: str, output_path: str) -> pd.DataFrame:
    """
    Read raw job descriptions, clean text, extract required skills.
    Save processed CSV.

    Args:
        jd_path: Path to raw job descriptions CSV
        output_path: Path to save processed job descriptions CSV

    Returns:
        Processed DataFrame

    Raises:
        FileNotFoundError: If JD file doesn't exist
        ValueError: If required columns are missing
    """
    try:
        if not os.path.exists(jd_path):
            raise FileNotFoundError(
                f"Job descriptions file not found: {jd_path}")

        logger.info(f"Loading job descriptions from {jd_path}")
        jds = pd.read_csv(jd_path)

        # Validate required columns
        required_cols = {"job_description", "skills_required", "job_title"}
        missing_cols = required_cols - set(jds.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        if jds.empty:
            raise ValueError("Job descriptions CSV is empty")

        jds["job_description_clean"] = jds["job_description"].apply(clean_text)
        jds["skills_required_list"] = jds["skills_required"].apply(
            extract_skills)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        jds.to_csv(output_path, index=False)
        logger.info(
            f"Processed {len(jds)} job descriptions and saved to {output_path}")
        return jds

    except Exception as e:
        logger.error(f"Error processing job descriptions: {str(e)}")
        raise


def compute_job_fit(resumes: pd.DataFrame, jds: pd.DataFrame, output_path: str):
    """
    For each resume, compute job-fit score for each job description.
    Save a long-format CSV: candidate_name, job_title, job_fit

    Args:
        resumes: DataFrame with processed resumes
        jds: DataFrame with processed job descriptions
        output_path: Path to save job fit scores CSV

    Returns:
        DataFrame with job fit scores

    Raises:
        ValueError: If DataFrames are empty or missing required columns
    """
    try:
        # Validate inputs
        if resumes.empty:
            raise ValueError("Resumes DataFrame is empty")
        if jds.empty:
            raise ValueError("Job descriptions DataFrame is empty")

        required_resume_cols = {"candidate_name", "skills_list"}
        required_jd_cols = {"job_title", "skills_required_list"}

        if not required_resume_cols.issubset(resumes.columns):
            raise ValueError(
                f"Missing columns in resumes: {required_resume_cols - set(resumes.columns)}")
        if not required_jd_cols.issubset(jds.columns):
            raise ValueError(
                f"Missing columns in job descriptions: {required_jd_cols - set(jds.columns)}")

        logger.info("Computing job-fit scores...")
        results = []

        for _, resume in resumes.iterrows():
            resume_name = resume["candidate_name"]
            resume_skills = resume["skills_list"]

            for _, jd in jds.iterrows():
                job_title = jd["job_title"]
                jd_skills = jd["skills_required_list"]
                fit_score = calculate_job_fit(resume_skills, jd_skills)

                results.append({
                    "candidate_name": resume_name,
                    "job_title": job_title,
                    "job_fit": fit_score
                })

        df_fit = pd.DataFrame(results)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df_fit.to_csv(output_path, index=False)
        logger.info(
            f"Job-fit scores for {len(df_fit)} pairs saved to {output_path}")
        return df_fit

    except Exception as e:
        logger.error(f"Error computing job fit: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        # File paths - use absolute paths from workspace root
        workspace_root = Path(__file__).parent.parent
        RESUME_RAW = workspace_root / "data" / "raw" / "resumes.csv"
        RESUME_PROCESSED = workspace_root / "data" / \
            "processed" / "resumes_processed.csv"
        JD_RAW = workspace_root / "data" / "raw" / "job_descriptions.csv"
        JD_PROCESSED = workspace_root / "data" / \
            "processed" / "job_descriptions_processed.csv"
        JOB_FIT_OUTPUT = workspace_root / "data" / "processed" / "job_fit_scores.csv"

        # Preprocess
        resumes_df = preprocess_resumes(str(RESUME_RAW), str(RESUME_PROCESSED))
        jds_df = preprocess_job_descriptions(str(JD_RAW), str(JD_PROCESSED))

        # Compute job-fit scores
        compute_job_fit(resumes_df, jds_df, str(JOB_FIT_OUTPUT))

        logger.info("Preprocessing complete. Phase 1 finished.")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        raise
