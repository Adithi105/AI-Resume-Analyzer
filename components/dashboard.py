import streamlit as st
from typing import Dict, Any
from components.ui_styles import render_badge

def render_candidate_dashboard(data: Dict[str, Any]):
    """
    Renders candidate executive overview metrics, weighted ATS score cards, and progress bars.
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

    # -----------------------------------------------------------------------------
    # Professional Weighted ATS Score Cards & Progress Bars
    # -----------------------------------------------------------------------------
    breakdown = data.get("ATS_Breakdown", {})
    if not isinstance(breakdown, dict):
        breakdown = {}

    overall_score = breakdown.get("Overall_ATS_Score", ats_score)
    skills_score = breakdown.get("Skills_Score", 0)
    exp_score = breakdown.get("Experience_Score", 0)
    projects_score = breakdown.get("Projects_Score", 0)
    kw_score = breakdown.get("Keyword_Match_Score", 0)
    edu_score = breakdown.get("Education_Score", 0)
    formatting_score = breakdown.get("Formatting_Score", 0)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Weighted ATS Category Breakdown")
    
    # Overall Progress Bar Banner
    st.markdown(f"#### 🏆 Overall Weighted ATS Score: **{overall_score}%**")
    st.progress(max(0, min(100, overall_score)) / 100.0)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6 Display Score Cards Grid (2 rows x 3 cols)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">', unsafe_allow_html=True)
        st.markdown(f"**🛠 Skills Score (25% Weight)**: `{skills_score}%`")
        st.progress(max(0, min(100, skills_score)) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">', unsafe_allow_html=True)
        st.markdown(f"**💼 Experience Score (25% Weight)**: `{exp_score}%`")
        st.progress(max(0, min(100, exp_score)) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">', unsafe_allow_html=True)
        st.markdown(f"**💻 Projects Score (15% Weight)**: `{projects_score}%`")
        st.progress(max(0, min(100, projects_score)) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">', unsafe_allow_html=True)
        st.markdown(f"**🏫 Education Score (10% Weight)**: `{edu_score}%`")
        st.progress(max(0, min(100, edu_score)) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">', unsafe_allow_html=True)
        st.markdown(f"**🎨 Formatting Score (5% Weight)**: `{formatting_score}%`")
        st.progress(max(0, min(100, formatting_score)) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 14px;">', unsafe_allow_html=True)
        st.markdown(f"**🔍 Keyword Match Score (15% Weight)**: `{kw_score}%`")
        st.progress(max(0, min(100, kw_score)) / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    if overall_score >= 80:
        st.success("🎉 **EXCELLENT ATS FIT**: High weighted compliance across skills, experience, projects, and formatting!")
    elif overall_score >= 60:
        st.warning("🙂 **GOOD ATS FIT**: Solid score foundation, but targeted improvements in projects, keywords, or formatting can optimize your rating.")
    else:
        st.error("🚨 **NEEDS OPTIMIZATION**: Low weighted score. High risk of automated screening filter rejection.")

    st.markdown('</div>', unsafe_allow_html=True)
