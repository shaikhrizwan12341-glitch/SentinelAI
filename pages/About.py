import streamlit as st

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title=f"About - {APP_NAME}",
    page_icon="ℹ️",
    layout="wide"
)

# Apply global dark glassmorphism theme & dynamic shield watermark
apply_theme()


# =========================================================
# SIDEBAR NAVIGATION & SYSTEM STATUS
# =========================================================

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
        '<div style="color:#94a3b8; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px;">System Status</div>',
        unsafe_allow_html=True
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
        '<div style="color:#94a3b8; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px;">Navigation</div>',
        unsafe_allow_html=True
    )
    st.info("Use the pages menu above to move between modules.")
    st.markdown("---")
    st.caption(f"© 2026 {APP_NAME} · All rights reserved.")


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    """
    <div style="padding: 14px 0 6px 0;">
        <div class="hero-title" style="font-size:38px;">About SentinelAI</div>
        <p class="hero-sub" style="margin-top:6px;">
            Next-generation multilingual threat detection system protecting users against social engineering and phishing attacks.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status Chips Row
st.markdown(
    """
    <div style="display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;">
        <div class="stat-chip">🛡️ Cyber Defense Engine</div>
        <div class="stat-chip">⚡ Real-Time ML Scoring</div>
        <div class="stat-chip">🧠 Explainable AI Intelligence</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ELECTRIFYING PULSING SHIELD COMPONENT
# =========================================================

st.markdown(
    """
    <style>
    @keyframes electric-scan {
        0% {
            left: -30%;
            opacity: 0.2;
        }
        50% {
            opacity: 1;
        }
        100% {
            left: 110%;
            opacity: 0.2;
        }
    }

    @keyframes shield-pulse {
        0% {
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2), inset 0 0 15px rgba(34, 211, 238, 0.1);
        }
        50% {
            box-shadow: 0 0 35px rgba(34, 211, 238, 0.5), inset 0 0 25px rgba(52, 211, 153, 0.25);
        }
        100% {
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.2), inset 0 0 15px rgba(34, 211, 238, 0.1);
        }
    }

    .electric-shield-card {
        position: relative;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(34, 211, 238, 0.35);
        border-radius: 20px;
        padding: 32px;
        overflow: hidden;
        margin-bottom: 28px;
        animation: shield-pulse 4s infinite ease-in-out;
        backdrop-filter: blur(16px);
    }

    .electric-line {
        position: absolute;
        top: 0;
        bottom: 0;
        width: 120px;
        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(34, 211, 238, 0.2) 20%,
            #22d3ee 50%,
            #34d399 70%,
            transparent 100%
        );
        filter: drop-shadow(0 0 12px #22d3ee);
        transform: skewX(-20deg);
        animation: electric-scan 3s infinite linear;
        pointer-events: none;
    }
    </style>

    <div class="electric-shield-card">
        <div class="electric-line"></div>
        <div style="display: flex; align-items: center; gap: 24px; position: relative; z-index: 2;">
            <div style="font-size: 64px; line-height: 1; filter: drop-shadow(0 0 18px rgba(34,211,238,0.6));">
                🛡️
            </div>
            <div>
                <div style="font-size: 22px; font-weight: 800; color: #f8fafc; letter-spacing: -0.5px;">
                    SentinelAI Core Defense Matrix
                </div>
                <div style="font-size: 14px; color: #cbd5e1; margin-top: 6px; max-width: 800px; line-height: 1.6;">
                    An integrated threat analysis platform designed to shield organizations and individuals from malicious vectors across 
                    <b>URLs</b>, <b>Emails</b>, and <b>SMS communications</b> using natural language processing and lexical features.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SYSTEM ARCHITECTURE & FEATURES
# =========================================================

st.markdown('<div style="font-size:18px; font-weight:700; color:#e2e8f0; margin-bottom:14px;">🚀 Built-In Security Features</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        """
        <div class="glass" style="padding:20px; border-radius:14px; height:100%;">
            <div style="font-size:24px; margin-bottom:8px;">🌐</div>
            <div style="font-size:16px; font-weight:700; color:#f8fafc;">URL Inspection</div>
            <p style="font-size:13px; color:#94a3b8; margin-top:6px; line-height:1.5;">
                Extracts over 30 structural and lexical URL parameters, detecting brand anti-spoofing and homograph attacks in real time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with f2:
    st.markdown(
        """
        <div class="glass" style="padding:20px; border-radius:14px; height:100%;">
            <div style="font-size:24px; margin-bottom:8px;">💬</div>
            <div style="font-size:16px; font-weight:700; color:#f8fafc;">NLP Text Analysis</div>
            <p style="font-size:13px; color:#94a3b8; margin-top:6px; line-height:1.5;">
                Evaluates social engineering triggers, urgency signals, and fraudulent request patterns across multilingual content.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with f3:
    st.markdown(
        """
        <div class="glass" style="padding:20px; border-radius:14px; height:100%;">
            <div style="font-size:24px; margin-bottom:8px;">🧠</div>
            <div style="font-size:16px; font-weight:700; color:#f8fafc;">Explainable AI</div>
            <p style="font-size:13px; color:#94a3b8; margin-top:6px; line-height:1.5;">
                Transparent decision reasoning explains <i>why</i> a message or link was flagged, helping analysts verify threats safely.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)


# =========================================================
# TECHNOLOGY STACK
# =========================================================

st.markdown('<div style="font-size:18px; font-weight:700; color:#e2e8f0; margin-bottom:14px;">🛠️ Technology Stack</div>', unsafe_allow_html=True)

tech_stack = [
    ("🐍 Python 3.12", "Core application programming language & backend ecosystem"),
    ("⚡ Streamlit Framework", "High-performance interactive web interface & dashboard engine"),
    ("🤖 Scikit-Learn & ML", "Custom-trained classifier models optimized for rapid feature evaluation"),
    ("🔤 Natural Language Processing", "Advanced text tokenization, vectorization, and urgency detection"),
    ("🧠 Explainable AI (XAI)", "Rule heuristics & model feature importance translation"),
    ("🗄️ SQLite Telemetry DB", "Lightweight, secure audit record and scan telemetry storage")
]

tcol1, tcol2 = st.columns(2)

for idx, (tech, desc) in enumerate(tech_stack):
    target_col = tcol1 if idx % 2 == 0 else tcol2
    with target_col:
        st.markdown(
            f"""
            <div class="glass" style="padding:16px 20px; border-radius:12px; margin-bottom:12px; display:flex; align-items:center; justify-content:space-between;">
                <div>
                    <div style="font-size:14px; font-weight:700; color:#22d3ee;">{tech}</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:2px;">{desc}</div>
                </div>
                <div style="color:#34d399; font-weight:800; font-size:12px;">ACTIVE</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
st.markdown(
    '<p style="color:#64748b;font-size:13px;text-align:center;">'
    'SentinelAI · Built for defensive cyber awareness. Always verify with multiple sources.'
    '</p>',
    unsafe_allow_html=True
)