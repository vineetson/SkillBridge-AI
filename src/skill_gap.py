# src/skill_gap.py

"""
Skill gap analysis module.
Integrates preprocessing, ML models, and RAG for comprehensive skill gap analysis.
"""

import logging
from typing import List, Dict, Optional, Tuple
import pandas as pd

from src.ml_model import (
    SkillMatcher,
    SkillGapAnalyzer,
    LearningPathBuilder,
    SimilarityCalculator
)
from src.preprocessing import calculate_job_fit
from src.config import settings

logger = logging.getLogger(__name__)


class SkillGapAnalysis:
    """Main skill gap analysis orchestrator."""

    def __init__(self):
        """Initialize skill gap analysis engine."""
        self.matcher = SkillMatcher()
        self.analyzer = SkillGapAnalyzer()
        self.path_builder = LearningPathBuilder()
        logger.info("✅ Skill Gap Analysis engine initialized")

    def analyze_candidate(
        self,
        candidate_name: str,
        candidate_skills: List[str],
        target_role: str,
        target_skills: List[str],
        experience_years: int = 0
    ) -> Dict:
        """
        Comprehensive skill gap analysis for a candidate.

        Args:
            candidate_name: Candidate name
            candidate_skills: List of candidate's skills
            target_role: Target job role
            target_skills: Required skills for target role
            experience_years: Years of experience

        Returns:
            Dictionary with comprehensive analysis
        """
        try:
            logger.info(
                f"Analyzing skill gap for {candidate_name} -> {target_role}")

            # Step 1: Analyze skill gap
            gap_analysis = self.analyzer.analyze_gap(
                candidate_skills,
                target_skills,
                threshold=settings.SKILL_MATCH_THRESHOLD
            )

            # Step 2: Prioritize missing skills
            missing_skills = gap_analysis["missing_skills"]
            prioritized_skills = self.analyzer.prioritize_skills(
                missing_skills)

            # Step 3: Build learning path
            learning_path = self.path_builder.build_learning_path(
                missing_skills,
                experience_level=self._get_experience_level(experience_years)
            )

            # Step 4: Calculate job fit score
            job_fit_score = calculate_job_fit(candidate_skills, target_skills)

            result = {
                "candidate": {
                    "name": candidate_name,
                    "skills": candidate_skills,
                    "experience_years": experience_years,
                    "experience_level": self._get_experience_level(experience_years)
                },
                "target_role": target_role,
                "skill_gap_analysis": {
                    "matched_skills": gap_analysis["matched_skills"],
                    "missing_skills": missing_skills,
                    "match_percentage": gap_analysis["match_percentage"],
                    "skill_count": gap_analysis["skill_count"]
                },
                "prioritized_missing_skills": prioritized_skills,
                "learning_path": learning_path,
                "job_fit_score": job_fit_score,
                "readiness_level": self._calculate_readiness(job_fit_score)
            }

            logger.info(f"✅ Analysis complete: {job_fit_score*100:.1f}% fit")
            return result

        except Exception as e:
            logger.error(f"Error analyzing skill gap: {e}")
            raise

    def compare_candidates(
        self,
        candidates: List[Dict],
        target_role: str,
        target_skills: List[str]
    ) -> List[Dict]:
        """
        Compare multiple candidates for a role.

        Args:
            candidates: List of candidate dicts with 'name', 'skills', 'experience_years'
            target_role: Target job role
            target_skills: Required skills for role

        Returns:
            List of analysis results sorted by fit score
        """
        analyses = []

        for candidate in candidates:
            try:
                analysis = self.analyze_candidate(
                    candidate_name=candidate.get("name", "Unknown"),
                    candidate_skills=candidate.get("skills", []),
                    target_role=target_role,
                    target_skills=target_skills,
                    experience_years=candidate.get("experience_years", 0)
                )
                analyses.append(analysis)
            except Exception as e:
                logger.error(
                    f"Error analyzing candidate {candidate.get('name', 'Unknown')}: {e}")
                continue

        # Sort by job fit score
        analyses.sort(key=lambda x: x["job_fit_score"], reverse=True)

        logger.info(f"Compared {len(analyses)} candidates")
        return analyses

    @staticmethod
    def _get_experience_level(years: int) -> str:
        """Determine experience level from years."""
        if years < 2:
            return "Junior"
        elif years < 5:
            return "Mid-level"
        else:
            return "Senior"

    @staticmethod
    def _calculate_readiness(job_fit_score: float) -> str:
        """Determine readiness level from job fit score."""
        if job_fit_score >= 0.8:
            return "Highly Qualified"
        elif job_fit_score >= 0.6:
            return "Well Qualified"
        elif job_fit_score >= 0.4:
            return "Moderately Qualified"
        elif job_fit_score >= 0.2:
            return "Entry Level"
        else:
            return "Needs Development"


class SkillGapReport:
    """Generate formatted skill gap analysis reports."""

    @staticmethod
    def generate_summary(analysis: Dict) -> str:
        """
        Generate text summary of skill gap analysis.

        Args:
            analysis: Analysis result from SkillGapAnalysis

        Returns:
            Formatted text report
        """
        report = []

        report.append("=" * 60)
        report.append("SKILL GAP ANALYSIS REPORT")
        report.append("=" * 60)

        # Candidate info
        candidate = analysis["candidate"]
        report.append(f"\nCandidate: {candidate['name']}")
        report.append(
            f"Experience: {candidate['experience_years']} years ({candidate['experience_level']})")
        report.append(f"Current Skills: {', '.join(candidate['skills'])}")

        # Target role
        report.append(f"\nTarget Role: {analysis['target_role']}")

        # Skill gap summary
        gap = analysis["skill_gap_analysis"]
        report.append(f"\n--- SKILL GAP SUMMARY ---")
        report.append(f"Match Percentage: {gap['match_percentage']}%")
        report.append(f"Job Fit Score: {analysis['job_fit_score']:.2f}")
        report.append(f"Readiness Level: {analysis['readiness_level']}")
        report.append(f"\nMatched Skills ({gap['skill_count']['matched']}):")
        for skill in gap["matched_skills"]:
            report.append(f"  ✓ {skill}")

        report.append(f"\nMissing Skills ({gap['skill_count']['missing']}):")
        for item in analysis["prioritized_missing_skills"]:
            report.append(f"  ✗ {item['skill']} ({item['priority']})")

        # Learning path
        report.append(f"\n--- LEARNING PATH ---")
        path = analysis["learning_path"]
        for step in path:
            report.append(
                f"\nWeek {step['start_week']}-{step['end_week']}: {step['skill']} ({step['level']})")
            report.append(f"  Duration: {step['duration_weeks']} weeks")
            for resource in step.get("resources", []):
                report.append(f"  • {resource}")

        report.append("\n" + "=" * 60)

        return "\n".join(report)

    @staticmethod
    def generate_dataframe(analyses: List[Dict]) -> pd.DataFrame:
        """
        Generate DataFrame from multiple analyses for comparison.

        Args:
            analyses: List of analysis results

        Returns:
            Comparison DataFrame
        """
        rows = []

        for analysis in analyses:
            rows.append({
                "Candidate": analysis["candidate"]["name"],
                "Experience (years)": analysis["candidate"]["experience_years"],
                "Target Role": analysis["target_role"],
                "Match %": analysis["skill_gap_analysis"]["match_percentage"],
                "Job Fit Score": analysis["job_fit_score"],
                "Readiness": analysis["readiness_level"],
                "Matched Skills": len(analysis["skill_gap_analysis"]["matched_skills"]),
                "Missing Skills": len(analysis["skill_gap_analysis"]["missing_skills"])
            })

        return pd.DataFrame(rows)


def main():
    """Example usage of skill gap analysis."""

    # Initialize analyzer
    analyzer = SkillGapAnalysis()

    # Example candidate
    candidate = {
        "name": "John Doe",
        "skills": ["Python", "SQL", "Pandas"],
        "experience_years": 3
    }

    # Example target role
    target_role = "Machine Learning Engineer"
    required_skills = ["Python", "SQL", "Pandas",
                       "NumPy", "PyTorch", "TensorFlow", "Statistics"]

    # Analyze
    result = analyzer.analyze_candidate(
        candidate_name=candidate["name"],
        candidate_skills=candidate["skills"],
        target_role=target_role,
        target_skills=required_skills,
        experience_years=candidate["experience_years"]
    )

    # Generate report
    report = SkillGapReport.generate_summary(result)
    print(report)


if __name__ == "__main__":
    main()
