import streamlit as st
import plotly.graph_objects as go
from utils.db import get_health_profile

METRIC_INFO = {
    "Blood Pressure": {
        "icon": "🩸", "unit": "mmHg", "normal_range": (90, 120),
        "warning": 130, "danger": 140,
        "explanation": "Blood pressure measures the force of blood against artery walls. Elevated levels (≥130 mmHg) cause arteries to harden over time and dramatically increase heart attack risk.",
        "symptoms": ["Headaches", "Dizziness", "Blurred vision", "Chest pain", "Shortness of breath"],
        "tips": "Reduce salt intake, manage stress, exercise regularly, limit alcohol.",
    },
    "Cholesterol": {
        "icon": "💉", "unit": "mg/dl", "normal_range": (150, 200),
        "warning": 200, "danger": 240,
        "explanation": "High cholesterol causes fatty deposits (plaques) to build up in blood vessels, narrowing them and restricting blood flow — the #1 cause of heart attacks.",
        "symptoms": ["Usually no symptoms", "Xanthomas (fatty deposits on skin)", "Chest pain (advanced stages)"],
        "tips": "Avoid trans fats, eat more fibre (oats, beans), take statins if prescribed.",
    },
    "Max Heart Rate": {
        "icon": "💓", "unit": "bpm", "normal_range": (60, 100),
        "warning": 100, "danger": 120,
        "explanation": "Resting heart rate above 100 bpm (tachycardia) may indicate the heart is working harder than it should, often a sign of underlying cardiac stress.",
        "symptoms": ["Palpitations", "Dizziness", "Shortness of breath", "Fatigue", "Chest discomfort"],
        "tips": "Practice deep breathing, stay hydrated, reduce caffeine, consult your cardiologist.",
    },
    "ST Depression": {
        "icon": "📉", "unit": "", "normal_range": (0.0, 0.5),
        "warning": 1.0, "danger": 2.0,
        "explanation": "ST Depression on an ECG is a key sign of reduced blood flow to the heart (myocardial ischaemia). Values > 1.0 mm are clinically significant and require immediate evaluation.",
        "symptoms": ["Exercise-induced chest pain", "Fatigue on exertion", "Breathlessness"],
        "tips": "Avoid strenuous activity, get an urgent ECG + stress test, follow cardiologist advice.",
    },
    "Age Risk Factor": {
        "icon": "👤", "unit": "years", "normal_range": (0, 45),
        "warning": 50, "danger": 65,
        "explanation": "Cardiovascular risk increases significantly after age 45 in men and 55 in women. Age-related arterial stiffening and accumulated risk factors compound over time.",
        "symptoms": ["Increased fatigue", "Reduced exercise tolerance", "Blood pressure changes"],
        "tips": "Annual cardiac check-ups, maintain a heart-healthy lifestyle, know your family history.",
    },
}

def risk_badge(val, warning, danger):
    if val >= danger:
        return "<span style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.25); border-radius:20px; padding:0.2rem 0.6rem; font-size:0.75rem; color:#ef4444;'>⚠ High Risk</span>"
    elif val >= warning:
        return "<span style='background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.25); border-radius:20px; padding:0.2rem 0.6rem; font-size:0.75rem; color:#f59e0b;'>⚡ Borderline</span>"
    else:
        return "<span style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); border-radius:20px; padding:0.2rem 0.6rem; font-size:0.75rem; color:#10b981;'>✓ Normal</span>"

def render_analysis():
    st.markdown("""
    <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
         border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.8rem;">
            <div style="font-size:2rem;">🔬</div>
            <div>
                <h1 style="font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700; margin:0; color:#e2e8f0;">
                    Deep Health Analysis</h1>
                <p style="color:#64748b; font-size:0.85rem; margin:0.15rem 0 0 0;">
                    Plain-English breakdown of each clinical metric — what it means, why it matters, what to do</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    vals = st.session_state.get("last_vitals", {
        "Blood Pressure": 120, "Cholesterol": 200,
        "Max Heart Rate": 150, "ST Depression": 1.0, "Age Risk Factor": 50
    })
    risk_pct = st.session_state.get("last_risk_pct", 0.0)

    risk_color = "#ef4444" if risk_pct >= 60 else "#f59e0b" if risk_pct >= 30 else "#10b981"
    risk_label = "High Risk" if risk_pct >= 60 else "Moderate Risk" if risk_pct >= 30 else "Low Risk"
    st.markdown(f"""
    <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
         border-radius:12px; padding:1.2rem 1.5rem; display:flex; align-items:center; gap:1.2rem; margin-bottom:1.2rem;">
        <div style="font-size:2.5rem; font-weight:800; color:{risk_color};">{risk_pct:.1f}%</div>
        <div>
            <div style="font-size:1rem; font-weight:700; color:{risk_color};">{risk_label} — Overall Cardiac Risk</div>
            <div style="color:#64748b; font-size:0.82rem; margin-top:0.15rem;">
                Based on your last Dashboard assessment. Adjust sliders on the Dashboard to update.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for metric, info in METRIC_INFO.items():
        val = vals.get(metric, info["normal_range"][1])
        badge = risk_badge(val, info["warning"], info["danger"])

        with st.expander(f"{info['icon']}  {metric}  —  {val} {info['unit']}  {badge}", expanded=False):
            col1, col2 = st.columns([2, 1.2])
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[info["danger"] * 1.5], y=[metric], orientation='h',
                    marker_color='rgba(239,68,68,0.1)', showlegend=False))
                fig.add_trace(go.Bar(x=[info["warning"]], y=[metric], orientation='h',
                    marker_color='rgba(245,158,11,0.12)', showlegend=False))
                fig.add_trace(go.Bar(x=[info["normal_range"][1]], y=[metric], orientation='h',
                    marker_color='rgba(16,185,129,0.15)', showlegend=False))
                fig.add_shape(type="line", x0=val, x1=val, y0=-0.4, y1=0.4,
                              line=dict(color="#8b5cf6", width=3))
                fig.add_annotation(x=val, y=0.5, text=f"<b>You: {val}</b>",
                                   showarrow=False, font=dict(color="#a78bfa", size=12))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.01)',
                    barmode='overlay', height=100, margin=dict(l=0, r=10, t=25, b=0),
                    xaxis=dict(showgrid=False, zeroline=False, visible=False),
                    yaxis=dict(showgrid=False, visible=False),
                    font=dict(color='#94a3b8', family='Inter')
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
                     border-radius:8px; padding:0.9rem 1rem; font-size:0.85rem; color:#94a3b8; line-height:1.7; margin-top:0.4rem;">
                    <b style="color:#e2e8f0;">📚 What this means:</b><br>{info['explanation']}<br><br>
                    <b style="color:#67e8f9;">💡 What to do:</b> {info['tips']}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                normal_range_text = f"{info['normal_range'][0]} – {info['normal_range'][1]} {info['unit']}"
                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.4); border:1px solid rgba(148,163,184,0.06);
                     border-radius:8px; padding:0.9rem; font-size:0.82rem; line-height:1.8;">
                    <div style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.4rem;">Reference</div>
                    <div>✅ Normal: <b style="color:#10b981;">{normal_range_text}</b></div>
                    <div>⚡ Borderline: <b style="color:#f59e0b;">{info['warning']} {info['unit']}</b></div>
                    <div>🚨 High Risk: <b style="color:#ef4444;">{info['danger']}+ {info['unit']}</b></div>
                    <div>📌 Your Value: <b style="color:#e2e8f0;">{val} {info['unit']}</b></div>
                    <hr style="border-color:rgba(148,163,184,0.06); margin:0.6rem 0;">
                    <div style="color:#64748b; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.4rem;">Watch for symptoms</div>
                    {"".join([f"<div style='color:#94a3b8;'>• {s}</div>" for s in info['symptoms']])}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 This analysis is based on general clinical guidelines. Always consult a cardiologist for personalized medical advice.")
