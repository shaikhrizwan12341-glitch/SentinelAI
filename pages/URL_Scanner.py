import validators
import streamlit as st
from utils.predict import predict_url

st.set_page_config(
    page_title="URL Scanner",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 URL Scanner")

st.write("Scan suspicious URLs using the SentinelAI phishing detection engine.")

st.markdown("---")

url = st.text_input(
    "Enter URL",
    placeholder="https://example.com"
)

if st.button("🔍 Scan URL", use_container_width=True):

    if url == "":
    st.warning("Please enter a URL.")

elif not validators.url(url):
    st.error("❌ Please enter a valid URL.")
    st.stop()

else:

    result = predict_url(url)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prediction",
                result["prediction"]
            )

        with col2:
            st.metric(
                "Confidence",
                f'{result["confidence"]}%'
            )

        with col3:
            st.metric(
                "Risk Level",
                result["risk"]
            )

        if result["prediction"] == "SAFE":
            st.success("This URL appears to be safe.")
        else:
            st.error("Potential phishing website detected.")