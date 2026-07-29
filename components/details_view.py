import streamlit as st
from typing import Dict, Any
from components.ui_styles import render_badge

def render_education_section(education_list: list):
    """
    Renders education entries inside styled glassmorphism containers.
    """
    st.subheader("🎓 Education")
    if not education_list:
        st.info("No education records found.")
        return

    for edu in education_list:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if isinstance(edu, dict):
            degree = edu.get("Degree", "Degree")
            institution = edu.get("Institution", "Institution Not Specified")
            session = edu.get("Session", "")
            score = edu.get("Score") or edu.get("CGP") or edu.get("Percentage") or ""

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### 🏫 {degree}")
                st.markdown(f"**Institution:** {institution}")
            with col2:
                if session:
                    st.caption(f"📅 **Session:** {session}")
                if score:
                    st.markdown(f"⭐ **Score/CGPA:** `{score}`")
        else:
            st.write(f"🎓 {edu}")
        st.markdown('</div>', unsafe_allow_html=True)

def render_projects_section(projects_list: list):
    """
    Renders projects handling object structure (Title, TechStack, Description) or plain string.
    """
    st.subheader("💻 Key Projects")
    if not projects_list:
        st.info("No projects found.")
        return

    for proj in projects_list:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if isinstance(proj, dict):
            title = proj.get("Title", "Project")
            tech_stack = proj.get("TechStack", "")
            desc = proj.get("Description", "")

            st.markdown(f"#### 📌 {title}")
            if tech_stack:
                # Render tech stack as blue badge pills if comma separated
                tech_items = [t.strip() for t in tech_stack.split(",") if t.strip()]
                if tech_items:
                    badges = "".join([render_badge(t, "blue", "⚙") for t in tech_items])
                    st.markdown(f'<div style="margin-bottom: 8px;">{badges}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"**Tech Stack:** `{tech_stack}`")
            if desc:
                st.write(desc)
        else:
            st.success(f"📌 {proj}")
        st.markdown('</div>', unsafe_allow_html=True)

def render_experience_section(experience_list: list):
    """
    Renders work experience with Company, Role, Duration, and Description.
    """
    st.subheader("💼 Professional Experience")
    if not experience_list:
        st.info("No professional experience found.")
        return

    for exp in experience_list:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if isinstance(exp, dict):
            company = exp.get("Company", "Company")
            role = exp.get("Role", "Role")
            duration = exp.get("Duration", "")
            desc = exp.get("Description", "")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### 👔 {role}")
                st.markdown(f"**Company:** {company}")
            with col2:
                if duration:
                    st.caption(f"📅 **Duration:** {duration}")
            if desc:
                st.write(desc)
        else:
            st.write(f"💼 {exp}")
        st.markdown('</div>', unsafe_allow_html=True)

def render_certifications_section(certifications_list: list):
    """
    Renders list of certifications in grid cards.
    """
    st.subheader("🏆 Certifications & Credentials")
    if not certifications_list:
        st.info("No certifications found.")
        return

    cols = st.columns(2)
    for i, cert in enumerate(certifications_list):
        with cols[i % 2]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            if isinstance(cert, dict):
                cert_title = cert.get("Certificate", "Certificate")
                inst = cert.get("Institution", "")
                st.markdown(f"🏅 **{cert_title}**")
                if inst:
                    st.caption(f"Issuing Authority: {inst}")
            else:
                st.markdown(f"🏅 {cert}")
            st.markdown('</div>', unsafe_allow_html=True)
