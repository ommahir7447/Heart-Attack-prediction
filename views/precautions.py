import streamlit as st
from utils.db import get_health_profile

def render_precautions():
    st.markdown("""<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08); border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;"><h1 style="font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700; margin:0; color:#e2e8f0;">Precautions &amp; Recommendations</h1><p style="color:#64748b; font-size:0.85rem; margin:0.15rem 0 0;">Personalized health guidance based on your profile and cardiac risk assessment</p></div>""", unsafe_allow_html=True)

    profile = get_health_profile(st.session_state.user_email) or {}
    conditions = profile.get("conditions", [])
    medications = profile.get("medications", [])
    smoker = profile.get("smoker", "Non-Smoker")
    activity = profile.get("activity", "Sedentary")
    alcohol = profile.get("alcohol", "None")
    age = profile.get("age", 50)
    risk_pct = st.session_state.get("last_risk_pct", 0.0)

    if not profile:
        st.warning("Please fill in your **My Health Profile** first so we can personalise your recommendations.")

    # ── EMERGENCY SIGNS ──
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        Warning Signs — Call Emergency Immediately
    </div>
    """, unsafe_allow_html=True)
    emergency_signs = [
        ("Chest Pain", "Severe pressure, tightness, or crushing feeling in chest — especially radiating to left arm, jaw, or back."),
        ("Sudden Breathlessness", "Difficulty breathing without exertion, especially at rest or while lying flat."),
        ("Sudden Weakness / Numbness", "Sudden weakness or numbness on one side of the body — possible stroke sign."),
        ("Rapid Irregular Heartbeat", "Heart pounding, fluttering, or racing suddenly — especially with dizziness."),
        ("Fainting / Loss of Consciousness", "Sudden loss of consciousness or near-fainting, especially during exertion."),
    ]
    eg1, eg2 = st.columns(2)
    for i, (sign, desc) in enumerate(emergency_signs):
        col = eg1 if i % 2 == 0 else eg2
        col.markdown(f"""
        <div style="background:rgba(239,68,68,0.06); border:1px solid rgba(239,68,68,0.15);
             border-radius:10px; padding:0.9rem 1rem; margin-bottom:0.5rem; display:flex; align-items:flex-start; gap:0.7rem;">
            <div style="font-size:1rem; margin-top:0.05rem; color:#ef4444; font-weight:700;">!</div>
            <div>
                <div style="font-weight:600; color:#ef4444; font-size:0.85rem;">{sign}</div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-top:0.15rem; line-height:1.5;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── DIET ──
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        Diet Recommendations
    </div>
    """, unsafe_allow_html=True)
    diet_tips = [
        ("Reduce Sodium", "Keep daily sodium under 1,500 mg. Avoid packaged, processed, and restaurant foods.", "#06b6d4"),
        ("Heart-Healthy Fats", "Choose olive oil, avocados, nuts and seeds. Avoid trans fats and limit saturated fats.", "#8b5cf6"),
        ("Increase Fibre", "Eat oats, whole grains, lentils, and vegetables daily. Soluble fibre reduces LDL cholesterol.", "#10b981"),
        ("Omega-3 Rich Foods", "Include fatty fish (salmon, mackerel), flaxseeds, and walnuts. Omega-3s reduce inflammation.", "#06b6d4"),
        ("Limit Refined Sugar", "Avoid sugary drinks, sweets, and white bread. High sugar raises triglycerides.", "#f59e0b"),
    ]
    if "Type 2 Diabetes" in conditions:
        diet_tips.append(("Diabetic Diet", "Follow a low GI diet. Avoid fruit juices, white rice, potatoes.", "#ef4444"))
    if "High Cholesterol" in conditions:
        diet_tips.append(("Anti-Cholesterol Diet", "Eat 30g of almonds daily. Include plant sterols. Reduce full-fat dairy.", "#8b5cf6"))

    dc = st.columns(3)
    for i, (title, desc, color) in enumerate(diet_tips):
        dc[i % 3].markdown(f"""
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
             border-radius:10px; padding:0.9rem; margin-bottom:0.5rem; border-top:3px solid {color};">
            <div style="font-weight:600; color:{color}; font-size:0.85rem;">{title}</div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-top:0.25rem; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EXERCISE ──
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        Exercise Guidelines
    </div>
    """, unsafe_allow_html=True)

    if risk_pct >= 60:
        exercise_note = "High cardiac risk detected. **Only light, supervised exercise** until you consult your cardiologist."
        exercises = [("Slow Walking", "15–20 min/day on flat ground. Stop if you feel chest pain."),
                     ("Seated Yoga", "Gentle stretching and pranayama breathing. 15 min morning and evening."),
                     ("Avoid Strenuous Activity", "Strenuous gym workouts, running, heavy lifting until cleared by doctor.")]
    elif activity == "Sedentary":
        exercise_note = "Start gradually. Even light movement every day significantly reduces cardiac risk."
        exercises = [("Brisk Walking", "30 min/day, 5 days/week. Start at a comfortable pace."),
                     ("Swimming", "Excellent low-impact cardio, 30 min 3x/week."),
                     ("Yoga / Pranayama", "Daily breathing exercises reduce blood pressure and stress.")]
    else:
        exercise_note = "Maintain your current routine. Heart health improves with consistent moderate activity."
        exercises = [("Cycling", "30–45 min, 4–5x/week. Moderate intensity."),
                     ("Strength Training", "2–3x/week, light weights, focus on form."),
                     ("Meditation", "10–15 min daily reduces cortisol and inflammation.")]

    st.markdown(f"<p style='color:#94a3b8; margin-bottom:0.8rem; font-size:0.85rem;'>{exercise_note}</p>", unsafe_allow_html=True)
    ec = st.columns(3)
    for i, (name, desc) in enumerate(exercises):
        ec[i % 3].markdown(f"""
        <div style="background:rgba(16,185,129,0.05); border:1px solid rgba(16,185,129,0.12);
             border-radius:10px; padding:0.9rem;">
            <div style="font-weight:600; color:#10b981; font-size:0.85rem;">{name}</div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-top:0.2rem; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MEDICATIONS ──
    if medications:
        st.markdown("""
        <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
             margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
            Medication Reminders
        </div>
        """, unsafe_allow_html=True)
        med_tips = {
            "Aspirin": ("Take after food to prevent stomach upset. Never stop suddenly.", "morning"),
            "Metformin": ("Take with meals to reduce GI side effects. Monitor blood sugar.", "morning & evening"),
            "Statins (Atorvastatin)": ("Best taken at night. Avoid grapefruit juice. Report muscle pain.", "bedtime"),
            "Beta-Blockers (Metoprolol)": ("Never miss a dose. Can cause dizziness — rise slowly.", "morning"),
            "ACE Inhibitors (Enalapril)": ("Can cause dry cough — report to doctor. Monitor potassium.", "morning"),
            "Calcium Channel Blockers (Amlodipine)": ("Take at same time daily. Avoid grapefruit.", "morning"),
            "Diuretics (Furosemide)": ("Take in morning to avoid nighttime urination.", "morning"),
            "Warfarin / Blood Thinners": ("Take at same time every day. Avoid NSAIDs. Regular INR testing.", "evening"),
            "Insulin": ("Rotate injection sites. Monitor blood sugar before meals.", "as prescribed"),
            "Nitroglycerin": ("Use only during chest pain. Sit or lie down first.", "as needed"),
        }
        mc = st.columns(2)
        for i, med in enumerate(medications):
            info = med_tips.get(med, ("Follow your doctor's prescription carefully.", "as prescribed"))
            mc[i % 2].markdown(f"""
            <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
                 border-radius:10px; padding:0.9rem 1.1rem; margin-bottom:0.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-weight:600; color:#e2e8f0; font-size:0.85rem;">{med}</div>
                    <div style="background:rgba(6,182,212,0.08); border:1px solid rgba(6,182,212,0.2);
                         border-radius:20px; padding:0.15rem 0.5rem; font-size:0.7rem; color:#67e8f9;">{info[1]}</div>
                </div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-top:0.3rem; line-height:1.5;">{info[0]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── LIFESTYLE ALERTS ──
    alerts = []
    if smoker == "Current Smoker":
        alerts.append(("Quit Smoking — Priority #1", "Smoking doubles heart attack risk. Nicotine patches, gum, or medications can help.", "#ef4444"))
    if alcohol in ["Moderate", "Heavy"]:
        alerts.append(("Reduce Alcohol", "Alcohol raises blood pressure and triglycerides. Limit to 1-2 units/day.", "#f59e0b"))
    if age >= 60:
        alerts.append(("Senior Heart Care", "Get annual ECG, echocardiogram, and full lipid panel.", "#8b5cf6"))

    if alerts:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
             margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
            Lifestyle Alerts
        </div>
        """, unsafe_allow_html=True)
        for title, desc, color in alerts:
            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.4); border:1px solid rgba(148,163,184,0.08);
                 border-radius:10px; padding:0.9rem 1.2rem; margin-bottom:0.5rem; border-left:3px solid {color};">
                <div style="font-weight:600; color:{color}; margin-bottom:0.2rem;">{title}</div>
                <div style="color:#94a3b8; font-size:0.85rem; line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
