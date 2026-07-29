import streamlit as st
from typing import Dict, Any, Callable
from components.ui_styles import render_badge
from helpers.report_generator import generate_builder_resume_pdf
from helpers.docx_generator import generate_builder_resume_docx

def render_resume_builder_section(generate_ai_resume_func: Callable[[Dict[str, Any]], Dict[str, Any]]):
    """
    Renders the AI Resume Builder suite featuring form inputs, template selector,
    AI polishing trigger, live interactive preview, PDF export, and DOCX export.
    """
    st.subheader("📝 AI Resume Builder & Professional Formatter")
    st.write("Fill in candidate details below. The AI engine will refine your inputs into quantified ATS bullet points, format them into professional templates, and export PDF or Word (.docx) files.")

    # -----------------------------------------------------------------------------
    # 1. Template Selector
    # -----------------------------------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        template_style = st.selectbox(
            "🎨 Select Resume Template Style",
            ["Classic Executive", "Modern Tech", "Minimalist Clean", "Creative Professional"],
            index=0,
            help="Select visual template style for Live Preview, PDF export, and DOCX export."
        )
    with col_t2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**Selected Style**: `{template_style}`")
    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------------------
    # 2. Form Input Tabs
    # -----------------------------------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Fill Candidate Details")

    ftab1, ftab2, ftab3, ftab4, ftab5, ftab6 = st.tabs([
        "👤 Personal Info",
        "🎓 Education",
        "💼 Experience",
        "💻 Projects",
        "🛠 Skills",
        "🏆 Certifications"
    ])

    with ftab1:
        c1, c2 = st.columns(2)
        with c1:
            b_name = st.text_input("Full Name", value="Alex Morgan", key="b_name")
            b_email = st.text_input("Email Address", value="alex.morgan@email.com", key="b_email")
            b_phone = st.text_input("Phone Number", value="+1 (555) 019-2834", key="b_phone")
        with c2:
            b_location = st.text_input("Location (City, State/Country)", value="San Francisco, CA", key="b_loc")
            b_linkedin = st.text_input("LinkedIn / Portfolio URL", value="linkedin.com/in/alexmorgan", key="b_link")
            b_summary = st.text_area("Draft Professional Summary (Optional - AI will polish)", value="Experienced Senior Software Engineer with expertise in building scalable microservices and cloud infrastructure.", height=70, key="b_sum")

    with ftab2:
        st.markdown("#### Education Entry")
        e_deg = st.text_input("Degree Name", value="B.S. in Computer Science", key="b_edeg")
        e_inst = st.text_input("Institution / University Name", value="Stanford University", key="b_einst")
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            e_sess = st.text_input("Session / Year", value="2018 - 2022", key="b_esess")
        with col_e2:
            e_score = st.text_input("Score / CGPA", value="3.9 / 4.0", key="b_escore")
        e_high = st.text_input("Highlights / Specialization", value="Specialized in Artificial Intelligence & Systems", key="b_ehigh")

    with ftab3:
        st.markdown("#### Professional Work Experience")
        w_comp = st.text_input("Company Name", value="TechCorp Solutions", key="b_wcomp")
        w_role = st.text_input("Job Title / Role", value="Senior Software Engineer", key="b_wrole")
        w_dur = st.text_input("Duration / Dates", value="2022 - Present", key="b_wdur")
        w_desc = st.text_area(
            "Responsibilities & Key Achievements (Paste bullet points or draft text)",
            value="- Led development of microservices handling 20M+ daily requests using Go and Docker\n- Improved database query latency by 40% with PostgreSQL indexing and Caching\n- Mentored junior engineers on CI/CD GitOps pipelines",
            height=120,
            key="b_wdesc"
        )

    with ftab4:
        st.markdown("#### Key Technical Project")
        p_title = st.text_input("Project Title", value="Real-Time Analytics Pipeline", key="b_ptime")
        p_tech = st.text_input("Tech Stack", value="Python, Kafka, Redis, Docker", key="b_ptech")
        p_desc = st.text_area(
            "Project Summary & Achievements",
            value="- Built event-driven streaming pipeline processing 10k events/second\n- Integrated ML sentiment analysis model with sub-50ms latency",
            height=100,
            key="b_pdesc"
        )

    with ftab5:
        st.markdown("#### Technical & Soft Skills")
        s_input = st.text_area(
            "Enter Skills (Comma-separated or bullet list)",
            value="Python, Go, Docker, Kubernetes, AWS, PostgreSQL, Redis, Microservices, CI/CD, System Architecture, Agile Leadership",
            height=80,
            key="b_sinput"
        )

    with ftab6:
        st.markdown("#### Certifications & Credentials")
        crt_title = st.text_input("Certification Title", value="AWS Certified Solutions Architect - Associate", key="b_crt")
        crt_inst = st.text_input("Issuing Authority", value="Amazon Web Services", key="b_crinst")

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------------------------------------------
    # 3. AI Generation Action Button
    # -----------------------------------------------------------------------------
    if st.button("🤖 Generate AI Professional Resume", type="primary", use_container_width=True):
        # Prepare User Inputs Payload
        raw_inputs = {
            "Name": b_name,
            "Email": b_email,
            "Phone": b_phone,
            "Location": b_location,
            "LinkedIn": b_linkedin,
            "Professional_Summary": b_summary,
            "Skills": [s.strip() for s in s_input.split(",") if s.strip()],
            "Education": [{
                "Degree": e_deg,
                "Institution": e_inst,
                "Session": e_sess,
                "Score": e_score,
                "Description": e_high
            }] if e_deg else [],
            "Experience": [{
                "Company": w_comp,
                "Role": w_role,
                "Duration": w_dur,
                "Description": [b.strip("- ").strip() for b in w_desc.split("\n") if b.strip()]
            }] if w_comp else [],
            "Projects": [{
                "Title": p_title,
                "TechStack": p_tech,
                "Description": [b.strip("- ").strip() for b in p_desc.split("\n") if b.strip()]
            }] if p_title else [],
            "Certifications": [{
                "Certificate": crt_title,
                "Institution": crt_inst
            }] if crt_title else []
        }

        with st.status("🤖 AI Engine Refining Resume & Generating Action Bullets...", expanded=True) as status:
            st.write("Polishing professional summary with executive keywords...")
            polished_data = generate_ai_resume_func(raw_inputs)
            st.write("Formatting quantified achievement bullet points...")
            st.session_state["builder_resume_data"] = polished_data
            status.update(label="🎉 AI Resume Generation Complete!", state="complete", expanded=False)

    st.markdown('</div>', unsafe_allow_html=True)

    # Use input fallback or generated data
    builder_data = st.session_state.get("builder_resume_data")
    if not builder_data:
        # Fallback payload from live form
        builder_data = {
            "Name": b_name,
            "Email": b_email,
            "Phone": b_phone,
            "Location": b_location,
            "LinkedIn": b_linkedin,
            "Professional_Summary": b_summary,
            "Skills": [s.strip() for s in s_input.split(",") if s.strip()],
            "Education": [{"Degree": e_deg, "Institution": e_inst, "Session": e_sess, "Score": e_score, "Description": e_high}] if e_deg else [],
            "Experience": [{"Company": w_comp, "Role": w_role, "Duration": w_dur, "Description": [b.strip("- ").strip() for b in w_desc.split("\n") if b.strip()]}] if w_comp else [],
            "Projects": [{"Title": p_title, "TechStack": p_tech, "Description": [b.strip("- ").strip() for b in p_desc.split("\n") if b.strip()]}] if p_title else [],
            "Certifications": [{"Certificate": crt_title, "Institution": crt_inst}] if crt_title else []
        }

    # -----------------------------------------------------------------------------
    # 4. Live Interactive Preview & Export Action Cards
    # -----------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 👁 Live Interactive Resume Preview & Exports")

    # Template Visual Colors
    if template_style == "Modern Tech":
        header_color = "#059669"
    elif template_style == "Minimalist Clean":
        header_color = "#334155"
    elif template_style == "Creative Professional":
        header_color = "#6366F1"
    else:
        header_color = "#1E3A8A"

    col_prev, col_exp = st.columns([3, 2])

    with col_prev:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"#### 📄 Live Preview — `{template_style}` Template")
        
        # HTML/CSS Formatted Preview Card
        b_name_val = builder_data.get("Name", "Candidate Name")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 24px; font-family: 'Plus Jakarta Sans', sans-serif;">
            <div style="text-align: center; border-bottom: 2px solid {header_color}; padding-bottom: 12px; margin-bottom: 16px;">
                <h2 style="color: {header_color}; margin: 0; font-size: 1.8rem; font-weight: 800;">{b_name_val}</h2>
                <p style="font-size: 0.88rem; color: #94A3B8; margin-top: 4px;">
                    {' | '.join([b for b in [builder_data.get('Email'), builder_data.get('Phone'), builder_data.get('Location'), builder_data.get('LinkedIn')] if b])}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Summary Preview
        sum_val = builder_data.get("Professional_Summary", "")
        if sum_val:
            st.markdown(f"<h4 style='color:{header_color}; margin-bottom:4px;'>PROFESSIONAL SUMMARY</h4><p style='font-size:0.92rem; line-height:1.5;'>{sum_val}</p>", unsafe_allow_html=True)

        # Skills Preview
        skills_val = builder_data.get("Skills", [])
        if skills_val:
            badges = "".join([render_badge(s, "green", "●") for s in skills_val])
            st.markdown(f"<h4 style='color:{header_color}; margin: 12px 0 6px 0;'>TECHNICAL COMPETENCIES</h4><div style='margin-bottom:12px;'>{badges}</div>", unsafe_allow_html=True)

        # Experience Preview
        exp_val = builder_data.get("Experience", [])
        if exp_val:
            st.markdown(f"<h4 style='color:{header_color}; margin: 12px 0 6px 0;'>PROFESSIONAL EXPERIENCE</h4>", unsafe_allow_html=True)
            for exp in exp_val:
                if isinstance(exp, dict):
                    c_name = exp.get("Company", "")
                    c_role = exp.get("Role", "")
                    c_dur = exp.get("Duration", "")
                    st.markdown(f"**{c_role}** — `{c_name}` ({c_dur})")
                    bullets = exp.get("Bullet_Points") or exp.get("Description") or []
                    if isinstance(bullets, list):
                        for b in bullets:
                            st.markdown(f"• {b}")
                    elif bullets:
                        st.markdown(f"• {bullets}")
                else:
                    st.write(f"• {exp}")

        # Projects Preview
        proj_val = builder_data.get("Projects", [])
        if proj_val:
            st.markdown(f"<h4 style='color:{header_color}; margin: 12px 0 6px 0;'>KEY PROJECTS</h4>", unsafe_allow_html=True)
            for proj in proj_val:
                if isinstance(proj, dict):
                    p_title_val = proj.get("Title", "")
                    p_tech_val = proj.get("TechStack", "")
                    st.markdown(f"📌 **{p_title_val}** `[{p_tech_val}]`")
                    bullets = proj.get("Bullet_Points") or proj.get("Description") or []
                    if isinstance(bullets, list):
                        for b in bullets:
                            st.markdown(f"• {b}")
                    elif bullets:
                        st.markdown(f"• {bullets}")
                else:
                    st.write(f"📌 {proj}")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # EXPORT ACTION CARD
    with col_exp:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📥 Export Resume Files")
        st.write("Download your AI-built resume formatted in the selected template style.")

        # Generate PDF and DOCX bytes
        pdf_bytes = generate_builder_resume_pdf(builder_data, template_style)
        docx_bytes = generate_builder_resume_docx(builder_data, template_style)

        filename_prefix = b_name_val.replace(" ", "_")

        st.download_button(
            label="📄 Download PDF Resume",
            data=pdf_bytes,
            file_name=f"{filename_prefix}_{template_style.replace(' ', '_')}_Resume.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.download_button(
            label="📝 Download Word Document (.docx)",
            data=docx_bytes,
            file_name=f"{filename_prefix}_{template_style.replace(' ', '_')}_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
