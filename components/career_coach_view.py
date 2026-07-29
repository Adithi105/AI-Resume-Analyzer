"""
AI Career Coach Module — UI Component

Generates and renders an executive career coaching dashboard including:
  - Career Roadmap (3 phases)
  - Learning Path
  - Weekly Study Plan & Monthly Goals
  - Recommended Courses & Certifications
  - Salary Estimation & Market Outlook
  - Suitable Job Roles & Match Percentages
  - Internship Suggestions & Company Recommendations
  - Skill Gap Analysis (Mastery vs. Gaps)
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Callable


def render_career_coach_section(
    resume_text: str,
    generate_coaching_fn: Callable[[str, str, str], Dict[str, Any]]
):
    """Renders the AI Career Coach Dashboard UI."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #10B981, #3B82F6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🧭 AI Executive Career Coach & Strategy Architect
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Personalized career roadmaps, weekly study plans, salary benchmarks, skill gap analysis, and target company recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Form Controls ──────────────────────────────────────────────────────
    st.markdown('<div class="glass-card" style="padding: 1.25rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("🎯 Career Goal Configuration")

    col_role, col_level = st.columns(2)

    with col_role:
        target_role = st.text_input(
            "Target Job Role",
            value="Senior Backend / Cloud Engineer",
            placeholder="e.g. Lead Machine Learning Engineer, DevOps Architect...",
            key="coach_target_role"
        )
    with col_level:
        experience_level = st.selectbox(
            "Target Experience Level",
            options=["Entry Level (0-2 YOE)", "Mid Level (3-5 YOE)", "Senior Level (6-8 YOE)", "Staff / Principal (9+ YOE)"],
            index=1,
            key="coach_exp_level"
        )

    col_btn, col_hint = st.columns([1, 2])
    with col_btn:
        generate_clicked = st.button(
            "🧭 Generate AI Career Plan",
            type="primary",
            use_container_width=True,
            key="btn_generate_career_plan"
        )
    with col_hint:
        st.caption("AI analyzes candidate background, target role requirements, and salary market data to build a custom career strategy.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Trigger or load cached coaching data
    if generate_clicked:
        with st.spinner("🤖 Architectural AI coach assembling personalized career roadmap and study plan..."):
            coaching_data = generate_coaching_fn(resume_text, target_role, experience_level)
            st.session_state["coaching_data"] = coaching_data
            st.success("🎉 AI Career Coaching Strategy & Dashboard Generated!")

    coaching_data = st.session_state.get("coaching_data")

    if not coaching_data:
        st.info("👆 Configure your target role and experience level above, then click **Generate AI Career Plan** to launch your dashboard.")
        return

    # ─── Executive Compensation & Market Outlook ───────────────────────────
    st.markdown("### 💰 Executive Compensation & Market Outlook")

    sal = coaching_data.get("Salary_Estimation", {})
    currency = sal.get("Currency", "USD")
    market_outlook = sal.get("Market_Outlook", "High Demand")

    c_entry, c_mid, c_senior, c_outlook = st.columns(4)

    with c_entry:
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3);
                    border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #60A5FA; letter-spacing:0.05em;">Entry Level</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{sal.get('Entry_Level', 'N/A')}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">0 - 2 YOE ({currency})</div>
        </div>
        """, unsafe_allow_html=True)

    with c_mid:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #34D399; letter-spacing:0.05em;">Mid Level</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{sal.get('Mid_Level', 'N/A')}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">3 - 5 YOE ({currency})</div>
        </div>
        """, unsafe_allow_html=True)

    with c_senior:
        st.markdown(f"""
        <div style="background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.3);
                    border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #C084FC; letter-spacing:0.05em;">Senior Level</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{sal.get('Senior_Level', 'N/A')}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">6+ YOE ({currency})</div>
        </div>
        """, unsafe_allow_html=True)

    with c_outlook:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3);
                    border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #FBBF24; letter-spacing:0.05em;">Market Demand</div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #F8FAFC; margin: 6px 0;">🔥 {market_outlook}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Growth Velocity</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Skill Gap Analysis & Suitable Job Roles ───────────────────────────
    col_gap, col_roles = st.columns([1, 1])

    with col_gap:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎯 Skill Gap Analysis")
        sg = coaching_data.get("Skill_Gap_Analysis", {})

        st.markdown("**✅ Current Technical Mastery**:")
        st.write(", ".join([f"`{s}`" for s in sg.get("Current_Mastery", [])]))

        st.markdown("**🛑 Priority Skill Gaps to Close**:")
        for g in sg.get("Gaps_To_Close", []):
            st.markdown(f"- 📌 **{g}**")

        st.info(f"🎯 **Critical Focus Area**: {sg.get('Critical_Focus_Area', '')}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_roles:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👔 Suitable Job Roles & Match %")
        roles = coaching_data.get("Suitable_Job_Roles", [])
        for r_item in roles:
            r_name = r_item.get("Role", "Role")
            r_match = r_item.get("Match_Percentage", 80)
            st.markdown(f"**{r_name}** ({r_match}% Match)")
            st.progress(r_match / 100.0)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Career Roadmap (3 Phases) ──────────────────────────────────────────
    st.markdown("### 🗺️ Strategic Career Roadmap")
    roadmap = coaching_data.get("Career_Roadmap", [])

    rm_cols = st.columns(len(roadmap) if roadmap else 3)
    for idx, phase in enumerate(roadmap):
        with rm_cols[min(idx, len(rm_cols)-1)]:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 14px; padding: 18px; height: 100%;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #818CF8; text-transform: uppercase;">
                    {phase.get('Phase', 'Phase')}
                </div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC; margin: 6px 0 10px 0;">
                    {phase.get('Focus', 'Focus Area')}
                </div>
                <div style="font-size: 0.88rem; color: #CBD5E1;">
            """, unsafe_allow_html=True)
            for m in phase.get("Milestones", []):
                st.markdown(f"- 🎯 {m}")
            st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Learning Path, Weekly Study Plan & Monthly Goals ──────────────────
    col_path, col_plan = st.columns([1, 1])

    with col_path:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📚 Learning Path & Core Topics")
        for topic in coaching_data.get("Learning_Path", []):
            st.markdown(f"- 📖 {topic}")

        st.divider()

        st.subheader("🏆 Monthly Goal Milestones")
        for mg in coaching_data.get("Monthly_Goals", []):
            st.markdown(f"**{mg.get('Month', 'Month')}**: {mg.get('Goal', '')}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_plan:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📅 Weekly Study Plan")
        wsp = coaching_data.get("Weekly_Study_Plan", [])
        for w in wsp:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border-left: 3px solid #10B981;
                        padding: 10px 14px; margin-bottom: 10px; border-radius: 0 8px 8px 0;">
                <div style="display:flex; justify-content:space-between;">
                    <strong style="color:#10B981;">{w.get('Week', 'Week')}</strong>
                    <span style="font-size:0.8rem; color:#94A3B8;">⏱️ {w.get('Hours', 10)} hrs/week</span>
                </div>
                <div style="color:#F8FAFC; font-weight:600; margin:2px 0;">{w.get('Topic', '')}</div>
                <div style="font-size:0.82rem; color:#CBD5E1;">📦 Deliverable: {w.get('Deliverable', '')}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Courses & Certifications ──────────────────────────────────────────
    col_courses, col_certs = st.columns(2)

    with col_courses:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎓 Recommended Courses")
        for c in coaching_data.get("Recommended_Courses", []):
            st.markdown(f"""
            - 📚 **{c.get('Course', '')}**  
              *Platform*: `{c.get('Platform', '')}` | *Target Skill*: `{c.get('Skill_Target', '')}`
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_certs:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📜 Recommended Certifications")
        for cert in coaching_data.get("Recommended_Certifications", []):
            st.markdown(f"""
            - 🏅 **{cert.get('Certification', '')}**  
              *Provider*: `{cert.get('Provider', '')}` | *Level*: `{cert.get('Difficulty', '')}`
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Internship & Company Recommendations ──────────────────────────────
    col_intern, col_comp = st.columns(2)

    with col_intern:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🚀 Internship & Apprenticeship Suggestions")
        for i_item in coaching_data.get("Internship_Suggestions", []):
            st.markdown(f"""
            - 💼 **{i_item.get('Track', '')}**  
              *Company Types*: `{i_item.get('Company_Types', '')}`  
              *Focus*: {i_item.get('Key_Focus', '')}
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_comp:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🏢 Target Company Recommendations")
        for comp in coaching_data.get("Company_Recommendations", []):
            st.markdown(f"""
            - 🏢 **{comp.get('Company', '')}** (`{comp.get('Type', '')}`)  
              *Why Fit*: {comp.get('Why_Fit', '')}
            """)
        st.markdown('</div>', unsafe_allow_html=True)
