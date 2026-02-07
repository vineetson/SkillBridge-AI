import os

# Define the folder structure
project_name = "SkillBridge-AI"

folders = [
    f"{project_name}/data/raw",
    f"{project_name}/data/processed",
    f"{project_name}/notebooks",
    f"{project_name}/src",
    f"{project_name}/app/backend",
    f"{project_name}/app/frontend",
    f"{project_name}/models",
    f"{project_name}/docs",
    f"{project_name}/tests"
]

# Define placeholder files to create
files = [
    f"{project_name}/src/preprocessing.py",
    f"{project_name}/src/ml_model.py",
    f"{project_name}/src/skill_gap.py",
    f"{project_name}/src/rag_pipeline.py",
    f"{project_name}/src/agents.py",
    f"{project_name}/app/backend/main.py",
    f"{project_name}/app/frontend/streamlit_app.py",
    f"{project_name}/requirements.txt",
    f"{project_name}/README.md"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

# Create empty files
for file in files:
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("")  # leave empty for now
        print(f"Created file: {file}")
