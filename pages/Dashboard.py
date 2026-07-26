import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from components.charts import threat_distribution_chart
from components.metric_card import metric_card
from database.database import (
    get_total_scans,
    get_safe_scans,
    get_phishing_scans,
    get_recent_scans
)

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
# Sidebar
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
    st.markdown('<div style="color:#94a3b8; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px;">System Status</div>', unsafe_allow_html=True)
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
    st.markdown('<div style="color:#94a3b8; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:12px;">Navigation</div>', unsafe_allow_html=True)
    st.info("Use the pages menu above to move between modules.")
    st.markdown("---")
    st.caption("© 2026 SentinelAI · All rights reserved.")

# ----------------------------
# Live data & calculations
# ----------------------------
total    = get_total_scans()
safe     = get_safe_scans()
phishing = get_phishing_scans()
accuracy = MODEL_ACCURACY

threat_pct = round((phishing / total * 100), 1) if total > 0 else 0
safe_pct   = round((safe    / total * 100), 1) if total > 0 else 0

# Fetch recent scan records
rows = get_recent_scans()
df_recent = pd.DataFrame(
    rows,
    columns=["Type", "Content", "Prediction", "Confidence", "Risk", "Scanned At"]
) if rows else pd.DataFrame(columns=["Type", "Content", "Prediction", "Confidence", "Risk", "Scanned At"])

# ----------------------------
# Page Header
# ----------------------------
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
)

# ----------------------------
# Metric Cards
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
# Analytics & Quick Actions Section
# ----------------------------
chart_col1, chart_col2, actions_col = st.columns([1.2, 1.2, 0.8], gap="medium")

# --- CHART 1: Threat Breakdown Donut ---
with chart_col1:
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Safe', 'Phishing'],
        values=[safe, phishing],
        hole=.6,
        marker=dict(colors=['#34d399', '#f87171']),
        textinfo='percent+label',
        textfont=dict(color="#e2e8f0", size=12)
    )])
    
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=220
    )

    st.markdown(
        """
        <div class="glass" style="padding:20px; border-radius:12px;">
            <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">Threat Breakdown</div>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CHART 2: Scan Distribution by Channel ---
with chart_col2:
    if not df_recent.empty and "Type" in df_recent.columns:
        type_counts = df_recent['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        
        fig_bar = px.bar(
            type_counts, 
            x='Type', 
            y='Count', 
            color='Type',
            color_discrete_sequence=['#22d3ee', '#2dd4bf', '#818cf8']
        )
    else:
        fig_bar = px.bar(
            x=['URL', 'Email', 'SMS'], 
            y=[0, 0, 0],
            labels={'x': 'Type', 'y': 'Count'},
            color_discrete_sequence=['#22d3ee']
        )

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        showlegend=False,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title=None),
        margin=dict(l=10, r=10, t=10, b=10),
        height=220
    )

    st.markdown(
        """
        <div class="glass" style="padding:20px; border-radius:12px;">
            <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:12px;">Scan Distribution by Type</div>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- QUICK ACTIONS PANEL ---
with actions_col:
    st.markdown(
        """
        <div class="glass" style="padding:20px; border-radius:12px; height:100%;">
            <div style="font-size:16px; font-weight:700; color:#e2e8f0; margin-bottom:16px;">Quick Actions</div>
        """,
        unsafe_allow_html=True
    )
    st.button("🌐  Scan URL", use_container_width=True)
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    st.button("📧  Scan Email", use_container_width=True)
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    st.button("💬  Scan SMS", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

# ----------------------------
# Recent Activity Table
# ----------------------------
st.markdown(
    """
    <div class="glass" style="padding:24px; border-radius:12px;">
        <div style="font-size:18px; font-weight:700; color:#e2e8f0; margin-bottom:16px;">Recent Activity</div>
    """,
    unsafe_allow_html=True
)

if not df_recent.empty:
    def _color_pred(val):
        color = "#f87171" if str(val).lower() == "phishing" else "#34d399"
        return f"color: {color}; font-weight: 600;"

    styled = (
        df_recent.style
        .map(_color_pred, subset=["Prediction"])
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