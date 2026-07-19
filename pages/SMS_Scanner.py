import streamlit as st

from utils.predict_sms import predict_sms
from database.database import save_scan

st.set_page_config(
    page_title="SMS Scanner",
    page_icon="💬",
    layout="wide"
)

st.title("💬 SMS Scanner")

st.write("Scan suspicious SMS messages using the SentinelAI phishing detection engine.")

st.markdown("---")

sms = st.text_area(
    "Paste SMS",
    height=200,
    placeholder="Paste the SMS content here..."
)

if st.button("💬 Scan SMS", use_container_width=True):

    if sms.strip() == "":
        st.warning("Please paste an SMS.")
        st.stop()

    result = predict_sms(sms)

    save_scan(
        "SMS",
        sms,
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
        st.success("🟢 This SMS appears to be safe.")
    else:
        st.error("🔴 Potential phishing SMS detected.")

    st.subheader("📊 AI Confidence")
    st.progress(result["confidence"] / 100)

    with st.expander("📄 Scan Details", expanded=True):

        st.write(f"**Prediction:** {result['prediction']}")
        st.write(f"**Confidence:** {result['confidence']}%")
        st.write(f"**Risk Level:** {result['risk']}")

    with st.expander("🤖 AI Explanation", expanded=True):

        if result["prediction"] == "SAFE":
            st.success("""
The SMS contains very few phishing indicators.

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