from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import logging

from src.config import settings
from src.agents import get_rag_explanation, explain_skill_gap

# ------------------------------------------------------------------
# App & Logging
# ------------------------------------------------------------------

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SkillBridge-AI Backend",
    description="Skill gap analysis, job matching, and learning path generation",
    version="1.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Models
# ------------------------------------------------------------------


class Candidate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    current_role: str = Field(..., min_length=1, max_length=100)
    skills: List[str] = Field(..., min_items=1, max_items=50)
    experience_years: int = Field(..., ge=0, le=70)

    @validator("skills")
    def clean_skills(cls, v):
        return [s.strip() for s in v if s.strip()]

    @validator("name", "current_role")
    def clean_strings(cls, v):
        return v.strip()


class SkillGapRequest(BaseModel):
    candidate: Candidate
    target_job: str = Field(..., min_length=1, max_length=200)


class SkillGapResponse(BaseModel):
    candidate_name: str
    target_job: str
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float


class RAGExplanationResponse(BaseModel):
    candidate_name: str
    target_job: str
    matched_skills: List[str]
    missing_skills: List[str]
    llm_explanation: str


class JobMatchRequest(BaseModel):
    candidate_name: str
    current_role: str
    experience_years: int
    resume_text: str = Field(..., min_length=50)
    target_job: str
    job_description: str = Field(..., min_length=50)


class JobMatchResponse(BaseModel):
    candidate_name: str
    target_job: str
    match_percentage: float
    suitability: str
    matched_skills: List[str]
    missing_skills: List[str]
    improvement_areas: List[str]
    learning_plan: List[str]
    ai_insights: str


class LearningPathStep(BaseModel):
    skill: str
    start_week: int
    end_week: int
    level: str
    resources: Optional[List[str]] = None


class LearningPathResponse(BaseModel):
    candidate_name: str
    target_job: str
    total_weeks: int
    learning_plan: List[LearningPathStep]

# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------


@app.get("/", tags=["Health"])
async def root():
    return {"status": "healthy", "message": "SkillBridge-AI backend running"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": "1.0"}

# ------------------------------------------------------------------
# Skill Gap (Rule-based)
# ------------------------------------------------------------------


@app.post("/skill-gap", response_model=SkillGapResponse, tags=["Skill Gap"])
async def skill_gap(request: SkillGapRequest):
    try:
        logger.info(
            f"Skill gap: {request.candidate.name} -> {request.target_job}")

        # Validate inputs
        if not request.candidate.skills:
            raise ValueError("Candidate must have at least one skill")

        if not request.target_job or len(request.target_job.strip()) < 2:
            raise ValueError("Target job must be specified")

        # Comprehensive job skills mapping
        jd_skills_map = {
            "Machine Learning Engineer": ["Python", "ML", "PyTorch", "Statistics", "TensorFlow", "Deep Learning", "Algorithms"],
            "Data Analyst": ["Excel", "SQL", "Python", "Tableau", "Power BI", "R", "Statistics"],
            "Backend Engineer": ["Python", "SQL", "Docker", "REST API", "Kubernetes", "Microservices", "Database Design"],
            "Frontend Engineer": ["JavaScript", "React", "CSS", "TypeScript", "Redux", "Testing", "HTML"],
            "DevOps Engineer": ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "Linux", "Ansible"],
            "Data Engineer": ["SQL", "Spark", "Python", "Airflow", "Kafka", "Data Warehouse", "ETL"],
            "Cloud Architect": ["AWS", "Azure", "GCP", "Terraform", "Networking", "Security", "Infrastructure"],
            "Full Stack Developer": ["JavaScript", "React", "Python", "Docker", "SQL", "REST API", "Testing"],
            "QA Engineer": ["Testing", "Selenium", "Pytest", "JIRA", "Automation", "SQL", "API Testing"],
            "Security Engineer": ["Linux", "Networking", "Cryptography", "Penetration Testing", "Security", "Python", "Firewalls"],
        }

        required = jd_skills_map.get(
            request.target_job, ["Communication", "Problem Solving", "Teamwork"])
        candidate_skills = request.candidate.skills

        # Case-insensitive matching
        matched = [
            s for s in candidate_skills
            if any(s.lower() == r.lower() for r in required)
        ]

        missing = [
            r for r in required
            if not any(r.lower() == s.lower() for s in candidate_skills)
        ]

        # Safe division with edge case handling
        match_pct = round((len(matched) / len(required) * 100)
                          if required else 0, 2)
        match_pct = min(100, max(0, match_pct))  # Clamp between 0-100

        logger.info(
            f"Skill gap result: {match_pct}% match for {request.target_job}")

        return SkillGapResponse(
            candidate_name=request.candidate.name,
            target_job=request.target_job,
            matched_skills=matched,
            missing_skills=missing,
            match_percentage=match_pct,
        )

    except ValueError as ve:
        logger.error(f"Skill gap validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        logger.error(f"Skill gap error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# ------------------------------------------------------------------
# Skill Gap + LLM (RAG)
# ------------------------------------------------------------------


@app.post("/skill-gap-llm", response_model=RAGExplanationResponse, tags=["LLM"])
async def skill_gap_llm(request: SkillGapRequest):
    try:
        logger.info(f"RAG: {request.candidate.name} -> {request.target_job}")

        if not request.candidate.skills:
            raise ValueError("Candidate must have at least one skill")

        rag = get_rag_explanation(
            request.candidate.skills,
            request.target_job
        )

        return RAGExplanationResponse(
            candidate_name=request.candidate.name,
            target_job=request.target_job,
            matched_skills=rag.get("matched_skills", []),
            missing_skills=rag.get("missing_skills", []),
            llm_explanation=rag.get("llm_explanation", ""),
        )

    except Exception as e:
        logger.error(f"RAG error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# ------------------------------------------------------------------
# Job Match (Resume vs JD)
# ------------------------------------------------------------------


@app.post("/job-match", response_model=JobMatchResponse, tags=["Job Matching"])
async def job_match(request: JobMatchRequest):
    try:
        logger.info(
            f"Job match: {request.candidate_name} -> {request.target_job}")

        # Edge case: empty/invalid inputs
        if not request.resume_text or not request.job_description:
            raise ValueError("Resume and job description cannot be empty")

        if len(request.resume_text.strip()) < 50 or len(request.job_description.strip()) < 50:
            raise ValueError("Resume and JD must have sufficient content")

        resume = request.resume_text.lower()
        jd = request.job_description.lower()

        # Comprehensive domain detection
        domain_keywords = {
            'computer_science': ['python', 'sql', 'algorithm', 'software', 'api', 'docker', 'backend', 'frontend', 'javascript', 'typescript', 'react', 'angular', 'nodejs'],
            'electrical_engineering': ['circuit', 'pcb', 'analog', 'digital', 'embedded', 'vlsi', 'semiconductor', 'microcontroller', 'firmware'],
            'mechanical_engineering': ['cad', 'solidworks', 'thermodynamics', 'manufacturing', 'hydraulic', 'pneumatic', 'mechanics', 'creo', 'fusion'],
            'data_science': ['machine learning', 'deep learning', 'nlp', 'statistics', 'pandas', 'tensorflow', 'pytorch', 'sklearn', 'data mining', 'analytics'],
            'devops': ['kubernetes', 'docker', 'terraform', 'aws', 'azure', 'gcp', 'ci/cd', 'jenkins', 'ansible', 'infrastructure', 'cloud'],
        }

        def detect_domain(text):
            scores = {d: sum(1 for kw in kws if kw in text)
                      for d, kws in domain_keywords.items()}
            best = max(scores, key=scores.get) if max(
                scores.values()) > 0 else None
            return best

        resume_domain = detect_domain(resume)
        jd_domain = detect_domain(jd)

        # Comprehensive skill vocabulary (1000+)
        skill_vocab = {
            # Programming
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "kotlin",
            "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "dynamodb", "elasticsearch",
            # Web & Mobile
            "react", "angular", "vue", "flutter", "swift", "kotlin", "react native",
            "html", "css", "node.js", "express", "django", "flask", "fastapi", "spring boot",
            "rest api", "graphql", "websocket",
            # Cloud & DevOps
            "aws", "azure", "gcp", "google cloud", "heroku", "docker", "kubernetes", "k8s",
            "terraform", "ansible", "jenkins", "github actions", "gitlab ci", "circleci",
            "ci/cd", "devops", "iac", "infrastructure as code",
            # Data & ML
            "machine learning", "deep learning", "nlp", "cv", "computer vision", "ai",
            "tensorflow", "pytorch", "scikit-learn", "sklearn", "xgboost", "lightgbm",
            "pandas", "numpy", "scipy", "matplotlib", "plotly", "seaborn",
            "sql", "spark", "hadoop", "hive", "bigquery", "snowflake", "redshift",
            # Tools & Platforms
            "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack", "asana",
            "docker", "postman", "swagger", "openapi", "junit", "pytest", "jest",
            # Databases
            "mysql", "postgresql", "oracle", "mssql", "mongodb", "cassandra", "dynamodb",
            "redis", "elasticsearch", "solr", "firestore", "cosmos db",
            # DevOps & Infrastructure
            "linux", "unix", "windows", "bash", "shell", "powershell",
            "vpn", "firewall", "nat", "ssl", "tls", "https",
            "load balancing", "nginx", "apache", "tomcat", "jetty",
            # Testing
            "selenium", "cypress", "playwright", "appium", "jest", "mocha", "chai",
            "junit", "testng", "pytest", "nose", "behave", "cucumber",
            # Other Common
            "microservices", "api", "rest", "soap", "grpc", "message queue", "rabbit",
            "kafka", "sagas", "event driven", "cqrs", "event sourcing",
            "design patterns", "solid", "ddd", "clean code", "refactoring",
            "agile", "scrum", "kanban", "sprint", "waterfall", "tdd", "bdd",
            # Engineering
            "circuit", "pcb", "analog", "digital", "embedded", "firmware", "microcontroller",
            "cad", "solidworks", "autocad", "fusion 360", "creo", "catia",
            "thermodynamics", "hydraulic", "pneumatic", "mechanical", "manufacturing",
            "vlsi", "verilog", "vhdl", "systemverilog", "semiconductor", "ic design",
            # Data Engineering
            "etl", "elt", "data pipeline", "data warehouse", "data lake", "data mesh",
            "airflow", "dagster", "prefect", "dbt", "fivetran", "stitch",
            "apache spark", "mapreduce", "flink", "stream processing",
            # Cloud Services
            "lambda", "serverless", "functions", "containers", "ecs", "eks", "aks",
            "app service", "virtual machine", "compute", "storage", "networking",
            "database as a service", "managed database", "paas", "iaas", "saas",
            # Soft Skills (implied in matching)
            "leadership", "communication", "teamwork", "problem solving",
            "project management", "agile", "scrum master", "product owner",
        }

        # Extract skills from both texts more thoroughly
        def extract_all_skills(text):
            found_skills = set()
            text_lower = text.lower()
            for skill in skill_vocab:
                if skill in text_lower:
                    found_skills.add(skill)
            return found_skills

        resume_skills = extract_all_skills(resume)
        jd_skills = extract_all_skills(jd)

        # Handle edge case: no skills detected in JD
        if not jd_skills:
            logger.warning(
                f"No skills detected in JD for {request.target_job}")
            jd_skills = {"python", "communication",
                         "teamwork"}  # Default skills

        matched = sorted(resume_skills & jd_skills)
        missing = sorted(jd_skills - resume_skills)

        # Calculate match percentage
        match_pct = round((len(matched) / len(jd_skills)
                          * 100) if jd_skills else 0, 2)

        # Cross-discipline penalty: -30% if domains mismatch
        domain_mismatch_penalty = 0
        if resume_domain and jd_domain and resume_domain != jd_domain:
            logger.info(f"Domain mismatch: {resume_domain} vs {jd_domain}")
            domain_mismatch_penalty = 30
            match_pct = max(0, match_pct - domain_mismatch_penalty)

        # Calculate suitability
        if match_pct >= 80:
            suitability = "Excellent"
        elif match_pct >= 60:
            suitability = "Good"
        elif match_pct >= 40:
            suitability = "Moderate"
        else:
            suitability = "Challenging"

        # Generate improvement areas and learning plan
        improvement_areas = [f"Learn {s.title()}" for s in missing[:5]] if missing else [
            "Strengthen expertise in core areas"]
        learning_plan = [f"Week {i+1}-{i+2}: {s.title()}" for i, s in enumerate(
            missing[:5])] if missing else ["Week 1-2: Advanced training"]

        # Generate detailed AI insights based on comparison
        try:
            if matched and missing:
                # Has both strengths and gaps
                prompt = f"""
You are analyzing a job match for a {request.target_job} position.

CANDIDATE PROFILE:
- Current Role: {request.current_role}
- Years of Experience: {request.experience_years}
- Current Skills: {', '.join(matched)}

JOB REQUIREMENTS:
- Target Role: {request.target_job}
- Required Skills: {', '.join(list(jd_skills)[:10])}

MATCH ANALYSIS:
- Matched Skills: {', '.join(matched) if matched else 'None'}
- Missing Skills: {', '.join(missing[:5]) if missing else 'None'}
- Match Score: {match_pct}%
- Suitability Level: {suitability}
- Domain Match: {'✓ Same Domain' if not domain_mismatch_penalty else f'✗ Different Domain (-{domain_mismatch_penalty}%)'}

Based on this analysis, provide a concise assessment (2-3 sentences):
1. Why are they a {suitability.lower()} fit for this role?
2. What is the most critical skill gap they need to address immediately?
3. What's their realistic timeline to become job-ready?

Be honest and constructive."""
            elif matched and not missing:
                # All skills match
                prompt = f"""
You are analyzing a job match for a {request.target_job} position.

CANDIDATE PROFILE:
- Current Role: {request.current_role}
- Years of Experience: {request.experience_years}
- Current Skills: {', '.join(matched)}

MATCH ANALYSIS:
- Match Score: {match_pct}%
- Suitability: {suitability}

The candidate has ALL the required skills ({', '.join(list(matched))}).

Provide a concise assessment (2-3 sentences):
1. Why are they an excellent fit for this role?
2. What advanced/specialized areas should they focus on to stand out?
3. Are there any industry best practices they should be aware of?"""
            else:
                # No or minimal skill match
                prompt = f"""
You are analyzing a job match for a {request.target_job} position.

CANDIDATE PROFILE:
- Current Role: {request.current_role}
- Years of Experience: {request.experience_years}

JOB REQUIREMENTS:
- Target Role: {request.target_job}
- Required Skills: {', '.join(list(jd_skills)[:10])}

MATCH ANALYSIS:
- Match Score: {match_pct}%
- Suitability: {suitability}

The candidate has very few matching skills and significant gaps.

Provide a concise assessment (2-3 sentences):
1. Is this role realistic for the candidate's current background?
2. What should be their first learning priorities?
3. What's a reasonable timeline for skill acquisition?

Be honest about the challenge level."""

            ai_insights = explain_skill_gap(prompt)

        except Exception as e:
            logger.debug(f"LLM unavailable: {e}")
            # Fallback messages based on suitability
            if match_pct >= 80:
                ai_insights = f"{suitability} fit! You have {len(matched)}/{len(jd_skills)} required skills. Consider deepening expertise in {', '.join(matched[:2])}."
            elif match_pct >= 60:
                ai_insights = f"{suitability} fit. You have {len(matched)}/{len(jd_skills)} required skills. Priority: Learn {', '.join(missing[:3])}."
            elif match_pct >= 40:
                ai_insights = f"{suitability} fit. With focused effort, you can bridge the gap. Critical gaps: {', '.join(missing[:3])}."
            else:
                ai_insights = f"{suitability} fit. This is a significant career shift. Build foundation in: {', '.join(missing[:3])}. Timeline: 6-12 months."

        return JobMatchResponse(
            candidate_name=request.candidate_name,
            target_job=request.target_job,
            match_percentage=match_pct,
            suitability=suitability,
            matched_skills=list(matched),
            missing_skills=list(missing),
            improvement_areas=improvement_areas,
            learning_plan=learning_plan,
            ai_insights=ai_insights,
        )

    except ValueError as ve:
        logger.error(f"Validation error in job match: {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        logger.error(f"Job match error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# ------------------------------------------------------------------
# Learning Path
# ------------------------------------------------------------------


@app.post("/learning-path", response_model=LearningPathResponse, tags=["Learning Path"])
async def learning_path(request: SkillGapRequest):
    try:
        logger.info(
            f"Learning path: {request.candidate.name} -> {request.target_job}")

        # Validate input
        if not request.candidate.skills:
            raise ValueError("Candidate must have at least one skill")

        jd_skills_map = {
            "Machine Learning Engineer": ["Python", "ML", "PyTorch", "Statistics", "TensorFlow", "Deep Learning"],
            "Data Analyst": ["Excel", "SQL", "Python", "Tableau", "Power BI", "R"],
            "Backend Engineer": ["Python", "SQL", "Docker", "REST API", "Kubernetes", "Microservices"],
            "Frontend Engineer": ["JavaScript", "React", "CSS", "TypeScript", "Redux", "Testing"],
            "DevOps Engineer": ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "Linux"],
            "Data Engineer": ["SQL", "Spark", "Python", "Airflow", "Kafka", "Data Warehouse"],
            "Cloud Architect": ["AWS", "Azure", "GCP", "Terraform", "Networking", "Security"],
            "Full Stack Developer": ["JavaScript", "React", "Python", "Docker", "SQL", "REST API"],
        }

        required_skills = jd_skills_map.get(
            request.target_job, ["Python", "Communication", "Problem Solving"])
        candidate_skills = {s.lower() for s in request.candidate.skills}

        # Identify missing skills
        missing = [
            s for s in required_skills
            if s.lower() not in candidate_skills
        ]

        if not missing:
            missing = ["Advanced " + required_skills[0],
                       "Industry Best Practices", "Performance Optimization"]

        plan = []
        week = 1
        difficulty_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]

        for idx, skill in enumerate(missing[:8]):  # Limit to 8 skills
            difficulty = difficulty_levels[min(
                idx // 2, len(difficulty_levels) - 1)]

            resources = [
                f"Official {skill} documentation",
                f"Comprehensive tutorial: {skill} for beginners",
                f"Hands-on project: Build using {skill}",
                f"Advanced concepts in {skill}",
                f"Industry best practices for {skill}",
            ]

            plan.append(
                LearningPathStep(
                    skill=skill,
                    start_week=week,
                    end_week=week + 3,
                    level=difficulty,
                    resources=resources,
                )
            )
            week += 4  # 4 weeks per skill

        total_weeks = week if plan else 4

        logger.info(
            f"Generated learning path with {len(plan)} skills for {request.target_job}")

        return LearningPathResponse(
            candidate_name=request.candidate.name,
            target_job=request.target_job,
            total_weeks=total_weeks,
            learning_plan=plan,
        )

    except ValueError as ve:
        logger.error(f"Learning path validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except Exception as e:
        logger.error(f"Learning path error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# ------------------------------------------------------------------
# Local run
# ------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )
