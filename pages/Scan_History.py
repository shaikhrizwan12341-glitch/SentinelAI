import streamlit as st
import pandas as pd

from database.database import (
    filter_scans,
    clear_scan_history,
    get_total_scans,
    get_safe_scans,
    get_phishing_scans
)

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title=f"Scan History - {APP_NAME}",
    page_icon="📜",
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
        <div class="hero-title" style="font-size:38px;">Scan History</div>
        <p class="hero-sub" style="margin-top:6px;">
            Comprehensive audit log of all threat detection events across URLs, Email content, and SMS text messages.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status Chips Row
st.markdown(
    """
    <div style="display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;">
        <div class="stat-chip">📜 Audit Log Engine</div>
        <div class="stat-chip">🔍 Multi-Criteria Search</div>
        <div class="stat-chip">📥 Data Export Ready</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# METRICS STATS SUMMARY
# =========================================================

st.markdown('<div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">📊 Threat Telemetry Stats</div>', unsafe_allow_html=True)

mc1, mc2, mc3 = st.columns(3)

def _metric_box(col, label, value, color):
    with col:
        st.markdown(
            f"""
            <div class="glass" style="padding:18px; border-radius:14px; text-align:center;">
                <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-bottom:6px;">{label}</div>
                <div style="font-size:32px; font-weight:800; color:{color};">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

_metric_box(mc1, "🌐 Total Scans Processed", get_total_scans(), "#22d3ee")
_metric_box(mc2, "✅ Verified Safe Items", get_safe_scans(), "#34d399")
_metric_box(mc3, "⚠️ Threats Intercepted", get_phishing_scans(), "#f87171")

st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)


# =========================================================
# FILTERS PANEL
# =========================================================

st.markdown(
    """
    <div class="glass" style="padding:20px; border-radius:16px; margin-bottom:24px;">
        <div style="font-size:15px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">🔍 Query & Filter Records</div>
    """,
    unsafe_allow_html=True
)

fcol1, fcol2, fcol3 = st.columns(3)

with fcol1:
    search = st.text_input(
        "🔍 Search Content",
        placeholder="Search URL, Email, or SMS..."
    )

with fcol2:
    scan_type = st.selectbox(
        "📂 Scan Vector Type",
        ["All", "URL", "EMAIL", "SMS"]
    )

with fcol3:
    prediction = st.selectbox(
        "🛡 Threat Classification",
        ["All", "SAFE", "PHISHING"]
    )

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# HISTORY TABLE DISPLAY
# =========================================================

st.markdown('<div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">📑 Detailed Audit Records</div>', unsafe_allow_html=True)

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
        hide_index=True,
        column_config={
            "Confidence": st.column_config.NumberColumn("Confidence (%)", format="%.2f"),
            "Scanned At": st.column_config.DatetimeColumn("Scanned At", format="YYYY-MM-DD HH:mm")
        }
    )

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # Export & Clear Action Row
    act_col1, act_col2 = st.columns(2)

    with act_col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export History as CSV",
            csv,
            "sentinelai_scan_history.csv",
            "text/csv",
            use_container_width=True
        )

    with act_col2:
        if st.button("🗑️ Clear Entire History", use_container_width=True, type="primary"):
            clear_scan_history()
            st.success("Scan history cleared successfully.")
            st.rerun()

else:
    st.markdown(
        """
        <div class="glass" style="padding:32px; border-radius:14px; text-align:center; color:#94a3b8;">
            <div style="font-size:24px; margin-bottom:8px;">🔍</div>
            <div style="font-size:15px; font-weight:600;">No matching audit logs found</div>
            <div style="font-size:13px; color:#64748b; margin-top:4px;">Try refining your search terms or clearing the active filters.</div>
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