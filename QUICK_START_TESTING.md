# SkillBridge-AI - Quick Testing Guide

## 🚀 Running the Application

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Start the backend
cd app/backend
python main.py

# In another terminal, start the frontend
cd app/frontend
streamlit run streamlit_app.py
```

---

## 📋 Test Cases for Job Matching

### Test Case 1: Cross-Discipline Mismatch (Fixed!)

**Scenario**: CS Grad vs Electrical Engineer role

**Resume Content**:

```
Software Developer with 3 years experience
Skills: Python, Django, React, SQL, Docker, Git, REST API
Experience: Built web applications, microservices architecture
```

**Job Description**:

```
Electrical Engineer - PCB Design
Requirements: Circuit design, PCB layout, VLSI, Microcontroller firmware,
Analog electronics, Oscilloscope, 5+ years experience
```

**Expected Result** (After Optimization):

- ✅ Domain Mismatch Detected: Computer Science vs Electrical Engineering
- ✅ Match: ~0-10% (was incorrectly 100%)
- ✅ Suitability: Challenging ❌
- ✅ AI Insight: "Different domain. This is a significant career shift. Critical gaps: circuit, PCB, embedded systems. Timeline: 12-18 months of focused learning."

---

### Test Case 2: Good Match with Gaps

**Scenario**: Python Dev applying for ML Engineer role

**Resume Content**:

```
Python Developer - 5 years experience
Skills: Python, SQL, Docker, AWS, Git, REST API, Pandas, NumPy
Projects: Data processing pipelines, microservices
```

**Job Description**:

```
Machine Learning Engineer
Requirements: Python, Machine Learning, TensorFlow, PyTorch, Statistics,
Deep Learning, Data Science, Scikit-learn, SQL, AWS
```

**Expected Result**:

- ✅ Match: ~55-65%
- ✅ Suitability: Good ✔️
- ✅ Matched Skills: Python, SQL, Docker, AWS, NumPy, Pandas
- ⚠️ Missing: Machine Learning, TensorFlow, PyTorch, Statistics, Deep Learning
- ✅ AI Insight: "Good fit. You have foundational skills. Critical gaps: machine learning frameworks (TensorFlow, PyTorch) and statistics. Timeline: 3-4 months of focused study."

---

### Test Case 3: Perfect Match

**Scenario**: ML Engineer applying for ML Engineer role

**Resume Content**:

```
Machine Learning Engineer - 6 years experience
Skills: Python, Machine Learning, TensorFlow, PyTorch, Scikit-learn,
Statistics, SQL, AWS, Deep Learning, Pandas, NumPy, Keras
```

**Job Description**:

```
Senior Machine Learning Engineer
Requirements: Python, Machine Learning, TensorFlow, PyTorch, Statistics,
Deep Learning, Scikit-learn, SQL, AWS, Kubernetes
```

**Expected Result**:

- ✅ Match: ~90%+
- ✅ Suitability: Excellent ✅
- ✅ Matched: 11 skills
- ⚠️ Missing: Kubernetes (1 skill)
- ✅ AI Insight: "Excellent fit! You have exceptional skill alignment. Only gap: Kubernetes orchestration. Can be picked up in 2-3 weeks. Ready to apply!"

---

## 🧪 Testing All Endpoints

### 1. Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status": "ok", "version": "1.0"}
```

### 2. Skill Gap Analysis

```bash
curl -X POST http://localhost:8000/skill-gap \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "name": "John Doe",
      "current_role": "Software Developer",
      "skills": ["Python", "SQL", "Docker"],
      "experience_years": 3
    },
    "target_job": "Backend Engineer"
  }'
```

**Expected Response**:

```json
{
	"candidate_name": "John Doe",
	"target_job": "Backend Engineer",
	"matched_skills": ["Python", "SQL", "Docker"],
	"missing_skills": ["REST API", "Kubernetes", "Microservices"],
	"match_percentage": 50.0
}
```

---

### 3. Job Match (Resume vs JD)

```bash
curl -X POST http://localhost:8000/job-match \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "current_role": "Python Developer",
    "experience_years": 4,
    "resume_text": "Expert in Python, Django, React, SQL. Built microservices for 4 years. Strong problem solving skills. Experience with Docker and AWS.",
    "target_job": "Backend Engineer",
    "job_description": "Backend Engineer position requires: Python, Django, SQL, Docker, REST API, Kubernetes, Microservices. 3+ years experience."
  }'
```

**Expected Response**:

```json
{
	"candidate_name": "John Doe",
	"target_job": "Backend Engineer",
	"match_percentage": 75.0,
	"suitability": "Good",
	"matched_skills": ["python", "django", "sql", "docker"],
	"missing_skills": ["rest api", "kubernetes", "microservices"],
	"improvement_areas": [
		"Learn Rest API",
		"Learn Kubernetes",
		"Learn Microservices"
	],
	"learning_plan": [
		"Week 1-4: Rest API",
		"Week 5-8: Kubernetes",
		"Week 9-12: Microservices"
	],
	"ai_insights": "Good fit! You have foundational backend skills. Critical gaps: Kubernetes and microservices architecture. Timeline: 8-10 weeks of focused learning with hands-on projects."
}
```

---

### 4. Learning Path

```bash
curl -X POST http://localhost:8000/learning-path \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "name": "Jane Smith",
      "current_role": "Junior Developer",
      "skills": ["Python", "HTML", "CSS"],
      "experience_years": 1
    },
    "target_job": "Frontend Engineer"
  }'
```

**Expected Response**:

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
      "resources": [...]
    },
    {
      "skill": "React",
      "start_week": 5,
      "end_week": 8,
      "level": "Beginner",
      "resources": [...]
    },
    ...
  ]
}
```

---

## 🎯 Frontend Testing (Streamlit)

### Test Workflow

1. **Enter Candidate Info**
   - Name: "Test Candidate"
   - Current Role: "Software Developer"
   - Experience: 3 years

2. **Upload Resume or Enter Skills**
   - Upload sample resume (PDF)
   - Or manually enter: Python, SQL, Docker, AWS

3. **Enter Target Job**
   - "Backend Engineer"

4. **Paste Job Description**

   ```
   Backend Engineer - 3+ years experience

   Responsibilities:
   - Design and develop scalable REST APIs
   - Build microservices architecture
   - Work with Docker and Kubernetes

   Requirements:
   - Python or Java
   - SQL Database design
   - Docker containerization
   - REST API design
   - Kubernetes orchestration
   - Microservices architecture
   ```

5. **Analyze Job Match**
   - Click "Analyze Job Match with AI"
   - Review tabs:
     - Match Score
     - Areas to Improve
     - Learning Plan
     - AI Insights

---

## ✅ Edge Cases to Test

### 1. Empty Inputs

```bash
# Empty resume_text - should return 422
curl -X POST http://localhost:8000/job-match \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test",
    "current_role": "Dev",
    "experience_years": 1,
    "resume_text": "",
    "target_job": "Engineer",
    "job_description": "Requirements..."
  }'
# Expected: 422 Unprocessable Entity
```

### 2. No Skills Detected

```bash
# Resume with no recognized skills
resume_text: "I am a hardworking professional with excellent communication skills"
# Expected: Match = 0%, with default fallback skills
```

### 3. Unknown Job Role

```bash
# Job role not in mapping
target_job: "Unicorn Wrangler"
# Expected: Uses default skills ["Communication", "Problem Solving", "Teamwork"]
```

### 4. Domain Mismatch

```bash
# CS resume vs Mechanical Engineering job
resume_text: "Python, JavaScript, React, Docker, AWS, REST API"
job_description: "CAD, Solidworks, Thermodynamics, Hydraulics, Manufacturing"
# Expected: ~0% match with -30% domain penalty, Clear explanation
```

### 5. Extreme Experience Years

```bash
experience_years: 0  # Should work (min_value=0)
experience_years: 70  # Should work (max_value=70)
experience_years: 100  # Should fail (validation error)
```

---

## 📊 Performance Testing

### Load Test

```bash
# Test with many concurrent requests
for i in {1..100}; do
  curl -X POST http://localhost:8000/health &
done
wait
```

### Response Time Targets

- `/health`: < 10ms
- `/skill-gap`: < 200ms
- `/job-match` (without LLM): < 300ms
- `/job-match` (with LLM): < 2000ms
- `/learning-path`: < 300ms

---

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
# In src/config.py
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Check Backend Logs

```bash
# Backend console shows:
# Job match: john_doe -> Backend Engineer
# Domain mismatch: computer_science vs electrical_engineering
# Match %: 40%
# LLM unavailable: <error message>
```

### Check Frontend Logs

```bash
# Streamlit console shows:
# Analyzing job match...
# API response: {...}
# Error: Connection refused (if backend not running)
```

---

## 📝 Checklist for Deployment

- [ ] All test cases pass
- [ ] Edge cases handled properly
- [ ] Error messages are clear and actionable
- [ ] LLM fallback works when API unavailable
- [ ] Logging is comprehensive
- [ ] Performance meets targets
- [ ] No syntax errors (run `python -m py_compile app/backend/main.py`)
- [ ] Dependencies installed (`pip freeze` vs requirements.txt)
- [ ] Documentation updated
- [ ] Environment variables set correctly

---

## 🚨 Common Issues & Solutions

### Issue: "Backend not available"

**Solution**:

```bash
# Make sure backend is running
cd app/backend
python main.py
# Should show: Uvicorn running on http://localhost:8000
```

### Issue: "Invalid request" (422 error)

**Solution**: Check that:

- resume_text has at least 50 characters
- job_description has at least 50 characters
- candidate_name is not empty
- All required fields are provided

### Issue: "Match always shows 100%"

**Solution**: Fixed in optimization! Now:

- Detects domain mismatches
- Applies -30% penalty for different domains
- Shows realistic percentages based on skill overlap

### Issue: LLM "Not Found" errors

**Solution**:

```python
# Check if LLM service is available
# If not, fallback messages are used automatically
# Check logs for: "LLM unavailable"
```

---

## 📚 Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Streamlit Docs**: https://docs.streamlit.io/
- **FastAPI Guide**: https://fastapi.tiangolo.com/

---

Generated: Feb 9, 2026
Last Updated: Optimization v2.0
