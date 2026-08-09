import streamlit as st

from utils.predict_sms import predict_sms
from utils.explanation import explain_sms
from database.database import save_scan

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title=f"SMS Scanner - {APP_NAME}",
    page_icon="💬",
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
        <div class="hero-title" style="font-size:38px;">SMS Scanner</div>
        <p class="hero-sub" style="margin-top:6px;">
            AI-powered Smishing detection engine to analyze suspicious text messages, spoofed sender IDs, and malicious links.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status Chips Row
st.markdown(
    """
    <div style="display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;">
        <div class="stat-chip">📱 Smishing Detection</div>
        <div class="stat-chip">⚡ Real-Time NLP Analysis</div>
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
        <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:6px;">💬 Message Threat Inspection</div>
        <div style="font-size:13px; color:#64748b; margin-bottom:16px;">
            Paste the suspicious SMS content below to inspect language vectors, social engineering urgency, and embedded links.
        </div>
    """,
    unsafe_allow_html=True
)

sms = st.text_area(
    "Paste SMS",
    height=160,
    placeholder="Paste the SMS message here...",
    label_visibility="collapsed"
)

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
scan_button = st.button("📱 Scan SMS Now", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# SCAN EXECUTION & RESULTS
# =========================================================

if scan_button:
    if not sms.strip():
        st.warning("⚠️ Please paste an SMS message to perform analysis.")
    else:
        with st.spinner("🤖 SentinelAI is analyzing message patterns and calculating threat risk..."):
            result = predict_sms(sms)

        # Save scan result to DB
        save_scan(
            "SMS",
            sms,
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
        status_text = "Safe SMS Verified" if is_safe else "Potential Phishing SMS Detected"
        desc_text = (
            "SentinelAI found no suspicious manipulation tactics, urgent psychological triggers, or scam patterns in this message."
            if is_safe else
            "High threat risk detected based on natural language analysis, social engineering indicators, or malicious intent context."
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
            summary, reasons = explain_sms(sms, result)
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
    unsafe_allow_html=True,
)