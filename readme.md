# kirohub

**kirohub** is a Streamlit-based AI productivity suite powered by Google's Gemini API. It brings together useful automation tools for developers and professionals, including:

- Resume tailoring & grammar fix tools
- Developer commit & GitHub issue generator
- Smart content rewriter
- Schedule and task organizer

---

## ✨ Features

- **🛠️ Resume Helper**: Get personalized resume suggestions based on job descriptions, check for grammar/style issues, and analyze resume–job matches.
- **⚙️ Dev Automation**: Generate commit messages and GitHub issues using conventional formats.
- **📝 Content Rewriter**: Rewrite any content (emails, messages, etc.) into a different tone.
- **📅 Calendar Organizer**: Summarize and prioritize your to-dos or calendar entries using AI.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google Generative AI API Key  
  Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Install dependencies

```bash
pip install streamlit google-generativeai PyPDF2 python-docx

kirohub/
│
├── app.py                    # Main app entrypoint
│
├── pages/
│   └── productivity_page.py  # Main page with productivity tools tabs
│
├── utils/
│   ├── resume_helper.py      # Prompt builders for resume features
│   ├── dev_automation.py     # Prompt builder for dev automation
│   ├── content_tools.py      # Prompt builder for content rewriting
│   └── calendar_helper.py    # Prompt builder for schedule summarization
│
└── .streamlit/
    └── config.toml           # Optional: Streamlit configuration for deployment
