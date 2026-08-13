import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import matplotlib.pyplot as plt

# Load data
resumes = pd.read_csv('output/parsed_resumes.csv')
jobs = pd.read_csv('output/all_jobs_dataset.csv')

# Select one job description
job_text = jobs.iloc[0]['Description']

results = []

for _, row in resumes.iterrows():
    resume_text = str(row['Resume Text'])

    # TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform([resume_text, job_text])
    tfidf_score = cosine_similarity(matrix[0], matrix[1])[0][0] * 100

    # N-gram
    ngram = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
    matrix2 = ngram.fit_transform([resume_text, job_text])
    ngram_score = cosine_similarity(matrix2[0], matrix2[1])[0][0] * 100

    # Word Embedding
    sentences = [resume_text.split(), job_text.split()]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

    def doc_vector(text):
        words = [w for w in text.split() if w in model.wv]
        if len(words) == 0:
            return np.zeros(100)
        return np.mean(model.wv[words], axis=0)

    rvec = doc_vector(resume_text)
    jvec = doc_vector(job_text)

    embed_score = cosine_similarity([rvec], [jvec])[0][0] * 100

    final_score = (
            0.35 * tfidf_score +
            0.35 * ngram_score +
            0.30 * embed_score
        )

    # normalize to 0–100
    final_score = max(0, min(100, final_score))

    results.append({
        'Resume ID': row['Resume ID'],
        'Candidate': row['Candidate Name'],
        'TF-IDF': round(tfidf_score,2),
        'N-gram': round(ngram_score,2),
        'Embedding': round(embed_score,2),
        'ATS Score': round(final_score,2)
    })

resume_skills = set(str(row['Skills']).lower().split(', '))
job_skills = set(str(jobs.iloc[0]['Skills']).lower().split(', '))

if len(job_skills) > 0:
    skill_score = len(resume_skills & job_skills) / len(job_skills) * 100
else:
    skill_score = 0

final_score = (
    0.30 * tfidf_score +
    0.30 * ngram_score +
    0.20 * embed_score +
    0.20 * skill_score
)
final_score = round(min(100, max(0, final_score)), 2)


result_df = pd.DataFrame(results)
result_df = result_df.sort_values('ATS Score', ascending=False)
result_df['Rank'] = range(1, len(result_df)+1)

result_df.to_csv('ats_scores.csv', index=False)

print(result_df)


# Replace missing candidate names with Resume ID
result_df['Candidate'] = result_df['Candidate'].fillna(result_df['Resume ID'])

# Plot only top 10 candidates for readability
top10 = result_df.head(10)

plt.figure(figsize=(10,5))
plt.bar(top10['Candidate'].astype(str), top10['ATS Score'])
plt.xticks(rotation=45, ha='right')
plt.ylabel('ATS Score (%)')
plt.title('Top 10 Resume ATS Ranking')
plt.tight_layout()
plt.savefig('ats_ranking.png')
plt.show()