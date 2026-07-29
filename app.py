import streamlit as st
from utils import extract_text_from_pdf
from ai_engine import analyze_resume, compare_resume_with_jd, rewrite_resume
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
from components.recruiter_view import render_recruiter_insights
from components.rewriter_view import render_resume_rewriter_section

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Injection
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer | Intelligent Recruiter & Rewriter Suite",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Sidebar Navigation & Theme Control
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="margin: 0; background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ⚡ ResuMind AI
        </h2>
        <span class="enterprise-badge">INTELLIGENT RECRUITER v3.5</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Dark/Light Mode Theme Selector
    theme_choice = st.radio(
        "🎨 Interface Theme",
        ["🌙 Dark Mode", "☀️ Light Mode"],
        index=0,
        help="Toggle between Dark and Light visual themes."
    )
    current_theme = "dark" if "Dark" in theme_choice else "light"
    
    st.divider()

    st.markdown("### 📥 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload Candidate Resume (PDF)",
        type=["pdf"],
        help="Upload a standard PDF resume file for automated AI parsing, scoring, and rewriting."
    )

    st.info("💡 **Pro Tip**: Ensure your PDF contains selectable text for best parsing accuracy.")

    # Re-analyze Trigger Button
    if uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Re-Analyze Document", use_container_width=True):
            st.session_state.pop("ai_response", None)
            st.session_state.pop("resume_text", None)
            st.session_state.pop("jd_match_result", None)
            st.session_state.pop("improved_resume_data", None)
            st.rerun()

    st.divider()
    
    # Workflow Steps Widget
    st.markdown("""
    #### 🚀 Workflow Steps
    1. **Upload** PDF Resume  
    2. **AI Recruiter Audit**  
    3. **Rewrite** ATS Resume  
    4. **Match** Job Description  
    5. **Export** PDF Reports  
    """)

# Apply Custom Styles according to chosen theme
apply_custom_styles(theme=current_theme)

# -----------------------------------------------------------------------------
# 3. Main Header Banner
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="app-header-container">
    <div>
        <h1 class="app-header-title">📄 Enterprise AI Resume Analyzer & Rewriter Suite</h1>
        <p class="app-header-subtitle">Deep neural ATS recruitment audit, 8-category weighted scoring, side-by-side resume rewriting, and PDF exports.</p>
    </div>
    <div>
        <span class="enterprise-badge">● System Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Processing & Analysis Controller
# -----------------------------------------------------------------------------
if uploaded_file is not None:

    # Extract text if not cached in session state
    if "resume_text" not in st.session_state or st.session_state.get("last_uploaded_file") != uploaded_file.name:
        with st.status("🔍 Extracting layout & text from PDF resume...", expanded=True) as status:
            st.write("Reading document layout, metadata, and structural content...")
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.session_state["resume_text"] = extracted_text
            st.session_state["last_uploaded_file"] = uploaded_file.name
            st.write("Extracting key entities, contact information, and technical sections...")
            status.update(label="✅ Resume text extracted successfully!", state="complete", expanded=False)

    resume_text = st.session_state.get("resume_text", "")

    if not resume_text:
        st.error("⚠️ Unable to extract text from the uploaded PDF file. Please verify that the PDF contains readable text and is not a scanned image.")
    else:
        # Perform AI analysis if not already cached
        if "ai_response" not in st.session_state:
            with st.status("🤖 Running Intelligent ATS Recruiter Audit (Llama 3.2 3B)...", expanded=True) as status:
                st.write("Evaluating executive summary, recruiter verdict, hiring probability, and candidate seniority level...")
                ai_response = analyze_resume(resume_text)
                st.write("Calculating weighted ATS category scores and growth roadmap...")
                st.session_state["ai_response"] = ai_response
                status.update(label="🎉 Recruiter AI Audit Complete!", state="complete", expanded=False)

        ai_response = st.session_state.get("ai_response", {})
        candidate_name = ai_response.get("Name", "Candidate")

        # -----------------------------------------------------------------------------
        # 5. Main Application Tabs
        # -----------------------------------------------------------------------------
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🤖 Recruiter AI Intelligence",
            "✨ AI Resume Rewriter",
            "📊 Executive Dashboard",
            "🎯 JD Matcher Engine",
            "💼 Candidate Details",
            "📥 Export & Raw Text"
        ])

        # TAB 1: RECRUITER AI INTELLIGENCE
        with tab1:
            render_recruiter_insights(ai_response)

        # TAB 2: AI RESUME REWRITER
        with tab2:
            render_resume_rewriter_section(resume_text, candidate_name, rewrite_resume)

        # TAB 3: EXECUTIVE DASHBOARD
        with tab3:
            render_candidate_dashboard(ai_response)
            st.markdown("<br>", unsafe_allow_html=True)
            render_analytics_section(ai_response, theme=current_theme)
            st.markdown("<br>", unsafe_allow_html=True)
            render_skills_and_insights(ai_response)

        # TAB 4: JOB DESCRIPTION MATCHER
        with tab4:
            render_jd_matching_section(resume_text, compare_resume_with_jd)

        # TAB 5: PROFILE DETAILS (Education, Experience, Projects, Certifications)
        with tab5:
            col_left, col_right = st.columns(2)
            with col_left:
                render_experience_section(ai_response.get("Experience", []))
                render_education_section(ai_response.get("Education", []))
            with col_right:
                render_projects_section(ai_response.get("Projects", []))
                render_certifications_section(ai_response.get("Certifications", []))

        # TAB 6: REPORT DOWNLOAD & RAW TEXT VIEWER
        with tab6:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📥 Export Executive Audit Report")
            st.write("Download a comprehensive executive PDF report containing candidate metrics, Recruiter Verdict, weighted ATS breakdown, and development roadmap.")

            jd_match_data = st.session_state.get("jd_match_result")
            pdf_bytes = generate_pdf_report(ai_response, jd_match_data)

            st.download_button(
                label="📄 Download Executive PDF Audit Report",
                data=pdf_bytes,
                file_name=f"{candidate_name}_Resume_Audit_Report.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🔍 Extracted Resume Text Viewer")
            with st.expander("Click to Expand/Collapse Raw Extracted Resume Text", expanded=False):
                st.code(resume_text, language="text")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Enterprise Hero Section for Empty State
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown("""
        <h2 style="font-size: 2rem; margin-bottom: 8px;">🚀 Welcome to Enterprise AI Resume Rewriter Suite</h2>
        <p style="font-size: 1.05rem; opacity: 0.85; max-width: 750px; margin: 0 auto 24px auto;">
            Upload your candidate PDF resume in the sidebar to perform automated ATS compliance auditing, 
            weighted 8-category scoring, side-by-side AI resume rewriting, and PDF exports.
        </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 **Recruiter Verdict & Decision**")
        st.write("Automated talent assessment verdict, hiring probability score, candidate level evaluation, and executive summary.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ✨ **Side-by-Side AI Rewriter**")
        st.write("Rewrite Professional Summary, Experience, Projects, and Achievements with action verbs, ATS bullet points, and PDF exports.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 **8-Category Weighted ATS Score**")
        st.write("Detailed weighted ATS category scores across Skills, Experience, Projects, Keywords, Education, and Formatting.")
        st.markdown('</div>', unsafe_allow_html=True)