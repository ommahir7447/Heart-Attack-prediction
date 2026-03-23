import streamlit as st

st.set_page_config(page_title="HeartGuard AI", page_icon="🫀", layout="wide", initial_sidebar_state="expanded")

# ── Tailwind CDN + Custom Theme + Streamlit Widget Overrides ──
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: { 50:'#f5f3ff',100:'#ede9fe',200:'#ddd6fe',300:'#c4b5fd',400:'#a78bfa',500:'#8b5cf6',600:'#7c3aed',700:'#6d28d9',800:'#5b21b6',900:'#4c1d95' },
        surface: { DEFAULT:'#0f172a', light:'#1e293b', lighter:'#334155' },
      },
      fontFamily: { sans: ['Inter','system-ui','sans-serif'], heading: ['Sora','Inter','sans-serif'] },
    }
  }
}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet">

<style>
/* ═══════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES (Tailwind style)
   ═══════════════════════════════════════ */

*, *::before, *::after { box-sizing: border-box; }

.stApp {
  background: #0f172a !important;
  font-family: 'Inter', system-ui, sans-serif;
  color: #e2e8f0;
}

/* Subtle radial gradient overlay */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 70% 50% at 20% 20%, rgba(139,92,246,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 80% 70%, rgba(6,182,212,0.05) 0%, transparent 55%);
  pointer-events: none; z-index: 0;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  color: #e2e8f0 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.5); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #0f172a !important;
  border-right: 1px solid rgba(148,163,184,0.08) !important;
}
[data-testid="stSidebar"] > div:first-child { background: transparent !important; }
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: #cbd5e1 !important; }

/* Sidebar radio nav */
[data-testid="stSidebar"] .stRadio > label {
  color: rgba(148,163,184,0.5) !important;
  font-size: 0.68rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1.5px;
  margin-bottom: 0.3rem; margin-top: 0.5rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 2px; display: flex; flex-direction: column; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  background: transparent !important;
  border: 1px solid transparent !important;
  border-radius: 8px !important;
  padding: 0.5rem 0.75rem !important;
  color: #94a3b8 !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  transition: all 0.15s ease !important;
  cursor: pointer !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: rgba(139,92,246,0.08) !important;
  color: #c4b5fd !important;
}

/* Sidebar slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div:nth-child(3) {
  background: linear-gradient(90deg, #8b5cf6, #06b6d4) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div:nth-child(5) {
  background: #a78bfa !important;
  border: 2px solid white !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: rgba(30,41,59,0.8) !important;
  border: 1px solid rgba(148,163,184,0.12) !important;
  border-radius: 8px !important;
}

/* ── Inputs ── */
input[type="text"], input[type="email"], input[type="password"],
[data-baseweb="input"] input, [data-baseweb="base-input"] input {
  background: #1e293b !important;
  border: 1px solid rgba(148,163,184,0.15) !important;
  border-radius: 8px !important;
  color: #e2e8f0 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.875rem !important;
  transition: border-color 0.15s, box-shadow 0.15s !important;
}
input:focus {
  border-color: #8b5cf6 !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
  outline: none !important;
}

[data-baseweb="input"], [data-baseweb="base-input"] {
  overflow: hidden !important; border-radius: 8px !important;
}
[data-baseweb="base-input"] > div { background: #1e293b !important; }

/* Hide "Press Enter to submit" */
[data-testid="InputInstructions"] {
  display: none !important;
}

/* ── Forms ── */
div[data-testid="stForm"] {
  background: rgba(30,41,59,0.5) !important;
  border-radius: 12px !important;
  padding: 1.5rem !important;
  border: 1px solid rgba(148,163,184,0.1) !important;
}
div[data-testid="stForm"] label {
  color: #94a3b8 !important; font-weight: 500 !important; font-size: 0.8rem !important;
}

[data-testid="stFormSubmitButton"] { margin-top: 0.75rem !important; }

/* Form submit button — force violet */
[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] > button {
  background: #7c3aed !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 0.6rem 1.2rem !important;
  transition: all 0.15s ease !important;
}
[data-testid="stFormSubmitButton"] button:hover {
  background: #6d28d9 !important;
  box-shadow: 0 4px 12px rgba(124,58,237,0.3) !important;
}

/* Password eye toggle — remove white bg */
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
  background: #7c3aed !important;
  color: white !important; border: none !important;
  border-radius: 8px !important; font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 0.5rem 1rem !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover {
  background: #6d28d9 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(124,58,237,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
  background: #059669 !important;
}
.stDownloadButton > button:hover {
  background: #047857 !important;
  box-shadow: 0 4px 12px rgba(5,150,105,0.3) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(30,41,59,0.6) !important;
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
  background: #7c3aed !important;
  color: white !important; font-weight: 600 !important;
}

/* ── Multiselect ── */
[data-baseweb="tag"] {
  background: rgba(139,92,246,0.15) !important;
  border: 1px solid rgba(139,92,246,0.3) !important;
  border-radius: 6px !important;
}
[data-baseweb="tag"] span { color: #c4b5fd !important; font-size: 0.8rem !important; }

/* ── Alerts ── */
.stAlert { border-radius: 8px !important; }

/* ── DataFrame ── */
.stDataFrame { border-radius: 8px !important; overflow: hidden !important; }
[data-testid="stDataFrameContainer"] {
  background: rgba(30,41,59,0.4) !important;
  border: 1px solid rgba(148,163,184,0.08) !important;
  border-radius: 8px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
  background: rgba(30,41,59,0.4) !important;
  border: 1px solid rgba(148,163,184,0.08) !important;
  border-radius: 10px !important;
}

/* ── Animation ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  14%      { transform: scale(1.2); }
  28%      { transform: scale(1); }
  42%      { transform: scale(1.12); }
  70%      { transform: scale(1); }
}
.animate-fade-up { animation: fadeUp 0.5s cubic-bezier(0.16,1,0.3,1) both; }
.animate-heartbeat { display: inline-block; animation: heartbeat 1.8s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)


# ── Auth imports (lightweight) ──
from utils.auth import login_user, signup_user

# Session state
for key, default in [('logged_in', False), ('user', None), ('user_email', None)]:
    if key not in st.session_state:
        st.session_state[key] = default

def auth_page():
    st.markdown("""
    <div class="animate-fade-up" style="text-align:center; padding:3rem 2rem;">
        <div class="animate-heartbeat" style="font-size:3.5rem; margin-bottom:0.5rem;">🫀</div>
        <h1 style="font-family:'Sora',sans-serif; font-size:2.8rem; font-weight:800;
            background:linear-gradient(135deg, #c4b5fd, #67e8f9, #f9a8d4);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            letter-spacing:-0.03em; margin:0;">HeartGuard AI</h1>
        <p style="color:#64748b; font-size:1rem; margin-top:0.4rem;">
            Advanced Cardiac Risk Stratification Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        st.markdown("""
        <div class="animate-fade-up" style="animation-delay:0.1s;
            background: rgba(30,41,59,0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(148,163,184,0.1);
            border-radius: 16px;
            padding: 2rem 1.8rem;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);">
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐  Login", "✨  Sign Up"])

        with tab1:
            with st.form("login_form"):
                st.markdown("""
                <h3 style="font-family:'Sora',sans-serif; color:#e2e8f0; font-size:1.5rem;
                    font-weight:700; margin-bottom:0.2rem;">Welcome Back</h3>
                <p style="color:#64748b; font-size:0.85rem; margin-bottom:1.2rem;">
                    Sign in to access your cardiac risk dashboard</p>
                """, unsafe_allow_html=True)
                login_email = st.text_input("Email Address", placeholder="you@example.com")
                login_password = st.text_input("Password", type="password", placeholder="••••••••")
                submit_login = st.form_submit_button("Sign In  →", use_container_width=True)
                if submit_login:
                    if login_email and login_password:
                        if login_user(login_email, login_password):
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password.")
                    else:
                        st.warning("Please fill in all fields.")

        with tab2:
            with st.form("signup_form"):
                st.markdown("""
                <h3 style="font-family:'Sora',sans-serif; color:#e2e8f0; font-size:1.5rem;
                    font-weight:700; margin-bottom:0.2rem;">Create Account</h3>
                <p style="color:#64748b; font-size:0.85rem; margin-bottom:1.2rem;">
                    Join HeartGuard to start monitoring your cardiac health</p>
                """, unsafe_allow_html=True)
                signup_name = st.text_input("Full Name", placeholder="Dr. Jane Smith")
                signup_email = st.text_input("Email Address", placeholder="jane@hospital.com")
                signup_password = st.text_input("Password", type="password", placeholder="••••••••")
                signup_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                submit_signup = st.form_submit_button("Create Account  →", use_container_width=True)
                if submit_signup:
                    if signup_name and signup_email and signup_password and signup_confirm:
                        success, msg = signup_user(signup_name, signup_email, signup_password, signup_confirm)
                        if success:
                            st.success("✅ " + msg + " Please login.")
                        else:
                            st.error("❌ " + msg)
                    else:
                        st.warning("Please fill in all fields.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Feature pills ──
    st.markdown("<br>", unsafe_allow_html=True)
    f1, f2, f3, f4, f5, f6 = st.columns(6)
    for col, icon, title, desc in [
        (f1, "🤖", "AI Prediction", "XGBoost · 84%"),
        (f2, "🔬", "Deep Analysis", "Per-metric insight"),
        (f3, "🛡️", "Precautions", "Personalised advice"),
        (f4, "👨‍⚕️", "Find Doctors", "City directory"),
        (f5, "📬", "Updates", "Real-time notes"),
        (f6, "📋", "History", "Track assessments"),
    ]:
        col.markdown(f"""
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
             border-radius:10px; padding:1rem 0.5rem; text-align:center;
             transition:all 0.15s ease; cursor:default;"
             onmouseover="this.style.borderColor='rgba(139,92,246,0.3)';this.style.transform='translateY(-3px)'"
             onmouseout="this.style.borderColor='rgba(148,163,184,0.08)';this.style.transform='translateY(0)'">
            <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
            <div style="font-weight:600; color:#e2e8f0; font-size:0.78rem;">{title}</div>
            <div style="color:#64748b; font-size:0.7rem; margin-top:0.15rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


if st.session_state.logged_in:
    # ── Lazy imports ──
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
    updates_label = f"📬  My Updates{'  🔴' if unread > 0 else ''}"

    # ── Sidebar ──
    st.sidebar.markdown(f"""
    <div style="background:rgba(30,41,59,0.6); border:1px solid rgba(148,163,184,0.08);
         border-radius:12px; padding:1rem; text-align:center; margin-bottom:1rem;">
        <div style="width:44px; height:44px; margin:0 auto 0.5rem;
             background:linear-gradient(135deg,#8b5cf6,#06b6d4);
             border-radius:50%; display:flex; align-items:center; justify-content:center;
             font-size:1.3rem;">👤</div>
        <div style="font-weight:600; font-size:0.9rem; color:#e2e8f0;">{st.session_state.user}</div>
        <div style="font-size:0.72rem; color:#64748b; margin-top:0.1rem;">HeartGuard Patient</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.sidebar.radio(
        "Navigation",
        [
            "📟  Dashboard",
            "🧬  My Health Profile",
            "🔬  Deep Analysis",
            "🛡️  Precautions",
            "👨‍⚕️  Find Doctors",
            updates_label,
            "📖  History",
        ],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪  Sign Out", use_container_width=True):
        from utils.auth import logout
        logout()
        st.rerun()

    st.sidebar.markdown("""
    <div style="margin-top:1rem; padding:0.8rem; background:rgba(30,41,59,0.5);
         border:1px solid rgba(148,163,184,0.06); border-radius:10px;
         font-size:0.72rem; color:#64748b; line-height:1.6; text-align:center;">
        🧠 <b style="color:#c4b5fd;">HeartGuard AI</b><br>
        XGBoost · SHAP · MongoDB<br>
        v3.0 · Health Companion
    </div>
    """, unsafe_allow_html=True)

    # ── Route pages ──
    if page == "📟  Dashboard":
        render_dashboard()
    elif page == "🧬  My Health Profile":
        render_health_profile()
    elif page == "🔬  Deep Analysis":
        render_analysis()
    elif page == "🛡️  Precautions":
        render_precautions()
    elif page == "👨‍⚕️  Find Doctors":
        render_doctors()
    elif "My Updates" in page:
        render_updates()
    elif page == "📖  History":
        render_history()
else:
    auth_page()
