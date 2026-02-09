# src/ml_model.py

"""
Machine Learning model utilities for SkillBridge-AI.
Provides functions for skill matching, similarity scoring, and model inference.
"""

import logging
from typing import List, Tuple, Dict, Optional
from difflib import SequenceMatcher
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from src.config import settings

logger = logging.getLogger(__name__)


class SkillMatcher:
    """Utility class for skill matching and comparison."""

    @staticmethod
    def fuzzy_match(skill1: str, skill2: str, threshold: float = 0.7) -> float:
        """
        Calculate fuzzy match score between two skills.

        Args:
            skill1: First skill
            skill2: Second skill
            threshold: Minimum similarity threshold (0-1)

        Returns:
            Similarity score (0-1)
        """
        skill1_lower = skill1.lower().strip()
        skill2_lower = skill2.lower().strip()

        # Exact match
        if skill1_lower == skill2_lower:
            return 1.0

        # Substring match
        if skill1_lower in skill2_lower or skill2_lower in skill1_lower:
            return 0.9

        # Fuzzy similarity using SequenceMatcher
        similarity = SequenceMatcher(None, skill1_lower, skill2_lower).ratio()

        return similarity if similarity >= threshold else 0.0

    @staticmethod
    def find_best_match(skill: str, candidates: List[str], threshold: float = 0.7) -> Optional[Tuple[str, float]]:
        """
        Find best matching skill from candidates.

        Args:
            skill: Target skill
            candidates: List of candidate skills
            threshold: Minimum similarity threshold

        Returns:
            Tuple of (best_match, score) or None
        """
        scores = [
            (candidate, SkillMatcher.fuzzy_match(skill, candidate, threshold))
            for candidate in candidates
        ]

        # Filter by threshold
        valid_scores = [(c, s) for c, s in scores if s >= threshold]

        if not valid_scores:
            return None

        # Return highest score
        return max(valid_scores, key=lambda x: x[1])

    @staticmethod
    def match_skills(
        candidate_skills: List[str],
        required_skills: List[str],
        threshold: float = 0.7
    ) -> Tuple[List[str], List[str]]:
        """
        Match candidate skills against required skills.

        Args:
            candidate_skills: List of candidate's skills
            required_skills: List of required skills for position
            threshold: Fuzzy match threshold

        Returns:
            Tuple of (matched_skills, missing_skills)
        """
        matched = []
        missing = []

        for req_skill in required_skills:
            best_match = SkillMatcher.find_best_match(
                req_skill,
                candidate_skills,
                threshold=threshold
            )

            if best_match:
                matched.append(best_match[0])
            else:
                missing.append(req_skill)

        return matched, missing

    @staticmethod
    def calculate_match_percentage(
        matched_count: int,
        total_required: int
    ) -> float:
        """
        Calculate skill match percentage.

        Args:
            matched_count: Number of matched skills
            total_required: Total required skills

        Returns:
            Match percentage (0-100)
        """
        if total_required == 0:
            return 0.0
        return round((matched_count / total_required) * 100, 2)


class SkillGapAnalyzer:
    """Analyze skill gaps between candidate and role requirements."""

    @staticmethod
    def analyze_gap(
        candidate_skills: List[str],
        required_skills: List[str],
        threshold: float = settings.SKILL_MATCH_THRESHOLD
    ) -> Dict:
        """
        Analyze skill gap.

        Args:
            candidate_skills: Candidate's current skills
            required_skills: Required skills for target role
            threshold: Fuzzy match threshold

        Returns:
            Dictionary with gap analysis
        """
        matched, missing = SkillMatcher.match_skills(
            candidate_skills,
            required_skills,
            threshold=threshold
        )

        match_pct = SkillMatcher.calculate_match_percentage(
            len(matched),
            len(required_skills)
        )

        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "match_percentage": match_pct,
            "skill_count": {
                "matched": len(matched),
                "missing": len(missing),
                "total_required": len(required_skills)
            }
        }

    @staticmethod
    def prioritize_skills(
        missing_skills: List[str],
        role_importance: Dict[str, float] = None
    ) -> List[Dict]:
        """
        Prioritize missing skills for learning.

        Args:
            missing_skills: List of missing skills
            role_importance: Optional dict mapping skills to importance scores

        Returns:
            List of prioritized skills with importance levels
        """
        if role_importance is None:
            role_importance = {}

        prioritized = []
        for skill in missing_skills:
            importance = role_importance.get(skill, 0.5)

            if importance >= 0.8:
                priority = "High"
            elif importance >= 0.5:
                priority = "Medium"
            else:
                priority = "Low"

            prioritized.append({
                "skill": skill,
                "priority": priority,
                "importance_score": importance
            })

        # Sort by importance
        prioritized.sort(key=lambda x: x["importance_score"], reverse=True)

        return prioritized


class SimilarityCalculator:
    """Calculate similarity between texts/skills using embeddings."""

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Similarity score (-1 to 1, typically 0-1 for embeddings)
        """
        if len(vec1.shape) == 1:
            vec1 = vec1.reshape(1, -1)
        if len(vec2.shape) == 1:
            vec2 = vec2.reshape(1, -1)

        similarity = cosine_similarity(vec1, vec2)[0][0]
        return float(similarity)

    @staticmethod
    def batch_cosine_similarity(
        query_vec: np.ndarray,
        candidate_vecs: np.ndarray
    ) -> np.ndarray:
        """
        Calculate cosine similarity between query and multiple candidates.

        Args:
            query_vec: Query vector (1D or 2D)
            candidate_vecs: Candidate vectors (2D)

        Returns:
            Array of similarity scores
        """
        if len(query_vec.shape) == 1:
            query_vec = query_vec.reshape(1, -1)

        similarities = cosine_similarity(query_vec, candidate_vecs)[0]
        return similarities


class LearningPathBuilder:
    """Build learning paths for skill development."""

    # Estimated learning time in weeks per skill level
    SKILL_DURATION = {
        "Beginner": 2,
        "Intermediate": 3,
        "Advanced": 4
    }

    @staticmethod
    def build_learning_path(
        missing_skills: List[str],
        experience_level: str = "Beginner"
    ) -> List[Dict]:
        """
        Build a structured learning path.

        Args:
            missing_skills: Skills to learn
            experience_level: Learner's current experience level

        Returns:
            List of learning path steps
        """
        path = []
        week = 1

        for i, skill in enumerate(missing_skills):
            # Determine difficulty based on order
            if i < len(missing_skills) * 0.33:
                level = "Beginner"
            elif i < len(missing_skills) * 0.66:
                level = "Intermediate"
            else:
                level = "Advanced"

            duration = LearningPathBuilder.SKILL_DURATION.get(level, 2)

            path.append({
                "skill": skill,
                "start_week": week,
                "end_week": week + duration,
                "level": level,
                "duration_weeks": duration,
                "resources": LearningPathBuilder.get_resources(skill, level)
            })

            week += duration + 1  # Add 1 week buffer

        return path

    @staticmethod
    def get_resources(skill: str, level: str = "Beginner") -> List[str]:
        """
        Get learning resources for a skill.

        Args:
            skill: Skill name
            level: Learning level

        Returns:
            List of resource suggestions
        """
        resources = [
            f"Udemy course on {skill}",
            f"Official {skill} documentation",
            f"Free online tutorials for {skill}",
            f"Practice projects using {skill}",
            f"Community forums and discussions on {skill}"
        ]

        # Enhance based on level
        if level == "Intermediate":
            resources.append(f"Advanced projects in {skill}")
        elif level == "Advanced":
            resources.append(f"Contribute to {skill} open-source projects")
            resources.append(f"Read research papers on {skill}")

        return resources
