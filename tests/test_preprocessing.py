# tests/test_preprocessing.py

"""Unit tests for preprocessing module."""

import pytest
import pandas as pd
from io import StringIO
from src.preprocessing import (
    clean_text,
    extract_skills,
    calculate_job_fit
)


class TestTextCleaning:
    """Test text cleaning functions."""

    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        text = "Python Programming & Development!!"
        cleaned = clean_text(text)
        assert cleaned == "python programming  development"

    def test_clean_text_extra_spaces(self):
        """Test extra space removal."""
        text = "Python    SQL   Docker"
        cleaned = clean_text(text)
        assert "  " not in cleaned

    def test_clean_text_special_chars(self):
        """Test special character removal."""
        text = "C++ @Python #SQL $Docker"
        cleaned = clean_text(text)
        assert "@" not in cleaned
        assert "#" not in cleaned
        assert "$" not in cleaned


class TestSkillExtraction:
    """Test skill extraction functions."""

    def test_extract_skills_basic(self):
        """Test basic skill extraction."""
        text = "Python, SQL, Docker"
        skills = extract_skills(text)
        assert len(skills) == 3
        assert "Python" in skills

    def test_extract_skills_empty_string(self):
        """Test extraction from empty string."""
        skills = extract_skills("")
        assert skills == []

    def test_extract_skills_none(self):
        """Test extraction from None."""
        skills = extract_skills(None)
        assert skills == []

    def test_extract_skills_nan(self):
        """Test extraction from NaN."""
        import pandas as pd
        skills = extract_skills(pd.NA)
        assert skills == []

    def test_extract_skills_with_whitespace(self):
        """Test skills with extra whitespace."""
        text = "  Python  ,  SQL  ,  Docker  "
        skills = extract_skills(text)
        assert all(skill == skill.strip() for skill in skills)


class TestJobFitCalculation:
    """Test job fit calculation."""

    def test_job_fit_perfect_match(self):
        """Test perfect skill match."""
        resume_skills = ["Python", "SQL", "Docker"]
        jd_skills = ["Python", "SQL", "Docker"]

        fit = calculate_job_fit(resume_skills, jd_skills)
        assert fit == 1.0

    def test_job_fit_no_match(self):
        """Test no skill match."""
        resume_skills = ["Java", "JavaScript"]
        jd_skills = ["Python", "Go"]

        fit = calculate_job_fit(resume_skills, jd_skills)
        assert fit == 0.0

    def test_job_fit_partial_match(self):
        """Test partial skill match."""
        resume_skills = ["Python", "SQL"]
        jd_skills = ["Python", "SQL", "Docker"]

        fit = calculate_job_fit(resume_skills, jd_skills)
        assert fit == round(2/3, 2)

    def test_job_fit_empty_jd_skills(self):
        """Test with empty JD skills."""
        resume_skills = ["Python"]
        jd_skills = []

        fit = calculate_job_fit(resume_skills, jd_skills)
        assert fit == 0.0

    def test_job_fit_case_insensitive(self):
        """Test case-insensitive matching."""
        resume_skills = ["python", "SQL"]
        jd_skills = ["Python", "sql"]

        fit = calculate_job_fit(resume_skills, jd_skills)
        assert fit == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
