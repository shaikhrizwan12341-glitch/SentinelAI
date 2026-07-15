from components.charts import threat_distribution_chart
from components.metric_card import metric_card
import streamlit as st

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
# Dashboard Cards
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Total Scans", "0", "🌐")

with col2:
    metric_card("Threats Found", "0", "⚠️", "#dc2626")

with col3:
    metric_card("Safe Scans", "0", "✅", "#16a34a")

with col4:
    metric_card("Model Accuracy", "97.8%", "🤖", "#2563eb")

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