import streamlit as st
from typing import Dict, Any
from components.ui_styles import render_badge

def render_skills_and_insights(data: Dict[str, Any]):
    """
    Renders skills in glowing green badges, missing skills in red badges,
    strengths in green cards, and AI suggestions in info callouts.
    """
    col1, col2 = st.columns(2)

    # Left Column: Skills & Missing Skills
    with col1:
        st.subheader("🛠 Extracted Skills")
        skills = data.get("Skills", [])
        if skills:
            badge_html = "".join([render_badge(s, "green") for s in skills])
            st.markdown(f'<div style="margin-bottom: 20px;">{badge_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No explicit skills detected in resume.")

        st.subheader("❌ Missing / Recommended Skills")
        missing = data.get("Missing_Skills", [])
        if missing:
            missing_html = "".join([render_badge(s, "red") for s in missing])
            st.markdown(f'<div style="margin-bottom: 20px;">{missing_html}</div>', unsafe_allow_html=True)
        else:
            st.success("No critical skill gaps identified.")

    # Right Column: Strengths & Suggestions
    with col2:
        st.subheader("✅ Key Strengths")
        strengths = data.get("Strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(f'<div class="strength-box">✔ {s}</div>', unsafe_allow_html=True)
        else:
            st.info("No specific strengths listed.")

        st.subheader("💡 AI Recommendations")
        suggestions = data.get("Suggestions", [])
        if suggestions:
            for s in suggestions:
                st.markdown(f'<div class="suggestion-box">💡 {s}</div>', unsafe_allow_html=True)
        else:
            st.info("No suggestions provided.")
