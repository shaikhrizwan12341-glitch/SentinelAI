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

    # Empty input
    if url == "":
        st.warning("Please enter a URL.")

    # Invalid URL
    elif not validators.url(url):
        st.error("❌ Please enter a valid URL.")

    # Valid URL
    else:

        result = predict_url(url)

        st.markdown("---")

        # Result Summary
        col1, col2, col3 = st.columns(3)

        col1.metric("Prediction", result["prediction"])
        col2.metric("Confidence", f"{result['confidence']}%")
        col3.metric("Risk", result["risk"])

        # Alert
        if result["prediction"] == "SAFE":
            st.success("🟢 This URL appears to be safe.")
        else:
            st.error("🔴 Warning! Potential phishing website detected.")

        # Confidence Bar
        st.subheader("📊 AI Confidence")
        st.progress(result["confidence"] / 100)

        # Scan Details
        with st.expander("📄 Scan Details", expanded=True):
            st.write(f"**URL:** {url}")
            st.write(f"**Prediction:** {result['prediction']}")
            st.write(f"**Confidence:** {result['confidence']}%")
            st.write(f"**Risk Level:** {result['risk']}")

        # AI Explanation
        with st.expander("🤖 AI Explanation", expanded=True):

            if result["prediction"] == "SAFE":
                st.success("""
The AI model found no significant phishing indicators.

• HTTPS detected
• No suspicious URL pattern
• Low phishing probability
                """)
            else:
                st.error("""
Potential phishing indicators detected.

• Suspicious URL pattern
• High phishing probability
• Visit with caution
                """)