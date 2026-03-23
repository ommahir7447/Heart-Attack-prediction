import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
import shap
from utils.model import load_artifacts
from utils.db import save_prediction


def render_dashboard():
    model, feature_names = load_artifacts()
    if model is None:
        st.error("Model not found. Please run `python train_model.py` first.")
        st.stop()

    # ── SIDEBAR INPUTS ──
    st.sidebar.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#94a3b8;font-weight:600;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;'>👤 Demographics</p>", unsafe_allow_html=True)
    age = st.sidebar.slider("Age", 20, 90, 50)
    sex = st.sidebar.selectbox("Sex", [0, 1], format_func=lambda x: "♂ Male" if x == 1 else "♀ Female")

    st.sidebar.markdown("<p style='color:#94a3b8;font-weight:600;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;margin-top:1rem;'>❤️ Symptoms</p>", unsafe_allow_html=True)
    cp_mapping = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal Pain", 3: "Asymptomatic"}
    cp = st.sidebar.selectbox("Chest Pain Type", [0, 1, 2, 3], format_func=lambda x: cp_mapping[x])
    exang = st.sidebar.selectbox("Exercise-Induced Angina", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    st.sidebar.markdown("<p style='color:#94a3b8;font-weight:600;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;margin-top:1rem;'>📊 Clinical Metrics</p>", unsafe_allow_html=True)
    trestbps = st.sidebar.slider("Resting Blood Pressure (mmHg)", 80, 200, 120)
    chol = st.sidebar.slider("Cholesterol (mg/dl)", 100, 600, 200)
    fbs = st.sidebar.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    thalach = st.sidebar.slider("Max Heart Rate (bpm)", 60, 220, 150)

    st.sidebar.markdown("<p style='color:#94a3b8;font-weight:600;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;margin-top:1rem;'>🔬 Diagnostics</p>", unsafe_allow_html=True)
    restecg_mapping = {0: "Normal", 1: "ST-T Abnormality", 2: "LV Hypertrophy"}
    restecg = st.sidebar.selectbox("Resting ECG", [0, 1, 2], format_func=lambda x: restecg_mapping[x])
    oldpeak = st.sidebar.slider("ST Depression", 0.0, 7.0, 1.0, step=0.1)
    slope_mapping = {0: "Upsloping", 1: "Flat", 2: "Downsloping"}
    slope = st.sidebar.selectbox("ST Slope", [0, 1, 2], format_func=lambda x: slope_mapping[x])
    ca = st.sidebar.selectbox("Major Vessels (0–3)", [0, 1, 2, 3])
    thal_mapping = {1: "Normal", 2: "Fixed Defect", 3: "Reversable Defect"}
    thal = st.sidebar.selectbox("Thalassemia", [1, 2, 3], format_func=lambda x: thal_mapping[x])

    data = {
        'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps, 'chol': chol,
        'fbs': fbs, 'restecg': restecg, 'thalach': thalach, 'exang': exang,
        'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
    }
    input_df = pd.DataFrame(data, index=[0])

    prediction_proba = model.predict_proba(input_df)[0][1] * 100
    prediction = 1 if prediction_proba > 50 else 0

    st.session_state["last_risk_pct"] = prediction_proba
    st.session_state["last_vitals"] = {
        "Blood Pressure": trestbps, "Cholesterol": chol,
        "Max Heart Rate": thalach, "ST Depression": oldpeak, "Age Risk Factor": age,
    }

    # ── HEADER ──
    st.markdown("""
    <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
         border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.8rem;">
            <div style="font-size:2.2rem;">🫀</div>
            <div>
                <h1 style="font-family:'Sora',sans-serif; font-size:1.8rem; font-weight:800; margin:0;
                    background:linear-gradient(135deg, #c4b5fd, #67e8f9);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">HeartGuard AI</h1>
                <p style="color:#64748b; font-size:0.85rem; margin:0.2rem 0 0 0;">
                    Professional Cardiac Risk Stratification & AI Interpretability</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ACTION BUTTONS ──
    cb1, cb2, cb3 = st.columns([1, 1, 3])
    with cb1:
        if st.button("💾  Save Assessment", use_container_width=True):
            save_prediction(st.session_state.user_email, data, prediction_proba, prediction)
            st.success("✅ Saved to History!")
    with cb2:
        if st.button("🔄  Reset Inputs", use_container_width=True):
            st.rerun()

    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

    # ── MAIN COLUMNS ──
    col1, col2 = st.columns([1.1, 2], gap="large")

    with col1:
        st.markdown("""
        <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
             margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
            📊 Risk Assessment
        </div>
        """, unsafe_allow_html=True)

        gauge_color = "#ef4444" if prediction_proba >= 60 else "#f59e0b" if prediction_proba >= 30 else "#10b981"
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction_proba,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'size': 48, 'color': '#e2e8f0', 'family': 'Sora'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155",
                         'tickfont': {'color': '#64748b', 'size': 10}},
                'bar': {'color': gauge_color, 'thickness': 0.25},
                'bgcolor': "rgba(255,255,255,0.02)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 30], 'color': "rgba(16,185,129,0.1)"},
                    {'range': [30, 60], 'color': "rgba(245,158,11,0.08)"},
                    {'range': [60, 100], 'color': "rgba(239,68,68,0.08)"}
                ],
                'threshold': {
                    'line': {'color': gauge_color, 'width': 3},
                    'thickness': 0.8, 'value': prediction_proba
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={'color': "#e2e8f0", 'family': 'Inter'},
            margin=dict(l=15, r=15, t=20, b=15), height=260
        )
        st.plotly_chart(fig, use_container_width=True)

        if prediction == 1:
            st.markdown("""
            <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2);
                 border-radius:10px; padding:0.9rem 1.1rem; margin-top:0.5rem;">
                <div style="font-weight:700; color:#ef4444; font-size:0.9rem;">🚨 Elevated Cardiac Risk</div>
                <div style="color:#fca5a5; font-size:0.8rem; margin-top:0.2rem; line-height:1.5;">
                    Patient profile indicates high probability of a cardiovascular event. Immediate clinical review recommended.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                 border-radius:10px; padding:0.9rem 1.1rem; margin-top:0.5rem;">
                <div style="font-weight:700; color:#10b981; font-size:0.9rem;">✅ Lower Cardiac Risk</div>
                <div style="color:#6ee7b7; font-size:0.8rem; margin-top:0.2rem; line-height:1.5;">
                    Patient profile indicates low acute cardiovascular risk. Continue standard preventative care.</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
             margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
            📋 Patient Vitals
        </div>
        """, unsafe_allow_html=True)

        r1c1, r1c2, r1c3 = st.columns(3)
        cards = [
            (r1c1, "🩸", f"{trestbps}", "mmHg", "Blood Pressure",
             "⬆ Elevated" if trestbps >= 130 else "✓ Optimal", trestbps >= 130),
            (r1c2, "💉", f"{chol}", "mg/dl", "Cholesterol",
             "⬆ High" if chol >= 200 else "✓ Target", chol >= 200),
            (r1c3, "💓", f"{thalach}", "bpm", "Max Heart Rate", "", False),
        ]
        for col_c, icon, val, unit, label, delta, is_bad in cards:
            delta_html = ""
            if delta:
                dc = "#ef4444" if is_bad else "#10b981"
                delta_html = f"<div style='font-size:0.72rem; font-weight:600; color:{dc}; margin-top:0.15rem;'>{delta}</div>"
            col_c.markdown(f"""
            <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
                 border-radius:10px; padding:1rem; text-align:center;
                 transition:all 0.15s ease;"
                 onmouseover="this.style.borderColor='rgba(139,92,246,0.25)'"
                 onmouseout="this.style.borderColor='rgba(148,163,184,0.08)'">
                <div style="font-size:1.2rem;">{icon}</div>
                <div style="font-size:1.4rem; font-weight:800; color:#e2e8f0; margin-top:0.2rem;">
                    {val} <span style="font-size:0.8rem; color:#64748b; font-weight:400;">{unit}</span></div>
                <div style="font-size:0.68rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin-top:0.2rem;">{label}</div>
                {delta_html}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

        r2c1, r2c2, r2c3 = st.columns(3)
        cards2 = [
            (r2c1, "👤", f"{age}y / {'M' if sex == 1 else 'F'}", "Age & Gender"),
            (r2c2, "🫀", cp_mapping[cp], "Chest Pain Type"),
            (r2c3, "📉", f"{oldpeak}", "ST Depression"),
        ]
        for col_c, icon, val, label in cards2:
            col_c.markdown(f"""
            <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
                 border-radius:10px; padding:1rem; text-align:center;">
                <div style="font-size:1.2rem;">{icon}</div>
                <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0; margin-top:0.2rem;">{val}</div>
                <div style="font-size:0.68rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin-top:0.2rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(6,182,212,0.06); border:1px solid rgba(6,182,212,0.12);
             border-radius:8px; padding:0.8rem 1rem; font-size:0.82rem; color:#67e8f9; line-height:1.6;">
            💡 <b>Clinical Note:</b> Risk probabilities are generated by an XGBoost ML classifier.
            These insights <em>augment</em> but do <em>not</em> replace professional diagnostic protocols.
        </div>
        """, unsafe_allow_html=True)

    # ── RADAR CHART ──
    st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        🎯 Vitals vs. Healthy Baseline
    </div>
    """, unsafe_allow_html=True)

    radar_col1, radar_col2 = st.columns([2, 1])
    with radar_col1:
        categories = ['Blood Pressure', 'Cholesterol', 'Max HR', 'ST Depression', 'Age Factor']
        patient_norm = [
            min((trestbps / 120) * 100, 180),
            min((chol / 200) * 100, 180),
            min((thalach / 150) * 100, 150),
            min((oldpeak / 1.0 + 1) * 50, 150) if oldpeak > 0 else 50,
            min((age / 50) * 100, 150),
        ]
        baseline = [100, 100, 100, 50, 100]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=baseline + [baseline[0]], theta=categories + [categories[0]],
            fill='toself', name='Healthy Baseline',
            line=dict(color='#10b981', width=2),
            fillcolor='rgba(16,185,129,0.08)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=patient_norm + [patient_norm[0]], theta=categories + [categories[0]],
            fill='toself', name='Patient Profile',
            line=dict(color='#8b5cf6', width=2.5),
            fillcolor='rgba(139,92,246,0.12)'
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(255,255,255,0.01)',
                radialaxis=dict(visible=True, range=[0, 180], gridcolor='rgba(148,163,184,0.06)',
                                tickfont=dict(color='#475569', size=9)),
                angularaxis=dict(gridcolor='rgba(148,163,184,0.06)', tickfont=dict(color='#94a3b8', size=11))
            ),
            showlegend=True,
            legend=dict(bgcolor='rgba(30,41,59,0.6)', bordercolor='rgba(148,163,184,0.1)',
                        borderwidth=1, font=dict(color='#e2e8f0', size=11)),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Inter'),
            margin=dict(l=40, r=40, t=30, b=30), height=320
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with radar_col2:
        st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
             border-radius:10px; padding:1.1rem; font-size:0.85rem; line-height:1.8; color:#94a3b8;">
            <b style="color:#e2e8f0;">How to Read:</b><br><br>
            🟢 <b style="color:#10b981;">Green Area</b> — Healthy baseline<br><br>
            🟣 <b style="color:#a78bfa;">Purple Area</b> — Patient profile<br><br>
            Values exceeding the green boundary indicate clinical deviations.<br><br>
            <i>Larger deviations → higher contribution to risk score.</i>
        </div>
        """, unsafe_allow_html=True)

    # ── SHAP ──
    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        🔍 AI Interpretability — SHAP Analysis
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-bottom:0.8rem;'>The SHAP waterfall chart reveals which clinical features drive the risk prediction.</p>", unsafe_allow_html=True)

    try:
        explainer = shap.Explainer(model)
        shap_values = explainer(input_df)

        shap_col1, shap_col2 = st.columns([2, 1])
        with shap_col1:
            matplotlib.rcParams.update({
                'text.color': '#94a3b8', 'axes.labelcolor': '#64748b',
                'xtick.color': '#475569', 'ytick.color': '#475569',
                'axes.edgecolor': (1, 1, 1, 0.06)
            })
            fig_s, ax = plt.subplots(figsize=(9, 4.5))
            fig_s.patch.set_facecolor('none')
            ax.set_facecolor('none')
            shap.plots.waterfall(shap_values[0], show=False)
            plt.tight_layout()
            st.pyplot(fig_s)

        with shap_col2:
            st.markdown("""
            <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
                 border-radius:10px; padding:1.1rem; font-size:0.84rem; line-height:1.8; color:#94a3b8; margin-top:0.5rem;">
                <b style="color:#e2e8f0;">Reading the Chart:</b><br><br>
                🔴 <b style="color:#ef4444;">Red Bars</b> — Increase risk<br><br>
                🔵 <b style="color:#67e8f9;">Blue Bars</b> — Decrease risk<br><br>
                📍 <b style="color:#e2e8f0;">E[f(x)]</b> — Population average risk<br><br>
                📍 <b style="color:#e2e8f0;">f(x)</b> — Final prediction for this patient<br><br>
                <i>Bar length = magnitude of impact.</i>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not generate SHAP explanation: {e}")
