# 🧠 SkillBridge-AI

> **Intelligent Job-Candidate Matching with AI-Powered Skill Gap Analysis & Personalized Learning Paths** || 
> **Note: This Project is still in progress!!**

[![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Key Innovation](#key-innovation)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Technology Stack](#technology-stack)
- [Usage Examples](#usage-examples)
- [Project Status](#project-status)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**SkillBridge-AI** is an intelligent AI-powered platform that bridges the gap between candidates and job opportunities by:

1. **Analyzing Resume-JD Fit** - Compares candidate skills against job requirements using advanced matching algorithms
2. **Identifying Skill Gaps** - Pinpoints exactly what skills are missing with priority levels
3. **Generating Learning Paths** - Creates personalized, phased learning plans with recommended resources
4. **Providing AI Insights** - Offers contextual, honest assessments of career readiness and transition feasibility

### Problem Solved

Traditional job matching is often inaccurate:

- ❌ False positives: Unqualified candidates appear as "100% matches"
- ❌ No cross-discipline detection: CS grad gets false match for Electrical Engineer role
- ❌ Generic feedback: No actionable guidance on what to learn
- ❌ No learning timeline: Candidates don't know how long skill acquisition takes

**SkillBridge-AI** solves these with:

- ✅ Domain-aware matching (-30% penalty for cross-discipline transitions)
- ✅ 1000+ skill vocabulary across 15+ engineering disciplines
- ✅ Context-aware AI insights (3-tier prompting: gaps, perfect match, challenge)
- ✅ Phased learning plans (4-week progressive phases with resources)

---

## ✨ Features

### Core Features

- **Intelligent Job Matching** - Resume vs Job Description analysis with semantic understanding
- **Skill Gap Analysis** - Rule-based and LLM-powered skill identification
- **Domain Detection** - Identifies engineering disciplines and applies cross-discipline penalties
- **Learning Path Generation** - Dynamic, phased learning plans with curated resources
- **AI-Powered Insights** - LLM-generated explanations with graceful fallback mechanisms

### Advanced Features

- **1000+ Skill Vocabulary** - Comprehensive coverage across all tech and engineering disciplines
- **5-Domain Support** - Computer Science, Electrical Engineering, Mechanical Engineering, Data Science, DevOps
- **Cross-Discipline Penalty** - -30% match penalty for career transition scenarios
- **3-Tier LLM Prompting** - Context-aware prompts based on skill gap severity:
  - Tier 1: Has gaps → Focus on critical skills & timeline
  - Tier 2: No gaps → Highlight strengths & advanced areas
  - Tier 3: Minimal match → Honest challenge assessment
- **Graceful Fallback** - Works perfectly even without LLM availability
- **Edge Case Handling** - 20+ edge cases covered with proper error messages
- **Full-Stack Implementation** - FastAPI backend + Streamlit frontend

### UI/UX Features

- **PDF Resume Upload** - Automatic skill extraction from PDF resumes
- **Manual Skill Entry** - Option to manually enter skills
- **Multi-Tab Analysis** - Organized results in 4 tabs (Match Score, Areas to Improve, Learning Plan, AI Insights)
- **Color-Coded Results** - Visual indicators (Green/Blue/Yellow/Red) for suitability levels
- **Interactive Visualizations** - Charts and timelines for learning paths

---

## 🚀 Key Innovation

### Problem: False 100% Matches

**Before Optimization**:

```
Resume: CS grad (Python, Django, React, Docker)
Job: Electrical Engineer (Circuit, PCB, VLSI, Microcontroller)
Result: 100% Match ❌ (WRONG!)
```

**After Optimization**:

```
Resume Domain: Computer Science (detected via keywords)
Job Domain: Electrical Engineering (detected via keywords)
Domain Mismatch: -30% penalty applied ✅
Matched Skills: 0
Missing Skills: Circuit, PCB, VLSI, Microcontroller...
Result: 0% Match with honest assessment (CORRECT!)

AI Insight: "Different domain - this is a significant career shift.
You currently have zero overlapping technical skills. Critical gaps:
foundational electronics, circuit analysis, PCB design.
Timeline: 12-18 months of structured learning."
```

### Algorithm Improvements

1. **Extended Domain Keywords** - Each domain has 10+ identifying keywords
2. **Comprehensive Skill Matching** - 1000+ skills vs old 20 skills
3. **Intelligent Penalty System** - Cross-discipline transitions get -30% penalty
4. **Context-Aware Prompting** - LLM receives full context about skill gaps
5. **Smart Fallback Logic** - Fallback messages are smarter and more helpful

---

## 🏃 Getting Started

### Prerequisites

- Python 3.8+
- pip/conda for package management
- Modern web browser

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/SkillBridge-AI.git
cd SkillBridge-AI
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure settings** (optional)

```bash
# Edit src/config.py to customize API settings
cp src/config.py.example src/config.py  # If example exists
```

### Running the Application

**Start the Backend API**

```bash
cd app/backend
python main.py
# Server runs on http://localhost:8000
# API docs: http://localhost:8000/docs
```

**In another terminal, start the Frontend**

```bash
cd app/frontend
streamlit run streamlit_app.py
# Frontend runs on http://localhost:8501
```

### Quick Test

1. Open frontend at http://localhost:8501
2. Enter your skills or upload a resume
3. Paste a job description
4. Click "Analyze Job Match with AI"
5. Review results in the multi-tab interface

---

## 📁 Project Structure

```
SkillBridge-AI/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── OPTIMIZATIONS.md                   # Detailed optimization breakdown
├── QUICK_START_TESTING.md            # Test cases and examples
├── FINAL_OPTIMIZATION_REPORT.md      # Architecture and innovations
├── COMPLETION_CHECKLIST.md           # Verification checklist
│
├── app/
│   ├── backend/
│   │   └── main.py                   # FastAPI server (558 lines, fully optimized)
│   │       ├── Models: Candidate, SkillGapRequest, JobMatchRequest, etc.
│   │       ├── Endpoints: /health, /skill-gap, /skill-gap-llm, /job-match, /learning-path
│   │       ├── Domain Detection: 5 domains with 8-10 keywords each
│   │       ├── Skill Vocabulary: 1000+ skills across all disciplines
│   │       ├── LLM Integration: 3-tier context-aware prompting
│   │       └── Error Handling: Comprehensive with proper status codes
│   │
│   └── frontend/
│       └── streamlit_app.py           # Streamlit UI (1231 lines)
│           ├── Resume Upload & Skill Extraction (1000+ keyword recognition)
│           ├── Job Description Input
│           ├── Multi-Tab Analysis Interface
│           ├── Error Handling & Validation
│           └── Beautiful Visualizations (Altair charts)
│
├── data/
│   ├── raw/
│   │   ├── job_descriptions.csv       # Sample JDs for testing
│   │   └── resumes.csv                # Sample resumes for testing
│   └── processed/
│
├── src/
│   ├── agents.py                      # LLM & RAG helpers
│   ├── ml_model.py                    # ML utilities
│   ├── preprocessing.py               # Data preprocessing
│   ├── rag_pipeline.py                # RAG pipeline
│   ├── skill_gap.py                   # Skill gap analysis logic
│   └── config.py                      # Configuration settings
│
├── models/                            # Pre-trained models (if any)
├── notebooks/                         # Jupyter notebooks for exploration
└── tests/                             # Unit and integration tests
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Returns API status and version.

### Skill Gap Analysis

```http
POST /skill-gap
Content-Type: application/json

{
  "candidate": {
    "name": "John Doe",
    "current_role": "Software Developer",
    "skills": ["Python", "SQL", "Docker"],
    "experience_years": 3
  },
  "target_job": "Backend Engineer"
}
```

**Response**:

```json
{
	"candidate_name": "John Doe",
	"target_job": "Backend Engineer",
	"matched_skills": ["Python", "SQL", "Docker"],
	"missing_skills": ["REST API", "Kubernetes", "Microservices"],
	"match_percentage": 50.0
}
```

### Job Match Analysis

```http
POST /job-match
Content-Type: application/json

{
  "candidate_name": "John Doe",
  "current_role": "Python Developer",
  "experience_years": 4,
  "resume_text": "Expert in Python, Django, React, SQL...",
  "target_job": "Backend Engineer",
  "job_description": "Backend Engineer: Python, Django, SQL, Docker, REST API..."
}
```

**Response**:

```json
{
	"candidate_name": "John Doe",
	"target_job": "Backend Engineer",
	"match_percentage": 75.0,
	"suitability": "Good",
	"matched_skills": ["python", "django", "sql", "docker"],
	"missing_skills": ["rest api", "kubernetes"],
	"improvement_areas": ["Learn REST API", "Learn Kubernetes"],
	"learning_plan": ["Week 1-4: REST API", "Week 5-8: Kubernetes"],
	"ai_insights": "Good fit! Critical gaps: Kubernetes and microservices. Timeline: 8-10 weeks."
}
```

### Learning Path

```http
POST /learning-path
Content-Type: application/json

{
  "candidate": {
    "name": "Jane Smith",
    "current_role": "Junior Developer",
    "skills": ["Python", "HTML", "CSS"],
    "experience_years": 1
  },
  "target_job": "Frontend Engineer"
}
```

**Response**:

```json
{
  "candidate_name": "Jane Smith",
  "target_job": "Frontend Engineer",
  "total_weeks": 24,
  "learning_plan": [
    {
      "skill": "JavaScript",
      "start_week": 1,
      "end_week": 4,
      "level": "Beginner",
      "resources": ["Official documentation", "Tutorial", "Project", ...]
    }
  ]
}
```

### Skill Gap with LLM Explanation

```http
POST /skill-gap-llm
Content-Type: application/json

{
  "candidate": {...},
  "target_job": "..."
}
```

See [API Documentation](http://localhost:8000/docs) for interactive Swagger UI.

---

## 💻 Technology Stack

### Backend

- **FastAPI** - Modern web framework for building APIs
- **Pydantic** - Data validation using Python type hints
- **Python 3.8+** - Core language

### Frontend

- **Streamlit** - Rapid UI development framework
- **Pandas** - Data manipulation and analysis
- **Altair** - Declarative visualization
- **pdfplumber** - PDF text extraction

### AI/ML Components

- **sentence-transformers** - Semantic similarity (optional)
- **LLM Integration** - Support for LLM-based explanations (OpenAI, Anthropic, etc.)
- **RAG Pipeline** - Retrieval-Augmented Generation for contextual insights

### Deployment Ready

- **Docker** support (Dockerfile can be added)
- **CORS Middleware** - Cross-origin request handling
- **Error Handling** - Comprehensive logging and error management

---

## 📖 Usage Examples

### Example 1: Career Transition Analysis

```python
# Frontend: Upload resume (CS grad), paste Electrical Engineer JD
# Backend processes:
# - Domain Detection: CS → Electrical Engineering
# - Applies -30% penalty
# - Result: 0% match (not 100%!)
# - AI Insight: "Significant career shift needed..."
```

### Example 2: Skill Gap Identification

```python
# Input: Python dev wanting to become ML Engineer
# Output:
# - Matched: Python, SQL, basic statistics
# - Missing: TensorFlow, PyTorch, Deep Learning
# - Timeline: 3-4 months with focused learning
```

### Example 3: Learning Path Generation

```python
# Input: Junior frontend dev aiming for full-stack
# Output: 24-week learning plan
# Week 1-4: Backend fundamentals
# Week 5-8: Database design
# Week 9-12: API development
# etc.
```

---

## 📊 Project Status

### ✅ Completed (v2.0)

- [x] Job matching with domain detection
- [x] 1000+ skill vocabulary
- [x] 3-tier LLM prompting
- [x] Learning path generation
- [x] Edge case handling (20+ cases)
- [x] Comprehensive documentation
- [x] Full-stack implementation
- [x] Error handling with fallbacks

### 🔄 In Progress

- [ ] Machine Learning model for resume parsing
- [ ] Advanced NLP for skill extraction
- [ ] Real-time job market data integration
- [ ] Skill prerequisite graphs
- [ ] Salary prediction based on skills
- [ ] Peer benchmarking features
- [ ] Resume optimization suggestions

### 🚀 Planned (Future Releases)

- [ ] Mobile app (React Native)
- [ ] Real-time job board integration
- [ ] Industry-specific algorithms
- [ ] Certification recommendations
- [ ] Mentorship matching
- [ ] Interview prep guidance
- [ ] Company-specific insights
- [ ] Competitive analysis dashboard

---

## 📈 Improvements & Roadmap

### v2.0 Optimizations (Current)

- **Domain Detection** - 5 domains with cross-discipline penalties
- **Extended Skills** - 1000+ keywords (was 20)
- **Smart Prompting** - 3-tier context-aware LLM integration
- **Better Fallbacks** - LLM-free operation with smart defaults
- **Edge Cases** - 20+ scenarios covered

### v2.1 (Next Release)

- [ ] Fuzzy skill matching (handle "reactjs" vs "react")
- [ ] Experience-weighted scoring
- [ ] Resume structure parsing
- [ ] Improved PDF text extraction

### v3.0 (Q2-Q3 2026)

- [ ] Machine Learning models for accuracy
- [ ] Semantic embeddings for skill matching
- [ ] Integration with real job boards
- [ ] Advanced analytics and reporting

### v4.0 (Future)

- [ ] Multi-language support
- [ ] Mobile applications
- [ ] Employer dashboard
- [ ] Certification marketplace

---

## 🧪 Testing

### Unit Tests

```bash
# Run tests (when available)
pytest tests/ -v
```

### Manual Testing

See [QUICK_START_TESTING.md](QUICK_START_TESTING.md) for:

- 5 comprehensive test scenarios
- Cross-discipline mismatch test
- API endpoint examples
- Edge case testing
- Performance benchmarks

### Test Cases

1. **Cross-Discipline Mismatch** - Validates domain detection
2. **Good Match with Gaps** - Tests partial skill overlap
3. **Perfect Match** - All skills present scenario
4. **No Skill Match** - Challenging fit detection
5. **Domain-Specific Skills** - Engineering discipline matching

---

## 📚 Documentation

### Main Documentation

- **[OPTIMIZATIONS.md](OPTIMIZATIONS.md)** - Detailed optimization breakdown
- **[QUICK_START_TESTING.md](QUICK_START_TESTING.md)** - Test cases and examples
- **[FINAL_OPTIMIZATION_REPORT.md](FINAL_OPTIMIZATION_REPORT.md)** - Architecture & innovations
- **[COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md)** - Verification checklist

### API Documentation

- **Swagger UI** - http://localhost:8000/docs (when running)
- **ReDoc** - http://localhost:8000/redoc

### Code Documentation

- Inline comments throughout codebase
- Type hints for all functions
- Pydantic model documentation
- Endpoint descriptions

---

## 🔍 Key Algorithms

### Domain Detection Algorithm

```
For each domain (CS, EE, ME, DS, DevOps):
  Score = count of keywords found in text
Pick domain with highest score
If no keywords found, return None
```

### Skill Matching Algorithm

```
For each skill in vocabulary:
  If skill found in resume AND in JD requirements:
    Add to matched_skills
  If skill required but not in resume:
    Add to missing_skills
match_percentage = matched / required * 100
If domains mismatch:
  match_percentage -= 30 (penalty)
```

### LLM Prompt Selection

```
If matched > 0 AND missing > 0:
  Use Tier 1: Focus on gaps (most common)
Else if missing == 0:
  Use Tier 2: Perfect match scenario
Else:
  Use Tier 3: Challenge assessment
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas for Contribution

- Add more job roles and skill mappings
- Improve ML models
- Expand engineering discipline support
- Add test cases
- Enhance documentation
- UI/UX improvements
- Performance optimization

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints for all functions
- Write docstrings for modules and functions
- Include test cases for new features
- Update documentation

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Developed by**: Vineet Soni & Contributors

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- Streamlit for the amazing UI framework
- Contributors and beta testers
- Open source community

---

## 📞 Support & Feedback

- **Issues**: Report bugs in GitHub Issues
- **Discussions**: Start discussions for feature requests
- **Email**: vs.iiitmg@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/vin-soni/

---

## ⭐ Show Your Support

If you find this project helpful, please:

- ⭐ Give it a star on GitHub
- 🔄 Share it with others
- 💬 Provide feedback and suggestions
- 🚀 Contribute to the project

---

## 📰 News & Updates

**Latest Updates (Feb 9, 2026)**

- v2.0 released with major optimizations
- Fixed false 100% match issue
- Added 1000+ skill vocabulary
- Implemented 3-tier LLM prompting
- Comprehensive error handling
- Full documentation

**Follow for Updates**: Star this repository to stay updated!

---

**Last Updated**: February 9, 2026
**Version**: 2.0 (Production-Ready)
**Status**: ✅ In Active Development & Continuous Improvement
