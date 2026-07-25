import streamlit as st
from typing import Dict, Any, Callable
from components.ui_styles import render_badge

def render_jd_matching_section(resume_text: str, compare_func: Callable[[str, str], Dict[str, Any]]):
    """
    Renders Job Description text area and matches candidate resume against target job profile.
    """
    st.subheader("🎯 Resume vs Job Description Matching")
    st.write("Compare candidate's resume against a specific target Job Description (JD) to evaluate match percentage, skill gaps, and keyword relevance.")

    jd_text = st.text_area(
        "Paste Target Job Description (JD) here:",
        height=180,
        placeholder="Paste full job posting requirements, responsibilities, and qualifications..."
    )

    if st.button("🚀 Analyze Job Description Match", type="primary", use_container_width=True):
        if not resume_text:
            st.error("Please upload a resume first.")
            return
        if not jd_text.strip():
            st.warning("Please paste a job description to perform matching.")
            return

        with st.status("🤖 Comparing Resume against Job Description...", expanded=True) as status:
            st.write("Analyzing core responsibilities & requirements...")
            match_result = compare_func(resume_text, jd_text)
            st.write("Calculated matching skills & skill gaps.")
            status.update(label="✅ Job Match Analysis Complete!", state="complete", expanded=False)

        # Store in session state
        st.session_state["jd_match_result"] = match_result

    # Display results if available
    match_result = st.session_state.get("jd_match_result")
    if match_result:
        st.markdown("<br>", unsafe_allow_html=True)
        match_score = match_result.get("Match_Score", 0)

        # Progress bar & Match %
        st.markdown(f"### 📈 Match Relevance: **{match_score}%**")
        st.progress(match_score / 100.0)

        if match_score >= 80:
            st.success("🎯 **GREAT MATCH**: Candidate resume aligns strongly with this position!")
        elif match_score >= 60:
            st.warning("⚠️ **MODERATE MATCH**: Candidate has foundational skills but is missing a few key qualifications.")
        else:
            st.error("❌ **LOW MATCH**: Significant gaps identified between candidate profile and position requirements.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matching Skills")
            matching_skills = match_result.get("Matching_Skills", [])
            if matching_skills:
                badges = "".join([render_badge(s, "green") for s in matching_skills])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.info("No explicit skill overlaps found.")

            st.subheader("❌ Missing JD Skills")
            missing_skills = match_result.get("Missing_Skills", [])
            if missing_skills:
                badges = "".join([render_badge(s, "red") for s in missing_skills])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.success("No critical job skills missing!")

        with col2:
            st.subheader("💡 Actionable JD Optimization Suggestions")
            suggestions = match_result.get("Suggestions", [])
            if suggestions:
                for s in suggestions:
                    st.markdown(f'<div class="suggestion-box">💡 {s}</div>', unsafe_allow_html=True)
            else:
                st.info("No recommendations needed.")
