import streamlit as st

st.set_page_config(page_title="HeartGuard AI", page_icon=None, layout="wide", initial_sidebar_state="expanded")

from utils.logo import logo_img_tag

# ── Global Theme ──
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
/* ═══════════════════════════════════════
   HEARTGUARD AI — AURORA PREMIUM THEME
   Midnight base · Emerald/Violet accents
   Glassmorphism · Animated orbs
   ═══════════════════════════════════════ */

*, *::before, *::after { box-sizing: border-box; }

:root {
  --bg-base: #060d1f;
  --bg-card: rgba(12, 20, 42, 0.65);
  --bg-card-hover: rgba(18, 28, 55, 0.8);
  --border-subtle: rgba(148, 163, 184, 0.07);
  --border-glow: rgba(52, 211, 153, 0.2);
  --accent-emerald: #34d399;
  --accent-emerald-dim: #10b981;
  --accent-violet: #a78bfa;
  --accent-violet-dim: #8b5cf6;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #475569;
  --glass-bg: rgba(15, 23, 42, 0.6);
  --glass-border: rgba(148, 163, 184, 0.08);
}

.stApp {
  background: var(--bg-base) !important;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-primary);
}

/* Animated gradient mesh background */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 600px 600px at 15% 20%, rgba(52,211,153,0.06) 0%, transparent 70%),
    radial-gradient(ellipse 500px 500px at 85% 80%, rgba(139,92,246,0.06) 0%, transparent 70%),
    radial-gradient(ellipse 400px 400px at 50% 50%, rgba(14,165,233,0.03) 0%, transparent 70%);
  pointer-events: none; z-index: 0;
}

/* Floating animated orbs */
.stApp::after {
  content: '';
  position: fixed;
  width: 300px; height: 300px;
  top: -50px; right: -50px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(52,211,153,0.08) 0%, rgba(139,92,246,0.04) 50%, transparent 70%);
  animation: orbFloat1 18s ease-in-out infinite;
  pointer-events: none; z-index: 0;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  color: var(--text-primary) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(52,211,153,0.3), rgba(139,92,246,0.3));
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(52,211,153,0.5), rgba(139,92,246,0.5));
}

/* ── Top Nav Bar ── */
.hg-topnav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 56px;
  background: rgba(6,13,31,0.92);
  backdrop-filter: blur(20px) saturate(1.6);
  -webkit-backdrop-filter: blur(20px) saturate(1.6);
  border-bottom: 1px solid rgba(148,163,184,0.06);
  z-index: 9999;
  display: flex; align-items: center;
  padding: 0 1.5rem; gap: 0.8rem;
}
.hg-nav-left { display: flex; align-items: center; gap: 0.6rem; flex-shrink: 0; }
.hg-nav-brand {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800; font-size: 0.95rem;
  background: linear-gradient(135deg, #34d399, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.01em;
}
.hg-nav-sep {
  width: 1px; height: 20px;
  background: linear-gradient(180deg, transparent, rgba(148,163,184,0.12), transparent);
  margin: 0 0.3rem;
}
.hg-nav-center { flex: 1; display: flex; justify-content: center; }
.hg-search {
  display: flex; align-items: center; gap: 0.55rem;
  background: rgba(15,23,42,0.8);
  border: 1px solid rgba(148,163,184,0.08);
  border-radius: 10px;
  padding: 0.35rem 0.8rem;
  font-size: 0.8rem; color: #475569;
  width: 220px; cursor: pointer;
  transition: all 0.2s ease;
}
.hg-search:hover {
  border-color: rgba(52,211,153,0.2);
  background: rgba(20,30,55,0.9);
  box-shadow: 0 0 20px rgba(52,211,153,0.04);
}
.hg-search kbd {
  margin-left: auto;
  background: rgba(148,163,184,0.06);
  border: 1px solid rgba(148,163,184,0.1);
  border-radius: 5px;
  padding: 0.08rem 0.3rem;
  font-size: 0.68rem; color: #334155;
  font-family: inherit;
}
.hg-nav-right { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.hg-version {
  display: flex; align-items: center; gap: 0.25rem;
  background: linear-gradient(135deg, rgba(52,211,153,0.08), rgba(139,92,246,0.08));
  border: 1px solid rgba(52,211,153,0.15);
  border-radius: 8px;
  padding: 0.25rem 0.6rem;
  font-size: 0.76rem; color: #34d399; font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.hg-version:hover {
  border-color: rgba(52,211,153,0.3);
  box-shadow: 0 0 16px rgba(52,211,153,0.08);
}
.hg-github {
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(15,23,42,0.6);
  border: 1px solid rgba(148,163,184,0.08);
  border-radius: 8px;
  color: #64748b; cursor: pointer;
  transition: all 0.2s;
}
.hg-github:hover {
  border-color: rgba(139,92,246,0.3);
  color: #a78bfa;
  box-shadow: 0 0 16px rgba(139,92,246,0.08);
}

/* Push app content below the top nav */
.stApp > div[data-testid="stAppViewContainer"] {
  padding-top: 56px !important;
  animation: pageFadeIn 0.6s ease-out both;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: rgba(6,13,31,0.97) !important;
  border-right: 1px solid rgba(148,163,184,0.05) !important;
  top: 56px !important;
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
  border-radius: 0 8px 8px 0 !important;
  padding: 0.42rem 0.8rem 0.42rem 0.95rem !important;
  color: #64748b !important;
  font-size: 0.86rem !important;
  font-weight: 400 !important;
  transition: all 0.15s ease !important;
  cursor: pointer !important;
  margin-left: 0 !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  color: #cbd5e1 !important;
  background: rgba(52,211,153,0.04) !important;
}
/* Active nav item */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  color: #34d399 !important;
  background: linear-gradient(90deg, rgba(52,211,153,0.1), rgba(139,92,246,0.05)) !important;
  border-left-color: #34d399 !important;
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
  color: #334155 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  padding: 0.9rem 0 0.3rem 0.95rem !important;
  margin: 0 !important;
  display: block !important;
}
[data-testid="stSidebar"] .stRadio:first-of-type > label {
  padding-top: 0.3rem !important;
}

/* Sidebar slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div:nth-child(3) {
  background: linear-gradient(90deg, #10b981, #34d399) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div:nth-child(5) {
  background: #34d399 !important;
  border: 2px solid white !important;
}
/* Sidebar selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: rgba(15,23,42,0.8) !important;
  border: 1px solid rgba(148,163,184,0.1) !important;
  border-radius: 10px !important;
}

/* ── Inputs ── */
input[type="text"], input[type="email"], input[type="password"],
[data-baseweb="input"] input, [data-baseweb="base-input"] input {
  background: rgba(10,18,36,0.9) !important;
  border: 1px solid rgba(148,163,184,0.1) !important;
  border-radius: 10px !important;
  color: #e2e8f0 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.875rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
input:focus {
  border-color: rgba(52,211,153,0.4) !important;
  box-shadow: 0 0 0 3px rgba(52,211,153,0.1), 0 0 20px rgba(52,211,153,0.06) !important;
  outline: none !important;
}
input::placeholder,
[data-baseweb="input"] input::placeholder,
[data-baseweb="base-input"] input::placeholder,
textarea::placeholder {
  color: #334155 !important;
  opacity: 1 !important;
}
[data-baseweb="input"], [data-baseweb="base-input"] {
  overflow: hidden !important; border-radius: 10px !important;
}
[data-baseweb="base-input"] > div { background: rgba(10,18,36,0.9) !important; }
[data-testid="InputInstructions"] { display: none !important; }

/* ── Forms ── */
div[data-testid="stForm"] {
  background: transparent !important;
  border-radius: 0 !important;
  padding: 0 !important;
  border: none !important;
}
div[data-testid="stForm"] label {
  color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.88rem !important;
}
[data-testid="stFormSubmitButton"] { margin-top: 0.75rem !important; }
[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] > button {
  background: linear-gradient(135deg, #10b981, #34d399, #a78bfa) !important;
  background-size: 200% 200% !important;
  animation: gradientShift 4s ease infinite !important;
  color: #071020 !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  padding: 0.78rem 1.2rem !important;
  transition: all 0.25s ease !important;
  letter-spacing: 0.01em !important;
}
[data-testid="stFormSubmitButton"] button:hover {
  box-shadow: 0 8px 30px rgba(52,211,153,0.25), 0 0 60px rgba(52,211,153,0.08) !important;
  transform: translateY(-2px) !important;
}
/* Password eye toggle */
button[kind="icon"],
[data-testid="stForm"] button[kind="icon"],
div[data-baseweb="input"] button,
.stTextInput button {
  background: transparent !important;
  border: none !important;
  color: #64748b !important;
}
div[data-baseweb="input"] button:hover,
.stTextInput button:hover {
  color: #34d399 !important;
  background: rgba(52,211,153,0.08) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #10b981, #34d399) !important;
  color: #071020 !important; border: none !important;
  border-radius: 10px !important; font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.52rem 1.1rem !important;
  transition: all 0.2s ease !important;
}
.stButton > button:hover {
  box-shadow: 0 6px 24px rgba(52,211,153,0.25) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
  background: linear-gradient(135deg, #059669, #10b981) !important;
  color: white !important;
}
.stDownloadButton > button:hover {
  background: linear-gradient(135deg, #047857, #059669) !important;
  box-shadow: 0 4px 16px rgba(5,150,105,0.3) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(15,23,42,0.7) !important;
  border-radius: 12px !important;
  border: 1px solid rgba(148,163,184,0.06) !important;
  padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; color: #64748b !important;
  border-radius: 8px !important; font-weight: 500 !important;
  transition: all 0.15s !important; padding: 0.42rem 1.1rem !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(52,211,153,0.12), rgba(139,92,246,0.08)) !important;
  color: #34d399 !important; font-weight: 600 !important;
}

/* ── Multiselect tags ── */
[data-baseweb="tag"] {
  background: rgba(52,211,153,0.08) !important;
  border: 1px solid rgba(52,211,153,0.2) !important;
  border-radius: 8px !important;
}
[data-baseweb="tag"] span { color: #6ee7b7 !important; font-size: 0.8rem !important; }

/* ── Misc ── */
.stAlert { border-radius: 10px !important; }
.stDataFrame { border-radius: 10px !important; overflow: hidden !important; }
[data-testid="stDataFrameContainer"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
}
[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 12px !important;
}

/* ── Glass card utility ── */
.glass-card {
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 1.4rem;
  transition: all 0.25s ease;
}
.glass-card:hover {
  border-color: rgba(52,211,153,0.15);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2), 0 0 40px rgba(52,211,153,0.04);
}

/* Section header utility */
.section-header {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 700; font-size: 0.88rem;
  color: #64748b;
  margin-bottom: 0.9rem;
  padding-bottom: 0.55rem;
  border-bottom: 1px solid rgba(148,163,184,0.07);
  display: flex; align-items: center; gap: 0.5rem;
}

/* Page header utility */
.page-header {
  background: linear-gradient(135deg, rgba(12,20,42,0.7), rgba(15,23,42,0.5));
  backdrop-filter: blur(16px);
  border: 1px solid rgba(148,163,184,0.06);
  border-radius: 16px;
  padding: 1.5rem 2rem;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}
.page-header::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(52,211,153,0.3), rgba(139,92,246,0.3), transparent);
}
.page-header h1 {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.6rem; font-weight: 800; margin: 0;
  background: linear-gradient(135deg, #f1f5f9, #cbd5e1);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.page-header p {
  color: #475569; font-size: 0.85rem; margin: 0.2rem 0 0;
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
@keyframes orbFloat1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(-30px, 40px) scale(1.05); }
  50% { transform: translate(20px, -20px) scale(0.95); }
  75% { transform: translate(-15px, -30px) scale(1.02); }
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 10px rgba(52,211,153,0.1); }
  50% { box-shadow: 0 0 25px rgba(52,211,153,0.2); }
}
@keyframes shimmerLine {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}

.animate-fade-up { animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) both; }
[data-testid="stSidebar"] { animation: pageFadeIn 0.5s ease-out 0.1s both; }
.stMainBlockContainer, [data-testid="stMainBlockContainer"] {
  animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) 0.05s both;
}
</style>
""", unsafe_allow_html=True)

# ── Top Navigation Bar ──
_logo_nav = logo_img_tag(width=28, style="margin:0; border-radius:6px; flex-shrink:0;")
st.markdown(f"""
<div class="hg-topnav">
  <div class="hg-nav-left">
    {_logo_nav}
    <span class="hg-nav-brand">HeartGuard AI</span>
    <div class="hg-nav-sep"></div>
  </div>
  <div class="hg-nav-center">
    <div class="hg-search">
      <svg width="13" height="13" fill="none" stroke="#475569" stroke-width="2" viewBox="0 0 24 24">
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
      background: linear-gradient(150deg, #04091a 0%, #0a1628 40%, #081220 70%, #060e1c 100%);
      border: 1px solid rgba(52,211,153,0.1);
      border-radius: 20px;
      padding: 2.8rem 2.2rem;
      min-height: 560px;
      overflow: hidden;
      animation: slideInLeft 0.65s cubic-bezier(0.16,1,0.3,1) both;
    }
    /* Gradient glow at top */
    .brand-hero::before {
      content: '';
      position: absolute; top: 0; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, transparent, rgba(52,211,153,0.35), rgba(139,92,246,0.35), transparent);
    }
    /* Glow orb */
    .brand-hero::after {
      content: '';
      position: absolute;
      top: -80px; right: -80px;
      width: 280px; height: 280px;
      background: radial-gradient(circle, rgba(52,211,153,0.07) 0%, rgba(139,92,246,0.04) 40%, transparent 70%);
      border-radius: 50%;
      animation: float 10s ease-in-out infinite;
    }

    .brand-content { position: relative; z-index: 1; }

    .brand-content h1 {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.18;
      margin: 0 0 1rem;
    }
    .brand-content h1 .grad-text {
      background: linear-gradient(135deg, #34d399, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-desc {
      color: rgba(148,163,184,0.75);
      font-size: 0.97rem;
      line-height: 1.75;
      margin-bottom: 2rem;
      max-width: 360px;
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
      background: rgba(4,9,20,0.9);
      border: 1px solid rgba(52,211,153,0.1);
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 1.8rem;
      animation: slideInLeft 0.8s cubic-bezier(0.16,1,0.3,1) 0.15s both;
    }
    .ecg-header {
      display: flex; align-items: center; justify-content: space-between;
      background: rgba(8,16,36,0.9);
      border-bottom: 1px solid rgba(52,211,153,0.06);
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
      color: #475569; letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .ecg-bpm {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.1rem; font-weight: 800;
      color: #34d399;
      letter-spacing: -0.01em;
    }
    .ecg-bpm-label { font-size: 0.62rem; color: #334155; margin-left: 0.2rem; }
    .ecg-canvas-wrap {
      overflow: hidden;
      height: 80px;
      position: relative;
      background:
        repeating-linear-gradient(0deg, transparent, transparent 19px, rgba(52,211,153,0.03) 20px),
        repeating-linear-gradient(90deg, transparent, transparent 19px, rgba(52,211,153,0.03) 20px);
    }
    .ecg-svg-track {
      display: flex;
      width: 200%;
      height: 80px;
      animation: ecgLoop 3.2s linear infinite;
    }
    .ecg-svg-track svg { flex-shrink: 0; }
    .ecg-vitals {
      display: flex; gap: 0; border-top: 1px solid rgba(52,211,153,0.05);
    }
    .ecg-vital {
      flex: 1; padding: 0.5rem 0.65rem;
      border-right: 1px solid rgba(52,211,153,0.05);
      text-align: center;
    }
    .ecg-vital:last-child { border-right: none; }
    .ecg-vital-val {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.92rem; font-weight: 700;
      color: #e2e8f0;
    }
    .ecg-vital-key {
      font-size: 0.6rem; color: #334155;
      text-transform: uppercase; letter-spacing: 0.07em;
      margin-top: 0.1rem;
    }
    .ecg-status-ok  { color: #34d399 !important; }
    .ecg-status-warn { color: #fbbf24 !important; }
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
      background: linear-gradient(135deg, rgba(52,211,153,0.05), rgba(139,92,246,0.03));
      border: 1px solid rgba(52,211,153,0.1);
      border-radius: 12px;
      padding: 1rem;
      text-align: center;
    }
    .stat-num {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.5rem; font-weight: 800;
      color: #ffffff; display: block;
    }
    .stat-label {
      color: rgba(100,116,139,0.8);
      font-size: 0.68rem; font-weight: 600;
      text-transform: uppercase; letter-spacing: 1px;
      margin-top: 0.2rem; display: block;
    }
    .shimmer-line {
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(52,211,153,0.25), rgba(139,92,246,0.25), transparent);
      background-size: 200% 100%;
      animation: shimmer 4s linear infinite;
      margin: 1.2rem 0;
    }
    .brand-footer { color: rgba(100,116,139,0.5); font-size: 0.72rem; line-height: 1.8; }

    /* ── Auth card (right) ── */
    .auth-card {
      position: relative;
      background: rgba(8,14,30,0.92);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(148,163,184,0.07);
      border-radius: 20px;
      padding: 2.4rem 2rem 2rem;
      box-shadow: 0 24px 64px rgba(0,0,0,0.5), 0 0 80px rgba(52,211,153,0.03);
      animation: slideInRight 0.65s cubic-bezier(0.16,1,0.3,1) 0.1s both;
    }
    .auth-card::before {
      content: '';
      position: absolute;
      top: 0; left: 40px; right: 40px; height: 1px;
      background: linear-gradient(90deg, transparent, rgba(52,211,153,0.25), rgba(139,92,246,0.25), transparent);
    }
    .auth-card label,
    .auth-card [data-testid="stForm"] label {
      color: #94a3b8 !important; font-weight: 600 !important; font-size: 0.88rem !important;
    }
    .auth-footer { text-align:center; margin-top:1.1rem; color:#64748b; font-size:0.84rem; }
    .auth-footer b { color: #34d399; }
    </style>""", unsafe_allow_html=True)

    left_col, gap, right_col = st.columns([1.15, 0.05, 1])

    with left_col:
        logo_tag = logo_img_tag(width=140, style="margin:0 0 1.6rem;")
        st.markdown(f"""<div class="brand-hero">
<div class="brand-content">

{logo_tag}

<h1>Smarter<br><span class="grad-text">Heart Health</span><br>Starts Here.</h1>

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
          stroke="#34d399" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
          fill="none"
        />
      </svg>
      <svg width="600" height="80" viewBox="0 0 600 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <polyline
          points="0,40 30,40 45,40 50,38 55,40 70,40 80,40 90,20 95,5 100,65 105,15 110,40 130,40 150,40 160,38 165,40 180,40 190,40 200,20 205,5 210,65 215,15 220,40 240,40 260,40 270,38 275,40 290,40 300,40 310,20 315,5 320,65 325,15 330,40 350,40 370,40 380,38 385,40 400,40 410,40 420,20 425,5 430,65 435,15 440,40 460,40 480,40 490,38 495,40 510,40 520,40 530,20 535,5 540,65 545,15 550,40 570,40 590,40 600,40"
          stroke="#34d399" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
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
<h3 style="font-family:'Plus Jakarta Sans',sans-serif; color:#f8fafc; font-size:1.65rem; font-weight:700; margin:0 0 0.4rem;">Welcome Back</h3>
<p style="color:#64748b; font-size:0.93rem; margin:0; line-height:1.6;">Sign in to access your health dashboard</p>
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
<h3 style="font-family:'Plus Jakarta Sans',sans-serif; color:#f8fafc; font-size:1.65rem; font-weight:700; margin:0 0 0.4rem;">Create Account</h3>
<p style="color:#64748b; font-size:0.93rem; margin:0; line-height:1.6;">Join and start monitoring your cardiac health</p>
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

    # Profile card with glow ring
    st.sidebar.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(12,20,42,0.8), rgba(15,23,42,0.6));
         border:1px solid rgba(148,163,184,0.06);
         border-radius:14px; padding:0.8rem; text-align:center; margin: 0.4rem 0 0.8rem;">
        <div style="width:38px; height:38px; margin:0 auto 0.4rem;
             background:linear-gradient(135deg,#34d399,#a78bfa);
             border-radius:50%; display:flex; align-items:center; justify-content:center;
             font-size:0.95rem; font-weight:700; color:#071020;
             box-shadow: 0 0 20px rgba(52,211,153,0.2);">{st.session_state.user[0].upper()}</div>
        <div style="font-weight:600; font-size:0.85rem; color:#e2e8f0;">{st.session_state.user}</div>
        <div style="font-size:0.68rem; color:#334155; margin-top:0.1rem;">HeartGuard Patient</div>
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
    <div style="margin-top:0.8rem; padding:0.7rem;
         background:linear-gradient(135deg, rgba(12,20,42,0.5), rgba(15,23,42,0.3));
         border:1px solid rgba(148,163,184,0.04); border-radius:12px;
         font-size:0.7rem; color:#1e293b; line-height:1.8; text-align:center;">
        {logo_img_tag(width=72, style="margin:0 auto 0.35rem; opacity:0.6;")}
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
