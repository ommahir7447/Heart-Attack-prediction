import streamlit as st
from utils.db import get_doctor_notes, get_user_appointments, mark_note_read, count_unread_notes

def render_updates():
    mark_note_read(st.session_state.user_email)

    st.markdown("""
    <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
         border-radius:12px; padding:1.5rem 2rem; margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.8rem;">
            <div style="font-size:2rem;">📬</div>
            <div>
                <h1 style="font-family:'Sora',sans-serif; font-size:1.6rem; font-weight:700; margin:0; color:#e2e8f0;">
                    My Updates</h1>
                <p style="color:#64748b; font-size:0.85rem; margin:0.15rem 0 0 0;">
                    Doctor notes, appointment confirmations, and health updates from your care team</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    notes = get_doctor_notes(st.session_state.user_email)
    appointments = get_user_appointments(st.session_state.user_email)

    # ── Summary ──
    uc1, uc2 = st.columns(2)
    for col, icon, val, label in [
        (uc1, "📋", len(appointments), "Total Appointments"),
        (uc2, "📝", len(notes), "Doctor Notes Received"),
    ]:
        col.markdown(f"""
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
             border-radius:10px; padding:1.2rem; text-align:center;">
            <div style="font-size:1.6rem;">{icon}</div>
            <div style="font-size:1.8rem; font-weight:800; color:#e2e8f0; margin-top:0.2rem;">{val}</div>
            <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; letter-spacing:0.8px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Doctor Notes ──
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        📝 Doctor Notes & Health Updates
    </div>
    """, unsafe_allow_html=True)

    if not notes:
        st.markdown("""
        <div style="background:rgba(30,41,59,0.3); border:1px dashed rgba(148,163,184,0.12);
             border-radius:12px; padding:3rem; text-align:center;">
            <div style="font-size:2.5rem;">📭</div>
            <div style="color:#e2e8f0; font-weight:600; margin-top:0.5rem;">No doctor notes yet</div>
            <div style="color:#64748b; font-size:0.85rem; margin-top:0.2rem;">Book an appointment to receive personalised health notes here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for note in notes:
            ts = note["timestamp"].strftime("%d %b %Y · %H:%M")
            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(148,163,184,0.08);
                 border-radius:12px; padding:1.3rem 1.5rem; margin-bottom:0.8rem; border-left:3px solid #06b6d4;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.7rem;">
                    <div>
                        <div style="font-weight:700; color:#e2e8f0; font-size:0.95rem;">👨‍⚕️ {note['doctor_name']}</div>
                        <div style="color:#64748b; font-size:0.78rem;">🏥 {note['hospital']} · {ts}</div>
                    </div>
                    <span style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                         border-radius:20px; padding:0.15rem 0.6rem; font-size:0.72rem; color:#10b981;">✓ Delivered</span>
                </div>
                <div style="background:rgba(15,23,42,0.6); border-radius:8px; padding:0.9rem;
                     font-size:0.85rem; color:#cbd5e1; line-height:1.7; margin-bottom:0.7rem;">
                    {note['note']}
                </div>
                <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.12);
                     border-radius:6px; padding:0.5rem 0.8rem; font-size:0.8rem; color:#fbbf24;">
                    📅 <b>Follow-up:</b> {note.get('follow_up', 'Visit as advised')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Appointments ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Sora',sans-serif; font-weight:600; font-size:0.9rem; color:#94a3b8;
         margin-bottom:0.8rem; padding-bottom:0.5rem; border-bottom:1px solid rgba(148,163,184,0.1);">
        📋 Appointment History
    </div>
    """, unsafe_allow_html=True)

    if not appointments:
        st.markdown("<p style='color:#64748b;'>No appointments booked yet. Visit <b>Find Doctors</b> to book one.</p>", unsafe_allow_html=True)
    else:
        for appt in appointments:
            ts = appt["timestamp"].strftime("%d %b %Y · %H:%M")
            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.4); border:1px solid rgba(148,163,184,0.06);
                 border-radius:10px; padding:0.9rem 1.2rem; margin-bottom:0.5rem;
                 display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:600; color:#e2e8f0; font-size:0.88rem;">👨‍⚕️ {appt['doctor_name']}</div>
                    <div style="color:#64748b; font-size:0.78rem;">🏥 {appt['hospital']} · 🩺 {appt['specialty']} · {ts}</div>
                </div>
                <span style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2);
                     border-radius:20px; padding:0.2rem 0.7rem; font-size:0.75rem; color:#10b981; font-weight:600;">
                    ✅ {appt.get('status','Confirmed')}
                </span>
            </div>
            """, unsafe_allow_html=True)
