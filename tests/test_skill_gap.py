# tests/test_skill_gap.py

"""Unit tests for skill gap analysis."""

import pytest
from src.skill_gap import SkillGapAnalysis, SkillGapReport


class TestSkillGapAnalysis:
    """Test SkillGapAnalysis class."""

    def test_initialization(self):
        """Test SkillGapAnalysis initialization."""
        analyzer = SkillGapAnalysis()
        assert analyzer is not None

    def test_analyze_candidate(self):
        """Test candidate analysis."""
        analyzer = SkillGapAnalysis()

        result = analyzer.analyze_candidate(
            candidate_name="John Doe",
            candidate_skills=["Python", "SQL"],
            target_role="Backend Engineer",
            target_skills=["Python", "SQL", "Docker", "AWS"],
            experience_years=3
        )

        assert result["candidate"]["name"] == "John Doe"
        assert result["target_role"] == "Backend Engineer"
        assert "skill_gap_analysis" in result
        assert "learning_path" in result

    def test_compare_candidates(self):
        """Test comparing multiple candidates."""
        analyzer = SkillGapAnalysis()

        candidates = [
            {"name": "Candidate A", "skills": [
                "Python", "SQL"], "experience_years": 2},
            {"name": "Candidate B", "skills": [
                "Python", "SQL", "Docker"], "experience_years": 4},
        ]

        results = analyzer.compare_candidates(
            candidates=candidates,
            target_role="Backend Engineer",
            target_skills=["Python", "SQL", "Docker", "AWS"]
        )

        assert len(results) == 2
        # Candidate B should be ranked higher (more skills)
        assert results[0]["candidate"]["name"] == "Candidate B"

    def test_experience_level_determination(self):
        """Test experience level classification."""
        assert SkillGapAnalysis._get_experience_level(0) == "Junior"
        assert SkillGapAnalysis._get_experience_level(3) == "Mid-level"
        assert SkillGapAnalysis._get_experience_level(7) == "Senior"

    def test_readiness_level_calculation(self):
        """Test readiness level determination."""
        assert SkillGapAnalysis._calculate_readiness(0.9) == "Highly Qualified"
        assert SkillGapAnalysis._calculate_readiness(0.7) == "Well Qualified"
        assert SkillGapAnalysis._calculate_readiness(
            0.5) == "Moderately Qualified"
        assert SkillGapAnalysis._calculate_readiness(0.3) == "Entry Level"
        assert SkillGapAnalysis._calculate_readiness(
            0.1) == "Needs Development"


class TestSkillGapReport:
    """Test SkillGapReport class."""

    def test_generate_summary(self):
        """Test report generation."""
        analyzer = SkillGapAnalysis()
        analysis = analyzer.analyze_candidate(
            candidate_name="Test User",
            candidate_skills=["Python", "SQL"],
            target_role="Data Scientist",
            target_skills=["Python", "SQL", "R", "Tableau"],
            experience_years=2
        )

        report = SkillGapReport.generate_summary(analysis)

        assert "SKILL GAP ANALYSIS REPORT" in report
        assert "Test User" in report
        assert "Data Scientist" in report
        assert "%" in report

    def test_generate_dataframe(self):
        """Test DataFrame generation."""
        analyzer = SkillGapAnalysis()
        analyses = [
            analyzer.analyze_candidate(
                candidate_name="User 1",
                candidate_skills=["Python"],
                target_role="Data Scientist",
                target_skills=["Python", "SQL", "R"],
                experience_years=1
            ),
            analyzer.analyze_candidate(
                candidate_name="User 2",
                candidate_skills=["Python", "SQL", "R"],
                target_role="Data Scientist",
                target_skills=["Python", "SQL", "R"],
                experience_years=3
            ),
        ]

        df = SkillGapReport.generate_dataframe(analyses)

        assert len(df) == 2
        assert "Candidate" in df.columns
        assert "Match %" in df.columns
        assert df.loc[0, "Candidate"] == "User 2"  # Better candidate first


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
