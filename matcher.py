from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from analyzer import extract_skills


def calculate_match(resume_text, job_description):

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def skill_match(resume_text, job_description):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    matched = sorted(
        resume_skills.intersection(job_skills)
    )

    missing = sorted(
        job_skills.difference(resume_skills)
    )

    return matched, missing