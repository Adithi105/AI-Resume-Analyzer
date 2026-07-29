"""
Interview Preparation Module — UI Component

Provides tailored interview questions with difficulty tags (Easy, Medium, Hard),
AI model answers (STAR methodology), interviewer tips, category filters, and an
interactive Interview Score Simulation dashboard.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Callable

DIFFICULTY_STYLES = {
    "Easy": {"bg": "rgba(16, 185, 129, 0.15)", "color": "#10B981", "border": "rgba(16, 185, 129, 0.4)", "icon": "🟢"},
    "Medium": {"bg": "rgba(245, 158, 11, 0.15)", "color": "#F59E0B", "border": "rgba(245, 158, 11, 0.4)", "icon": "🟡"},
    "Hard": {"bg": "rgba(239, 68, 68, 0.15)", "color": "#EF4444", "border": "rgba(239, 68, 68, 0.4)", "icon": "🔴"},
}

CATEGORY_ICONS = {
    "Technical": "💻",
    "HR": "👥",
    "Behavioural": "🧠",
    "Coding": "⚡",
    "Project": "🏗️",
}


def _render_difficulty_badge(difficulty: str) -> str:
    style = DIFFICULTY_STYLES.get(difficulty, DIFFICULTY_STYLES["Medium"])
    return f"""
    <span style="background: {style['bg']}; color: {style['color']}; border: 1px solid {style['border']};
                 padding: 2px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 600;
                 display: inline-flex; align-items: center; gap: 4px;">
        {style['icon']} {difficulty}
    </span>
    """


def _render_score_gauge(score: int) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "/100", "font": {"size": 28, "color": "#F8FAFC"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748B"},
            "bar": {"color": "#3B82F6", "thickness": 0.25},
            "bgcolor": "rgba(30, 41, 59, 0.5)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "rgba(239, 68, 68, 0.2)"},
                {"range": [50, 75], "color": "rgba(245, 158, 11, 0.2)"},
                {"range": [75, 100], "color": "rgba(16, 185, 129, 0.2)"},
            ],
        }
    ))
    fig.update_layout(
        height=180,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC", "family": "Inter, sans-serif"}
    )
    return fig


def render_question_card(q_data: Dict[str, Any], index: int, category: str):
    question = q_data.get("Question", "Question not available")
    difficulty = q_data.get("Difficulty", "Medium")
    answer = q_data.get("Answer", "No answer provided")
    tips = q_data.get("Tips", "")
    badge_html = _render_difficulty_badge(difficulty)
    icon = CATEGORY_ICONS.get(category, "❓")

    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px; padding: 16px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
            <div style="font-weight: 600; font-size: 1.02rem; color: #F8FAFC; line-height: 1.4;">
                {icon} Q{index}: {question}
            </div>
            <div>{badge_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"💡 View AI Model Answer & Interviewer Tips (Q{index})", expanded=False):
        st.markdown(f"**🤖 AI Model Answer:**\n\n{answer}")
        if tips:
            st.info(f"🎯 **Interviewer Tip**: {tips}")


def render_interview_prep_section(
    resume_text: str,
    generate_interview_fn: Callable[[str, str], Dict[str, Any]]
):
    """Renders the complete Interview Preparation Module tab."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #6366F1, #A855F7);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎯 AI Interview Preparation & Simulation
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Practice role-specific interview questions generated from your resume and target JD across Technical, HR, Behavioural, Coding, and Project categories.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Input & Trigger Bar ──────────────────────────────────────────
    with st.container():
        st.markdown('<div class="glass-card" style="padding: 1.25rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
        st.subheader("🎯 Target Position Context (Optional)")
        target_jd = st.text_area(
            "Paste Target Job Description (or leave empty for general role analysis)",
            height=100,
            placeholder="Paste Job Description to tailor interview questions specifically to job requirements...",
            key="interview_target_jd"
        )
        col_btn, col_info = st.columns([1, 2])
        with col_btn:
            generate_clicked = st.button(
                "⚡ Generate AI Interview Prep",
                type="primary",
                use_container_width=True,
                key="btn_generate_interview"
            )
        with col_info:
            st.caption("AI analyzes resume skills, project complexity, and target JD requirements to simulate interview performance and generate tailored Q&A.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Execute generation if clicked or retrieve cached results
    if generate_clicked:
        with st.spinner("🤖 Generating tailored interview questions and calculating readiness score..."):
            interview_data = generate_interview_fn(resume_text, target_jd)
            st.session_state["interview_data"] = interview_data
            st.success("🎉 Interview Preparation Package & Readiness Simulation Generated!")

    interview_data = st.session_state.get("interview_data")

    if not interview_data:
        st.info("👆 Click **Generate AI Interview Prep** above to generate tailored questions, model answers, and your simulated readiness score.")
        return

    # ─── Interview Readiness Score Simulation Dashboard ──────────────
    st.markdown('<div class="glass-card" style="margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("📊 Interview Readiness Score Simulation")

    score = interview_data.get("Interview_Score", 0)
    breakdown = interview_data.get("Score_Breakdown", {})
    summary = interview_data.get("Score_Summary", "")

    col_gauge, col_bars = st.columns([1, 2])

    with col_gauge:
        st.markdown("<div style='text-align: center; font-weight: 700; color: #94A3B8; margin-bottom: -10px;'>Overall Readiness Score</div>", unsafe_allow_html=True)
        st.plotly_chart(_render_score_gauge(score), use_container_width=True)
        verdict_color = "#10B981" if score >= 75 else "#F59E0B" if score >= 50 else "#EF4444"
        verdict_text = "Interview Ready 🔥" if score >= 75 else "Needs Refinement ⚠️" if score >= 50 else "High Preparation Needed 🛑"
        st.markdown(f"<div style='text-align: center; color: {verdict_color}; font-weight: 700; font-size: 1.1rem; margin-top: -15px;'>{verdict_text}</div>", unsafe_allow_html=True)

    with col_bars:
        st.markdown(f"<p style='color: #CBD5E1; font-size: 0.95rem; line-height: 1.5;'>{summary}</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for cat_name, cat_score in breakdown.items():
            icon = CATEGORY_ICONS.get(cat_name, "📌")
            col_lbl, col_prog = st.columns([1, 3])
            with col_lbl:
                st.markdown(f"**{icon} {cat_name}**")
            with col_prog:
                st.progress(cat_score / 100.0, text=f"{cat_score}%")

    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Question Categories & Difficulty Filter ─────────────────────
    st.markdown("### 📚 Interview Question Bank")

    col_diff, col_search = st.columns([1, 2])
    with col_diff:
        selected_difficulty = st.selectbox(
            "Filter by Difficulty Level",
            options=["All Difficulties", "Easy", "Medium", "Hard"],
            key="interview_diff_filter"
        )

    # Category Tabs
    t_tech, t_hr, t_behav, t_code, t_proj = st.tabs([
        "💻 Technical (3)",
        "👥 HR & Culture (2)",
        "🧠 Behavioural (STAR) (2)",
        "⚡ Coding & System (2)",
        "🏗️ Project Deep Dive (2)"
    ])

    tab_map = [
        (t_tech, "Technical_Questions", "Technical"),
        (t_hr, "HR_Questions", "HR"),
        (t_behav, "Behavioural_Questions", "Behavioural"),
        (t_code, "Coding_Questions", "Coding"),
        (t_proj, "Project_Questions", "Project"),
    ]

    for tab, cat_key, cat_name in tab_map:
        with tab:
            questions = interview_data.get(cat_key, [])
            if selected_difficulty != "All Difficulties":
                questions = [q for q in questions if q.get("Difficulty") == selected_difficulty]

            if not questions:
                st.info(f"No {selected_difficulty} difficulty questions found in this category.")
            else:
                for idx, q_item in enumerate(questions, 1):
                    render_question_card(q_item, idx, cat_name)
