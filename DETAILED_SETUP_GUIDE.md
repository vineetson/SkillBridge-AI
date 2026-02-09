# SkillBridge-AI - Complete & Super Detailed Setup Guide

**Last Updated:** February 8, 2026
**Status:** Production Ready ✅
**Tested On:** Windows 10/11, Python 3.9+

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Setup Checklist](#pre-setup-checklist)
3. [Installation (Step-by-Step)](#installation-step-by-step)
4. [Running the Application](#running-the-application)
5. [Using the Application](#using-the-application)
6. [API Reference](#api-reference)
7. [Comprehensive Troubleshooting](#comprehensive-troubleshooting)
8. [Tips &amp; Best Practices](#tips--best-practices)
9. [Project Structure](#project-structure)
10. [FAQ](#faq)

---

## System Requirements

### Minimum Requirements

- **OS:** Windows 10/11, macOS 10.14+, or Linux
- **Python:** 3.9, 3.10, 3.11, or 3.12
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 2.5GB (for Python packages and ML models)
- **Internet:** Required for first-time model downloads (~500MB)

### Verify Your Python Version

Open Command Prompt and run:

```bash
python --version
```

**Expected output:**

```
Python 3.10.5
```

**Don't have Python?** [Download from python.org](https://www.python.org/downloads/)

---

## Pre-Setup Checklist

Before you start, verify:

- [ ] Python 3.9+ installed (`python --version`)
- [ ] You have internet connection (models download ~500MB)
- [ ] At least 2.5GB free disk space
- [ ] No other services on ports 8000 or 8501
- [ ] Command Prompt/PowerShell access
- [ ] Optional: Administrator access (may help)

---

## Installation (Step-by-Step)

### 🟢 Phase 1: Prepare Your Environment

#### Step 1.1: Open Command Prompt/PowerShell

**On Windows:**

1. Press `Win + R`
2. Type `cmd` or `powershell`
3. Press Enter

You should see:

```
C:\Users\YourUsername>
```

#### Step 1.2: Navigate to Project Directory

```bash
cd c:\Users\ac\Desktop\SkillBridge-AI
```

**Verify correct directory:**

```bash
dir
```

You should see folders:

```
📁 app          📁 tests
📁 data         📁 models
📁 src          📄 requirements.txt
📄 config.yaml  📄 SETUP_GUIDE.md
```

---

### 🟢 Phase 2: Create Virtual Environment

Virtual environments isolate project packages from your system Python.

#### Step 2.1: Create Virtual Environment

```bash
python -m venv venv
```

**What happens:**

- Creates a `venv` folder
- Sets up clean Python environment inside
- Takes ~10-30 seconds

**You should see a new `venv` folder:**

```
📁 venv/         (newly created)
  📁 Scripts/
  📁 Lib/
  📁 Include/
```

#### Step 2.2: Activate Virtual Environment

**Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

If you get execution policy error in PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Type 'Y' and press Enter
# Then run activation again: venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Success indicator:**
Your command prompt now shows `(venv)` prefix:

```
(venv) C:\Users\ac\Desktop\SkillBridge-AI>
```

**⚠️ IMPORTANT:** Keep this activated throughout all steps!

---

### 🟢 Phase 3: Install Dependencies

#### Step 3.1: Upgrade pip

```bash
python -m pip install --upgrade pip
```

Expected output:

```
Successfully installed pip-23.3.1
```

#### Step 3.2: Install Requirements

```bash
pip install -r requirements.txt
```

**⏱️ Timing:**

- Downloading packages: 1-2 minutes
- Installing packages: 2-4 minutes
- **Total: 3-5 minutes**

**Progress indication:**
You'll see packages installing one by one:

```
Collecting fastapi==0.104.1
Collecting streamlit==1.29.0
Collecting torch==2.1.1
...
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 streamlit-1.29.0 ... (40+ packages)
```

**Success indicator:**

```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 streamlit-1.29.0 pydantic-2.5.0 ... [40+ packages]
```

#### Step 3.3: Verify Installation

Verify all packages installed:

```bash
python -c "import fastapi, streamlit, transformers, torch; print('✅ All packages installed successfully!')"
```

Expected output:

```
✅ All packages installed successfully!
```

**If verification fails:**

```bash
# Reinstall with verbose output:
pip install -r requirements.txt --verbose
```

---

### 🟢 Phase 4: (Optional) Install Development Tools

For running tests:

```bash
pip install -r requirements-dev.txt
```

Installs:

- pytest (testing framework)
- black (code formatter)
- flake8 (linter)

---

## Running the Application

### 🏗️ Architecture Overview

```
User Browser (http://localhost:8501)
        ↓
  [Streamlit Frontend]
        ↓ HTTP Requests
        ↓
  [FastAPI Backend] (http://localhost:8000)
        ↓
  [ML Core Modules]
  - ml_model.py (skill matching)
  - skill_gap.py (analysis)
  - agents.py (LLM reasoning)
  - rag_pipeline.py (context retrieval)
```

### 🖥️ Terminal Setup

You need **minimum 2 terminals**:

- **Terminal 1:** Backend API (port 8000)
- **Terminal 2:** Frontend UI (port 8501)
- **(Optional) Terminal 3:** Tests/Monitoring

---

### Step-by-Step Execution

#### Step 1: Prepare Terminal 1 (Backend)

**Open first terminal/cmd and run:**

```bash
cd c:\Users\ac\Desktop\SkillBridge-AI
```

**Verify you're in right place:**

```bash
cd
# Should show: C:\Users\ac\Desktop\SkillBridge-AI
```

**Activate virtual environment:**

```bash
venv\Scripts\activate
```

**Verify activation:**

```bash
# Should show (venv) prefix
echo %VIRTUAL_ENV%
# Should show path to venv folder
```

---

#### Step 2: Start Backend API

**In Terminal 1, run:**

```bash
python -m uvicorn app.backend.main:app --reload --port 8000
```

**First run takes 15-30 seconds** (loading models)

**Expected output:**

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**✅ Backend is running!**

**Keep Terminal 1 open** - backend must stay running

---

#### Step 3: Open Terminal 2 (Frontend)

**Open NEW Command Prompt/PowerShell window**

1. Press `Win + R` → Type `cmd` → Enter
2. Navigate: `cd c:\Users\ac\Desktop\SkillBridge-AI`
3. Activate virtual env: `venv\Scripts\activate`

**Verify:**

```
(venv) C:\Users\ac\Desktop\SkillBridge-AI>
```

---

#### Step 4: Start Frontend

**In Terminal 2, run:**

```bash
streamlit run app/frontend/streamlit_app.py
```

**Expected output:**

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

**✅ Frontend is running!**

---

#### Step 5: Open Application in Browser

**Open web browser and go to:**

```
http://localhost:8501
```

You should see the SkillBridge-AI interface:

```
═══════════════════════════════════════════════════════════
              🧠 SkillBridge-AI
  Analyze skill gaps, generate learning paths, and get
  AI-guided explanations for career growth.
═══════════════════════════════════════════════════════════

👤 Candidate Profile
├─ Candidate Name: [________________]
├─ Current Role: [________________]
└─ Years of Experience: [===●===] 3

📄 Skills Input
├─ [Tab: Upload Resume (PDF)]
└─ [Tab: Manual Skills Entry]

🎯 Target Job
└─ Target Job Role: [Machine Learning Engineer________]

📊 Analysis
├─ [🔍 Analyze Skill Gap]
├─ [📚 Generate Learning Path]
└─ [💡 Get AI Explanation]
```

**🎉 Application is ready to use!**

---

## Using the Application

### Complete Workflow Example

**Scenario:** Transition from Backend Developer to ML Engineer

---

#### Step 1: Enter Candidate Information

**Input:**

```
Candidate Name: John Doe
Current Role: Backend Developer
Years of Experience: 3 (use slider)
```

---

#### Step 2: Provide Skills

**Option A: Upload Resume (PDF)**

1. Click "📄 Upload Resume (PDF)"
2. Select a PDF file
3. System extracts skills automatically

**What you see:**

```
✅ PDF parsed successfully

Extracted Resume Text:
"Senior Python developer with 3 years experience
in REST APIs, Docker containerization, SQL design..."

📌 Extracted 8 potential skills

Selected Skills (8):
[Python] [SQL] [Docker] [REST APIs] [Git] [AWS] [Linux] [Node.js]
```

**Option B: Manual Entry**

1. Click "Manual Skills Entry" tab
2. Enter skills (comma or newline separated):
   ```
   Python, SQL, Docker
   REST APIs, Git
   AWS
   ```

Skills appear as chips:

```
[Python] [SQL] [Docker]
[REST APIs] [Git] [AWS]
```

---

#### Step 3: Select Target Job

Enter target role:

```
Target Job Role: Machine Learning Engineer
```

---

#### Step 4: Click Analysis Buttons

### Button 1️⃣: 🔍 Analyze Skill Gap

**Click:** "🔍 Analyze Skill Gap"

**Status:** `🔄 Analyzing skill gap...` (1-2 seconds)

**Results displayed:**

```
✅ Analysis complete!

┌──────────────────────────────────────┐
│ Matched Skills │ Missing Skills │ Match % │
│       4        │       6        │  40%   │
└──────────────────────────────────────┘

[📊 Bar Chart: 40% match]

✅ Matched Skills (4)
   • Python
   • SQL
   • Docker
   • REST APIs

❌ Missing Skills (6)
   • Machine Learning
   • Deep Learning
   • PyTorch
   • TensorFlow
   • Statistics
   • NumPy/Pandas
```

---

### Button 2️⃣: 📚 Generate Learning Path

**Click:** "📚 Generate Learning Path"

**Status:** `📚 Generating learning path...` (1-2 seconds)

**Results displayed:**

```
✅ Learning path created!

📊 Total Duration: 14 weeks

[📈 Timeline Chart showing weekly progression]

📋 Learning Steps

▶ Week 1: Machine Learning (Beginner)
  Duration: 2 weeks
  Resources:
    • Udemy course on Machine Learning
    • Official ML documentation
    • Free online tutorials
    • Practice projects

▶ Week 3: Deep Learning (Beginner)
  Duration: 2 weeks
  Resources:
    • (similar resources)

▶ Week 5: PyTorch (Intermediate)
  Duration: 3 weeks
  Resources:
    • Udemy course on PyTorch
    • Advanced projects in PyTorch
    • (other resources)

▶ Week 8: TensorFlow (Advanced)
  Duration: 4 weeks
  Resources:
    • (resources)
    • Contribute to open-source
    • Research papers
```

---

### Button 3️⃣: 💡 Get AI Explanation

**Click:** "💡 Get AI Explanation"

**Status:** `💭 Generating AI explanation...` (3-5 seconds on first call, 1-2 on subsequent)

**Results displayed:**

```
✅ AI analysis ready!

📚 Retrieved Job Context
  [Expandable section showing retrieved job descriptions]

  Context 1: "The ML Engineer role requires strong programming
  skills in Python, familiarity with PyTorch and TensorFlow..."

  Context 2: "We seek candidates with statistics background..."

🎯 Key Skills to Develop
  [Machine Learning] [Deep Learning] [Statistics]

💡 AI Reasoning

Based on your background as a Backend Developer with 3 years
of experience and Python/SQL/Docker skills:

**Your Strengths:**
✓ Python expertise is excellent foundation
✓ REST API knowledge for ML model serving
✓ Docker skills for ML deployment
✓ SQL for data handling

**Skills You Need to Learn:**

1️⃣ Machine Learning Fundamentals (Weeks 1-2)
   Why: Essential foundation for all ML work
   How: Take Andrew Ng's ML course
   Resources: Coursera (free audit), YouTube tutorials

2️⃣ Deep Learning & Neural Networks (Weeks 3-5)
   Why: Powers modern ML applications
   How: Study backpropagation, CNNs, RNNs
   Resources: Fast.ai, Deep Learning course

3️⃣ PyTorch Framework (Weeks 6-9)
   Why: Industry standard for research
   How: Build models from scratch
   Resources: Official PyTorch tutorials, Kaggle

4️⃣ Statistics & Probability (Weeks 10-14)
   Why: Understand model behavior
   How: Review statistics fundamentals
   Resources: Khan Academy, 3Blue1Brown

**Timeline:** 3-4 months intensive learning

**Success Indicators:**
• Complete ML specialization course
• Build 2-3 projects (MNIST, NLP, CV)
• Contribute to ML open-source
• Achieve 90%+ accuracy on Kaggle dataset
```

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Quick Endpoint Summary

| Method | Endpoint         | Purpose                  |
| ------ | ---------------- | ------------------------ |
| GET    | `/health`        | Check if backend running |
| GET    | `/docs`          | Interactive API docs     |
| POST   | `/skill-gap`     | Analyze skill gap        |
| POST   | `/skill-gap-llm` | LLM explanation          |
| POST   | `/learning-path` | Generate learning path   |

---

### Detailed Endpoint Examples

#### Endpoint 1: GET /health

**Check if backend is running**

```bash
curl http://localhost:8000/health
```

**Response (200 OK):**

```json
{
	"status": "healthy",
	"version": "1.0",
	"backend_url": "http://localhost:8000"
}
```

---

#### Endpoint 2: POST /skill-gap

**Analyze skill gap**

```bash
curl -X POST http://localhost:8000/skill-gap \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "name": "John Doe",
      "current_role": "Backend Developer",
      "skills": ["Python", "SQL", "Docker"],
      "experience_years": 3
    },
    "target_job": "Machine Learning Engineer"
  }'
```

**Response (200 OK):**

```json
{
	"candidate_name": "John Doe",
	"target_job": "Machine Learning Engineer",
	"matched_skills": ["Python", "SQL"],
	"missing_skills": [
		"Machine Learning",
		"Deep Learning",
		"PyTorch",
		"TensorFlow"
	],
	"match_percentage": 33.33
}
```

**Error Response (422 - Invalid Input):**

```json
{
	"detail": [
		{
			"loc": ["body", "candidate", "skills"],
			"msg": "ensure this value has at least 1 items",
			"type": "value_error"
		}
	]
}
```

---

#### Endpoint 3: POST /skill-gap-llm

**Get AI-powered insights**

```bash
curl -X POST http://localhost:8000/skill-gap-llm \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "name": "John Doe",
      "current_role": "Backend Developer",
      "skills": ["Python", "SQL", "Docker"],
      "experience_years": 3
    },
    "target_job": "Machine Learning Engineer"
  }'
```

**Response (200 OK):**

```json
{
	"candidate_name": "John Doe",
	"target_job": "Machine Learning Engineer",
	"matched_skills": ["Python", "SQL"],
	"missing_skills": ["Machine Learning", "Deep Learning"],
	"retrieved_context": [
		"ML Engineer roles require strong Python, PyTorch, TensorFlow...",
		"Deep learning expertise in CNN, RNN architectures..."
	],
	"llm_explanation": "Based on your background as a Backend Developer..."
}
```

---

#### Endpoint 4: POST /learning-path

**Generate learning path**

```bash
curl -X POST http://localhost:8000/learning-path \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "name": "John Doe",
      "current_role": "Backend Developer",
      "skills": ["Python"],
      "experience_years": 3
    },
    "target_job": "Data Scientist"
  }'
```

**Response (200 OK):**

```json
{
	"candidate_name": "John Doe",
	"target_job": "Data Scientist",
	"total_weeks": 14,
	"learning_plan": [
		{
			"skill": "SQL",
			"start_week": 1,
			"end_week": 3,
			"level": "Beginner",
			"resources": [
				"Udemy course on SQL",
				"Official SQL documentation",
				"Practice projects using SQL"
			]
		},
		{
			"skill": "Pandas",
			"start_week": 4,
			"end_week": 7,
			"level": "Intermediate",
			"resources": [
				"Pandas documentation",
				"DataCamp Pandas course",
				"Real data analysis projects"
			]
		}
	]
}
```

---

### Interactive API Docs

**Visit:** `http://localhost:8000/docs`

Shows:

- All endpoints with descriptions
- Try-out feature (execute requests directly)
- Request/response schemas
- Parameter documentation
- Error examples

---

## Comprehensive Troubleshooting

### 🔴 Issue 1: "Port 8000 already in use"

**Error:**

```
ERROR:    [Errno 48] Address already in use
```

**Cause:** Another app using port 8000

**Solution A: Use different port**

```bash
python -m uvicorn app.backend.main:app --reload --port 8001
```

Then update Streamlit's BACKEND_URL:

```python
# In app/frontend/streamlit_app.py, change line 15 from:
BACKEND_URL = "http://localhost:8000"
# To:
BACKEND_URL = "http://localhost:8001"
```

**Solution B: Kill process on port 8000**

Windows:

```bash
netstat -ano | findstr :8000
# Find the PID in last column
taskkill /PID <PID_NUMBER> /F
```

Mac/Linux:

```bash
lsof -ti:8000 | xargs kill -9
```

---

### 🔴 Issue 2: "Port 8501 already in use" (Streamlit)

**Error:**

```
Port 8501 is already in use.
```

**Solution:**

```bash
streamlit run app/frontend/streamlit_app.py --server.port 8502
```

Then visit: `http://localhost:8502`

---

### 🔴 Issue 3: "ModuleNotFoundError: No module named 'torch'"

**Error:**

```
ModuleNotFoundError: No module named 'torch'
```

**Cause:** Installation incomplete

**Solution:**

```bash
# Verify virtual environment is activated (should show (venv) prefix)
# Then reinstall:
pip install -r requirements.txt --force-reinstall --no-cache-dir
```

**⏱️ Takes 5-10 minutes** - be patient

---

### 🔴 Issue 4: Virtual environment won't activate

**Symptom:** No `(venv)` prefix after running activation

**Windows Command Prompt:**

```bash
# Check if script exists:
dir venv\Scripts\activate

# Try different path:
call venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
# Set execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Type 'Y' and press Enter

# Then activate:
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
# Use source command:
source venv/bin/activate

# Should show (venv) prefix now
```

---

### 🔴 Issue 5: "Connection refused" - Can't connect to backend

**Error in Streamlit:**

```
Cannot connect to backend at http://localhost:8000
```

**Checklist:**

- [ ] Terminal 1 still running? (backend should show "Uvicorn running on...")
- [ ] Backend shows no errors?
- [ ] Port 8000 correct in BACKEND_URL?
- [ ] Both using same network?

**Debug:**

```bash
# In new terminal, test backend:
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","version":"1.0","backend_url":"http://localhost:8000"}
```

**If still broken:**

1. Stop both terminals (Ctrl+C)
2. Close browser
3. Start backend again
4. Wait 5 seconds
5. Start frontend again
6. Refresh browser

---

### 🔴 Issue 6: "No such file or directory" - Data missing

**Error:**

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/resumes.csv'
```

**Solution:** Verify data exists

```bash
# Check files exist:
ls data/raw/
ls data/processed/
ls models/embeddings/

# Should show:
# data/raw/resumes.csv
# data/raw/job_descriptions.csv
# models/embeddings/jd_index.faiss
# models/embeddings/jd_metadata.pkl
```

If missing, check with admin/supervisor.

---

### 🔴 Issue 7: Models downloading very slowly

**Symptom:** First API call takes 5-10 minutes

**Why:** Downloading transformer models (~500MB)

**This is NORMAL!** Be patient - first run only.

**To pre-download models:**

```bash
python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; AutoTokenizer.from_pretrained('gpt2'); AutoModelForCausalLM.from_pretrained('gpt2')"
```

Takes 3-5 minutes but only once. Next calls are instant.

---

### 🔴 Issue 8: "Permission denied" on Windows

**Error:**

```
PermissionError: [Errno 13] Permission denied
```

**Solution:**

1. Right-click Command Prompt
2. Select "Run as Administrator"
3. Try commands again

---

### 🟡 Issue 9: Streamlit shows "Updating" forever

**Symptom:** Streamlit page keeps updating, doesn't complete

**Solution:**

```bash
# Stop Streamlit (Ctrl+C in Terminal 2)
# Clear cache:
streamlit cache clear

# Restart:
streamlit run app/frontend/streamlit_app.py
```

---

### 🟡 Issue 10: Python shows "command not found"

**Error:**

```
'python' is not recognized as an internal or external command
```

**Cause:** Python not in system PATH

**Solution:**

1. [Download Python from python.org](https://www.python.org/downloads/)
2. During installation: **CHECK "Add Python to PATH"**
3. Restart Command Prompt
4. Try again: `python --version`

---

## Tips & Best Practices

### ⚡ Performance Tips

1. **First-time model loading is slow**
   - First API call: 30-60 seconds
   - Subsequent: < 1 second
   - This is NORMAL!

2. **Use Chrome or Edge browser**
   - Better Streamlit performance
   - More responsive UI

3. **Upload smaller resumes**
   - < 5MB PDFs work best
   - Manual entry faster for quick testing

4. **Keep both terminals open**
   - Closing Terminal 1 stops backend
   - Closing Terminal 2 stops frontend

5. **Monitor Terminal 1 logs**
   - Shows all API requests
   - Useful for debugging

---

### ✅ Best Practices

1. **Always activate virtual environment first**

   ```bash
   (venv) should appear before command prompt
   ```

2. **Test API before using frontend**

   ```bash
   curl http://localhost:8000/health
   # Should return healthy status
   ```

3. **Use descriptive skill names**
   - ✅ "Machine Learning", "PyTorch", "Docker"
   - ❌ "ML", "pytorch", "containers"

4. **Screenshot results for reference**
   - Save skill gap analysis
   - Track progress over time

5. **Run tests regularly**

   ```bash
   pytest tests/ -v
   # Should show 30+ tests passing
   ```

---

### 🔧 Optimization Commands

**Faster backend startup:**

```bash
python -m uvicorn app.backend.main:app --port 8000 --workers 2
```

**Streamlit performance mode:**

```bash
streamlit run app/frontend/streamlit_app.py --logger.level=warning
```

**Development mode (auto-reload):**

```bash
python -m uvicorn app.backend.main:app --reload --port 8000
```

---

## Project Structure

```
SkillBridge-AI/
├── 📁 app/
│   ├── 📁 backend/
│   │   └── main.py              # FastAPI endpoints
│   └── 📁 frontend/
│       └── streamlit_app.py     # Web interface
│
├── 📁 src/
│   ├── config.py                # Configuration
│   ├── preprocessing.py         # Data preprocessing
│   ├── ml_model.py              # ML utilities
│   ├── skill_gap.py             # Gap analysis
│   ├── agents.py                # LLM agent
│   ├── rag_pipeline.py          # RAG system
│   └── __init__.py
│
├── 📁 data/
│   ├── 📁 raw/
│   │   ├── resumes.csv
│   │   └── job_descriptions.csv
│   └── 📁 processed/
│       ├── resumes_processed.csv
│       ├── job_descriptions_processed.csv
│       └── job_fit_scores.csv
│
├── 📁 models/
│   └── 📁 embeddings/
│       ├── resume_index.faiss
│       ├── jd_index.faiss
│       └── (metadata files)
│
├── 📁 tests/
│   ├── test_ml_model.py
│   ├── test_preprocessing.py
│   ├── test_skill_gap.py
│   └── conftest.py
│
├── 📄 requirements.txt           # Dependencies
├── 📄 requirements-dev.txt       # Dev dependencies
├── 📄 config.yaml               # Settings
├── 📄 SETUP_GUIDE.md            # This file
└── 📄 README.md                 # Overview
```

---

## FAQ

### Q: Do I need to run any setup script?

**A:** No! Just: (1) Install requirements, (2) Start backend, (3) Start frontend, (4) Open browser.

### Q: Can I use just the API without frontend?

**A:** Yes! Run only the backend and call endpoints with curl/Postman.

### Q: Does this work on Mac/Linux?

**A:** Yes! Everything works. Only difference: activation command uses `source venv/bin/activate`

### Q: Do I need a GPU?

**A:** No! Works on CPU. GPU speeds things up but not required.

### Q: How much internet bandwidth?

**A:** ~500MB first time (model download), then minimal (<10MB/session).

### Q: Can multiple users use it simultaneously?

**A:** Yes for API. Frontend is single-user per browser, but API handles multiple concurrent requests.

### Q: How do I update packages?

**A:** Run: `pip install --upgrade -r requirements.txt`

### Q: Can I deploy to production?

**A:** Yes! Use gunicorn for backend, deploy Streamlit separately.

### Q: The first API call is very slow. Why?

**A:** First time downloads LLM models (~500MB) from Hugging Face. Subsequent calls are instant.

### Q: How do I use a different LLM model?

**A:** Edit `src/config.py` and change `LLM_MODEL_NAME` to another model like "facebook/opt-350m"

### Q: What if I only want to run tests?

**A:** Run: `pytest tests/ -v` (tests don't need backend running)

---

## 🎉 You're Ready!

Once everything is running:

1. **Try different career transitions**
2. **Upload your own resume**
3. **Explore API documentation** at `http://localhost:8000/docs`
4. **Run the test suite** to validate
5. **Review code** in `src/` folder
6. **Customize config.yaml** for your needs

---

**Last Updated:** February 8, 2026
**Status:** Production Ready ✅
**Support:** Check IMPROVEMENTS.md for recent changes
