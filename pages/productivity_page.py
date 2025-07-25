import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx

from utils.resume_helper import (
    build_resume_prompt,
    grammar_style_fix_prompt,
    company_resume_match_prompt
)
from utils.dev_automation import generate_commit_and_issue
from utils.content_tools import rewrite_content
from utils.calendar_helper import summarize_schedule


def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


def extract_text_from_docx(uploaded_file):
    try:
        doc = docx.Document(uploaded_file)
        full_text = [para.text for para in doc.paragraphs]
        return "\n".join(full_text)
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""


def extract_text(uploaded_file):
    if uploaded_file is None:
        return ""
    file_type = uploaded_file.type
    if file_type == "text/plain":
        try:
            return uploaded_file.getvalue().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading TXT file: {e}")
            return ""
    elif file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    else:
        st.warning("Unsupported file type. Please upload PDF, DOCX, or TXT.")
        return ""


def run_productivity():
    st.set_page_config(page_title="KiroHub", layout="wide", initial_sidebar_state="expanded")
    st.title("📄 Productivity & Workflow Tools")
    st.markdown("""
Build tools that save time, reduce friction, or simplify everyday tasks - for developers or anyone else.
If it boosts your flow, it fits here. Examples: dev workflow automations, resume helpers, content tools, calendar organizers.
""")

    # Sidebar Navigation
    st.sidebar.title("📂 Select a Tool")
    section = st.sidebar.radio(
        "Navigate",
        [
            "🛠️ Resume Helper",
            "⚙️ Dev Automation",
            "📝 Content Rewriter",
            "📅 Calendar Organizer"
        ]
    )

    model = genai.GenerativeModel("gemini-1.5-flash")

    if section == "🛠️ Resume Helper":
        st.header("🛠️ Resume Helper with AI Suggestions")
        subtab = st.radio("Choose an option", [
            "Resume + Job Description Suggestions",
            "Upload Resume for Grammar & Style Fix",
            "Company Desc + Resume Match Check"
        ])

        if subtab == "Resume + Job Description Suggestions":
            st.markdown("""Example:

**Resume**: Experienced software developer with 5 years in Python and AI.

**Job Description**: Looking for a Python developer familiar with AI and ML techniques.
""")
            uploaded_resume = st.file_uploader("Upload your resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
            if uploaded_resume:
                resume_text = extract_text(uploaded_resume)
            else:
                resume_text = st.text_area("Or paste your resume here:", height=180)

            job_desc = st.text_area("Paste the job description here:", height=180)
            if st.button("Get Suggestions"):
                if not resume_text.strip() or not job_desc.strip():
                    st.warning("Both fields are required.")
                else:
                    prompt = build_resume_prompt(resume_text, job_desc)
                    with st.spinner("Analyzing..."):
                        response = model.generate_content(prompt)
                    st.subheader("💡 Suggestions:")
                    st.write(response.text)

        elif subtab == "Upload Resume for Grammar & Style Fix":
            st.markdown("Upload your resume (PDF, DOCX, TXT) or paste text to get grammar and style fixes.")
            uploaded_resume2 = st.file_uploader("Upload your resume here:", type=["pdf", "docx", "txt"])
            if uploaded_resume2:
                resume_text2 = extract_text(uploaded_resume2)
            else:
                resume_text2 = st.text_area("Or paste your resume text here:", height=360)

            if st.button("Fix Grammar & Style"):
                if not resume_text2.strip():
                    st.warning("Please provide your resume text.")
                else:
                    prompt = grammar_style_fix_prompt(resume_text2)
                    with st.spinner("Checking grammar and style..."):
                        response = model.generate_content(prompt)
                    st.subheader("📝 Fixed Resume:")
                    st.write(response.text)

        elif subtab == "Company Desc + Resume Match Check":
            st.markdown("Check if your resume matches the company description / job requirements.")
            company_desc = st.text_area("Paste company/job description here:", height=180)

            uploaded_resume3 = st.file_uploader("Upload your resume here:", type=["pdf", "docx", "txt"])
            if uploaded_resume3:
                resume_text3 = extract_text(uploaded_resume3)
            else:
                resume_text3 = st.text_area("Or paste your resume here:", height=180)

            if st.button("Check Match"):
                if not company_desc.strip() or not resume_text3.strip():
                    st.warning("Both fields are required.")
                else:
                    prompt = company_resume_match_prompt(company_desc, resume_text3)
                    with st.spinner("Checking match..."):
                        response = model.generate_content(prompt)
                    st.subheader("✅ Match Analysis:")
                    st.write(response.text)

    elif section == "⚙️ Dev Automation":
        st.header("⚙️ Generate Dev Commit & GitHub Issue")
        st.markdown("""
**Prompt format examples**:

- *Simple:* Generate a commit message and issue for automating Python tests on AWS using GitHub Actions.
- *Detailed:* Set up CI/CD with GitHub Actions to run automated tests on AWS.
""")
        task = st.text_area("Describe your dev task or bug:")
        if st.button("Generate Dev Artifacts"):
            if task.strip():
                prompt = generate_commit_and_issue(task)
                with st.spinner("Working..."):
                    response = model.generate_content(prompt)
                st.subheader("🔧 Output:")
                st.write(response.text)
            else:
                st.warning("Please enter a task description.")

    elif section == "📝 Content Rewriter":
        st.header("📝 Rewrite Content with AI")
        st.markdown("""Example:

Hi team,  
please find the attached report for Q2.  
thanks,  
John
""")
        content = st.text_area("Paste your content (email, text, etc.):")
        tone = st.selectbox("Select tone", ["Formal", "Friendly", "Persuasive"])
        if st.button("Rewrite Content"):
            if content.strip():
                prompt = rewrite_content(content, tone)
                with st.spinner("Rewriting..."):
                    response = model.generate_content(prompt)
                st.subheader("✏️ Rewritten Content:")
                st.write(response.text)
            else:
                st.warning("Please paste some content.")

    elif section == "📅 Calendar Organizer":
        st.header("📅 Smart Schedule Organizer")
        st.markdown("""Example:

Submit assignment by 25th July  
Doctor appointment on Saturday  
Buy groceries  
23rd July 2025 Job in Oracle  
""")
        schedule = st.text_area("Paste your schedule, tasks, or to-dos:")
        if st.button("Summarize & Prioritize"):
            if schedule.strip():
                prompt = summarize_schedule(schedule)
                with st.spinner("Organizing..."):
                    response = model.generate_content(prompt)
                st.subheader("✅ Prioritized Tasks:")
                st.write(response.text)
            else:
                st.warning("Please provide your schedule or task list.")
