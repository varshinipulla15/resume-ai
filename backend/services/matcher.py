from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_match_score(resume_text: str, jd_text: str) -> dict:
    # Vectorize both texts
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])

    # Calculate cosine similarity
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    percentage = round(score * 100, 2)

    # Give a label based on score
    if percentage >= 70:
        label = "Strong Match"
    elif percentage >= 40:
        label = "Moderate Match"
    else:
        label = "Weak Match"

    return {
        "score": percentage,
        "label": label
    }