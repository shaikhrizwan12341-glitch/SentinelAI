import streamlit as st

st.set_page_config(
    page_title="Email Scanner",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Email Scanner")

email = st.text_area("Paste Email Content")

if st.button("Scan Email"):
    st.success("Email scanning feature coming soon.")