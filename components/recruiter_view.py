import streamlit as st
from typing import Dict, Any
from components.ui_styles import render_badge

def render_recruiter_decision_card(data: Dict[str, Any]):
    """
    Renders top-level recruiter assessment widgets: Recruiter Verdict badge,
    Hiring Probability, Candidate Seniority Level, and Executive Summary.
    """
    st.subheader("🤖 Recruiter Decision & Talent Assessment")

    verdict = data.get("Recruiter_Verdict", "Under Review")
    hiring_prob = data.get("Hiring_Probability", "0%")
    candidate_level = data.get("Candidate_Level", "Not Specified")
    executive_summary = data.get("Executive_Summary", "Not Provided")
    resume_overview = data.get("Resume_Overview", "Not Provided")

    # Verdict Badge Color Mapping
    verdict_lower = verdict.lower()
    if "strong" in verdict_lower or "hire" in verdict_lower:
        badge_type = "green"
        verdict_icon = "🔥"
    elif "interview" in verdict_lower or "shortlist" in verdict_lower:
        badge_type = "blue"
        verdict_icon = "⚡"
    elif "borderline" in verdict_lower:
        badge_type = "blue"
        verdict_icon = "⚠️"
    else:
        badge_type = "red"
        verdict_icon = "🚨"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>RECRUITER VERDICT</p>", unsafe_allow_html=True)
        badge_html = render_badge(f"{verdict_icon} {verdict}", badge_type)
        st.markdown(f"<div style='margin-top: 8px;'>{badge_html}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>HIRING PROBABILITY</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin: 4px 0 0 0; color: #38BDF8;'>🎯 {hiring_prob}</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>CANDIDATE LEVEL</p>", unsafe_allow_html=True)
        badge_level = render_badge(f"👑 {candidate_level}", "blue")
        st.markdown(f"<div style='margin-top: 8px;'>{badge_level}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Executive Summary & Resume Overview Box
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Executive Summary")
    st.markdown(f"<p style='font-size: 1rem; line-height: 1.6;'>{executive_summary}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 16px 0;'>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Candidate Overview")
    st.markdown(f"<p style='font-size: 0.95rem; color: #94A3B8;'>{resume_overview}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_risks_and_weaknesses(data: Dict[str, Any]):
    """
    Renders Resume Risks/Red Flags, Weaknesses, and Soft Skill Strengths.
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚠️ Resume Risks & Red Flags")
        risks = data.get("Resume_Risks", [])
        if risks:
            for r in risks:
                st.markdown(f'<div class="suggestion-box" style="border-left-color: #EF4444; background: rgba(239, 68, 68, 0.1);">🚩 {r}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical resume red flags detected!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🤝 Soft Skill Strengths & Weaknesses")
        soft_skills = data.get("Soft_Skill_Strengths", [])
        weaknesses = data.get("Weaknesses", [])

        if soft_skills:
            st.markdown("**Soft Skill Highlights:**")
            badges = "".join([render_badge(s, "blue", "✦") for s in soft_skills])
            st.markdown(f"<div style='margin-bottom: 14px;'>{badges}</div>", unsafe_allow_html=True)

        if weaknesses:
            st.markdown("**Identified Profile Weaknesses:**")
            for w in weaknesses:
                st.markdown(f'<div class="strength-box" style="border-left-color: #F59E0B; background: rgba(245, 158, 11, 0.1);">⚡ {w}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_growth_roadmap(data: Dict[str, Any]):
    """
    Renders Learning Roadmap, Recommended Certifications, Suggested Projects,
    and Resume Rewrite Suggestions.
    """
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🗺 Learning & Career Roadmap")
    roadmap = data.get("Learning_Roadmap", [])
    if roadmap:
        for idx, step in enumerate(roadmap, 1):
            st.markdown(f"""
            <div style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 12px; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; border-left: 3px solid #6366F1;">
                <div style="background: #6366F1; color: white; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.85rem; flex-shrink: 0;">{idx}</div>
                <div style="font-size: 0.95rem; font-weight: 500;">{step}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No learning roadmap available.")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🏅 Recommended Certifications")
        certs = data.get("Recommended_Certifications", [])
        if certs:
            badges = "".join([render_badge(c, "green", "🏆") for c in certs])
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No explicit certifications recommended.")

        st.subheader("💻 Suggested Portfolio Projects")
        projects = data.get("Suggested_Projects", [])
        if projects:
            for p in projects:
                if isinstance(p, dict):
                    st.markdown(f"📌 **{p.get('Title', 'Project')}**: {p.get('Description', '')}")
                else:
                    st.markdown(f"📌 {p}")
        else:
            st.info("No suggested projects listed.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("✍️ Resume Rewrite Suggestions")
        rewrites = data.get("Resume_Rewrite_Suggestions", [])
        if rewrites:
            for r in rewrites:
                st.markdown(f'<div class="suggestion-box">✍️ {r}</div>', unsafe_allow_html=True)
        else:
            st.info("No rewrite suggestions needed.")
        st.markdown('</div>', unsafe_allow_html=True)

def render_recruiter_insights(data: Dict[str, Any]):
    """
    Renders full Intelligent Recruiter dashboard tab.
    """
    render_recruiter_decision_card(data)
    st.markdown("<br>", unsafe_allow_html=True)
    render_risks_and_weaknesses(data)
    st.markdown("<br>", unsafe_allow_html=True)
    render_growth_roadmap(data)
