import streamlit as st
import validators
from database.database import save_scan
from utils.explanation import explain_url
from utils.predict_v2 import predict_url

st.set_page_config(page_title="URL Scanner", page_icon="🌐", layout="wide")

st.title("🌐 URL Scanner")
st.write("Scan suspicious URLs using the SentinelAI phishing detection engine.")

st.markdown("---")

url = st.text_input("Enter URL", placeholder="https://example.com")

if st.button("🔍 Scan URL", use_container_width=True):

    # Empty input
    if url.strip() == "":
        st.warning("Please enter a URL.")

    # Invalid URL
    elif not validators.url(url):
        st.error("❌ Please enter a valid URL.")

    # Valid URL
    else:
        # Run prediction
        result = predict_url(url)

        # -------------------------------------------------------------
        # Data Normalization for Streamlit UI
        # -------------------------------------------------------------
        prediction = result["prediction"].lower()  # 'phishing' or 'safe'
        confidence_val = result["confidence"]  # e.g., 0.9989 or 0.95

        # Convert confidence to percentage for UI display
        confidence_pct = (
            confidence_val * 100 if confidence_val <= 1.0 else confidence_val
        )

        # Derive Risk Level based on prediction & confidence
        if prediction == "phishing":
            risk = "HIGH" if confidence_pct >= 80 else "MEDIUM"
        else:
            risk = "LOW"

        # Inject normalized keys into result dictionary for database & UI
        result["prediction_display"] = prediction.upper()
        result["confidence_pct"] = round(confidence_pct, 2)
        result["risk"] = risk

        # Save to database
        save_scan(
            "URL",
            url,
            result["prediction_display"],
            result["confidence_pct"],
            result["risk"],
        )

        st.markdown("---")

        # Result Summary Cards
        col1, col2, col3 = st.columns(3)

        col1.metric("Prediction", result["prediction_display"])
        col2.metric("Confidence", f"{result['confidence_pct']}%")
        col3.metric("Risk Level", result["risk"])

        # Alert Banner
        if prediction == "safe":
            st.success("🟢 This URL appears to be safe.")
        else:
            st.error("🔴 Warning! Potential phishing website detected.")

        # Progress Bar (Streamlit expects float between 0.0 and 1.0)
        st.subheader("📊 AI Confidence")
        st.progress(confidence_val if confidence_val <= 1.0 else confidence_val / 100)

        # Scan Details Expander
        with st.expander("📄 Scan Details", expanded=True):
            st.write(f"**URL:** {url}")
            st.write(f"**Prediction:** {result['prediction_display']}")
            st.write(f"**Confidence:** {result['confidence_pct']}%")
            st.write(f"**Risk Level:** {result['risk']}")

        # AI Explanation
        summary, reasons = explain_url(url, result)

        with st.expander("🤖 AI Explanation", expanded=True):
            st.write(summary)
            st.markdown("### Why the AI reached this decision")
            for reason in reasons:
                st.write(f"• {reason}")