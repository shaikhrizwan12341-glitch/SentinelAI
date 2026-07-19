import streamlit as st

from utils.predict_sms import predict_sms
from database.database import save_scan

st.set_page_config(
    page_title="SMS Scanner",
    page_icon="💬",
    layout="wide"
)

st.title("💬 SMS Scanner")

st.write("Scan SMS messages using the SentinelAI phishing detection engine.")

st.markdown("---")

sms = st.text_area(
    "Paste SMS Message",
    placeholder="Paste the SMS content here..."
)

if st.button("🔍 Scan SMS", use_container_width=True):

    # Empty Input
    if sms.strip() == "":
        st.warning("Please enter an SMS message.")

    else:

        # AI Prediction
        result = predict_sms(sms)

        # Save Scan to Database
        save_scan(
            "SMS",
            sms,
            result["prediction"],
            result["confidence"],
            result["risk"]
        )

        st.markdown("---")

        # ----------------------------
        # Result Summary
        # ----------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prediction",
                result["prediction"]
            )

        with col2:
            st.metric(
                "Confidence",
                f"{result['confidence']}%"
            )

        with col3:
            st.metric(
                "Risk",
                result["risk"]
            )

        # ----------------------------
        # Alert Message
        # ----------------------------
        if result["prediction"] == "SAFE":
            st.success("🟢 This SMS appears to be safe.")
        else:
            st.error("🔴 Potential phishing/spam SMS detected.")

        # ----------------------------
        # Confidence Bar
        # ----------------------------
        st.subheader("📊 AI Confidence")
        st.progress(result["confidence"] / 100)

        # ----------------------------
        # Scan Details
        # ----------------------------
        with st.expander("📄 Scan Details", expanded=True):

            st.write(f"**Prediction:** {result['prediction']}")
            st.write(f"**Confidence:** {result['confidence']}%")
            st.write(f"**Risk Level:** {result['risk']}")

            st.write("**SMS Message:**")
            st.code(sms)

        # ----------------------------
        # AI Explanation
        # ----------------------------
        with st.expander("🤖 AI Explanation", expanded=True):

            if result["prediction"] == "SAFE":
                st.success("""
The AI model classified this SMS as legitimate.

• No significant phishing indicators detected
• Normal SMS language
• Low phishing probability
                """)

            else:
                st.error("""
Potential phishing indicators detected.

• Suspicious wording or spam patterns
• High phishing probability
• Avoid clicking unknown links
• Never share OTPs, passwords, or banking details
                """)