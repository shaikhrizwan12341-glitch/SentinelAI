import streamlit as st

from utils.predict_email import predict_email
from utils.explanation import explain_email
from database.database import save_scan

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title=f"Email Scanner - {APP_NAME}",
    page_icon="📧",
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
        <div class="hero-title" style="font-size:38px;">Email Scanner</div>
        <p class="hero-sub" style="margin-top:6px;">
            AI-powered email body inspection engine for analyzing spear-phishing, credential harvest vectors, and social engineering language.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status Chips Row
st.markdown(
    """
    <div style="display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;">
        <div class="stat-chip">📧 Email Body Inspection</div>
        <div class="stat-chip">⚡ NLP Threat Analyzer</div>
        <div class="stat-chip">🧠 Explainable AI Enabled</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SCAN INPUT PANEL
# =========================================================

st.markdown(
    """
    <div class="glass" style="padding:24px; border-radius:16px; margin-bottom: 24px;">
        <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:6px;">📧 Content Threat Inspection</div>
        <div style="font-size:13px; color:#64748b; margin-bottom:16px;">
            Paste suspicious email text below to perform NLP semantic analysis, intent classification, and phishing risk scoring.
        </div>
    """,
    unsafe_allow_html=True
)

email = st.text_area(
    "Paste Email Content",
    height=200,
    placeholder="Paste the email content here...",
    label_visibility="collapsed"
)

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
scan_button = st.button("📧 Scan Email Now", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# SCAN EXECUTION & RESULTS
# =========================================================

if scan_button:
    if not email.strip():
        st.warning("⚠️ Please paste an email message to perform analysis.")
    else:
        with st.spinner("🤖 SentinelAI is analyzing email content and evaluating threat risk..."):
            result = predict_email(email)

        # Save scan result to DB
        save_scan(
            "EMAIL",
            email,
            result["prediction"],
            result["confidence"],
            result["risk"]
        )

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

        # ----------------------------
        # Result Banner Card
        # ----------------------------
        is_safe = str(result["prediction"]).upper() == "SAFE"
        border_color = "#34d399" if is_safe else "#f87171"
        bg_color = "rgba(52, 211, 153, 0.08)" if is_safe else "rgba(248, 113, 113, 0.08)"
        icon = "🟢" if is_safe else "🔴"
        status_text = "Safe Email Verified" if is_safe else "Potential Phishing Email Detected"
        desc_text = (
            "SentinelAI detected no malicious indicators, deceptive urgency, or spear-phishing patterns in this content."
            if is_safe else
            "High threat risk detected based on natural language analysis, suspicious requests, or social engineering indicators."
        )

        st.markdown(
            f"""
            <div class="glass" style="padding:20px; border-left: 6px solid {border_color}; background: {bg_color}; border-radius:14px; margin-bottom:24px;">
                <div style="font-size:18px; font-weight:700; color:#f8fafc;">{icon} {status_text}</div>
                <div style="font-size:14px; color:#cbd5e1; margin-top:4px;">{desc_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------
        # Metrics Breakdown
        # ----------------------------
        st.markdown('<div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">📊 Threat Assessment Summary</div>', unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3)

        def _metric_box(col, label, value, color):
            with col:
                st.markdown(
                    f"""
                    <div class="glass" style="padding:18px; border-radius:14px; text-align:center;">
                        <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-bottom:6px;">{label}</div>
                        <div style="font-size:28px; font-weight:800; color:{color};">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        _metric_box(mc1, "Prediction", str(result["prediction"]).upper(), "#34d399" if is_safe else "#f87171")
        _metric_box(mc2, "Confidence", f"{result['confidence']}%", "#22d3ee")
        _metric_box(mc3, "Risk Level", str(result["risk"]).upper(), "#34d399" if is_safe else "#f87171")

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

        # ----------------------------
        # Confidence Score Bar Card
        # ----------------------------
        st.markdown(
            """
            <div class="glass" style="padding:20px; border-radius:14px; margin-bottom:24px;">
                <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">🤖 AI Confidence Score</div>
            """,
            unsafe_allow_html=True
        )

        conf_value = float(result["confidence"])
        st.progress(conf_value / 100.0 if conf_value > 1.0 else conf_value)

        st.markdown(
            f"""
            <div style="padding:6px 0 0 0; text-align:right;">
                <span style="color:#64748b; font-size:13px; font-weight:600;">Overall Model Certainty:</span>
                <span style="color:#22d3ee; font-weight:800; font-size:15px; margin-left:6px;">{result['confidence']}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------
        # Detailed Logs & Explainable AI
        # ----------------------------
        with st.expander("📄 Scan Details", expanded=True):
            st.write(f"**Classification:** `{str(result['prediction']).upper()}`")
            st.write(f"**Confidence Score:** `{result['confidence']}%`")
            st.write(f"**Calculated Risk Level:** `{str(result['risk']).upper()}`")

        try:
            summary, reasons = explain_email(email, result)
            with st.expander("🤖 Explainable AI Decision Reasoning", expanded=True):
                st.write(summary)
                st.markdown("#### Why the AI reached this decision:")
                for reason in reasons:
                    st.write(f"• {reason}")
        except Exception:
            pass


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