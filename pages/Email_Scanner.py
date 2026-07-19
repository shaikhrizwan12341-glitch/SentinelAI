import streamlit as st

from utils.predict_email import predict_email
from database.database import save_scan

st.set_page_config(
    page_title="Email Scanner",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Email Scanner")

st.write("Scan suspicious email content using the SentinelAI phishing detection engine.")

st.markdown("---")

email = st.text_area(
    "Paste Email Content",
    height=250,
    placeholder="Paste the email content here..."
)

if st.button("📧 Scan Email", use_container_width=True):

    if email.strip() == "":
        st.warning("Please paste an email.")
        st.stop()

    result = predict_email(email)

    save_scan(
        "EMAIL",
        email,
        result["prediction"],
        result["confidence"],
        result["risk"]
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    col1.metric("Prediction", result["prediction"])
    col2.metric("Confidence", f"{result['confidence']}%")
    col3.metric("Risk", result["risk"])

    if result["prediction"] == "SAFE":
        st.success("🟢 This email appears to be safe.")
    else:
        st.error("🔴 Potential phishing email detected.")

    st.subheader("📊 AI Confidence")
    st.progress(result["confidence"] / 100)

    with st.expander("📄 Scan Details", expanded=True):

        st.write(f"**Prediction:** {result['prediction']}")
        st.write(f"**Confidence:** {result['confidence']}%")
        st.write(f"**Risk Level:** {result['risk']}")

    with st.expander("🤖 AI Explanation", expanded=True):

        if result["prediction"] == "SAFE":
            st.success("""
The email contains very few phishing indicators.

• No suspicious keywords detected
• Low phishing probability
• Appears legitimate
""")
        else:
            st.error("""
Potential phishing indicators detected.

• Urgent language
• Credential request
• Suspicious keywords
• High phishing probability
""")