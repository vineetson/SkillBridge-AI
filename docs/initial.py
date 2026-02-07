# initial.py
import pandas as pd
import random
from faker import Faker

fake = Faker()
random.seed(42)

# --- Define Industries and Roles ---
industries = {
    "Technology": ["Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer", "DevOps Engineer", "Cloud Engineer", "QA Engineer"],
    "Data": ["Data Analyst", "Data Scientist", "ML Engineer", "Business Analyst", "Data Engineer", "AI Researcher"],
    "Finance": ["Accountant", "Financial Analyst", "Investment Analyst", "Risk Analyst", "Auditor"],
    "Marketing": ["Marketing Manager", "SEO Specialist", "Digital Marketing Analyst", "Content Strategist", "Brand Manager"],
    "Engineering": ["Mechanical Engineer", "Electrical Engineer", "Civil Engineer", "Industrial Engineer", "Automation Engineer", "Robotics Engineer"],
    "Healthcare": ["Nurse", "Clinical Researcher", "Biostatistician", "Medical Data Analyst", "Lab Technician"],
    "Education": ["Teacher", "Professor", "Instructional Designer", "Education Consultant"],
    "Sales": ["Sales Manager", "Account Executive", "Business Development Manager", "Sales Analyst"],
    "Operations": ["Operations Manager", "Project Manager", "Supply Chain Analyst", "Logistics Coordinator"]
}

# --- Define Skills by Industry ---
skills_by_industry = {
    "Technology": ["Python", "Java", "C++", "React", "Node.js", "Git", "Docker", "Kubernetes", "SQL", "Agile", "CI/CD", "Cloud", "Microservices", "Linux"],
    "Data": ["Python", "SQL", "Excel", "Tableau", "PowerBI", "Machine Learning", "Deep Learning", "NLP", "R", "Statistics", "Big Data", "Spark", "Pandas", "TensorFlow", "PyTorch"],
    "Finance": ["Accounting", "Excel", "Financial Analysis", "SQL", "Risk Management", "Investment Modeling", "Budgeting", "Forecasting", "Taxation"],
    "Marketing": ["SEO", "Google Analytics", "Social Media", "Content Marketing", "Excel", "Email Marketing", "PPC", "Brand Management", "Marketing Strategy"],
    "Engineering": ["CAD", "MATLAB", "Robotics", "Project Management", "Python", "C++", "AutoCAD", "SolidWorks", "PLC Programming"],
    "Healthcare": ["Clinical Data Analysis", "Biostatistics", "Python", "Medical Terminology", "Research", "Patient Care", "Healthcare Analytics"],
    "Education": ["Teaching", "Curriculum Design", "Educational Technology", "Python", "Research", "Communication"],
    "Sales": ["CRM", "Negotiation", "Excel", "Business Development", "Presentation Skills", "Sales Strategy", "Lead Generation"],
    "Operations": ["Project Management", "Supply Chain", "Logistics", "Excel", "Lean Six Sigma", "Process Improvement", "Agile"]
}

# --- Education options ---
education_list = ["BSc Computer Science", "BSc Statistics", "BSc IT", "MSc Data Science", "MBA",
                  "BSc Engineering", "MSc Engineering", "BSc Finance", "BSc Marketing", "MSc Biostatistics", "BSc Nursing", "BEd", "PhD"]

# --- Generate 20,000 resumes ---
resumes = []
for _ in range(20000):
    name = fake.name()

    industry = random.choice(list(industries.keys()))
    role = random.choice(industries[industry])

    # Fix for random.sample issue
    skills_list_for_industry = skills_by_industry[industry]
    num_skills = random.randint(3, min(7, len(skills_list_for_industry)))
    skills = random.sample(skills_list_for_industry, num_skills)

    experience = random.randint(1, 20)
    education = random.choice(education_list)

    resume_text = f"{name} with {experience} years experience as {role}. Skills: {', '.join(skills)}. Education: {education}."

    resumes.append({
        "candidate_name": name,
        "resume_text": resume_text,
        "industry": industry,
        "job_role": role,
        "skills": ", ".join(skills),
        "experience_years": experience,
        "education": education
    })

df_resumes = pd.DataFrame(resumes)
df_resumes.to_csv("data/raw/resumes.csv", index=False)
print("✅ 20,000 synthetic resumes created: data/raw/resumes.csv")

# --- Generate 500 diverse job descriptions ---
job_descriptions = []
for _ in range(500):
    industry = random.choice(list(industries.keys()))
    role = random.choice(industries[industry])

    # Fix for random.sample issue
    skills_list_for_industry = skills_by_industry[industry]
    num_skills = random.randint(3, min(7, len(skills_list_for_industry)))
    skills = random.sample(skills_list_for_industry, num_skills)

    experience_required = random.randint(2, 10)

    jd_text = f"{role} role in {industry} requiring skills: {', '.join(skills)} with {experience_required}+ years experience."

    job_descriptions.append({
        "job_title": role,
        "industry": industry,
        "job_description": jd_text,
        "skills_required": ", ".join(skills),
        "experience_required": experience_required
    })

df_jds = pd.DataFrame(job_descriptions)
df_jds.to_csv("data/raw/job_descriptions.csv", index=False)
print("✅ 500 job descriptions created: data/raw/job_descriptions.csv")
