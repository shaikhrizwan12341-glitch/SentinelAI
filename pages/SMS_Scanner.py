import streamlit as st

st.set_page_config(
    page_title="SMS Scanner",
    page_icon="💬",
    layout="wide"
)

st.title("💬 SMS Scanner")

sms = st.text_area("Paste SMS")

if st.button("Scan SMS"):
    st.success("SMS scanning feature coming soon.")