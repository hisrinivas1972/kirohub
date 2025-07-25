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
    st.title("📄 Productivity & Workflow Tools")

    st.markdown("""
Build tools that save time, reduce friction, or simplify everyday tasks - for developers or anyone else.
If it boosts your flow, it fits here. Examples: dev workflow automations, resume helpers, content tools, calendar organizers.
""")

# Sidebar menu
st.sidebar.title("📂 Tools")
section = st.sidebar.radio(
    "Select a tool:",
    [
        "🛠️ Resume Helper",
        "⚙️ Dev Automation",
        "📝 Content Rewriter",
        "📅 Calendar Organizer"
    ]
)

    model = genai.GenerativeModel("gemini-1.5-flash")

    # Resume Helper Tab
    with tab1:
        st.header("🛠️ Resume Helper with AI Suggestions")
        subtab1, subtab2, subtab3 = st.tabs([
            "Resume + Job Description Suggestions",
            "Upload Resume for Grammar & Style Fix",
            "Company Desc + Resume Match Check"
        ])

        # 1. Resume + Job Description Suggestions
        with subtab1:
            st.markdown("""
Example:

Resume:
Experienced software developer with 5 years in Python and AI.

Job Description:
Looking for a Python developer familiar with AI and ML techniques.
""")
            uploaded_resume = st.file_uploader("Upload your resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="upload_res1")
            if uploaded_resume:
                resume_text = extract_text(uploaded_resume)
            else:
                resume_text = st.text_area("Or paste your resume here:", height=180, key="res1")

            job_desc = st.text_area("Paste the job description here:", height=180, key="job1")
            if st.button("Get Suggestions", key="btn1"):
                if not resume_text.strip() or not job_desc.strip():
                    st.warning("Both fields are required.")
                else:
                    prompt = build_resume_prompt(resume_text, job_desc)
                    with st.spinner("Analyzing..."):
                        response = model.generate_content(prompt)
                    st.subheader("💡 Suggestions:")
                    st.write(response.text)

        # 2. Upload Resume for Grammar & Style Fix
        with subtab2:
            st.markdown("Upload your resume (PDF, DOCX, TXT) or paste text to get grammar and style fixes.")
            uploaded_resume2 = st.file_uploader("Upload your resume here:", type=["pdf", "docx", "txt"], key="upload_res2")
            if uploaded_resume2:
                resume_text2 = extract_text(uploaded_resume2)
            else:
                resume_text2 = st.text_area("Or paste your resume text here:", height=360, key="res2")

            if st.button("Fix Grammar & Style", key="btn2"):
                if not resume_text2.strip():
                    st.warning("Please provide your resume text.")
                else:
                    prompt = grammar_style_fix_prompt(resume_text2)
                    with st.spinner("Checking grammar and style..."):
                        response = model.generate_content(prompt)
                    st.subheader("📝 Fixed Resume:")
                    st.write(response.text)

        # 3. Company Description + Resume Match Check
        with subtab3:
            st.markdown("Check if your resume matches the company description / job requirements.")
            company_desc = st.text_area("Paste company/job description here:", height=180, key="comp5")

            uploaded_resume3 = st.file_uploader("Upload your resume here:", type=["pdf", "docx", "txt"], key="upload_res5")
            if uploaded_resume3:
                resume_text3 = extract_text(uploaded_resume3)
            else:
                resume_text3 = st.text_area("Or paste your resume here:", height=180, key="res5")

            if st.button("Check Match", key="btn5"):
                if not company_desc.strip() or not resume_text3.strip():
                    st.warning("Both fields are required.")
                else:
                    prompt = company_resume_match_prompt(company_desc, resume_text3)
                    with st.spinner("Checking match..."):
                        response = model.generate_content(prompt)
                    st.subheader("✅ Match Analysis:")
                    st.write(response.text)

    # Dev Automation Tab
    with tab2:
        st.header("⚙️ Generate Dev Commit & GitHub Issue")
        st.markdown("""
**Prompt format examples**

- *Simple, keyword-based prompt:*
  Generate a conventional commit message and GitHub issue for automating Python tests on AWS using GitHub Actions for CI/CD.

- *More detailed prompt:*
  Write a conventional commit message and a detailed GitHub issue for setting up a CI/CD pipeline using GitHub Actions to run automated Python tests on AWS infrastructure.

- *Step-wise prompt for detailed issue:*
  Generate a conventional commit message with scope and a GitHub issue including description, checklist, and labels for automating Python testing with GitHub Actions and AWS.
""")
        task = st.text_area("Describe your dev task or bug:", key="dev_task")
        if st.button("Generate Dev Artifacts"):
            if task.strip():
                try:
                    prompt = generate_commit_and_issue(task)
                    with st.spinner("Working..."):
                        response = model.generate_content(prompt)
                    st.subheader("🔧 Output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please enter a task description.")

    # Content Rewriter Tab
    with tab3:
        st.header("📝 Rewrite Content with AI")
        st.markdown("""
Example:

Paste an email or message and choose a tone (Formal, Friendly, Persuasive).

Hi team,

please find the attached report for Q2.

thanks,
John
""")
        content = st.text_area("Paste your content (email, text, etc.):", key="content_text")
        tone = st.selectbox("Select tone", ["Formal", "Friendly", "Persuasive"], key="tone_select")
        if st.button("Rewrite Content"):
            if content.strip():
                try:
                    prompt = rewrite_content(content, tone)
                    with st.spinner("Rewriting..."):
                        response = model.generate_content(prompt)
                    st.subheader("✏️ Rewritten Content:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please paste some content.")

    # Calendar Organizer Tab
    with tab4:
        st.header("📅 Smart Schedule Organizer")
        st.markdown("""
Example:

Paste your tasks or schedule like:

Submit assignment by 25th July  
Doctor appointment on Saturday  
Buy groceries  
23rd July 2025 Job in Oracle  
""")
        schedule = st.text_area("Paste your schedule, tasks, or to-dos:", key="schedule_input")
        if st.button("Summarize & Prioritize"):
            if schedule.strip():
                try:
                    prompt = summarize_schedule(schedule)
                    with st.spinner("Organizing..."):
                        response = model.generate_content(prompt)
                    st.subheader("✅ Prioritized Tasks:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide your schedule or task list.")
