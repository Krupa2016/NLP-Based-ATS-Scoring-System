import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# ---------------- Skill Dictionary ---------------- #
SKILLS = [
    # Tech
    "Python", "Java", "C++", "SQL", "MySQL", "PostgreSQL",
    "Django", "Flask", "FastAPI", "React", "Node.js",
    "AWS", "Docker", "Kubernetes", "Git", "TensorFlow",
    "Pandas", "NumPy", "Machine Learning", "REST API",

    # Sales & Marketing
    "Sales", "Lead Generation", "CRM", "Salesforce",
    "Digital Marketing", "SEO", "Content Marketing",

    # HR
    "Recruitment", "Talent Acquisition", "HR", "Onboarding",

    # Support
    "Customer Support", "Technical Support", "Troubleshooting",
    "Communication", "Documentation",

    # Business
    "Excel", "Power BI", "Finance", "Accounting",
    "Project Management"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

all_jobs = []

# ---------------- Python.org Tech Jobs ---------------- #
python_url = "https://www.python.org/jobs/"

response = requests.get(python_url, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

for li in soup.select("ol.list-recent-jobs li"):
    title = li.find("h2").get_text(strip=True)

    company = ""
    company_tag = li.find("span", class_="listing-company-name")
    if company_tag:
        company = company_tag.get_text(strip=True)

    location = ""
    location_tag = li.find("span", class_="listing-location")
    if location_tag:
        location = location_tag.get_text(strip=True)

    description = li.get_text(separator=" ", strip=True)

    found_skills = [s for s in SKILLS if s.lower() in description.lower()]

    exp_match = re.search(r"(\d+\+?\s*(?:years?|yrs?))", description, re.I)
    experience = exp_match.group(1) if exp_match else ""

    all_jobs.append({
        "Source": "Python.org",
        "Job Title": title,
        "Company": company,
        "Location": location,
        "Category": "Tech",
        "Skills": ", ".join(found_skills),
        "Experience": experience,
        "Description": description,
        "URL": python_url
    })

# ---------------- Remotive Mixed Jobs ---------------- #
remotive_url = "https://remotive.com/api/remote-jobs"

response = requests.get(remotive_url)
data = response.json()

for job in data["jobs"][:100]:
    description = re.sub("<.*?>", " ", job["description"])

    found_skills = [s for s in SKILLS if s.lower() in description.lower()]

    exp_match = re.search(r"(\d+\+?\s*(?:years?|yrs?))", description, re.I)
    experience = exp_match.group(1) if exp_match else ""

    all_jobs.append({
        "Source": "Remotive",
        "Job Title": job["title"],
        "Company": job["company_name"],
        "Location": job["candidate_required_location"],
        "Category": job["category"],
        "Skills": ", ".join(found_skills),
        "Experience": experience,
        "Description": description,
        "URL": job["url"]
    })

# ---------------- Save Combined Dataset ---------------- #
df = pd.DataFrame(all_jobs)

df.to_csv("all_jobs_dataset.csv", index=False)

print(df.head())
print(f"Total jobs collected: {len(df)}")
print(f"Saved to: all_jobs_dataset.csv")