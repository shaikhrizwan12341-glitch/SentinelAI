from database.database import create_database
import streamlit as st

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS, MODEL_ACCURACY

# Create database and tables if they don't exist
create_database()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
)

# Global theme: dark glassmorphism + animated shield watermark
apply_theme()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div class="sb-logo">
            <div class="badge">🛡️</div>
            <div>
                <div class="sb-title">{APP_NAME}</div>
                <div class="sb-version">v{APP_VERSION} · CYBER DEFENSE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown(
        '<div class="sb-section-label">System Status</div>',
        unsafe_allow_html=True,
    )
    for label, value in SYSTEM_STATUS.items():
        is_green = "🟢" in value
        dot_color = "#34d399" if is_green else "#f87171"
        clean = value.replace("🟢", "").replace("🔴", "").strip()
        st.markdown(
            f"""
            <div class="sb-status-row glass-flat">
                <span><span class="dot" style="color:{dot_color};background:{dot_color};"></span>{label}</span>
                <span style="color:{dot_color};font-weight:600;">{clean}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        '<div class="sb-section-label">Navigation</div>',
        unsafe_allow_html=True,
    )
    st.info("Use the pages menu above to move between modules.")

    st.markdown("---")
    st.caption("© 2025 SentinelAI · All rights reserved.")

# -----------------------------
# Main Page
# -----------------------------
st.markdown(
    f"""
    <div style="padding: 18px 0 8px 0;">
        <div class="hero-title">{APP_NAME}</div>
        <p class="hero-sub">
            AI-Powered Multilingual Phishing Detection Platform. Scan URLs, emails,
            and SMS messages in real time and get an explainable confidence score
            for every threat.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin: 6px 0 26px 0;">
        <span class="stat-chip">🧠 Model Accuracy · <b style="color:#22d3ee">{MODEL_ACCURACY}</b></span>
        <span class="stat-chip">⚡ Real-Time Scan</span>
        <span class="stat-chip">🌐 Multilingual NLP</span>
        <span class="stat-chip">📜 Full Scan History</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sb-section-label" style="margin-top:8px;">Core Modules</div>',
    unsafe_allow_html=True,
)

features = [
    ("🔗", "URL Scanner", "Detect malicious links and phishing domains using lexical and host-based features."),
    ("📧", "Email Scanner", "Analyze email content and headers for phishing signals with NLP models."),
    ("💬", "SMS Scanner", "Flag smishing attempts in text messages across multiple languages."),
    ("📊", "Dashboard", "Track threat distribution, totals, and recent activity at a glance."),
    ("📜", "Scan History", "Review every past scan with verdicts, confidence, and timestamps."),
    ("🧠", "Explainable AI", "Understand why a scan was flagged with confidence-driven insights."),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="glass feature-card">
                <div class="ic">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.markdown(
    '<p style="color:#64748b;font-size:13px;text-align:center;">'
    'SentinelAI · Built for defensive cyber awareness. Always verify with multiple sources.'
    '</p>',
    unsafe_allow_html=True,
)
