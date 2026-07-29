import streamlit as st
from typing import Dict, Any, Callable
from components.ui_styles import render_badge

def render_jd_matching_section(resume_text: str, compare_func: Callable[[str, str], Dict[str, Any]]):
    """
    Renders Job Description text area and matches candidate resume against target job profile.
    """
    st.subheader("🎯 Target Job Description (JD) Optimizer")
    st.write("Compare candidate's resume against a specific job posting to evaluate match percentage, skill gaps, and alignment requirements.")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste Target Job Description (JD) text below:",
        height=190,
        placeholder="Paste full job description, requirements, technical qualifications, and responsibilities here..."
    )

    if st.button("🚀 Run Job Description Match Engine", type="primary", use_container_width=True):
        if not resume_text:
            st.error("⚠️ Please upload a resume first using the sidebar control.")
            return
        if not jd_text.strip():
            st.warning("⚠️ Please paste a job description to perform ATS matching.")
            return

        with st.status("🤖 Comparing Resume against Target Job Description...", expanded=True) as status:
            st.write("Analyzing core responsibilities & technical requirements...")
            match_result = compare_func(resume_text, jd_text)
            st.write("Extracting skill overlap and identifying key missing qualifications...")
            status.update(label="✅ Job Match Analysis Complete!", state="complete", expanded=False)

        # Store in session state
        st.session_state["jd_match_result"] = match_result

    st.markdown('</div>', unsafe_allow_html=True)

    # Display results if available
    match_result = st.session_state.get("jd_match_result")
    if match_result:
        st.markdown("<br>", unsafe_allow_html=True)
        match_score = match_result.get("Match_Score", 0)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Progress bar & Match %
        st.markdown(f"### 📈 Job Fit Relevance: **{match_score}%**")
        st.progress(match_score / 100.0)

        if match_score >= 80:
            st.success("🎯 **GREAT MATCH**: Candidate resume aligns strongly with this position requirements!")
        elif match_score >= 60:
            st.warning("⚠️ **MODERATE MATCH**: Candidate has foundational skills but is missing a few key qualifications.")
        else:
            st.error("❌ **LOW MATCH**: Significant skill gaps identified between candidate profile and position requirements.")
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("✅ Overlapping Skills Found")
            matching_skills = match_result.get("Matching_Skills", [])
            if matching_skills:
                badges = "".join([render_badge(s, "green", "●") for s in matching_skills])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.info("No explicit skill overlaps found.")

            st.subheader("❌ Missing Target Skills")
            missing_skills = match_result.get("Missing_Skills", [])
            if missing_skills:
                badges = "".join([render_badge(s, "red", "▲") for s in missing_skills])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.success("No critical job skills missing!")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("💡 Targeted Optimization Guidance")
            suggestions = match_result.get("Suggestions", [])
            if suggestions:
                for s in suggestions:
                    st.markdown(f'<div class="suggestion-box">💡 {s}</div>', unsafe_allow_html=True)
            else:
                st.info("No recommendations needed.")
            st.markdown('</div>', unsafe_allow_html=True)
