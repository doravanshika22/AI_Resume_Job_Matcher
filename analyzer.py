import re


SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "streamlit",
    "react",
    "node.js",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "natural language processing",
    "computer vision",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_resume_score(text, skills):

    score = 0

    text_lower = text.lower()

    # Skill score
    skill_score = min(len(skills) * 3, 30)
    score += skill_score

    # Education
    education_keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "degree",
        "education",
        "computer science",
    ]

    if any(word in text_lower for word in education_keywords):
        score += 15

    # Experience
    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "work experience",
    ]

    if any(word in text_lower for word in experience_keywords):
        score += 15

    # Projects
    if "project" in text_lower or "projects" in text_lower:
        score += 15

    # Contact information
    if re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text):
        score += 10

    # Resume length
    word_count = len(text.split())

    if word_count >= 300:
        score += 15
    elif word_count >= 150:
        score += 10
    else:
        score += 5

    return min(score, 100)


def generate_suggestions(text, skills):

    suggestions = []

    text_lower = text.lower()

    if "project" not in text_lower:
        suggestions.append(
            "Add a Projects section with 2-3 important projects."
        )

    if "experience" not in text_lower and "internship" not in text_lower:
        suggestions.append(
            "Add internship, training, or work experience if available."
        )

    if len(skills) < 5:
        suggestions.append(
            "Add more relevant technical skills to your resume."
        )

    if "github" not in text_lower:
        suggestions.append(
            "Add your GitHub profile or relevant project links."
        )

    if "linkedin" not in text_lower:
        suggestions.append(
            "Add your LinkedIn profile."
        )

    if len(text.split()) < 150:
        suggestions.append(
            "Your resume appears short. Add relevant projects, skills, and achievements."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has a good basic structure. Continue tailoring it for each job."
        )

    return suggestiona