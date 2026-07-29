import streamlit as st
from typing import Dict, Any, Callable
from components.ui_styles import render_badge
from helpers.report_generator import generate_improved_resume_pdf

def render_resume_rewriter_section(resume_text: str, candidate_name: str, rewrite_func: Callable[[str], Dict[str, Any]]):
    """
    Renders AI Resume Rewriter tab featuring the Improve Resume action trigger,
    Side-by-Side Comparison (Original vs Improved), and PDF Export.
    """
    st.subheader("✨ AI Resume Rewriter & ATS Enhancer")
    st.write("Transform raw resume content into high-impact, ATS-optimized bullet points led by action verbs, quantified metrics, and structured executive formatting.")

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if st.button("🚀 Improve Resume with AI", type="primary", use_container_width=True):
        if not resume_text:
            st.error("⚠️ Please upload a resume PDF first using the sidebar.")
            return

        with st.status("🤖 Rewriting Resume with Action Verbs & ATS Bullet Points...", expanded=True) as status:
            st.write("Optimizing professional summary and technical core competencies...")
            improved = rewrite_func(resume_text)
            st.write("Generating quantified achievement bullet points for work experience & projects...")
            st.session_state["improved_resume_data"] = improved
            status.update(label="🎉 Resume Rewriting Complete!", state="complete", expanded=False)

    st.markdown('</div>', unsafe_allow_html=True)

    improved_data = st.session_state.get("improved_resume_data")

    # Side-by-Side Comparison Container
    if improved_data or resume_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔄 Side-by-Side Resume Comparison")

        col1, col2 = st.columns(2)

        # LEFT COLUMN: Original Resume
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📄 Original Resume")
            st.caption("Raw extracted content before AI optimization")
            if resume_text:
                st.code(resume_text, language="text")
            else:
                st.info("No original text uploaded.")
            st.markdown('</div>', unsafe_allow_html=True)

        # RIGHT COLUMN: Improved ATS Resume
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("✨ Improved ATS-Optimized Resume")
            st.caption("Rewritten with action verbs, quantified ROI, and clear bullet structure")

            if improved_data:
                # Professional Summary
                prof_sum = improved_data.get("Professional_Summary")
                if prof_sum:
                    st.markdown("#### 📝 Professional Summary")
                    st.markdown(f"<p style='font-size: 0.95rem; line-height: 1.6;'>{prof_sum}</p>", unsafe_allow_html=True)
                    st.divider()

                # Skills
                skills = improved_data.get("Skills", [])
                if skills:
                    st.markdown("#### 🛠 Technical & Core Skills")
                    badges = "".join([render_badge(s, "green", "●") for s in skills])
                    st.markdown(badges, unsafe_allow_html=True)
                    st.divider()

                # Experience
                exp_list = improved_data.get("Experience", [])
                if exp_list:
                    st.markdown("#### 💼 Professional Experience")
                    for exp in exp_list:
                        if isinstance(exp, dict):
                            company = exp.get("Company", "Company")
                            role = exp.get("Role", "Role")
                            duration = exp.get("Duration", "")
                            bullets = exp.get("Bullet_Points") or exp.get("Description") or []

                            st.markdown(f"**{role}** — `{company}` ({duration})")
                            if isinstance(bullets, list):
                                for b in bullets:
                                    st.markdown(f"• {b}")
                            elif bullets:
                                st.markdown(f"• {bullets}")
                        else:
                            st.write(f"• {exp}")
                        st.markdown("<br>", unsafe_allow_html=True)
                    st.divider()

                # Key Projects
                proj_list = improved_data.get("Projects", [])
                if proj_list:
                    st.markdown("#### 💻 Technical Projects")
                    for proj in proj_list:
                        if isinstance(proj, dict):
                            title = proj.get("Title", "Project")
                            tech = proj.get("TechStack", "")
                            bullets = proj.get("Bullet_Points") or proj.get("Description") or []

                            st.markdown(f"📌 **{title}** `[{tech}]`")
                            if isinstance(bullets, list):
                                for b in bullets:
                                    st.markdown(f"• {b}")
                            elif bullets:
                                st.markdown(f"• {bullets}")
                        else:
                            st.write(f"📌 {proj}")
                        st.markdown("<br>", unsafe_allow_html=True)
                    st.divider()

                # Key Achievements
                achievements = improved_data.get("Achievements", [])
                if achievements:
                    st.markdown("#### 🏆 Quantified Key Achievements")
                    for a in achievements:
                        st.markdown(f'<div class="strength-box">🏆 {a}</div>', unsafe_allow_html=True)
                    st.divider()

                # Education
                edu_list = improved_data.get("Education", [])
                if edu_list:
                    st.markdown("#### 🎓 Education Credentials")
                    for edu in edu_list:
                        if isinstance(edu, dict):
                            deg = edu.get("Degree", "Degree")
                            inst = edu.get("Institution", "")
                            session = edu.get("Session", "")
                            high = edu.get("Highlights") or edu.get("Description") or ""
                            st.markdown(f"🏫 **{deg}** — {inst} (`{session}`)")
                            if high:
                                st.caption(f"• {high}")
                        else:
                            st.write(f"🎓 {edu}")

                st.markdown("<br>", unsafe_allow_html=True)

                # PDF Export for Improved Resume
                pdf_bytes = generate_improved_resume_pdf(improved_data, candidate_name)
                st.download_button(
                    label="📄 Export Improved Resume as PDF",
                    data=pdf_bytes,
                    file_name=f"{candidate_name}_Improved_ATS_Resume.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            else:
                st.info("👈 Click **'🚀 Improve Resume with AI'** above to generate the rewritten ATS resume!")
            st.markdown('</div>', unsafe_allow_html=True)
