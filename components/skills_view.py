import streamlit as st
from typing import Dict, Any
from components.ui_styles import render_badge

def render_skills_and_insights(data: Dict[str, Any]):
    """
    Renders technical skills, soft skill strengths, technical strengths, weaknesses,
    missing skills, and AI suggestions in organized glass cards.
    """
    col1, col2 = st.columns(2)

    # Left Column: Extracted Skills, Tech Strengths & Missing Skills
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🛠 Technical Skills & Core Matrix")
        skills = data.get("Skills", [])
        if skills:
            badge_html = "".join([render_badge(s, "green", "●") for s in skills])
            st.markdown(f'<div style="margin-bottom: 16px;">{badge_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No explicit skills detected in resume.")

        st.subheader("⚡ Technical Strengths")
        tech_strengths = data.get("Technical_Strengths", []) or data.get("Strengths", [])
        if tech_strengths:
            for s in tech_strengths:
                st.markdown(f'<div class="strength-box">✔ {s}</div>', unsafe_allow_html=True)
        else:
            st.info("No specific technical strengths listed.")

        st.subheader("❌ Missing / Recommended Skills")
        missing = data.get("Missing_Skills", [])
        if missing:
            missing_html = "".join([render_badge(s, "red", "▲") for s in missing])
            st.markdown(f'<div style="margin-bottom: 10px;">{missing_html}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical skill gaps identified.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column: Soft Skills, Weaknesses & Career Suggestions
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🤝 Soft Skill Strengths")
        soft_skills = data.get("Soft_Skill_Strengths", [])
        if soft_skills:
            badges = "".join([render_badge(s, "blue", "✦") for s in soft_skills])
            st.markdown(f'<div style="margin-bottom: 16px;">{badges}</div>', unsafe_allow_html=True)
        else:
            st.info("No soft skills highlighted.")

        st.subheader("🚩 Weaknesses & Profile Gaps")
        weaknesses = data.get("Weaknesses", [])
        if weaknesses:
            for w in weaknesses:
                st.markdown(f'<div class="suggestion-box" style="border-left-color: #F59E0B; background: rgba(245, 158, 11, 0.1);">⚡ {w}</div>', unsafe_allow_html=True)
        else:
            st.success("No specific weaknesses highlighted.")

        st.subheader("💡 AI Recommendations & Suggestions")
        suggestions = data.get("Suggestions", []) or data.get("Career_Suggestions", [])
        if suggestions:
            for s in suggestions:
                st.markdown(f'<div class="suggestion-box">💡 {s}</div>', unsafe_allow_html=True)
        else:
            st.info("No suggestions provided.")
        st.markdown('</div>', unsafe_allow_html=True)
