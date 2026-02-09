# tests/conftest.py

"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_candidate_skills():
    """Sample candidate skills."""
    return ["Python", "SQL", "Pandas", "Docker"]


@pytest.fixture
def sample_required_skills():
    """Sample required skills for a role."""
    return ["Python", "SQL", "Docker", "AWS", "Kubernetes"]


@pytest.fixture
def sample_resume_csv(tmp_path):
    """Create a sample resume CSV."""
    csv_file = tmp_path / "resumes.csv"
    csv_file.write_text(
        "candidate_name,resume_text,skills,job_role,experience_years\n"
        "John Doe,Python developer with SQL experience,Python SQL,Developer,3\n"
        "Jane Smith,Data scientist expert,Python Pandas NumPy,Data Scientist,5\n"
    )
    return csv_file


@pytest.fixture
def sample_jd_csv(tmp_path):
    """Create a sample job descriptions CSV."""
    csv_file = tmp_path / "job_descriptions.csv"
    csv_file.write_text(
        "job_title,job_description,skills_required,industry,experience_required\n"
        "Backend Engineer,Build scalable APIs,Python Docker SQL,Tech,2-4\n"
        "Data Scientist,Analyze data trends,Python SQL Pandas,Finance,3-5\n"
    )
    return csv_file
