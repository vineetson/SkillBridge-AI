# src/rag_pipeline.py

import pandas as pd
import logging
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingPipeline:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Lightweight, fast, open-source embedding model.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: list) -> np.ndarray:
        """
        Convert list of texts into embeddings.
        """
        logger.info(f"Generating embeddings for {len(texts)} texts")
        return self.model.encode(texts, show_progress_bar=True)


def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """
    Create FAISS index from embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    logger.info(f"FAISS index created with {index.ntotal} vectors")
    return index


def save_index(index, metadata, index_path, metadata_path):
    """
    Save FAISS index and metadata.
    """
    faiss.write_index(index, str(index_path))
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)
    logger.info(
        f"Index and metadata saved to {index_path} and {metadata_path}")


def load_index(index_path, metadata_path):
    """
    Load FAISS index and metadata.
    """
    index = faiss.read_index(str(index_path))
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata


def retrieve_job_context(candidate_skills: list, top_k: int = 5):
    """
    Retrieve the most relevant job descriptions for a candidate based on skills.
    Returns a list of context dicts.

    Args:
        candidate_skills: list of candidate skills
        top_k: number of top matching jobs to retrieve

    Returns:
        List[dict]: Each dict has job_title, industry, job_description, skills_required, experience_required
    """
    ROOT = Path(__file__).parent.parent
    jd_index_path = ROOT / "models/embeddings/jd_index.faiss"
    jd_metadata_path = ROOT / "models/embeddings/jd_metadata.pkl"

    if not jd_index_path.exists() or not jd_metadata_path.exists():
        raise FileNotFoundError(
            "JD FAISS index or metadata not found. Run embedding pipeline first."
        )

    # Load index and metadata
    jd_index, jd_metadata = load_index(jd_index_path, jd_metadata_path)

    # Embed candidate skills
    embedder = EmbeddingPipeline()
    candidate_text = " ".join(candidate_skills)
    candidate_embedding = embedder.generate_embeddings([candidate_text])

    # Search top-k similar job descriptions
    D, I = jd_index.search(candidate_embedding, top_k)
    retrieved_context = [jd_metadata[i] for i in I[0]]
    logger.info(
        f"Retrieved top-{top_k} jobs for candidate skills: {candidate_skills}")
    return retrieved_context


if __name__ == "__main__":
    ROOT = Path(__file__).parent.parent

    resumes_path = ROOT / "data/processed/resumes_processed.csv"
    jds_path = ROOT / "data/processed/job_descriptions_processed.csv"

    model_dir = ROOT / "models/embeddings"
    model_dir.mkdir(parents=True, exist_ok=True)

    # Load processed data
    resumes = pd.read_csv(resumes_path)
    jds = pd.read_csv(jds_path)

    # Texts to embed
    resume_texts = resumes["resume_text_clean"].tolist()
    jd_texts = jds["job_description_clean"].tolist()

    embedder = EmbeddingPipeline()

    # Generate embeddings
    logger.info("Generating resume embeddings...")
    resume_embeddings = embedder.generate_embeddings(resume_texts)

    logger.info("Generating job description embeddings...")
    jd_embeddings = embedder.generate_embeddings(jd_texts)

    # Build FAISS indexes
    resume_index = build_faiss_index(resume_embeddings)
    jd_index = build_faiss_index(jd_embeddings)

    # Save resume index + metadata
    save_index(
        resume_index,
        resumes[["candidate_name", "job_role", "skills", "experience_years"]]
        .to_dict(orient="records"),
        model_dir / "resume_index.faiss",
        model_dir / "resume_metadata.pkl"
    )

    # Save full JD context
    save_index(
        jd_index,
        jds[
            [
                "job_title",
                "industry",
                "job_description_clean",
                "skills_required",
                "experience_required",
            ]
        ].to_dict(orient="records"),
        model_dir / "jd_index.faiss",
        model_dir / "jd_metadata.pkl"
    )

    logger.info("✅ Embedding pipeline and RAG setup completed successfully")
