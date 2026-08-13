import fitz
import pandas as pd
import re
import os
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------

RESUME_FOLDER = "resumes"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# SKILL DATABASE
# -----------------------------

SKILLS_DB = [

    # Programming
    "python", "java", "c", "c++", "c#", "javascript",
    "typescript", "php", "ruby", "go", "rust",

    # Web
    "html", "css", "bootstrap", "tailwind",
    "react", "nextjs", "nodejs", "express",
    "angular", "vue",

    # Database
    "mysql", "postgresql", "mongodb",
    "sqlite", "oracle", "sql",

    # Cloud
    "aws", "azure", "gcp",

    # DevOps
    "docker", "kubernetes", "jenkins",
    "git", "github", "gitlab",

    # AI/ML
    "machine learning",
    "deep learning",
    "tensorflow",
    "keras",
    "pytorch",
    "nlp",
    "computer vision",
    "scikit-learn",

    # Cybersecurity
    "burp suite",
    "wireshark",
    "nmap",
    "metasploit",
    "owasp",
    "sqlmap",
    "ethical hacking",

    # Data
    "power bi",
    "tableau",
    "excel",
    "data analysis",

    # Mobile
    "flutter",
    "android",
    "react native"
]

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------

def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text


# -----------------------------
# NAME EXTRACTION
# -----------------------------

def extract_name(text):

    lines = [x.strip() for x in text.split("\n") if x.strip()]

    for line in lines[:10]:

        if (
            len(line.split()) <= 4
            and not re.search("@", line)
            and not re.search(r"\d", line)
            and len(line) > 3
        ):
            return line

    return ""


# -----------------------------
# EMAIL
# -----------------------------

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else ""


# -----------------------------
# PHONE
# -----------------------------

def extract_phone(text):

    match = re.search(
        r"(\+?\d[\d\s\-]{8,15}\d)",
        text
    )

    return match.group(0) if match else ""


# -----------------------------
# LINKEDIN
# -----------------------------

def extract_linkedin(text):

    match = re.search(
        r"(https?://)?(www\.)?linkedin\.com/[^\s]+",
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else ""


# -----------------------------
# GITHUB
# -----------------------------

def extract_github(text):

    match = re.search(
        r"(https?://)?(www\.)?github\.com/[^\s]+",
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else ""


# -----------------------------
# SKILLS
# -----------------------------

def extract_skills(text):

    text_lower = text.lower()

    found = []

    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found.append(skill)

    return ", ".join(sorted(set(found)))


# -----------------------------
# EDUCATION
# -----------------------------

def extract_education(text):

    education_keywords = [
        "b.e",
        "b.tech",
        "m.tech",
        "bachelor",
        "master",
        "engineering",
        "computer science",
        "computer engineering",
        "information technology",
        "diploma"
    ]

    found = []

    text_lower = text.lower()

    for edu in education_keywords:
        if edu in text_lower:
            found.append(edu)

    return ", ".join(found)


# -----------------------------
# EXPERIENCE
# -----------------------------

def extract_experience(text):

    matches = re.findall(
        r"(\d+)\+?\s*(?:years?|yrs?)",
        text,
        re.IGNORECASE
    )

    if matches:
        return max([int(x) for x in matches])

    months = re.findall(
        r"(\d+)\s*months?",
        text,
        re.IGNORECASE
    )

    if months:
        return round(max([int(x) for x in months]) / 12, 1)

    return 0


# -----------------------------
# PROJECT COUNT
# -----------------------------

def count_projects(text):

    keywords = [
        "project",
        "projects",
        "developed",
        "implemented",
        "built"
    ]

    total = 0

    text_lower = text.lower()

    for word in keywords:
        total += text_lower.count(word)

    return total


# -----------------------------
# MAIN
# -----------------------------

records = []

resume_files = list(Path(RESUME_FOLDER).glob("*.pdf"))

for idx, pdf_file in enumerate(resume_files, start=1):

    text = extract_text_from_pdf(str(pdf_file))

    records.append({

        "Resume ID": f"R{idx:03d}",

        "File Name": pdf_file.name,

        "Candidate Name": extract_name(text),

        "Email": extract_email(text),

        "Phone": extract_phone(text),

        "LinkedIn": extract_linkedin(text),

        "GitHub": extract_github(text),

        "Education": extract_education(text),

        "Experience (Years)": extract_experience(text),

        "Skills": extract_skills(text),

        "Projects Count": count_projects(text),

        "Word Count": len(text.split()),

        "Resume Text": text[:5000]
    })

df = pd.DataFrame(records)

output_file = os.path.join(
    OUTPUT_FOLDER,
    "parsed_resumes.csv"
)

df.to_csv(output_file, index=False)

print(df.head())

print(f"\nProcessed {len(df)} resumes")
print(f"CSV saved to: {output_file}")