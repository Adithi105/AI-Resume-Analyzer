import streamlit as st
from typing import Dict, Any
from components.ui_styles import render_badge

def render_candidate_dashboard(data: Dict[str, Any]):
    """
    Renders candidate executive overview metrics, recruiter decision badges, and ATS Score status card.
    """
    st.subheader("👤 Candidate Executive Overview")
    
    # 4 Primary Metric Cards
    col1, col2, col3, col4 = st.columns(4)

    name = data.get("Name", "Not Provided")
    email = data.get("Email", "Not Provided")
    phone = data.get("Phone", "Not Provided")
    ats_score = data.get("ATS_Score", 0)

    with col1:
        st.metric("👤 Candidate Name", name)

    with col2:
        st.metric("📧 Email Address", email)

    with col3:
        st.metric("📞 Phone Number", phone)

    with col4:
        st.metric("⭐ Overall ATS Score", f"{ats_score} / 100")

    # Recruiter Intelligence Summary Row
    verdict = data.get("Recruiter_Verdict", "Under Review")
    hiring_prob = data.get("Hiring_Probability", "0%")
    level = data.get("Candidate_Level", "Not Specified")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Recruiter Intelligence Snapshot")
    
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        st.markdown(f"**Recruiter Verdict:** {render_badge(verdict, 'green' if 'hire' in verdict.lower() else 'blue')}", unsafe_allow_html=True)

    with r_col2:
        st.markdown(f"**Hiring Probability:** <span style='color: #38BDF8; font-weight: 800; font-size: 1.1rem;'>🎯 {hiring_prob}</span>", unsafe_allow_html=True)

    with r_col3:
        st.markdown(f"**Candidate Level:** {render_badge(level, 'blue', '👑')}", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ATS Score Status Badge & Progress Bar Container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 ATS Readiness Assessment")
    
    progress_val = max(0, min(100, ats_score)) / 100.0
    st.progress(progress_val)

    if ats_score >= 80:
        st.success("🎉 **EXCELLENT RESUME**: High ATS compliance! Strong formatting, relevant technical keywords, and quantitative achievements detected.")
    elif ats_score >= 60:
        st.warning("🙂 **GOOD RESUME**: Solid foundation, but targeted improvements in keywords, formatting, or project metrics can boost your score.")
    elif ats_score >= 40:
        st.info("⚠️ **AVERAGE RESUME**: Missing key sections or technical keywords required by modern automated screening systems.")
    else:
        st.error("🚨 **POOR RESUME**: Significant optimization needed. High risk of rejection by automated ATS screening filters.")

    st.markdown('</div>', unsafe_allow_html=True)
