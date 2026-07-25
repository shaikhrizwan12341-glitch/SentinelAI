import streamlit as st

_WATERMARK_HTML = """
<div class="shield-watermark" aria-hidden="true">
  <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#22d3ee"/>
        <stop offset="100%" stop-color="#2dd4bf"/>
      </linearGradient>
      <radialGradient id="shieldFill" cx="50%" cy="40%" r="60%">
        <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.10"/>
        <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <path d="M100 12 L24 42 V104 C24 152 56 192 100 210 C144 192 176 152 176 104 V42 Z"
          fill="url(#shieldFill)" stroke="url(#shieldGrad)" stroke-width="2.5"/>
    <path d="M100 40 L48 62 V104 C48 138 72 168 100 182 C128 168 152 138 152 104 V62 Z"
          fill="none" stroke="url(#shieldGrad)" stroke-width="1.2" stroke-opacity="0.55"/>
    <circle cx="100" cy="108" r="26" fill="none" stroke="url(#shieldGrad)" stroke-width="1.5" stroke-opacity="0.7"/>
    <path d="M88 108 L97 118 L114 98" fill="none" stroke="url(#shieldGrad)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</div>
"""

_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ---------- Base ---------- */
html, body, p, span, div, input, textarea {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
code, pre, .stCode {
  font-family: 'JetBrains Mono', monospace !important;
}

section[data-testid="stMain"] {
  background: transparent !important;
}
section[data-testid="stMain"] > div {
  position: relative;
  z-index: 1;
}
.stApp {
  background:
    radial-gradient(1200px 600px at 80% -10%, rgba(34,211,238,0.10), transparent 60%),
    radial-gradient(900px 500px at 0% 100%, rgba(45,212,191,0.08), transparent 55%),
    linear-gradient(180deg, #0a0e1a 0%, #070b15 100%);
}

/* ---------- Animated shield watermark ---------- */
/* Fixed to the viewport center of the main content area (sidebar ~21rem wide) */
.shield-watermark {
  position: fixed;
  top: 50vh;
  left: calc(50% + 10.5rem);
  width: 520px;
  height: 560px;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 0;
  animation: shieldFloat 9s ease-in-out infinite, shieldGlow 7s ease-in-out infinite;
}
.shield-watermark svg { width: 100%; height: 100%; }

@keyframes shieldFloat {
  0%, 100% { transform: translate(-50%, -50%) translateY(0px) rotate(0deg); }
  50%      { transform: translate(-50%, -50%) translateY(-22px) rotate(1.5deg); }
}
@keyframes shieldGlow {
  0%, 100% { opacity: 0.32; filter: drop-shadow(0 0 28px rgba(34,211,238,0.28)); }
  50%      { opacity: 0.58; filter: drop-shadow(0 0 52px rgba(34,211,238,0.58)); }
}

/* ---------- Glassmorphism utility ---------- */
.glass {
  background: rgba(255, 255, 255, 0.045);
  backdrop-filter: blur(14px) saturate(140%);
  -webkit-backdrop-filter: blur(14px) saturate(140%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
  transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
}
.glass:hover {
  transform: translateY(-4px);
  border-color: rgba(34, 211, 238, 0.35);
  box-shadow: 0 14px 44px rgba(0, 0, 0, 0.45), 0 0 24px rgba(34, 211, 238, 0.12);
}
.glass-flat {
  background: rgba(255, 255, 255, 0.035);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 14px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(17,24,39,0.82) 0%, rgba(10,14,26,0.96) 100%);
  backdrop-filter: blur(18px) saturate(150%);
  -webkit-backdrop-filter: blur(18px) saturate(150%);
  border-right: 1px solid rgba(34, 211, 238, 0.14);
}
section[data-testid="stSidebar"] * {
  font-family: 'Inter', sans-serif !important;
}
.sb-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 4px 6px 4px;
}
.sb-logo .badge {
  width: 46px; height: 46px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(34,211,238,0.25), rgba(45,212,191,0.12));
  border: 1px solid rgba(34,211,238,0.4);
  box-shadow: 0 0 18px rgba(34,211,238,0.25);
  font-size: 22px;
  animation: badgePulse 4s ease-in-out infinite;
}
@keyframes badgePulse {
  0%, 100% { box-shadow: 0 0 18px rgba(34,211,238,0.25); }
  50%      { box-shadow: 0 0 30px rgba(34,211,238,0.55); }
}
.sb-title {
  font-size: 20px; font-weight: 800; letter-spacing: 0.5px;
  background: linear-gradient(90deg, #22d3ee, #2dd4bf);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
}
.sb-version {
  font-size: 11px; color: #64748b; letter-spacing: 1px; margin-top: 2px;
}
.sb-status-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 7px 12px; margin: 4px 0;
  font-size: 13px; color: #cbd5e1;
}
.sb-status-row .dot {
  width: 8px; height: 8px; border-radius: 50%;
  display: inline-block; margin-right: 8px;
  box-shadow: 0 0 8px currentColor;
}
.sb-section-label {
  font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
  color: #475569; margin: 14px 4px 6px 4px; font-weight: 600;
}

/* ---------- Headings & text ---------- */
h1, h2, h3 { letter-spacing: -0.02em; }
.hero-title {
  font-size: 52px; font-weight: 800; line-height: 1.05;
  background: linear-gradient(120deg, #f1f5f9 30%, #22d3ee 60%, #2dd4bf 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}
.hero-sub {
  font-size: 17px; color: #94a3b8; line-height: 1.6; max-width: 640px;
}
.feature-card {
  padding: 22px 22px 20px 22px;
}
.feature-card .ic {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; margin-bottom: 14px;
  background: rgba(34,211,238,0.12);
  border: 1px solid rgba(34,211,238,0.25);
}
.feature-card h4 { margin: 0 0 6px 0; font-size: 16px; color: #e2e8f0; }
.feature-card p  { margin: 0; font-size: 13px; color: #94a3b8; line-height: 1.55; }

.stat-chip {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 8px 14px; border-radius: 999px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  font-size: 13px; color: #cbd5e1;
}

/* ---------- Buttons ---------- */
.stButton > button {
  border-radius: 10px !important;
  border: 1px solid rgba(34,211,238,0.3) !important;
  background: linear-gradient(135deg, rgba(34,211,238,0.18), rgba(45,212,191,0.10)) !important;
  color: #e2e8f0 !important;
  font-weight: 600 !important;
  transition: all 0.25s ease !important;
}
.stButton > button:hover {
  border-color: rgba(34,211,238,0.7) !important;
  box-shadow: 0 0 18px rgba(34,211,238,0.3) !important;
  transform: translateY(-1px);
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #1e293b, #0f172a);
  border-radius: 8px; border: 2px solid #0a0e1a;
}
::-webkit-scrollbar-thumb:hover { background: #22d3ee; }

/* ---------- Links ---------- */
a { color: #22d3ee; text-decoration: none; transition: color 0.2s; }
a:hover { color: #2dd4bf; }
</style>
"""


def apply_theme():
    """Inject the global SentinelAI theme: dark glassmorphism + animated shield watermark.

    Call once near the top of any page (after st.set_page_config) to apply the
    shared look. Safe to call on every page.
    """
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(_WATERMARK_HTML, unsafe_allow_html=True)
