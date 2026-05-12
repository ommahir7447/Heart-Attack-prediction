import streamlit as st
from utils.db import get_doctor_notes, get_user_appointments, mark_note_read, count_unread_notes

def render_updates():
    mark_note_read(st.session_state.user_email)

    st.markdown("""<div class="page-header"><h1>My Updates</h1><p>Doctor notes, appointment confirmations, and health updates from your care team</p></div>""", unsafe_allow_html=True)

    notes = get_doctor_notes(st.session_state.user_email)
    appointments = get_user_appointments(st.session_state.user_email)

    # ── Summary ──
    uc1, uc2 = st.columns(2)
    for col, val, label in [
        (uc1, len(appointments), "Total Appointments"),
        (uc2, len(notes), "Doctor Notes Received"),
    ]:
        col.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:1.2rem;">
            <div style="font-size:1.8rem; font-weight:800; color:#e2e8f0; margin-top:0.2rem;">{val}</div>
            <div style="font-size:0.7rem; color:#475569; text-transform:uppercase; letter-spacing:0.8px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Doctor Notes ──
    st.markdown("""<div class="section-header">Doctor Notes & Health Updates</div>""", unsafe_allow_html=True)

    if not notes:
        st.markdown("""
        <div style="background:rgba(12,20,42,0.5); border:1px dashed rgba(148,163,184,0.08);
             border-radius:16px; padding:3rem; text-align:center;">
            <div style="font-size:1.5rem; color:#334155;">—</div>
            <div style="color:#e2e8f0; font-weight:600; margin-top:0.5rem;">No doctor notes yet</div>
            <div style="color:#475569; font-size:0.85rem; margin-top:0.2rem;">Book an appointment to receive personalised health notes here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for note in notes:
            ts = note["timestamp"].strftime("%d %b %Y · %H:%M")
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:0.8rem; border-left:3px solid #a78bfa;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.7rem;">
                    <div>
                        <div style="font-weight:700; color:#e2e8f0; font-size:0.95rem;">Dr. {note['doctor_name']}</div>
                        <div style="color:#475569; font-size:0.78rem;">{note['hospital']} · {ts}</div>
                    </div>
                    <span style="background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.15);
                         border-radius:20px; padding:0.15rem 0.6rem; font-size:0.72rem; color:#34d399;">✓ Delivered</span>
                </div>
                <div style="background:rgba(6,13,31,0.6); border-radius:10px; padding:0.9rem;
                     font-size:0.85rem; color:#94a3b8; line-height:1.7; margin-bottom:0.7rem;">
                    {note['note']}
                </div>
                <div style="background:rgba(251,191,36,0.04); border:1px solid rgba(251,191,36,0.1);
                     border-radius:8px; padding:0.5rem 0.8rem; font-size:0.8rem; color:#fbbf24;">
                    <b>Follow-up:</b> {note.get('follow_up', 'Visit as advised')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Appointments ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-header">Appointment History</div>""", unsafe_allow_html=True)

    if not appointments:
        st.markdown("<p style='color:#475569;'>No appointments booked yet. Visit <b>Find Doctors</b> to book one.</p>", unsafe_allow_html=True)
    else:
        for appt in appointments:
            ts = appt["timestamp"].strftime("%d %b %Y · %H:%M")
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:0.5rem; padding:0.9rem 1.2rem;
                 display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:600; color:#e2e8f0; font-size:0.88rem;">Dr. {appt['doctor_name']}</div>
                    <div style="color:#475569; font-size:0.78rem;">{appt['hospital']} · {appt['specialty']} · {ts}</div>
                </div>
                <span style="background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.15);
                     border-radius:20px; padding:0.2rem 0.7rem; font-size:0.75rem; color:#34d399; font-weight:600;">
                    {appt.get('status','Confirmed')}
                </span>
            </div>
            """, unsafe_allow_html=True)
