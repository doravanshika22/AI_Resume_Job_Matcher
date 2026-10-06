import streamlit as st

from resume_parser import extract_resume_text
from analyzer import (
    extract_skills,
    calculate_resume_score,
    generate_suggestions
)
from matcher import (
    calculate_match,
    skill_match
)


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .score-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background-color: #f0f2f6;
        margin: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    '<div class="main-title">🤖 AI Resume Analyzer & Job Matcher</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume and find out how well it matches a job.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Choose an option",
    [
        "Resume Analyzer",
        "Job Matcher",
        "About Project"
    ]
)


# ============================================================
# RESUME ANALYZER
# ============================================================

if page == "Resume Analyzer":

    st.header("📄 Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        file_path = "uploaded_resume"

        if uploaded_file.name.lower().endswith(".pdf"):
            file_path += ".pdf"
        else:
            file_path += ".docx"

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        resume_text = extract_resume_text(file_path)

        if not resume_text.strip():

            st.error(
                "Unable to extract text from this resume."
            )

        else:

            st.success(
                "Resume uploaded and analyzed successfully!"
            )

            # -----------------------------
            # Extract skills
            # -----------------------------

            skills = extract_skills(resume_text)

            # -----------------------------
            # Resume score
            # -----------------------------

            score = calculate_resume_score(
                resume_text,
                skills
            )

            st.subheader("📊 Resume Score")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Overall Score",
                    f"{score}/100"
                )

            with col2:

                st.metric(
                    "Skills Found",
                    len(skills)
                )

            with col3:

                st.metric(
                    "Words",
                    len(resume_text.split())
                )

            st.progress(score / 100)

            # -----------------------------
            # Skills
            # -----------------------------

            st.subheader("🛠️ Skills Detected")

            if skills:

                skill_text = " • ".join(
                    skill.title()
                    for skill in skills
                )

                st.info(skill_text)

            else:

                st.warning(
                    "No predefined technical skills were detected."
                )

            # -----------------------------
            # Suggestions
            # -----------------------------

            st.subheader("💡 Improvement Suggestions")

            suggestions = generate_suggestions(
                resume_text,
                skills
            )

            for suggestion in suggestions:

                st.write(
                    "✅ " + suggestion
                )

            # -----------------------------
            # Resume text
            # -----------------------------

            with st.expander("📃 View Extracted Resume Text"):

                st.text_area(
                    "Resume Content",
                    resume_text,
                    height=400
                )


# ============================================================
# JOB MATCHER
# ============================================================

elif page == "Job Matcher":

    st.header("🎯 AI Job Matcher")

    st.write(
        "Upload your resume and enter a job description "
        "to calculate the match."
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="job_resume"
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=300,
        placeholder=(
            "Example:\n"
            "We are looking for a Python Developer "
            "with experience in SQL, Machine Learning, "
            "Pandas, Git and Flask..."
        )
    )

    if uploaded_file and job_description.strip():

        file_path = "job_resume"

        if uploaded_file.name.lower().endswith(".pdf"):
            file_path += ".pdf"
        else:
            file_path += ".docx"

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        resume_text = extract_resume_text(
            file_path
        )

        if not resume_text.strip():

            st.error(
                "Could not extract text from the resume."
            )

        else:

            match_percentage = calculate_match(
                resume_text,
                job_description
            )

            matched_skills, missing_skills = skill_match(
                resume_text,
                job_description
            )

            st.subheader("📊 Job Match Result")

            st.metric(
                "Match Percentage",
                f"{match_percentage}%"
            )

            st.progress(
                min(match_percentage / 100, 1.0)
            )

            # -----------------------------
            # Matched skills
            # -----------------------------

            st.subheader("✅ Matching Skills")

            if matched_skills:

                for skill in matched_skills:

                    st.write(
                        f"🟢 {skill.title()}"
                    )

            else:

                st.warning(
                    "No matching predefined skills found."
                )

            # -----------------------------
            # Missing skills
            # -----------------------------

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.write(
                        f"🔴 {skill.title()}"
                    )

            else:

                st.success(
                    "Excellent! No predefined skills are missing."
                )

            # -----------------------------
            # Recommendation
            # -----------------------------

            st.subheader("💡 Recommendation")

            if match_percentage >= 80:

                st.success(
                    "Excellent match! Your resume is highly "
                    "relevant to this job."
                )

            elif match_percentage >= 60:

                st.info(
                    "Good match. Adding the missing skills "
                    "could improve your chances."
                )

            elif match_percentage >= 40:

                st.warning(
                    "Moderate match. Consider improving your "
                    "skills and tailoring your resume."
                )

            else:

                st.error(
                    "Low match. This job may require skills "
                    "that are currently missing from your resume."
                )


# ============================================================
# ABOUT
# ============================================================

elif page == "About Project":

    st.header("ℹ️ About the Project")

    st.write(
        """
        ### AI Resume Analyzer & Job Matcher

        This project uses Natural Language Processing (NLP)
        techniques to analyze resumes and compare them with
        job descriptions.

        ### Main Features

        - 📄 Resume PDF/DOCX extraction
        - 🤖 AI-style resume analysis
        - 📊 Resume scoring
        - 🛠️ Skill extraction
        - 🎯 Job matching
        - ✅ Matching skill detection
        - ❌ Missing skill detection
        - 💡 Resume improvement suggestions

        ### Technologies Used

        - Python
        - Streamlit
        - NLP
        - TF-IDF
        - Cosine Similarity
        - Scikit-learn
        - PyPDF
        - python-docx
        """
    )