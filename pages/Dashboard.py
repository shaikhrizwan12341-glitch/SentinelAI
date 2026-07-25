from components.charts import (
    threat_distribution_chart,
    scan_type_chart,
    daily_scan_chart
)
from components.metric_card import metric_card
from database.database import (
    get_total_scans,
    get_safe_scans,
    get_phishing_scans,
    get_recent_scans
)

import streamlit as st
import pandas as pd

from components.theme import apply_theme
from utils.constants import APP_NAME, APP_VERSION, SYSTEM_STATUS, MODEL_ACCURACY

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="SentinelAI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

apply_theme()

# ----------------------------
# Sidebar (consistent with home page)
# ----------------------------
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
    st.markdown('<div class="sb-section-label">System Status</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="sb-section-label">Navigation</div>', unsafe_allow_html=True)
    st.info("Use the pages menu above to move between modules.")
    st.markdown("---")
    st.caption("© 2025 SentinelAI · All rights reserved.")

# ----------------------------
# Live data (all DB calls unchanged)
# ----------------------------
total    = get_total_scans()
safe     = get_safe_scans()
phishing = get_phishing_scans()
accuracy = MODEL_ACCURACY

threat_pct = round((phishing / total * 100), 1) if total > 0 else 0
safe_pct   = round((safe    / total * 100), 1) if total > 0 else 0

# ----------------------------
# Page header
# ----------------------------
<<<<<<< HEAD
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
st.subheader("📊 Security Analytics")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        threat_distribution_chart(),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        scan_type_chart(),
        use_container_width=True
    )

st.plotly_chart(
    daily_scan_chart(),
    use_container_width=True
=======
st.markdown(
    """
    <div style="padding: 14px 0 6px 0;">
        <div class="hero-title" style="font-size:38px;">Dashboard</div>
        <p class="hero-sub" style="margin-top:6px;">
            Live threat intelligence across all scan modules.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
>>>>>>> origin/main
)

# ----------------------------
# Metric cards
# ----------------------------
c1, c2, c3, c4 = st.columns(4)

def _metric_glass(col, icon, label, value, sub, accent):
    with col:
        st.markdown(
            f"""
            <div class="glass" style="padding:22px 20px 18px 20px; position:relative; overflow:hidden;">
              <div style="font-size:26px; margin-bottom:10px;">{icon}</div>
              <div style="font-size:12px; color:#64748b; text-transform:uppercase;
                          letter-spacing:1.5px; font-weight:600; margin-bottom:4px;">{label}</div>
              <div style="font-size:40px; font-weight:800; color:{accent};
                          line-height:1; margin-bottom:6px;">{value}</div>
              <div style="font-size:12px; color:#475569;">{sub}</div>
              <div style="position:absolute; bottom:-18px; right:-14px; font-size:80px;
                          opacity:0.06; pointer-events:none;">{icon}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

_metric_glass(c1, "🌐", "Total Scans",    total,    "all time",            "#e2e8f0")
_metric_glass(c2, "⚠️", "Threats Found",  phishing, f"{threat_pct}% of total", "#f87171")
_metric_glass(c3, "✅", "Safe Scans",     safe,     f"{safe_pct}% of total",   "#34d399")
_metric_glass(c4, "🤖", "Model Accuracy", accuracy, "on validation set",    "#22d3ee")

st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)


# ----------------------------
# Threat distribution chart + Quick Actions
# ----------------------------
chart_col, actions_col = st.columns([2, 1], gap="large")

with chart_col:
    st.markdown(
        '<div class="glass" style="padding:24px;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sb-section-label" style="margin-top:0;">Threat Distribution</div>',
        unsafe_allow_html=True,
    )

    fig = threat_distribution_chart()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
        ),
        title_font=dict(color="#e2e8f0"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_traces(
        marker=dict(colors=["#34d399", "#f87171"]),
        textfont=dict(color="#e2e8f0"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with actions_col:
    st.markdown(
        '<div class="glass" style="padding:24px; height:100%;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sb-section-label" style="margin-top:0;">Quick Actions</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    st.button("🌐  Scan a URL",    use_container_width=True)
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    st.button("📧  Scan an Email", use_container_width=True)
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    st.button("💬  Scan an SMS",   use_container_width=True)

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
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
            <div class="sb-status-row glass-flat" style="margin:4px 0;">
                <span><span class="dot" style="color:{dot_color};background:{dot_color};"></span>{label}</span>
                <span style="color:{dot_color};font-weight:600;font-size:12px;">{clean}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

# ----------------------------
# Recent Activity (DB call unchanged)
# ----------------------------
st.markdown(
    '<div class="glass" style="padding:24px;">',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sb-section-label" style="margin-top:0;">Recent Activity</div>',
    unsafe_allow_html=True,
)

rows = get_recent_scans()

if rows:

    df = pd.DataFrame(
        rows,
<<<<<<< HEAD
        columns=[
            "Scan Type",
            "Content",
            "Prediction",
            "Confidence",
            "Risk",
            "Scanned At"
        ]
=======
        columns=["Type", "Content", "Prediction", "Confidence", "Risk", "Scanned At"]
>>>>>>> origin/main
    )

    def _color_pred(val):
        color = "#f87171" if str(val).lower() == "phishing" else "#34d399"
        return f"color: {color}; font-weight: 600;"

    styled = (
        df.style
        .applymap(_color_pred, subset=["Prediction"])
        .set_properties(**{
            "background-color": "rgba(255,255,255,0.02)",
            "color": "#cbd5e1",
            "border-color": "rgba(255,255,255,0.05)",
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "rgba(34,211,238,0.08)"),
                    ("color", "#94a3b8"),
                    ("font-size", "12px"),
                    ("letter-spacing", "1.5px"),
                    ("text-transform", "uppercase"),
                    ("border-bottom", "1px solid rgba(34,211,238,0.2)"),
                ],
            },
            {
                "selector": "tr:hover td",
                "props": [("background-color", "rgba(34,211,238,0.05)")],
            },
        ])
    )
<<<<<<< HEAD

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
=======
    st.dataframe(styled, use_container_width=True, hide_index=True)
else:
    st.markdown(
        """
        <div style="text-align:center; padding:40px 0; color:#475569;">
            <div style="font-size:36px; margin-bottom:12px;">📭</div>
            <div style="font-size:14px;">No scans have been performed yet.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
>>>>>>> origin/main

# ----------------------------
# Footer
# ----------------------------
st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
st.markdown(
    '<p style="color:#64748b;font-size:13px;text-align:center;">'
    'SentinelAI · Built for defensive cyber awareness. Always verify with multiple sources.'
    '</p>',
    unsafe_allow_html=True,
)
