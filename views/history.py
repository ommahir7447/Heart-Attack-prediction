import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.db import get_user_predictions


def render_history():
    st.markdown("""<div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08); border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;"><h1 style="font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700; margin:0; color:#e2e8f0;">Assessment History</h1><p style="color:#64748b; font-size:0.85rem; margin:0.15rem 0 0;">Review, analyse, and export your past cardiac risk predictions</p></div>""", unsafe_allow_html=True)

    predictions = get_user_predictions(st.session_state.user_email)

    if not predictions:
        st.markdown("""
        <div style="background:rgba(30,41,59,0.3); border:1px dashed rgba(148,163,184,0.15);
             border-radius:12px; padding:3rem; text-align:center; margin-top:1rem;">
            <div style="font-size:1.5rem; margin-bottom:0.8rem; color:#64748b;">—</div>
            <div style="font-size:1rem; color:#e2e8f0; font-weight:600;">No Assessments Yet</div>
            <div style="color:#64748b; margin-top:0.3rem;">Head to the Dashboard and save your first cardiac risk assessment.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    total = len(predictions)
    high_risk = sum(1 for p in predictions if p["prediction_class"] == 1)
    avg_prob = sum(p["prediction_proba"] for p in predictions) / total

    sc1, sc2, sc3 = st.columns(3)
    for col, val, label in [
        (sc1, str(total), "Total Assessments"),
        (sc2, str(high_risk), "High Risk Findings"),
        (sc3, f"{avg_prob:.1f}%", "Average Risk Score"),
    ]:
        col.markdown(f"""
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
             border-radius:10px; padding:1.2rem; text-align:center;">
            <div style="font-size:1.8rem; font-weight:800; color:#e2e8f0; margin-top:0.2rem;">{val}</div>
            <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin-top:0.2rem;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)

    # ── Risk trend chart ──
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        Risk Score Trend
    </div>
    """, unsafe_allow_html=True)

    dates = [p["timestamp"].strftime("%m/%d %H:%M") for p in reversed(predictions[-15:])]
    probas = [round(p["prediction_proba"], 1) for p in reversed(predictions[-15:])]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=dates, y=probas, mode='lines+markers',
        line=dict(color='#0ea5e9', width=2.5, shape='spline'),
        marker=dict(size=8, color=probas, colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
                    line=dict(color='#0b1120', width=1.5)),
        fill='tozeroy', fillcolor='rgba(14,165,233,0.07)', name='Risk %'
    ))
    fig_line.add_hline(y=50, line_dash="dot", line_color="rgba(239,68,68,0.4)",
                       annotation_text="Risk Threshold (50%)",
                       annotation_font_color="#ef4444", annotation_font_size=10)
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.01)',
        font=dict(color='#94a3b8', family='Inter'),
        xaxis=dict(gridcolor='rgba(148,163,184,0.04)', tickfont=dict(size=10)),
        yaxis=dict(gridcolor='rgba(148,163,184,0.04)', range=[0, 105],
                   title='Risk (%)', tickfont=dict(size=10)),
        margin=dict(l=10, r=10, t=20, b=10), height=250
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ── History table ──
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        Assessment Log
    </div>
    """, unsafe_allow_html=True)

    history_rows = []
    for p in predictions:
        risk_label = "High Risk" if p["prediction_class"] == 1 else "Low Risk"
        history_rows.append({
            "Timestamp": p["timestamp"].strftime("%Y-%m-%d %H:%M"),
            "Risk %": f"{p['prediction_proba']:.1f}%",
            "Assessment": risk_label,
            "Age": p["input_data"]["age"],
            "Sex": "Male" if p["input_data"]["sex"] == 1 else "Female",
            "Cholesterol": f"{p['input_data']['chol']} mg/dl",
            "Blood Pressure": f"{p['input_data']['trestbps']} mmHg",
            "Max HR": f"{p['input_data']['thalach']} bpm",
        })

    df = pd.DataFrame(history_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

    csv = pd.DataFrame([{
        "Timestamp": p["timestamp"].strftime("%Y-%m-%d %H:%M"),
        "Risk_Probability_%": round(p["prediction_proba"], 2),
        "Risk_Class": "High" if p["prediction_class"] == 1 else "Low",
        **p["input_data"]
    } for p in predictions]).to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Export Full History as CSV",
        data=csv,
        file_name="heartguard_history.csv",
        mime="text/csv",
        use_container_width=True
    )
