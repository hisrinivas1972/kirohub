def build_resume_prompt(resume_text: str, job_description: str) -> str:
    return (
        f"Given the following resume:\n{resume_text}\n\n"
        f"And the following job description:\n{job_description}\n\n"
        "Provide suggestions on how to improve or tailor the resume "
        "to better match the job description. Include keywords, skills, "
        "and phrasing recommendations."
    )

def grammar_style_fix_prompt(resume_text: str) -> str:
    return (
        f"Check and fix grammar and style for this resume text:\n\n{resume_text}"
    )

def company_resume_match_prompt(company_description: str, resume_text: str) -> str:
    return (
        f"Given this company or job description:\n{company_description}\n\n"
        f"And this resume:\n{resume_text}\n\n"
        "Analyze if the resume matches the description and list matching skills and gaps."
    )
