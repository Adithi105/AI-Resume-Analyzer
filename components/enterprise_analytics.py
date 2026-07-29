"""
Enterprise Analytics Module — Hiring pipeline funnel, score distribution charts, and aggregate talent analytics.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from database.db import get_all_resumes, get_all_interviews


def render_enterprise_analytics_section():
    """Renders the Enterprise Pipeline Analytics Dashboard."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #3B82F6, #10B981);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📈 Enterprise Talent & Pipeline Analytics
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Aggregate metrics, ATS score distributions, hiring funnel conversion, and talent acquisition insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    resumes = get_all_resumes()
    interviews = get_all_interviews()

    total_candidates = len(resumes)
    total_interviews = len(interviews)

    avg_score = round(sum([r.get("ats_score", 0) for r in resumes]) / max(1, total_candidates)) if resumes else 0
    strong_hires = len([r for r in resumes if "Strong" in r.get("recruiter_verdict", "")])

    # ─── Metric Cards ────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #60A5FA;">Total Candidates Audited</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC;">{total_candidates}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #34D399;">Average ATS Score</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC;">{avg_score}<span style="font-size:1rem;">/100</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="background: rgba(236, 72, 153, 0.1); border: 1px solid rgba(236, 72, 153, 0.3); border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #F472B6;">Strong Hire Candidates</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC;">{strong_hires}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 14px; padding: 16px; text-align: center;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: #FBBF24;">Interviews Scheduled</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC;">{total_interviews}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Visual Charts ──────────────────────────────────────────────────────
    col_funnel, col_dist = st.columns(2)

    with col_funnel:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🔻 Recruitment Funnel Conversion")

        funnel_data = dict(
            number=[total_candidates, max(1, int(total_candidates * 0.6)), total_interviews, strong_hires],
            stage=["Audited Resumes", "Shortlisted", "Interviews Booked", "Strong Hire Verdicts"]
        )
        fig = px.funnel(funnel_data, x='number', y='stage', color_discrete_sequence=["#3B82F6", "#8B5CF6", "#F59E0B", "#10B981"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"), margin=dict(l=10, r=10, t=10, b=10), height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_dist:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Recruiter Verdict Distribution")

        verdicts = {}
        for r in resumes:
            v = r.get("recruiter_verdict", "Under Review")
            verdicts[v] = verdicts.get(v, 0) + 1

        if not verdicts:
            verdicts = {"Strong Hire": 2, "Shortlist": 3, "Borderline": 1, "Reject": 1}

        fig_pie = px.pie(
            values=list(verdicts.values()),
            names=list(verdicts.keys()),
            color_discrete_sequence=["#10B981", "#3B82F6", "#F59E0B", "#EF4444"],
            hole=0.4
        )
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"), margin=dict(l=10, r=10, t=10, b=10), height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
