import streamlit as st

st.set_page_config(
    page_title="URL Scanner",
    page_icon="🔗",
    layout="wide"
)

st.title("🔗 URL Scanner")

url = st.text_input("Enter a URL")

if st.button("Scan URL"):
    st.success("Scanning feature will be added soon.")