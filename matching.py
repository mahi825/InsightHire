"""
matching.py

Compares a candidate's resume text against a job description (JD) text
and returns a similarity score using sentence embeddings + cosine similarity.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_match_score(resume_text, jd_text):
    """
    Calculate how well a resume matches a job description.

    Parameters
    ----------
    resume_text : str
        The full resume text (skills, experience, etc.)
    jd_text : str
        The full job description text.

    Returns
    -------
    float
        A similarity score between 0.0 and 1.0
        (1.0 = perfect match, 0.0 = completely unrelated).
        Returns 0.0 if either input is empty/invalid.
    """
    if not resume_text or not jd_text:
        return 0.0

    if not isinstance(resume_text, str) or not isinstance(jd_text, str):
        return 0.0

    resume_embedding = _model.encode(resume_text)
    jd_embedding = _model.encode(jd_text)

    score = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    score = float(max(0.0, min(1.0, score)))

    return score
