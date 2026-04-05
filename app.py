import streamlit as st

st.set_page_config(page_title="HeartGuard AI", page_icon=None, layout="wide", initial_sidebar_state="expanded")

from utils.logo import logo_img_tag

# ── Global Theme ──
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet">

<style>
/* ═══════════════════════════════════════
   HEARTGUARD AI — CACHEADVANCE THEME
   Teal/Sky accent · Dot-grid · Top Nav
   ═══════════════════════════════════════ */

*, *::before, *::after { box-sizing: border-box; }

.stApp {
  background: #0b1120 !important;
  font-family: 'Inter', system-ui, sans-serif;
  color: #e2e8f0;
}

/* Dot-grid background texture */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background-image: radial-gradient(rgba(148,163,184,0.06) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none; z-index: 0;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  color: #e2e8f0 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(56,189,248,0.25); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(56,189,248,0.45); }

/* ── Top Nav Bar ── */
.hg-topnav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 54px;
  background: rgba(11,17,32,0.94);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(148,163,184,0.08);
  z-index: 9999;
  display: flex; align-items: center;
  padding: 0 1.4rem; gap: 0.8rem;
}
.hg-nav-left { display: flex; align-items: center; gap: 0.55rem; flex-shrink: 0; }
.hg-nav-brand {
  font-family: 'Sora', sans-serif;
  font-weight: 700; font-size: 0.92rem;
  color: #f1f5f9; letter-spacing: -0.01em;
}
.hg-nav-sep {
  width: 1px; height: 18px;
  background: rgba(148,163,184,0.12);
  margin: 0 0.2rem;
}
.hg-nav-center { flex: 1; display: flex; justify-content: center; }
.hg-search {
  display: flex; align-items: center; gap: 0.55rem;
  background: rgba(20,30,50,0.8);
  border: 1px solid rgba(148,163,184,0.1);
  border-radius: 8px;
  padding: 0.32rem 0.75rem;
  font-size: 0.8rem; color: #64748b;
  width: 210px; cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.hg-search:hover { border-color: rgba(56,189,248,0.28); background: rgba(30,41,60,0.8); }
.hg-search kbd {
  margin-left: auto;
  background: rgba(148,163,184,0.08);
  border: 1px solid rgba(148,163,184,0.14);
  border-radius: 4px;
  padding: 0.05rem 0.28rem;
  font-size: 0.68rem; color: #475569;
  font-family: inherit;
}
.hg-nav-right { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.hg-version {
  display: flex; align-items: center; gap: 0.25rem;
  background: rgba(56,189,248,0.05);
  border: 1px solid rgba(56,189,248,0.14);
  border-radius: 6px;
  padding: 0.22rem 0.55rem;
  font-size: 0.76rem; color: #7dd3fc; font-weight: 600;
  cursor: pointer;
}
.hg-github {
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(30,41,59,0.5);
  border: 1px solid rgba(148,163,184,0.1);
  border-radius: 6px;
  color: #94a3b8; cursor: pointer;
  transition: all 0.15s;
}
.hg-github:hover { border-color: rgba(56,189,248,0.3); color: #38bdf8; }

/* Push app content below the top nav */
.stApp > div[data-testid="stAppViewContainer"] {
  padding-top: 54px !important;
  animation: pageFadeIn 0.55s ease-out both;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #0b1120 !important;
  border-right: 1px solid rgba(148,163,184,0.07) !important;
  top: 54px !important;
}
[data-testid="stSidebar"] > div:first-child { background: transparent !important; }
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #cbd5e1 !important; }

/* ── Doc-style sidebar radio nav ── */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
  gap: 0 !important;
  display: flex !important;
  flex-direction: column !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  background: transparent !important;
  border: none !important;
  border-left: 2px solid transparent !important;
  border-radius: 0 6px 6px 0 !important;
  padding: 0.38rem 0.75rem 0.38rem 0.9rem !important;
  color: #94a3b8 !important;
  font-size: 0.855rem !important;
  font-weight: 400 !important;
  transition: all 0.12s ease !important;
  cursor: pointer !important;
  margin-left: 0 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  color: #cbd5e1 !important;
  background: rgba(148,163,184,0.05) !important;
}
/* Active item */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  color: #38bdf8 !important;
  background: rgba(56,189,248,0.08) !important;
  border-left-color: #38bdf8 !important;
  font-weight: 500 !important;
}
/* Hide the radio circle */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child {
  display: none !important;
}

/* ── Sidebar radio section GROUP LABELS ── */
[data-testid="stSidebar"] .stRadio > label {
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  color: #475569 !important;
  text-transform: none !important;
  letter-spacing: 0.02em !important;
  padding: 0.9rem 0 0.3rem 0.9rem !important;
  margin: 0 !important;
  display: block !important;
}
/* First section — less top padding */
[data-testid="stSidebar"] .stRadio:first-of-type > label {
  padding-top: 0.3rem !important;
}

/* Sidebar slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div:nth-child(3) {
  background: linear-gradient(90deg, #0ea5e9, #38bdf8) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div:nth-child(5) {
  background: #38bdf8 !important;
  border: 2px solid white !important;
}
/* Sidebar selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: rgba(20,30,50,0.8) !important;
  border: 1px solid rgba(148,163,184,0.12) !important;
  border-radius: 8px !important;
}

/* ── Inputs ── */
input[type="text"], input[type="email"], input[type="password"],
[data-baseweb="input"] input, [data-baseweb="base-input"] input {
  background: #131c30 !important;
  border: 1px solid rgba(148,163,184,0.12) !important;
  border-radius: 8px !important;
  color: #e2e8f0 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.875rem !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
}
input:focus {
  border-color: #0ea5e9 !important;
  box-shadow: 0 0 0 3px rgba(14,165,233,0.14) !important;
  outline: none !important;
}
/* Placeholder text visible on dark background */
input::placeholder,
[data-baseweb="input"] input::placeholder,
[data-baseweb="base-input"] input::placeholder,
textarea::placeholder {
  color: #64748b !important;
  opacity: 1 !important;
}
[data-baseweb="input"], [data-baseweb="base-input"] {
  overflow: hidden !important; border-radius: 8px !important;
}
[data-baseweb="base-input"] > div { background: #131c30 !important; }
[data-testid="InputInstructions"] { display: none !important; }

/* ── Forms ── */
div[data-testid="stForm"] {
  background: transparent !important;
  border-radius: 0 !important;
  padding: 0 !important;
  border: none !important;
}
div[data-testid="stForm"] label {
  color: #cbd5e1 !important; font-weight: 600 !important; font-size: 0.88rem !important;
}
[data-testid="stFormSubmitButton"] { margin-top: 0.75rem !important; }
[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] > button {
  background: linear-gradient(135deg, #0ea5e9, #38bdf8) !important;
  color: #071020 !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  padding: 0.75rem 1.2rem !important;
  transition: all 0.2s ease !important;
  letter-spacing: 0.01em !important;
}
[data-testid="stFormSubmitButton"] button:hover {
  background: linear-gradient(135deg, #38bdf8, #7dd3fc) !important;
  box-shadow: 0 6px 24px rgba(56,189,248,0.28) !important;
  transform: translateY(-1px) !important;
}
/* Password eye toggle */
button[kind="icon"],
[data-testid="stForm"] button[kind="icon"],
div[data-baseweb="input"] button,
.stTextInput button {
  background: transparent !important;
  border: none !important;
  color: #94a3b8 !important;
}
div[data-baseweb="input"] button:hover,
.stTextInput button:hover {
  color: #e2e8f0 !important;
  background: rgba(148,163,184,0.1) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: #0ea5e9 !important;
  color: #071020 !important; border: none !important;
  border-radius: 8px !important; font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover {
  background: #38bdf8 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 14px rgba(56,189,248,0.28) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
  background: #059669 !important;
  color: white !important;
}
.stDownloadButton > button:hover {
  background: #047857 !important;
  box-shadow: 0 4px 12px rgba(5,150,105,0.3) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(20,30,50,0.7) !important;
  border-radius: 10px !important;
  border: 1px solid rgba(148,163,184,0.08) !important;
  padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: #94a3b8 !important;
  border-radius: 6px !important; font-weight: 500 !important;
  transition: all 0.15s !important; padding: 0.4rem 1rem !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(14,165,233,0.14) !important;
  color: #38bdf8 !important; font-weight: 600 !important;
}

/* ── Multiselect tags ── */
[data-baseweb="tag"] {
  background: rgba(14,165,233,0.12) !important;
  border: 1px solid rgba(14,165,233,0.25) !important;
  border-radius: 6px !important;
}
[data-baseweb="tag"] span { color: #7dd3fc !important; font-size: 0.8rem !important; }

/* ── Misc ── */
.stAlert { border-radius: 8px !important; }
.stDataFrame { border-radius: 8px !important; overflow: hidden !important; }
[data-testid="stDataFrameContainer"] {
  background: rgba(20,30,50,0.5) !important;
  border: 1px solid rgba(148,163,184,0.08) !important;
  border-radius: 8px !important;
}
[data-testid="stExpander"] {
  background: rgba(20,30,50,0.5) !important;
  border: 1px solid rgba(148,163,184,0.08) !important;
  border-radius: 10px !important;
}

/* ── Animations ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pageFadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.animate-fade-up { animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) both; }
[data-testid="stSidebar"] { animation: pageFadeIn 0.5s ease-out 0.1s both; }
.stMainBlockContainer, [data-testid="stMainBlockContainer"] {
  animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.05s both;
}
</style>
""", unsafe_allow_html=True)

# ── Top Navigation Bar ──
_logo_nav = logo_img_tag(width=26, style="margin:0; border-radius:5px; flex-shrink:0;")
st.markdown(f"""
<div class="hg-topnav">
  <div class="hg-nav-left">
    {_logo_nav}
    <span class="hg-nav-brand">HeartGuard AI</span>
    <div class="hg-nav-sep"></div>
  </div>
  <div class="hg-nav-center">
    <div class="hg-search">
      <svg width="13" height="13" fill="none" stroke="#64748b" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
      </svg>
      Search&nbsp;docs&hellip;
      <kbd>&#x2318;K</kbd>
    </div>
  </div>
  <div class="hg-nav-right">
    <div class="hg-version">v3.0 &#9660;</div>
    <div class="hg-github" title="GitHub">
      <svg width="15" height="15" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
      </svg>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Auth imports ──
from utils.auth import login_user, signup_user, restore_session_from_cookie, get_cookie_manager

# Cookie manager MUST be instantiated at the top level (not inside functions)
_cookie_manager = get_cookie_manager()

# Session state defaults
for key, default in [('logged_in', False), ('user', None), ('user_email', None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Restore session from cookie on refresh ──
restore_session_from_cookie()



def auth_page():
    st.markdown("""<style>
    [data-testid="stSidebar"] { display: none !important; }

    @keyframes slideInLeft {
      from { opacity:0; transform:translateX(-36px); }
      to   { opacity:1; transform:translateX(0); }
    }
    @keyframes slideInRight {
      from { opacity:0; transform:translateX(36px); }
      to   { opacity:1; transform:translateX(0); }
    }
    @keyframes float {
      0%,100% { transform: translateY(0); }
      50%     { transform: translateY(-14px); }
    }
    @keyframes shimmer {
      0%   { background-position: -200% center; }
      100% { background-position:  200% center; }
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

    /* ── Brand hero (left) ── */
    .brand-hero {
      position: relative;
      background: linear-gradient(150deg, #071428 0%, #0c2040 40%, #062035 70%, #091828 100%);
      border: 1px solid rgba(56,189,248,0.12);
      border-radius: 20px;
      padding: 2.8rem 2.2rem;
      min-height: 560px;
      overflow: hidden;
      animation: slideInLeft 0.65s cubic-bezier(0.16,1,0.3,1) both;
    }
    /* Dot-grid overlay inside hero */
    .brand-hero::before {
      content: '';
      position: absolute; inset: 0;
      background-image: radial-gradient(rgba(56,189,248,0.07) 1px, transparent 1px);
      background-size: 24px 24px;
      border-radius: 20px;
      pointer-events: none;
    }
    /* Glow orbs */
    .brand-hero::after {
      content: '';
      position: absolute;
      top: -80px; right: -80px;
      width: 260px; height: 260px;
      background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
      border-radius: 50%;
      animation: float 9s ease-in-out infinite;
    }

    .brand-content { position: relative; z-index: 1; }

    .brand-content h1 {
      font-family: 'Sora', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.18;
      margin: 0 0 1rem;
    }
    .brand-content h1 span {
      background: linear-gradient(135deg, #38bdf8, #7dd3fc);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-desc {
      color: rgba(186,230,253,0.7);
      font-size: 0.97rem;
      line-height: 1.75;
      margin-bottom: 2rem;
      max-width: 360px;
    }

    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
    @keyframes ecgScroll {
      0%   { stroke-dashoffset: 1200; }
      100% { stroke-dashoffset: 0; }
    }
    @keyframes ecgLoop {
      0%   { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }
    @keyframes heartPulse {
      0%,100% { transform: scale(1);   filter: drop-shadow(0 0 6px rgba(239,68,68,0.4)); }
      50%     { transform: scale(1.18); filter: drop-shadow(0 0 16px rgba(239,68,68,0.85)); }
    }
    @keyframes dotBlink {
      0%,100% { opacity:1; } 50% { opacity:0.2; }
    }

    /* ── ECG Monitor Panel ── */
    .ecg-panel {
      background: rgba(6,14,28,0.9);
      border: 1px solid rgba(56,189,248,0.14);
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 1.8rem;
      animation: slideInLeft 0.8s cubic-bezier(0.16,1,0.3,1) 0.15s both;
    }
    .ecg-header {
      display: flex; align-items: center; justify-content: space-between;
      background: rgba(10,22,44,0.9);
      border-bottom: 1px solid rgba(56,189,248,0.08);
      padding: 0.5rem 0.9rem;
    }
    .ecg-header-left { display: flex; align-items: center; gap: 0.5rem; }
    .ecg-dot {
      width: 7px; height: 7px; border-radius: 50%;
      background: #ef4444;
      animation: dotBlink 1.2s ease-in-out infinite;
    }
    .ecg-label {
      font-size: 0.72rem; font-weight: 600;
      color: #94a3b8; letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .ecg-bpm {
      font-family: 'Sora', sans-serif;
      font-size: 1.1rem; font-weight: 800;
      color: #10b981;
      letter-spacing: -0.01em;
    }
    .ecg-bpm-label { font-size: 0.62rem; color: #475569; margin-left: 0.2rem; }
    .ecg-canvas-wrap {
      overflow: hidden;
      height: 80px;
      position: relative;
      background:
        repeating-linear-gradient(0deg, transparent, transparent 19px, rgba(56,189,248,0.04) 20px),
        repeating-linear-gradient(90deg, transparent, transparent 19px, rgba(56,189,248,0.04) 20px);
    }
    .ecg-svg-track {
      display: flex;
      width: 200%;
      height: 80px;
      animation: ecgLoop 3.2s linear infinite;
    }
    .ecg-svg-track svg { flex-shrink: 0; }
    .ecg-vitals {
      display: flex; gap: 0; border-top: 1px solid rgba(56,189,248,0.07);
    }
    .ecg-vital {
      flex: 1; padding: 0.5rem 0.65rem;
      border-right: 1px solid rgba(56,189,248,0.07);
      text-align: center;
    }
    .ecg-vital:last-child { border-right: none; }
    .ecg-vital-val {
      font-family: 'Sora', sans-serif;
      font-size: 0.92rem; font-weight: 700;
      color: #e2e8f0;
    }
    .ecg-vital-key {
      font-size: 0.6rem; color: #475569;
      text-transform: uppercase; letter-spacing: 0.07em;
      margin-top: 0.1rem;
    }
    .ecg-status-ok  { color: #10b981 !important; }
    .ecg-status-warn { color: #f59e0b !important; }
    /* Heart icon */
    .ecg-heart {
      font-size: 1rem;
      display: inline-block;
      animation: heartPulse 0.85s ease-in-out infinite;
      color: #ef4444;
    }

    /* Stats row */
    .stat-row { display: flex; gap: 0.75rem; margin-bottom: 1.8rem; }
    .stat-box {
      flex: 1;
      background: rgba(56,189,248,0.06);
      border: 1px solid rgba(56,189,248,0.14);
      border-radius: 12px;
      padding: 1rem;
      text-align: center;
    }
    .stat-num {
      font-family: 'Sora', sans-serif;
      font-size: 1.5rem; font-weight: 800;
      color: #ffffff; display: block;
    }
    .stat-label {
      color: rgba(125,211,252,0.65);
      font-size: 0.68rem; font-weight: 600;
      text-transform: uppercase; letter-spacing: 1px;
      margin-top: 0.2rem; display: block;
    }
    .shimmer-line {
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(56,189,248,0.3), rgba(125,211,252,0.3), transparent);
      background-size: 200% 100%;
      animation: shimmer 4s linear infinite;
      margin: 1.2rem 0;
    }
    .brand-footer { color: rgba(125,211,252,0.4); font-size: 0.72rem; line-height: 1.8; }

    /* ── Auth card (right) ── */
    .auth-card {
      position: relative;
      background: rgba(11,17,32,0.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(148,163,184,0.09);
      border-radius: 20px;
      padding: 2.4rem 2rem 2rem;
      box-shadow: 0 24px 56px rgba(0,0,0,0.45);
      animation: slideInRight 0.65s cubic-bezier(0.16,1,0.3,1) 0.1s both;
    }
    .auth-card::before {
      content: '';
      position: absolute;
      top: 0; left: 40px; right: 40px; height: 1px;
      background: linear-gradient(90deg, transparent, rgba(56,189,248,0.22), rgba(125,211,252,0.22), transparent);
    }
    .auth-card label,
    .auth-card [data-testid="stForm"] label {
      color: #cbd5e1 !important; font-weight: 600 !important; font-size: 0.88rem !important;
    }
    .auth-footer { text-align:center; margin-top:1.1rem; color:#94a3b8; font-size:0.84rem; }
    .auth-footer b { color: #38bdf8; }
    </style>""", unsafe_allow_html=True)

    left_col, gap, right_col = st.columns([1.15, 0.05, 1])

    with left_col:
        logo_tag = logo_img_tag(width=140, style="margin:0 0 1.6rem;")
        st.markdown(f"""<div class="brand-hero">
<div class="brand-content">

{logo_tag}

<h1>Smarter<br><span>Heart Health</span><br>Starts Here.</h1>

<p class="brand-desc">
AI-driven cardiac risk assessment with transparent,
explainable predictions you can trust and act on.
</p>

<div class="ecg-panel">
  <div class="ecg-header">
    <div class="ecg-header-left">
      <span class="ecg-dot"></span>
      <span class="ecg-label">Live Cardiac Monitor</span>
    </div>
    <div>
      <span class="ecg-heart">&#10084;</span>
      <span class="ecg-bpm">72</span>
      <span class="ecg-bpm-label">BPM</span>
    </div>
  </div>
  <div class="ecg-canvas-wrap">
    <div class="ecg-svg-track">
      <svg width="600" height="80" viewBox="0 0 600 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <polyline
          points="0,40 30,40 45,40 50,38 55,40 70,40 80,40 90,20 95,5 100,65 105,15 110,40 130,40 150,40 160,38 165,40 180,40 190,40 200,20 205,5 210,65 215,15 220,40 240,40 260,40 270,38 275,40 290,40 300,40 310,20 315,5 320,65 325,15 330,40 350,40 370,40 380,38 385,40 400,40 410,40 420,20 425,5 430,65 435,15 440,40 460,40 480,40 490,38 495,40 510,40 520,40 530,20 535,5 540,65 545,15 550,40 570,40 590,40 600,40"
          stroke="#10b981" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
          fill="none"
        />
      </svg>
      <svg width="600" height="80" viewBox="0 0 600 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <polyline
          points="0,40 30,40 45,40 50,38 55,40 70,40 80,40 90,20 95,5 100,65 105,15 110,40 130,40 150,40 160,38 165,40 180,40 190,40 200,20 205,5 210,65 215,15 220,40 240,40 260,40 270,38 275,40 290,40 300,40 310,20 315,5 320,65 325,15 330,40 350,40 370,40 380,38 385,40 400,40 410,40 420,20 425,5 430,65 435,15 440,40 460,40 480,40 490,38 495,40 510,40 520,40 530,20 535,5 540,65 545,15 550,40 570,40 590,40 600,40"
          stroke="#10b981" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
          fill="none"
        />
      </svg>
    </div>
  </div>
  <div class="ecg-vitals">
    <div class="ecg-vital">
      <div class="ecg-vital-val ecg-status-ok">118/76</div>
      <div class="ecg-vital-key">BP mmHg</div>
    </div>
    <div class="ecg-vital">
      <div class="ecg-vital-val ecg-status-warn">210</div>
      <div class="ecg-vital-key">Chol mg/dl</div>
    </div>
    <div class="ecg-vital">
      <div class="ecg-vital-val ecg-status-ok">98%</div>
      <div class="ecg-vital-key">SpO&#8322;</div>
    </div>
    <div class="ecg-vital">
      <div class="ecg-vital-val ecg-status-ok">36.6&#176;</div>
      <div class="ecg-vital-key">Temp</div>
    </div>
  </div>
</div>

<div class="stat-row">
  <div class="stat-box">
    <span class="stat-num">84%</span>
    <span class="stat-label">Accuracy</span>
  </div>
  <div class="stat-box">
    <span class="stat-num">13</span>
    <span class="stat-label">Risk Factors</span>
  </div>
  <div class="stat-box">
    <span class="stat-num">SHAP</span>
    <span class="stat-label">Explainable</span>
  </div>
</div>

<div class="shimmer-line"></div>
<p class="brand-footer">XGBoost ML &middot; SHAP Interpretability &middot; Real-time Analysis<br>For educational &amp; research purposes</p>

</div>
</div>""", unsafe_allow_html=True)

    with right_col:
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        logo_sm = logo_img_tag(width=90, style="margin:0 auto;")
        st.markdown(f"""<div style="text-align:center; margin-bottom:1rem;">{logo_sm}</div>""", unsafe_allow_html=True)
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["  Sign In  ", "  Create Account  "])

        with tab1:
            st.markdown("""<div style="margin:0.4rem 0 1.3rem; text-align:center;">
<h3 style="font-family:'Sora',sans-serif; color:#f8fafc; font-size:1.65rem; font-weight:700; margin:0 0 0.4rem;">Welcome Back</h3>
<p style="color:#94a3b8; font-size:0.93rem; margin:0; line-height:1.6;">Sign in to access your health dashboard</p>
</div>""", unsafe_allow_html=True)
            with st.form("login_form"):
                login_email    = st.text_input("Email Address", placeholder="you@example.com")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password")
                st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)
                submit_login   = st.form_submit_button("Sign In  →", use_container_width=True)
                if submit_login:
                    if login_email and login_password:
                        if login_user(login_email, login_password):
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again.")
                    else:
                        st.warning("Please enter both email and password.")
            st.markdown("""<p class="auth-footer">Don't have an account? Switch to <b>Create Account</b> above.</p>""", unsafe_allow_html=True)

        with tab2:
            st.markdown("""<div style="margin:0.4rem 0 1.3rem; text-align:center;">
<h3 style="font-family:'Sora',sans-serif; color:#f8fafc; font-size:1.65rem; font-weight:700; margin:0 0 0.4rem;">Create Account</h3>
<p style="color:#94a3b8; font-size:0.93rem; margin:0; line-height:1.6;">Join and start monitoring your cardiac health</p>
</div>""", unsafe_allow_html=True)
            with st.form("signup_form"):
                signup_name  = st.text_input("Full Name", placeholder="Dr. Jane Smith")
                signup_email = st.text_input("Email Address", placeholder="jane@hospital.com")
                c_a, c_b = st.columns(2)
                with c_a:
                    signup_password = st.text_input("Password", type="password", placeholder="Create password")
                with c_b:
                    signup_confirm  = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
                st.markdown("<div style='height:0.3rem;'></div>", unsafe_allow_html=True)
                submit_signup = st.form_submit_button("Create Account  →", use_container_width=True)
                if submit_signup:
                    if signup_name and signup_email and signup_password and signup_confirm:
                        success, msg = signup_user(signup_name, signup_email, signup_password, signup_confirm)
                        if success:
                            st.success(msg + " Please sign in.")
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please fill in all fields.")
            st.markdown("""<p class="auth-footer">Already have an account? Switch to <b>Sign In</b> above.</p>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.logged_in:
    from views.dashboard import render_dashboard
    from views.history import render_history
    from views.health_profile import render_health_profile
    from views.analysis import render_analysis
    from views.precautions import render_precautions
    from views.doctors import render_doctors
    from views.my_updates import render_updates

    for k, v in [("last_risk_pct", 0.0), ("last_vitals", {}), ("health_profile", None)]:
        if k not in st.session_state:
            st.session_state[k] = v

    from utils.db import count_unread_notes
    unread = count_unread_notes(st.session_state.user_email)
    updates_label = f"My Updates{' (!)' if unread > 0 else ''}"

    # ── Sidebar ──
    st.sidebar.markdown(f"""
    <div style="text-align:center; padding:0.7rem 0 0.3rem;">
        {logo_img_tag(width=120, style="margin:0 auto;")}
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
    <div style="background:rgba(20,30,50,0.7); border:1px solid rgba(148,163,184,0.08);
         border-radius:10px; padding:0.7rem; text-align:center; margin: 0.4rem 0 0.8rem;">
        <div style="width:34px; height:34px; margin:0 auto 0.35rem;
             background:linear-gradient(135deg,#0ea5e9,#38bdf8);
             border-radius:50%; display:flex; align-items:center; justify-content:center;
             font-size:0.9rem; font-weight:700; color:#071020;">{st.session_state.user[0].upper()}</div>
        <div style="font-weight:600; font-size:0.85rem; color:#e2e8f0;">{st.session_state.user}</div>
        <div style="font-size:0.68rem; color:#475569; margin-top:0.1rem;">HeartGuard Patient</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3-group nav: track which group is active via session state ──
    if "_nav_section" not in st.session_state:
        st.session_state["_nav_section"] = 1  # 1=getting_started, 2=core, 3=account

    grp1 = ["Dashboard", "My Health Profile"]
    grp2 = ["Deep Analysis", "Precautions", "Find Doctors"]
    grp3 = [updates_label, "History"]

    def _idx(lst, target):
        for i, v in enumerate(lst):
            if v == target or ("My Updates" in v and "My Updates" in target):
                return i
        return 0

    active_sec = st.session_state["_nav_section"]
    idx1 = _idx(grp1, st.session_state.get("page", "Dashboard")) if active_sec == 1 else 0
    idx2 = _idx(grp2, st.session_state.get("page", "")) if active_sec == 2 else 0
    idx3 = _idx(grp3, st.session_state.get("page", "")) if active_sec == 3 else 0

    g1 = st.sidebar.radio("Getting started", grp1, index=idx1, key="nav_g1")
    g2 = st.sidebar.radio("Core concepts",   grp2, index=idx2, key="nav_g2")
    g3 = st.sidebar.radio("My account",      grp3, index=idx3, key="nav_g3")

    # Detect which group was last changed
    prev_g1 = st.session_state.get("_prev_g1", grp1[0])
    prev_g2 = st.session_state.get("_prev_g2", grp2[0])
    prev_g3 = st.session_state.get("_prev_g3", grp3[0])

    if g1 != prev_g1:
        st.session_state["_nav_section"] = 1
        st.session_state["page"] = g1
    elif g2 != prev_g2:
        st.session_state["_nav_section"] = 2
        st.session_state["page"] = g2
    elif g3 != prev_g3:
        st.session_state["_nav_section"] = 3
        st.session_state["page"] = g3
    else:
        # First run or no change: page driven by active section
        if active_sec == 1:
            st.session_state["page"] = g1
        elif active_sec == 2:
            st.session_state["page"] = g2
        else:
            st.session_state["page"] = g3

    st.session_state["_prev_g1"] = g1
    st.session_state["_prev_g2"] = g2
    st.session_state["_prev_g3"] = g3

    page = st.session_state["page"]

    st.sidebar.markdown("---")
    if st.sidebar.button("Sign Out", use_container_width=True):
        from utils.auth import logout
        logout()
        st.rerun()

    st.sidebar.markdown(f"""
    <div style="margin-top:0.8rem; padding:0.7rem; background:rgba(20,30,50,0.5);
         border:1px solid rgba(148,163,184,0.06); border-radius:10px;
         font-size:0.7rem; color:#334155; line-height:1.8; text-align:center;">
        {logo_img_tag(width=72, style="margin:0 auto 0.35rem; opacity:0.75;")}
        XGBoost &middot; SHAP &middot; MongoDB<br>
        v3.0 &middot; Health Companion
    </div>
    """, unsafe_allow_html=True)

    # ── Route pages ──
    if page == "Dashboard":
        render_dashboard()
    elif page == "My Health Profile":
        render_health_profile()
    elif page == "Deep Analysis":
        render_analysis()
    elif page == "Precautions":
        render_precautions()
    elif page == "Find Doctors":
        render_doctors()
    elif "My Updates" in page:
        render_updates()
    elif page == "History":
        render_history()
else:
    auth_page()
