import streamlit as st
import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not configured. Set GOOGLE_API_KEY environment variable.")

from pages.productivity_page import run_productivity

if __name__ == "__main__":
    run_productivity()
