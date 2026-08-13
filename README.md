# 📜AI-Based Resume Parsing and ATS Scoring System

## Project description

The AI-Based Resume Parsing and ATS Scoring System is an NLP-powered recruitment automation project that extracts structured information from resume PDFs and evaluates their compatibility with job descriptions. The system performs automated resume parsing, skill extraction, experience analysis, and ATS scoring using TF-IDF, N-gram, and Word Embedding-based similarity techniques.

The project demonstrates how Artificial Intelligence and Natural Language Processing can improve candidate screening by reducing manual effort and ranking resumes according to their relevance for a given job role.

## Features

* Resume PDF text extraction
* Candidate information extraction

  * Name
  * Email
  * Education
  * Experience
  * Technical skills

* Job description collection from online sources
* Text preprocessing
* TF-IDF similarity
* N-gram similarity
* Word Embedding similarity
* Skill matching score
* Final ATS compatibility score
* Resume ranking
* CSV report generation
* ATS ranking graph visualization

## Project structure

```
AI-ATS-Scoring/
│
├── resumes/
│   ├── resume1.pdf
│   ├── resume2.pdf
│
├── output/
│   └── parsed_resumes.csv
│
├── ats_scores.csv
├── ats_ranking.png
├── all_jobs_dataset.csv
├── resume_scraper.py
├── jobScrapper.py
├── ats_scoring.py
└── README.md
```

## Workflow

```
Resume PDFs
       │
       ▼
Resume Parser
       │
       ▼
Parsed Resume Dataset
       │
       ▼
Text Preprocessing
       │
       ▼
Feature Extraction
(TF-IDF, N-grams, Embeddings)
       │
       ▼
Cosine Similarity
       │
       ▼
ATS Score Calculation
       │
       ▼
Resume Ranking
```

## Technologies used

* Python 3.11
* Pandas
* Scikit-learn
* Gensim
* PyMuPDF (fitz)
* BeautifulSoup
* Requests
* Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/AI-ATS-Scoring.git
cd AI-ATS-Scoring
```

Install dependencies:

```bash
pip install pandas scikit-learn gensim pymupdf beautifulsoup4 requests matplotlib
```

## Usage

### Step 1: Parse resumes

Place resume PDF files inside the `resumes/` folder.

Run:

```bash
python resume_scraper.py
```

Output:

```
output/parsed_resumes.csv
```

### Step 2: Collect job descriptions

Run:

```bash
python jobScrapper.py
```

Output:

```
all_jobs_dataset.csv
```

### Step 3: Generate ATS scores

Run:

```bash
python ats_scoring.py
```

Outputs:

```
ats_scores.csv
ats_ranking.png
```

## ATS scoring method

The final ATS score is computed using a weighted combination of multiple similarity techniques.

| Technique                 | Weight |
| ------------------------- | ------ |
| TF-IDF similarity         | 30%    |
| N-gram similarity         | 30%    |
| Word Embedding similarity | 20%    |
| Skill matching            | 20%    |

Formula:

```
ATS Score =
0.30 × TF-IDF +
0.30 × N-gram +
0.20 × Embedding +
0.20 × Skill Match
```

## Sample output

| Resume ID | Candidate    | ATS Score | Rank |
| --------- | ------------ | --------- | ---- |
| R020      | John Huber   | 10.15     | 1    |
| R002      | Mia Allen    | 9.48      | 2    |
| R019      | Esther Scott | 7.37      | 3    |

## Output files

### parsed_resumes.csv

Contains extracted candidate information.

### all_jobs_dataset.csv

Contains collected job descriptions.

### ats_scores.csv

Contains similarity scores and ATS ranking.

### ats_ranking.png

Bar chart showing the top-ranked resumes.

## Advantages

* Automated resume screening
* Faster recruitment process
* Reduced manual effort
* Improved skill-based matching
* Candidate ranking
* Scalable ATS implementation

## Future improvements

* BERT / Sentence-BERT embeddings
* Named Entity Recognition (NER)
* Resume section classification
* Job-role recommendation
* Experience-based weighting
* Web dashboard using Streamlit or Flask
* Resume formatting quality analysis

## Applications

* Campus recruitment
* Corporate hiring
* HR automation
* Online job portals
* Resume screening systems

## Author

Krupa

Computer Engineering (AI & Cybersecurity)

This project was developed as an Artificial Intelligence and Machine Learning practical implementation of Resume Parsing and Applicant Tracking System (ATS) scoring using Natural Language Processing techniques.
