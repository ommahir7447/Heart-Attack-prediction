import streamlit as st
from utils.db import get_doctors, get_all_cities, book_appointment, get_health_profile

SPECIALTIES = ["All Specialties", "Cardiologist", "Cardiac Surgeon", "General Physician"]

def star_rating(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    return "★" * full + "½" * half + "☆" * (5 - full - half)

def render_doctors():
    st.markdown("""<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08); border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;"><h1 style="font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700; margin:0; color:#e2e8f0;">Find Doctors</h1><p style="color:#64748b; font-size:0.85rem; margin:0.15rem 0 0;">Connect with cardiologists and specialists — request an appointment instantly</p></div>""", unsafe_allow_html=True)

    profile = get_health_profile(st.session_state.user_email) or {}
    profile_city = profile.get("city", "Mumbai")
    all_cities = ["All Cities"] + get_all_cities()
    default_city_idx = all_cities.index(profile_city) if profile_city in all_cities else 0

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        selected_city = st.selectbox("Filter by City", all_cities, index=default_city_idx)
    with fc2:
        selected_specialty = st.selectbox("Filter by Specialty", SPECIALTIES)
    with fc3:
        available_only = st.checkbox("Available Now Only", value=False)

    doctors = get_doctors(
        city=selected_city if selected_city != "All Cities" else None,
        specialty=selected_specialty if selected_specialty != "All Specialties" else None,
        available_only=available_only
    )

    st.markdown(f"<p style='color:#64748b; margin:0.6rem 0; font-size:0.85rem;'>Found <b style='color:#e2e8f0;'>{len(doctors)}</b> doctors matching your criteria</p>", unsafe_allow_html=True)

    if not doctors:
        st.markdown("""
        <div style="text-align:center; padding:3rem; background:rgba(30,41,59,0.4);
             border:1px dashed rgba(148,163,184,0.15); border-radius:12px;">
            <div style="font-size:1.5rem; color:#64748b;">—</div>
            <div style="color:#e2e8f0; font-weight:600; margin-top:0.5rem;">No doctors found</div>
            <div style="color:#64748b; font-size:0.85rem;">Try changing your filters</div>
        </div>
        """, unsafe_allow_html=True)
        return

    cards_left, cards_right = st.columns(2)
    for i, doc in enumerate(doctors):
        col = cards_left if i % 2 == 0 else cards_right
        avail_badge = (
            "<span style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); border-radius:20px; padding:0.2rem 0.6rem; font-size:0.72rem; color:#10b981;'>● Available</span>"
            if doc["available"] else
            "<span style='background:rgba(100,116,139,0.1); border:1px solid rgba(100,116,139,0.2); border-radius:20px; padding:0.2rem 0.6rem; font-size:0.72rem; color:#64748b;'>○ Booking Only</span>"
        )
        specialty_color = {
            "Cardiologist": "#38bdf8", "Cardiac Surgeon": "#ef4444", "General Physician": "#10b981"
        }.get(doc["specialty"], "#94a3b8")

        col.markdown(f"""
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
             border-radius:12px; padding:1.1rem 1.2rem; margin-bottom:0.8rem;
             transition:all 0.15s ease;"
             onmouseover="this.style.borderColor='rgba(56,189,248,0.22)'"
             onmouseout="this.style.borderColor='rgba(148,163,184,0.08)'">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.7rem;">
                <div>
                    <div style="font-weight:700; font-size:1rem; color:#e2e8f0;">{doc['name']}</div>
                    <div style="color:{specialty_color}; font-size:0.8rem; font-weight:600; margin-top:0.15rem;">{doc['specialty']}</div>
                    <div style="color:#64748b; font-size:0.78rem; margin-top:0.1rem;">{doc['hospital']} · {doc['city']}</div>
                </div>
                {avail_badge}
            </div>
            <div style="display:flex; gap:1.2rem; font-size:0.8rem; color:#94a3b8; margin-bottom:0.6rem;">
                <span>Rating: <b style="color:#f59e0b;">{doc['rating']}</b>/5.0</span>
                <span>{doc['experience']} yrs exp</span>
                <span>{doc['fee']}</span>
            </div>
            <div style="font-size:0.78rem; color:#64748b;">Ph: {doc['phone']}</div>
        </div>
        """, unsafe_allow_html=True)

        btn_key = f"book_{doc['name'].replace(' ', '_')}_{i}"
        if col.button(f"Book with {doc['name'].split()[1]} {doc['name'].split()[-1]}", key=btn_key, use_container_width=True):
            risk_pct = st.session_state.get("last_risk_pct", 35.0)
            book_appointment(st.session_state.user_email, doc["name"], doc["hospital"], doc["specialty"], risk_pct)
            st.success(f"Appointment requested with **{doc['name']}**! Check My Updates for the response.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(14,165,233,0.05); border:1px solid rgba(14,165,233,0.11);
         border-radius:8px; padding:0.8rem 1.1rem; font-size:0.8rem; color:#7dd3fc;">
        <b>Note:</b> This is a demo platform. Appointments are simulated for educational purposes.
    </div>
    """, unsafe_allow_html=True)
