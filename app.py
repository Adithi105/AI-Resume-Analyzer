import streamlit as st
from utils import extract_text_from_pdf
from ai_engine import analyze_resume, compare_resume_with_jd
from helpers.report_generator import generate_pdf_report
from components.ui_styles import apply_custom_styles
from components.dashboard import render_candidate_dashboard
from components.skills_view import render_skills_and_insights
from components.charts_view import render_analytics_section
from components.details_view import (
    render_education_section,
    render_projects_section,
    render_experience_section,
    render_certifications_section
)
from components.match_view import render_jd_matching_section

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Injection
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer | Enterprise ATS Audit",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

# -----------------------------------------------------------------------------
# 2. Header & Application Introduction
# -----------------------------------------------------------------------------
st.title("📄 Enterprise AI Resume Analyzer & ATS Optimizer")
st.write(
    "Upload your resume to perform deep AI-driven ATS compliance auditing, "
    "skill gap analysis, project verification, and targeted job description matching."
)
st.divider()

# -----------------------------------------------------------------------------
# 3. Sidebar Setup & PDF Resume Upload
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Controls & Upload")
    uploaded_file = st.file_uploader(
        "Upload Candidate Resume (PDF)",
        type=["pdf"],
        help="Upload a standard PDF resume file for automated AI parsing."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Tip**: Ensure your PDF contains selectable text for best parsing accuracy.")

    # Re-analyze Trigger Button
    if uploaded_file is not None:
        if st.button("🔄 Re-Analyze Resume", use_container_width=True):
            st.session_state.pop("ai_response", None)
            st.session_state.pop("resume_text", None)
            st.session_state.pop("jd_match_result", None)

# -----------------------------------------------------------------------------
# 4. Processing & Analysis Controller
# -----------------------------------------------------------------------------
if uploaded_file is not None:

    # Extract text if not cached in session state
    if "resume_text" not in st.session_state or st.session_state.get("last_uploaded_file") != uploaded_file.name:
        with st.status("🔍 Extracting text from PDF resume...", expanded=True) as status:
            st.write("Reading document layout and structure...")
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.session_state["resume_text"] = extracted_text
            st.session_state["last_uploaded_file"] = uploaded_file.name
            st.write("Extracting key entities and technical sections...")
            status.update(label="✅ Resume text extracted!", state="complete", expanded=False)

    resume_text = st.session_state.get("resume_text", "")

    if not resume_text:
        st.error("⚠️ Unable to extract text from the uploaded PDF file. Please verify that the PDF contains readable text and is not a scanned image.")
    else:
        # Perform AI analysis if not already cached
        if "ai_response" not in st.session_state:
            with st.status("🤖 Running AI Engine Audit (Llama 3.2 3B)...", expanded=True) as status:
                st.write("Evaluating ATS formatting & keyword compliance...")
                ai_response = analyze_resume(resume_text)
                st.write("Parsing candidate contact info, skills, education, and projects...")
                st.session_state["ai_response"] = ai_response
                status.update(label="🎉 Resume Audit Complete!", state="complete", expanded=False)

        ai_response = st.session_state.get("ai_response", {})

        # -----------------------------------------------------------------------------
        # 5. Main Application Tabs
        # -----------------------------------------------------------------------------
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Executive Dashboard",
            "🎯 JD Matcher",
            "💼 Profile Details",
            "📥 Download & Raw Text"
        ])

        # TAB 1: EXECUTIVE DASHBOARD
        with tab1:
            render_candidate_dashboard(ai_response)
            st.divider()
            render_analytics_section(ai_response)
            st.divider()
            render_skills_and_insights(ai_response)

        # TAB 2: JOB DESCRIPTION MATCHER
        with tab2:
            render_jd_matching_section(resume_text, compare_resume_with_jd)

        # TAB 3: PROFILE DETAILS (Education, Experience, Projects, Certifications)
        with tab3:
            col_left, col_right = st.columns(2)
            with col_left:
                render_experience_section(ai_response.get("Experience", []))
                render_education_section(ai_response.get("Education", []))
            with col_right:
                render_projects_section(ai_response.get("Projects", []))
                render_certifications_section(ai_response.get("Certifications", []))

        # TAB 4: REPORT DOWNLOAD & RAW TEXT VIEWER
        with tab4:
            st.subheader("📥 Export Audit Report")
            st.write("Download a comprehensive PDF summary report containing candidate metrics, ATS score, skills analysis, and recommendations.")

            jd_match_data = st.session_state.get("jd_match_result")
            pdf_bytes = generate_pdf_report(ai_response, jd_match_data)

            st.download_button(
                label="📄 Download PDF Audit Report",
                data=pdf_bytes,
                file_name=f"{ai_response.get('Name', 'Candidate')}_Resume_Audit_Report.pdf",
                mime="application/pdf",
                type="primary"
            )

            st.divider()

            st.subheader("🔍 Extracted Resume Text Viewer")
            with st.expander("Click to Expand/Collapse Raw Extracted Resume Text", expanded=False):
                st.code(resume_text, language="text")

else:
    # Empty State Hero Section
    st.info("👆 Please upload a PDF resume using the sidebar control to start the AI analysis.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎯 **ATS Score Audit**")
        st.write("Get an instant quantitative readiness score evaluated against modern corporate ATS screening filters.")

    with col2:
        st.markdown("### 🛠 **Skill Gap Analysis**")
        st.write("Identify technical skill badges, highlighted strengths, and missing tech stack qualifications.")

    with col3:
        st.markdown("### 📥 **PDF Executive Export**")
        st.write("Export a clean executive PDF report to share with hiring managers or candidates.")