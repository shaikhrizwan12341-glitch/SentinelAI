import streamlit as st
import pandas as pd

from database.database import (
    filter_scans,
    clear_scan_history,
    get_total_scans,
    get_safe_scans,
    get_phishing_scans
)

st.set_page_config(
    page_title="Scan History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Scan History")

st.markdown("---")

# -----------------------------
# Filters
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    search = st.text_input(
        "🔍 Search",
        placeholder="Search URL, Email or SMS..."
    )

with col2:
    scan_type = st.selectbox(
        "📂 Scan Type",
        ["All", "URL", "EMAIL", "SMS"]
    )

with col3:
    prediction = st.selectbox(
        "🛡 Prediction",
        ["All", "SAFE", "PHISHING"]
    )

st.markdown("---")

# -----------------------------
# Statistics
# -----------------------------

c1, c2, c3 = st.columns(3)

c1.metric("🌐 Total", get_total_scans())
c2.metric("✅ Safe", get_safe_scans())
c3.metric("⚠️ Phishing", get_phishing_scans())

st.markdown("---")

# -----------------------------
# History Table
# -----------------------------

rows = filter_scans(
    search,
    scan_type,
    prediction
)

if rows:

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Scan Type",
            "Content",
            "Prediction",
            "Confidence",
            "Risk",
            "Scanned At"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Export CSV",
        csv,
        "scan_history.csv",
        "text/csv",
        use_container_width=True
    )

else:

    st.info("No matching scans found.")

st.markdown("---")

# -----------------------------
# Clear History
# -----------------------------

if st.button(
    "🗑 Clear Scan History",
    use_container_width=True,
    type="primary"
):

    clear_scan_history()

    st.success("Scan history cleared successfully.")

    st.rerun()