import validators
import streamlit as st

from utils.predict_v2 import predict_url
from database.database import save_scan
from utils.explanation import explain_url

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title=f"URL Scanner - {APP_NAME}",
    page_icon="🌐",
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
        <div class="hero-title" style="font-size:38px;">URL Scanner</div>
        <p class="hero-sub" style="margin-top:6px;">
            AI-powered threat analysis engine for real-time phishing detection, lexical inspection, and brand anti-spoofing.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status Chips Row
st.markdown(
    """
    <div style="display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;">
        <div class="stat-chip">⚡ Real-Time Scan Engine</div>
        <div class="stat-chip">🛡️ Anti-Spoofing Rules</div>
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
        <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:6px;">🔗 URL Threat Inspection</div>
        <div style="font-size:13px; color:#64748b; margin-bottom:16px;">
            Enter any target address to extract lexical features and assess credential harvesting risks.
        </div>
    """,
    unsafe_allow_html=True
)

url = st.text_input(
    "Enter URL",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
scan_button = st.button("🔍 Scan URL Now", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# SCAN EXECUTION & RESULTS
# =========================================================

if scan_button:
    if not url.strip():
        st.warning("⚠️ Please enter a valid URL.")
    elif not validators.url(url):
        st.error("❌ Invalid URL format. Please include a full protocol (e.g., https://).")
    else:
        with st.spinner("🤖 SentinelAI is extracting lexical features and evaluating risk..."):
            result = predict_url(url)

        risk = "Low" if result["prediction"].lower() == "safe" else "High"

        # Save scan result to DB
        save_scan(
            "URL",
            url,
            result["prediction"],
            result["confidence"],
            risk
        )

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

        # ----------------------------
        # Result Banner Card
        # ----------------------------
        is_safe = result["prediction"].lower() == "safe"
        border_color = "#34d399" if is_safe else "#f87171"
        bg_color = "rgba(52, 211, 153, 0.08)" if is_safe else "rgba(248, 113, 113, 0.08)"
        icon = "🟢" if is_safe else "🔴"
        status_text = "Safe URL Verified" if is_safe else "Phishing Threat Detected"
        desc_text = (
            f"SentinelAI found no malicious patterns or brand impersonation signals in <code>{url}</code>."
            if is_safe else
            f"High risk detected for <code>{url}</code> based on machine learning scoring and heuristic rules."
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
        st.markdown('<div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">📊 Detection Summary</div>', unsafe_allow_html=True)

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

        _metric_box(mc1, "Prediction", result["prediction"].upper(), "#34d399" if is_safe else "#f87171")
        _metric_box(mc2, "Confidence", f"{result['confidence'] * 100:.2f}%", "#22d3ee")
        _metric_box(mc3, "Risk Level", risk.upper(), "#34d399" if is_safe else "#f87171")

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

        # ----------------------------
        # Probability Breakdown & Progress
        # ----------------------------
        st.markdown(
            """
            <div class="glass" style="padding:20px; border-radius:14px; margin-bottom:24px;">
                <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">🤖 AI Probability Distribution</div>
            """,
            unsafe_allow_html=True
        )
        
        st.progress(float(result["confidence"]))

        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.markdown(
                f"""
                <div style="padding:8px 0;">
                    <span style="color:#f87171; font-weight:700; font-size:14px;">🔴 Phishing Probability:</span>
                    <span style="color:#f8fafc; font-weight:800; font-size:16px; margin-left:8px;">{result['phishing_probability'] * 100:.2f}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with pcol2:
            st.markdown(
                f"""
                <div style="padding:8px 0;">
                    <span style="color:#34d399; font-weight:700; font-size:14px;">🟢 Safe Probability:</span>
                    <span style="color:#f8fafc; font-weight:800; font-size:16px; margin-left:8px;">{result['safe_probability'] * 100:.2f}%</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------
        # Heuristic Warning (if present)
        # ----------------------------
        if "flag" in result:
            if is_safe:
                st.info(f"ℹ️ **System Flag:** {result['flag']}")
            else:
                st.warning(f"⚠️ **Threat Flag:** {result['flag']}")

        # ----------------------------
        # Inspection Logs & Explainable AI
        # ----------------------------
        with st.expander("📄 Detailed Technical Logs", expanded=True):
            st.write(f"**Target URL:** `{url}`")
            st.write(f"**Classification:** `{result['prediction'].upper()}`")
            st.write(f"**Confidence Score:** `{result['confidence'] * 100:.2f}%`")
            st.write(f"**Phishing Risk Score:** `{result['phishing_probability'] * 100:.2f}%`")
            st.write(f"**Legitimacy Score:** `{result['safe_probability'] * 100:.2f}%`")
            st.write(f"**Calculated Risk Level:** `{risk.upper()}`")

        try:
            summary, reasons = explain_url(url, result)
            with st.expander("🧠 Explainable AI Decision Reasoning", expanded=True):
                st.write(summary)
                st.markdown("#### Key Indicators:")
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