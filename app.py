import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.image(
    "https://img.icons8.com/fluency/96/shield.png",
    width=80
)

st.sidebar.title("SentinelAI")

st.sidebar.markdown("---")

st.sidebar.success("✅ System Status")
st.sidebar.write("AI Engine : Ready")
st.sidebar.write("Database : Offline")
st.sidebar.write("Model : Not Loaded")

st.sidebar.markdown("---")

st.sidebar.info(
    "Select a page from the navigation menu above."
)

# -----------------------------
# Main Page
# -----------------------------
st.title("🛡️ SentinelAI")

st.subheader("AI-Powered Multilingual Phishing Detection Platform")

st.write(
    """
Welcome to SentinelAI!

This platform helps users detect phishing attacks using Artificial Intelligence.

### Features

- 🔗 URL Phishing Detection
- 📧 Email Phishing Detection
- 💬 SMS Phishing Detection
- 📊 AI Confidence Score
- 🧠 Explainable AI
- 📜 Scan History

Use the sidebar to navigate between modules.
"""
)