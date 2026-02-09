# src/rag_qa.py

import faiss
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGQA:
    def __init__(self):
        self.root = Path(__file__).parent.parent

        # Embedding model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Load FAISS index
        self.index = faiss.read_index(
            str(self.root / "models/embeddings/jd_index.faiss")
        )

        # Load metadata
        with open(self.root / "models/embeddings/jd_metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

        # Load LLM
        model_name = "microsoft/phi-2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="auto"
        )

    def retrieve_context(self, query: str, k: int = 3) -> str:
        """
        Retrieve top-k relevant job descriptions.
        """
        query_embedding = self.embedder.encode([query])
        distances, indices = self.index.search(query_embedding, k)

        contexts = []
        for idx in indices[0]:
            item = self.metadata[idx]
            contexts.append(
                f"""
Job Title: {item['job_title']}
Industry: {item['industry']}
Required Skills: {item['skills_required']}
Experience Required: {item['experience_required']} years
Job Description: {item['job_description_clean']}
"""
            )

        return "\n".join(contexts)

    def generate_answer(self, query: str) -> str:
        """
        Generate grounded answer using retrieved context.
        """
        context = self.retrieve_context(query)

        # 🔍 Debug: see what LLM sees
        print("\n--- RETRIEVED CONTEXT ---")
        print(context)
        print("------------------------\n")

        prompt = f"""
You are a professional career advisor AI.
Answer ONLY using the context provided.
If information is missing, say so clearly.

Context:
{context}

Question:
{query}

Answer:
"""

        inputs = self.tokenizer(
            prompt, return_tensors="pt").to(self.model.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=250,
            do_sample=False
        )

        return self.tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    rag = RAGQA()

    query = "What skills are required to become a Machine Learning Engineer?"
    answer = rag.generate_answer(query)

    print("🔍 Question:")
    print(query)
    print("\n🤖 Answer:")
    print(answer)
