# tests/test_ml_model.py

"""Unit tests for ML model utilities."""

import pytest
from src.ml_model import (
    SkillMatcher,
    SkillGapAnalyzer,
    LearningPathBuilder,
    SimilarityCalculator
)


class TestSkillMatcher:
    """Test SkillMatcher class."""

    def test_fuzzy_match_exact(self):
        """Test exact skill match."""
        score = SkillMatcher.fuzzy_match("Python", "python")
        assert score == 1.0

    def test_fuzzy_match_substring(self):
        """Test substring match."""
        score = SkillMatcher.fuzzy_match("Python", "Python 3")
        assert score > 0.8

    def test_fuzzy_match_no_match(self):
        """Test non-matching skills."""
        score = SkillMatcher.fuzzy_match("Python", "JavaScript", threshold=0.7)
        assert score < 0.7

    def test_find_best_match(self):
        """Test finding best matching skill."""
        candidates = ["Python", "Java", "JavaScript"]
        result = SkillMatcher.find_best_match("Python 3", candidates)
        assert result is not None
        assert result[0] == "Python"

    def test_match_skills(self):
        """Test skill matching."""
        candidate_skills = ["Python", "SQL", "Pandas"]
        required_skills = ["Python", "SQL", "NumPy", "Docker"]

        matched, missing = SkillMatcher.match_skills(
            candidate_skills,
            required_skills,
            threshold=0.9
        )

        assert len(matched) >= 2
        assert "Docker" in missing

    def test_calculate_match_percentage(self):
        """Test match percentage calculation."""
        pct = SkillMatcher.calculate_match_percentage(3, 5)
        assert pct == 60.0

        pct = SkillMatcher.calculate_match_percentage(0, 5)
        assert pct == 0.0

        pct = SkillMatcher.calculate_match_percentage(5, 0)
        assert pct == 0.0


class TestSkillGapAnalyzer:
    """Test SkillGapAnalyzer class."""

    def test_analyze_gap(self):
        """Test gap analysis."""
        candidate_skills = ["Python", "SQL"]
        required_skills = ["Python", "SQL", "Docker", "AWS"]

        result = SkillGapAnalyzer.analyze_gap(
            candidate_skills,
            required_skills,
            threshold=0.8
        )

        assert "matched_skills" in result
        assert "missing_skills" in result
        assert "match_percentage" in result
        assert result["match_percentage"] <= 100.0

    def test_prioritize_skills(self):
        """Test skill prioritization."""
        missing_skills = ["Docker", "Kubernetes", "Terraform"]
        importance = {"Docker": 0.9, "Kubernetes": 0.7, "Terraform": 0.4}

        prioritized = SkillGapAnalyzer.prioritize_skills(
            missing_skills, importance)

        assert len(prioritized) == 3
        assert prioritized[0]["skill"] == "Docker"  # Highest importance first
        assert prioritized[0]["priority"] == "High"


class TestLearningPathBuilder:
    """Test LearningPathBuilder class."""

    def test_build_learning_path(self):
        """Test learning path building."""
        skills = ["Docker", "Kubernetes", "Terraform"]

        path = LearningPathBuilder.build_learning_path(skills)

        assert len(path) == 3
        assert all("skill" in step for step in path)
        assert all("start_week" in step for step in path)
        assert all("level" in step for step in path)

    def test_get_resources(self):
        """Test resource suggestions."""
        resources_beginner = LearningPathBuilder.get_resources(
            "Python", "Beginner")
        resources_advanced = LearningPathBuilder.get_resources(
            "Python", "Advanced")

        assert len(resources_beginner) > 0
        assert len(resources_advanced) > len(resources_beginner)


class TestSimilarityCalculator:
    """Test SimilarityCalculator class."""

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        import numpy as np

        vec1 = np.array([1, 0, 0])
        vec2 = np.array([1, 0, 0])

        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert abs(similarity - 1.0) < 0.01

    def test_cosine_similarity_orthogonal(self):
        """Test orthogonal vectors."""
        import numpy as np

        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])

        similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
        assert abs(similarity) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
