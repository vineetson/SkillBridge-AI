# src/config.py

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration using environment variables.
    Can be overridden via .env file or environment variables.
    """

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_RAW_DIR: Path = PROJECT_ROOT / "data" / "raw"
    DATA_PROCESSED_DIR: Path = PROJECT_ROOT / "data" / "processed"
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    EMBEDDINGS_DIR: Path = MODELS_DIR / "embeddings"

    # Input files
    RESUME_RAW_PATH: Path = DATA_RAW_DIR / "resumes.csv"
    JOB_DESCRIPTIONS_RAW_PATH: Path = DATA_RAW_DIR / "job_descriptions.csv"

    # Output files
    RESUME_PROCESSED_PATH: Path = DATA_PROCESSED_DIR / "resumes_processed.csv"
    JOB_DESCRIPTIONS_PROCESSED_PATH: Path = (
        DATA_PROCESSED_DIR / "job_descriptions_processed.csv"
    )
    JOB_FIT_OUTPUT_PATH: Path = DATA_PROCESSED_DIR / "job_fit_scores.csv"

    # Embeddings
    RESUME_INDEX_PATH: Path = EMBEDDINGS_DIR / "resume_index.faiss"
    RESUME_METADATA_PATH: Path = EMBEDDINGS_DIR / "resume_metadata.pkl"
    JD_INDEX_PATH: Path = EMBEDDINGS_DIR / "jd_index.faiss"
    JD_METADATA_PATH: Path = EMBEDDINGS_DIR / "jd_metadata.pkl"

    # Model configuration
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    LLM_MODEL_NAME: str = "gpt2"  # Changed from Falcon 7B to lightweight model
    LLM_DEVICE: str = "cpu"  # or "cuda" if GPU available
    LLM_MAX_TOKENS: int = 300

    # API configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False
    API_RELOAD: bool = False
    API_WORKERS: int = 1

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    # Frontend
    FRONTEND_URL: str = "http://localhost:8501"
    BACKEND_URL: str = "http://localhost:8000"

    # RAG Configuration
    TOP_K_RETRIEVALS: int = 5
    SIMILARITY_THRESHOLD: float = 0.5

    # Skill matching
    SKILL_MATCH_THRESHOLD: float = 0.7  # For fuzzy matching

    # Performance
    BATCH_SIZE: int = 32
    ENABLE_CACHING: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def validate_paths() -> bool:
    """Validate that all required paths exist."""
    required_paths = [
        settings.RESUME_RAW_PATH,
        settings.JOB_DESCRIPTIONS_RAW_PATH,
    ]

    missing_paths = [p for p in required_paths if not p.exists()]
    if missing_paths:
        print(f"⚠️  Warning: Missing data files: {missing_paths}")
        return False
    return True


def create_output_directories() -> None:
    """Create output directories if they don't exist."""
    dirs_to_create = [
        settings.DATA_PROCESSED_DIR,
        settings.EMBEDDINGS_DIR,
    ]

    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
