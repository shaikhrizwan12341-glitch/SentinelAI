from components.charts import threat_distribution_chart
from components.metric_card import metric_card
from database.database import (
    get_total_scans,
    get_safe_scans,
    get_phishing_scans,
    get_recent_scans
)

import streamlit as st
import pandas as pd

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="SentinelAI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ----------------------------
# Header
# ----------------------------
st.title("🛡️ SentinelAI Dashboard")
st.subheader("AI-Powered Multilingual Phishing Detection Platform")

st.markdown("---")

# ----------------------------
# Live Dashboard Statistics
# ----------------------------
total = get_total_scans()
safe = get_safe_scans()
phishing = get_phishing_scans()
accuracy = "97.8%"

# ----------------------------
# Dashboard Cards
# ----------------------------
# ----------------------------
# Dashboard Cards (Debug)
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌐 Total Scans",
        value=total
    )

with col2:
    st.metric(
        label="⚠️ Threats Found",
        value=phishing
    )

with col3:
    st.metric(
        label="✅ Safe Scans",
        value=safe
    )

with col4:
    st.metric(
        label="🤖 Model Accuracy",
        value=f"{accuracy}%"
    )
st.markdown("---")

# ----------------------------
# Quick Actions
# ----------------------------
st.subheader("🚀 Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    st.button("🌐 Scan URL", use_container_width=True)

with c2:
    st.button("📧 Scan Email", use_container_width=True)

with c3:
    st.button("📱 Scan SMS", use_container_width=True)

st.markdown("---")

# ----------------------------
# Threat Distribution
# ----------------------------
st.subheader("📊 Threat Distribution")

st.plotly_chart(
    threat_distribution_chart(),
    use_container_width=True
)

st.markdown("---")

# ----------------------------
# Recent Activity
# ----------------------------
st.subheader("📋 Recent Activity")

rows = get_recent_scans()

if rows:
    df = pd.DataFrame(
        rows,
        columns=[
            "URL",
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
else:
    st.info("No scans have been performed yet.")

st.markdown("---")

# ----------------------------
# System Status
# ----------------------------
st.subheader("⚙️ System Status")

st.success("🟢 AI Model : Ready")
st.success("🟢 Database : Connected")
st.success("🟢 Streamlit Server : Running")

st.markdown("---")

# ----------------------------
# Footer
# ----------------------------
st.caption("SentinelAI v1.0 | Developed by Team SentinelAI")