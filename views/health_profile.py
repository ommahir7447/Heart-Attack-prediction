import streamlit as st
from utils.db import save_health_profile, get_health_profile

CONDITIONS = ["Hypertension", "Type 2 Diabetes", "High Cholesterol", "Coronary Artery Disease",
              "Atrial Fibrillation", "Heart Failure", "Obesity", "Family History of Heart Disease",
              "Chronic Kidney Disease", "Thyroid Disorder", "Anemia"]

MEDICATIONS = ["Aspirin", "Metformin", "Statins (Atorvastatin)", "Beta-Blockers (Metoprolol)",
               "ACE Inhibitors (Enalapril)", "Calcium Channel Blockers (Amlodipine)",
               "Diuretics (Furosemide)", "Warfarin / Blood Thinners", "Insulin", "Nitroglycerin"]

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Chandigarh", "Lucknow", "Other"]

def render_health_profile():
    st.markdown("""<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;">
<div style="display:flex; align-items:center; gap:0.8rem;">
<div>
<h1 style="font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700; margin:0; color:#e2e8f0;">
My Health Profile</h1>
<p style="color:#64748b; font-size:0.85rem; margin:0.15rem 0 0 0;">
Your personal health record — helps us tailor analysis, precautions, and doctor matches</p>
</div>
</div>
</div>""", unsafe_allow_html=True)

    existing = get_health_profile(st.session_state.user_email) or {}

    with st.form("health_profile_form"):
        st.markdown("""<div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
Personal Information
</div>""", unsafe_allow_html=True)
        pc1, pc2 = st.columns(2)
        with pc1:
            dob_age = st.number_input("Your Age", min_value=18, max_value=110, value=existing.get("age", 50))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                  index=["Male", "Female", "Other"].index(existing.get("gender", "Male")))
        with pc2:
            city = st.selectbox("Your City", CITIES,
                                index=CITIES.index(existing.get("city", "Mumbai")) if existing.get("city") in CITIES else 0)
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
                                       index=["A+","A-","B+","B-","O+","O-","AB+","AB-"].index(existing.get("blood_group","O+")) if existing.get("blood_group") else 0)
        emergency_contact = st.text_input("Emergency Contact Name & Phone", value=existing.get("emergency_contact", ""))

        st.markdown("""<div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
margin:1.2rem 0 0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
Known Conditions
</div>""", unsafe_allow_html=True)
        st.caption("Select all conditions that apply to you:")
        selected_conditions = st.multiselect("Conditions", CONDITIONS, default=existing.get("conditions", []))

        st.markdown("""<div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
margin:1.2rem 0 0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
Current Medications
</div>""", unsafe_allow_html=True)
        selected_meds = st.multiselect("Medications", MEDICATIONS, default=existing.get("medications", []))
        other_meds = st.text_input("Other medications (free text)", value=existing.get("other_meds", ""))

        st.markdown("""<div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
margin:1.2rem 0 0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
Lifestyle
</div>""", unsafe_allow_html=True)
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            smoker = st.selectbox("Smoking Status", ["Non-Smoker", "Ex-Smoker", "Current Smoker"],
                                  index=["Non-Smoker", "Ex-Smoker", "Current Smoker"].index(existing.get("smoker", "Non-Smoker")))
        with lc2:
            activity = st.selectbox("Physical Activity", ["Sedentary", "Light (1-2x/week)", "Moderate (3-4x/week)", "Active (5+/week)"],
                                    index=["Sedentary","Light (1-2x/week)","Moderate (3-4x/week)","Active (5+/week)"].index(existing.get("activity", "Sedentary")))
        with lc3:
            diet = st.selectbox("Diet Type", ["Regular", "Vegetarian", "Vegan", "Low-Sodium", "Diabetic Diet"],
                                index=["Regular","Vegetarian","Vegan","Low-Sodium","Diabetic Diet"].index(existing.get("diet", "Regular")))
        alcohol = st.selectbox("Alcohol Consumption", ["None", "Occasional", "Moderate", "Heavy"],
                               index=["None","Occasional","Moderate","Heavy"].index(existing.get("alcohol", "None")))

        submitted = st.form_submit_button("Save Health Profile", use_container_width=True)

    if submitted:
        profile_data = {
            "age": dob_age, "gender": gender, "city": city, "blood_group": blood_group,
            "emergency_contact": emergency_contact, "conditions": selected_conditions,
            "medications": selected_meds, "other_meds": other_meds,
            "smoker": smoker, "activity": activity, "diet": diet, "alcohol": alcohol,
        }
        save_health_profile(st.session_state.user_email, profile_data)
        st.session_state.health_profile = profile_data
        st.success("Health profile saved! Your analysis and doctor matches are now personalised.")
        st.snow()

    if existing:
        st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
        st.markdown("""<div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
Current Profile Summary
</div>""", unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        for col, label, val in [
            (s1, "City", existing.get("city", "—")),
            (s2, "Blood Group", existing.get("blood_group", "—")),
            (s3, "Smoking", existing.get("smoker", "—")),
            (s4, "Activity", existing.get("activity", "—")),
        ]:
            col.markdown(f"""<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
border-radius:10px; padding:1rem; text-align:center;">
<div style="font-size:1rem; font-weight:700; color:#e2e8f0; margin-top:0.2rem;">{val}</div>
<div style="font-size:0.68rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin-top:0.2rem;">{label}</div>
</div>""", unsafe_allow_html=True)

        if existing.get("conditions"):
            st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
            conditions_html = " ".join([
                f"<span style='background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2); border-radius:20px; padding:0.25rem 0.7rem; font-size:0.78rem; color:#fca5a5; margin:0.15rem; display:inline-block;'>{c}</span>"
                for c in existing["conditions"]
            ])
            st.markdown(f"<div><b style='color:#94a3b8; font-size:0.85rem;'>Known Conditions:</b><div style='margin-top:0.4rem;'>{conditions_html}</div></div>", unsafe_allow_html=True)
