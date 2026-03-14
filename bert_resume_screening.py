import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# -------------------------------
# Step 1: Load Resume Dataset
# -------------------------------

data = pd.read_csv("Resume.csv")

# Ensure correct column name
resumes = data["Resume_str"]

# -------------------------------
# Step 2: Text Preprocessing
# -------------------------------

def clean_text(text):

    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


resumes_clean = resumes.apply(clean_text)

# -------------------------------
# Step 3: Load BERT Model
# -------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert resumes to embeddings
resume_embeddings = model.encode(resumes_clean.tolist())

# -------------------------------
# Step 4: Input Job Description
# -------------------------------

job_description = input("\nEnter Job Description:\n")

job_description = clean_text(job_description)

job_embedding = model.encode([job_description])

# -------------------------------
# Step 5: Similarity Computation
# -------------------------------

similarity_scores = cosine_similarity(job_embedding, resume_embeddings)

data["Similarity Score"] = similarity_scores[0]

# -------------------------------
# Step 6: Candidate Ranking
# -------------------------------

ranked_candidates = data.sort_values(
    by="Similarity Score",
    ascending=False
)

top_candidates = ranked_candidates.head(10)

print("\nTop Matching Candidates\n")

print(top_candidates[["Category", "Similarity Score"]])

# -------------------------------
# Step 7: Visualization
# -------------------------------

plt.figure()

plt.bar(
    top_candidates["Category"],
    top_candidates["Similarity Score"]
)

plt.xticks(rotation=45)

plt.title("Top 10 Resume Matches")

plt.xlabel("Candidate Category")

plt.ylabel("Similarity Score")

plt.tight_layout()

plt.show()