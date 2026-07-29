"""
Candidate Portal Module — Candidate self-service portal for tracking submission history,
viewing personal ATS score audit, and uploading updated resumes.
"""
import streamlit as st
from database.db import get_resumes_by_user_id
from helpers.auth import get_logged_in_user


def render_candidate_portal():
    """Renders Candidate Personal Self-Service Portal."""
    user = get_logged_in_user()

    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #10B981, #3B82F6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            👤 Candidate Self-Service Portal
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Track your submitted resume history, view recruiter verdicts, and access personalized career feedback.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not user:
        st.info("💡 Please log in via the sidebar to view your personalized candidate submission history.")
        user_id = 3  # Demo fallback candidate
    else:
        user_id = user.get("id", 3)

    records = get_resumes_by_user_id(user_id)

    if not records:
        st.info("ℹ️ You haven't uploaded any resumes yet under this account. Use **🔍 AI Resume Analyzer** in the sidebar to run your first audit.")
        return

    st.markdown(f"### 📂 Your Resume History ({len(records)} Submissions)")

    for idx, r in enumerate(records, 1):
        score = r.get("ats_score", 0)
        verdict = r.get("recruiter_verdict", "Under Review")
        hiring_prob = r.get("hiring_probability", "0%")
        created = r.get("created_at", "")[:10]

        v_color = "#10B981" if "Strong" in verdict or "Shortlist" in verdict else "#F59E0B" if "Borderline" in verdict else "#EF4444"

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 14px; padding: 16px; margin-bottom: 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="font-size:1.05rem; color:#F8FAFC;">Submission #{idx} ({created})</strong>
                    <span style="color:#94A3B8; font-size:0.85rem; margin-left:8px;">{r.get('candidate_name')}</span>
                </div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <span style="background:rgba(59,130,246,0.15); color:#60A5FA; padding:4px 12px; border-radius:12px; font-weight:700; font-size:0.85rem;">
                        ATS Score: {score}/100
                    </span>
                    <span style="background:{v_color}22; color:{v_color}; border:1px solid {v_color}44; padding:4px 12px; border-radius:12px; font-weight:700; font-size:0.85rem;">
                        {verdict}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🔍 View Full Recruiter Feedback for Submission #{idx}", expanded=False):
            full_json = r.get("full_json", {})
            st.markdown(f"**Executive Summary**: {full_json.get('Executive_Summary', 'N/A')}")
            st.markdown(f"**Learning Roadmap**: {', '.join(full_json.get('Learning_Roadmap', []))}")
            st.markdown(f"**Recommended Certifications**: {', '.join(full_json.get('Recommended_Certifications', []))}")
