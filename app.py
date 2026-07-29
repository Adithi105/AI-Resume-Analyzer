import streamlit as st
from utils import extract_text_from_pdf
from ai_engine import analyze_resume, compare_resume_with_jd, rewrite_resume, generate_builder_resume
from helpers.report_generator import generate_pdf_report
from helpers.config_manager import load_config, get_current_provider_name, get_current_model
from helpers.providers import PROVIDER_ICONS
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
from components.builder_view import render_resume_builder_section
from components.settings_view import render_settings

# Load AI provider config from .env / session state on every cold start
load_config()

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Injection
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer & Builder Suite | Enterprise ATS",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Sidebar Navigation, Mode Switcher & Theme Control
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="margin: 0; background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ⚡ ResuMind AI
        </h2>
        <span class="enterprise-badge">DUAL ATS SUITE v4.0</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Primary Application Suite Mode Switcher
    suite_mode = st.radio(
        "🚀 Select Application Suite",
        ["🔍 AI Resume Analyzer", "📝 AI Resume Builder", "⚙️ AI Settings"],
        index=0,
        help="Switch between analyzing a resume, building a new one, or configuring your AI provider."
    )

    # Active provider badge in sidebar
    _prov = get_current_provider_name()
    _model = get_current_model()
    _icon = PROVIDER_ICONS.get(_prov, "🤖")
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
                border-radius:10px; padding:0.5rem 0.9rem; margin-top:0.4rem;
                font-size:0.78rem; color:#94a3b8; display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:1rem;">{_icon}</span>
        <span><strong style="color:#e2e8f0;">{_prov}</strong> / {_model}</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Dark/Light Mode Theme Selector
    theme_choice = st.radio(
        "🎨 Interface Theme",
        ["🌙 Dark Mode", "☀️ Light Mode"],
        index=0,
        help="Toggle between Dark and Light visual themes."
    )
    current_theme = "dark" if "Dark" in theme_choice else "light"
    
    st.divider()

    # Analyzer Controls (Only show when in Analyzer Suite)
    if "Analyzer" in suite_mode:
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
        #### 🚀 Analyzer Workflow
        1. **Upload** PDF Resume  
        2. **AI Recruiter Audit**  
        3. **Rewrite** ATS Resume  
        4. **Match** Job Description  
        5. **Export** PDF Reports  
        """)
    elif "Builder" in suite_mode:
        uploaded_file = None
        st.markdown("""
        #### 🚀 Builder Workflow
        1. **Fill** Candidate Details  
        2. **Select** Resume Template  
        3. **Generate** AI ATS Bullets  
        4. **Preview** Live Resume  
        5. **Export** PDF / Word DOCX  
        """)
    else:
        # Settings mode
        uploaded_file = None
        st.markdown("""
        #### ⚙️ Settings
        - Switch AI providers
        - Enter API keys
        - Test connection
        - Save preferences
        """)

# Apply Custom Styles according to chosen theme
apply_custom_styles(theme=current_theme)

# Inject active provider into the audit status label dynamically
_active_provider_label = f"{PROVIDER_ICONS.get(get_current_provider_name(), '🤖')} Running {get_current_provider_name()} / {get_current_model()}"

# -----------------------------------------------------------------------------
# 3. Main Header Banner
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="app-header-container">
    <div>
        <h1 class="app-header-title">📄 Enterprise AI Resume Analyzer & Builder Suite</h1>
        <p class="app-header-subtitle">Deep neural ATS recruitment audit, 8-category weighted scoring, AI resume rewriting, and interactive multi-template resume builder.</p>
    </div>
    <div>
        <span class="enterprise-badge">● {'Analyzer Active' if 'Analyzer' in suite_mode else 'Builder Active'}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Suite Controller
# -----------------------------------------------------------------------------

# =============================================================================
# SUITE A: AI SETTINGS
# =============================================================================
if "Settings" in suite_mode:
    render_settings()

# =============================================================================
# SUITE B: AI RESUME BUILDER
# =============================================================================
elif "Builder" in suite_mode:
    render_resume_builder_section(generate_builder_resume)

# =============================================================================
# SUITE B: AI RESUME ANALYZER
# =============================================================================
else:
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
                with st.status(f"🤖 {_active_provider_label} — Running Intelligent ATS Recruiter Audit...", expanded=True) as status:
                    st.write("Evaluating executive summary, recruiter verdict, hiring probability, and candidate seniority level...")
                    ai_response = analyze_resume(resume_text)
                    st.write("Calculating weighted ATS category scores and growth roadmap...")
                    st.session_state["ai_response"] = ai_response
                    status.update(label="🎉 Recruiter AI Audit Complete!", state="complete", expanded=False)

            ai_response = st.session_state.get("ai_response", {})
            candidate_name = ai_response.get("Name", "Candidate")

            # -----------------------------------------------------------------------------
            # 5. Main Application Tabs for Analyzer
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
            <h2 style="font-size: 2rem; margin-bottom: 8px;">🚀 Welcome to Enterprise AI Resume Suite</h2>
            <p style="font-size: 1.05rem; opacity: 0.85; max-width: 750px; margin: 0 auto 24px auto;">
                Upload your candidate PDF resume in the sidebar to perform automated ATS compliance auditing, 
                weighted 8-category scoring, side-by-side AI resume rewriting, or switch to <b>📝 AI Resume Builder</b> in the sidebar to build a new resume from scratch.
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
            st.markdown("### 📝 **AI Resume Builder Suite**")
            st.write("Build a brand new ATS-optimized resume with AI bullet points, multiple templates, live preview, PDF & Word DOCX exports.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 **8-Category Weighted ATS Score**")
            st.write("Detailed weighted ATS category scores across Skills, Experience, Projects, Keywords, Education, and Formatting.")
            st.markdown('</div>', unsafe_allow_html=True)