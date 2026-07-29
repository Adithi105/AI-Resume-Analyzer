"""
Interview Scheduler Module — Schedule candidate interviews, update slot statuses, and preview email invitations.
"""
import streamlit as st
from database.db import schedule_interview, get_all_interviews, update_interview_status
from helpers.email_notifier import send_interview_invitation_email
from helpers.auth import get_logged_in_user


def render_interview_scheduler_section():
    """Renders the Interview Scheduler & Invitation UI."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #F59E0B, #EC4899);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📅 Enterprise Interview Scheduler
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Book candidate interview slots, manage interview statuses, and trigger automated email invitations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user = get_logged_in_user()
    recruiter_name = user.get("name", "Lead Recruiter") if user else "Lead Recruiter"

    # ─── New Interview Form ──────────────────────────────────────────────────
    with st.expander("➕ Schedule New Candidate Interview Slot", expanded=False):
        c_name = st.text_input("Candidate Name", placeholder="Alex Morgan", key="sch_c_name")
        c_email = st.text_input("Candidate Email", placeholder="alex@example.com", key="sch_c_email")
        c_role = st.text_input("Job Role", value="Senior Software Engineer", key="sch_c_role")

        col_d, col_t, col_type = st.columns(3)
        with col_d:
            i_date = st.date_input("Interview Date", key="sch_i_date")
        with col_t:
            i_time = st.selectbox("Time Slot", options=["09:00 AM EST", "11:00 AM EST", "02:00 PM EST", "04:00 PM EST"], key="sch_i_time")
        with col_type:
            i_type = st.selectbox("Interview Type", options=["Technical Architecture", "HR & Culture", "Coding Live Session", "System Design"], key="sch_i_type")

        i_notes = st.text_area("Interviewer Notes / Instructions", placeholder="Prepare system design questions on distributed caching...", key="sch_i_notes")

        if st.button("📅 Confirm & Schedule Interview", type="primary", use_container_width=True, key="btn_confirm_schedule"):
            if not c_name or not c_email:
                st.error("Please fill candidate name and email.")
            else:
                int_id = schedule_interview(
                    candidate_name=c_name,
                    candidate_email=c_email,
                    recruiter_name=recruiter_name,
                    role=c_role,
                    interview_date=str(i_date),
                    time_slot=i_time,
                    interview_type=i_type,
                    notes=i_notes
                )
                st.success(f"🎉 Interview #{int_id} successfully scheduled!")

                # Preview Email Notification
                email_preview = send_interview_invitation_email(
                    candidate_name=c_name,
                    candidate_email=c_email,
                    role=c_role,
                    interview_date=str(i_date),
                    time_slot=i_time,
                    recruiter_name=recruiter_name
                )
                st.session_state["email_preview"] = email_preview

    # Preview Email Notification Box if triggered
    email_preview = st.session_state.get("email_preview")
    if email_preview:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📧 Automated Email Invitation Preview")
        st.markdown(f"**To**: `{email_preview['recipient']}`")
        st.markdown(f"**Subject**: `{email_preview['subject']}`")
        st.code(email_preview['body'], language="text")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ─── Scheduled Interviews List ─────────────────────────────────────────
    st.markdown("### 📋 Scheduled Interviews Calendar")

    interviews = get_all_interviews()

    if not interviews:
        st.info("ℹ️ No interviews scheduled yet. Use the scheduler above to book your first interview.")
        return

    for idx, item in enumerate(interviews, 1):
        status = item.get("status", "Scheduled")
        status_color = "#10B981" if status == "Completed" else "#F59E0B" if status == "Scheduled" else "#EF4444"

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 14px; padding: 16px; margin-bottom: 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="font-size:1.1rem; color:#F8FAFC;">#{idx} {item.get('candidate_name')}</strong>
                    <span style="color:#94A3B8; font-size:0.85rem; margin-left:8px;">({item.get('candidate_email')})</span>
                </div>
                <div style="background:{status_color}22; color:{status_color}; border:1px solid {status_color}44; padding:4px 12px; border-radius:12px; font-weight:700; font-size:0.85rem;">
                    {status}
                </div>
            </div>
            <div style="margin-top:8px; font-size:0.85rem; color:#CBD5E1; display:flex; gap:20px;">
                <span>🎯 Role: <strong>{item.get('role')}</strong></span>
                <span>📅 Date: <strong>{item.get('interview_date')} ({item.get('time_slot')})</strong></span>
                <span>👤 Recruiter: <strong>{item.get('recruiter_name')}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
