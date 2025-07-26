import streamlit as st
import google.generativeai as genai
import os

# Get API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Show error if key is missing
if not GOOGLE_API_KEY:
    st.error("❌ API key not configured. Set GOOGLE_API_KEY environment variable.")
    st.stop()  # Halt the app if key is missing

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Import your main app page
from pages.productivity_page import run_productivity

# ---------- Login UI ----------
def login():
    st.title("🔐 Login with your Google API Key")

    password = st.text_input("Enter password", type="password")

    if st.button("Login"):
        if password == GOOGLE_API_KEY:
            st.session_state["logged_in"] = True
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Wrong password")

# ---------- Optional Info Section ----------
def show_info_section():
    with st.expander("📘 How to get a Google API Key and Student Access"):
        st.markdown("""
### ✅ How to Register for a Google API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs under **APIs & Services > Library**
4. Generate a key in **APIs & Services > Credentials**

---

### 🎓 Free Credits for Students (1 Year)
- Apply here: [Student Program](https://cloud.google.com/free/docs/student-credits)
- Or through [GitHub Student Pack](https://education.github.com/pack)

---

### 🔐 Optional: Use Google Login Instead of Password
Check: [Google OAuth2 Guide](https://developers.google.com/identity/protocols/oauth2)
""")

# ---------- Logout Button ----------
def logout():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

# ---------- Session Init ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# ---------- App Flow ----------
if st.session_state["logged_in"]:
    run_productivity()
    logout()
else:
    login()
    show_info_section()
