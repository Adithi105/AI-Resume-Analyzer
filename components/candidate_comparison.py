"""
Candidate Comparison & Resume Ranking Module — Side-by-side comparison of 2-4 candidates
and automated ATS score ranking engine.
"""
import streamlit as st
import plotly.graph_objects as go
from database.db import get_all_resumes
from helpers.export_helper import generate_candidate_rankings_csv
from typing import List, Dict, Any


def render_candidate_comparison_section():
    """Renders the Candidate Comparison & Resume Ranking Interface."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #EC4899, #8B5CF6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📊 Candidate Comparison & Resume Ranking Engine
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Compare candidate profiles side-by-side across weighted ATS scores, technical competencies, and recruiter verdicts.
        </p>
    </div>
    """, unsafe_allow_html=True)

    resumes = get_all_resumes()

    if len(resumes) < 2:
        st.info("ℹ️ Minimum 2 candidate resume records required for comparison. Upload resumes in **AI Resume Analyzer** to compare.")
        return

    candidate_options = {f"{r['candidate_name']} ({r['email']}) - Score: {r['ats_score']}": r for r in resumes}

    st.markdown('<div class="glass-card" style="padding: 1.25rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("👥 Select Candidates to Compare (2 to 4 Candidates)")

    selected_labels = st.multiselect(
        "Choose Candidates",
        options=list(candidate_options.keys()),
        default=list(candidate_options.keys())[:min(3, len(candidate_options))],
        key="comp_multiselect"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if not selected_labels:
        st.warning("Please select at least 2 candidates above.")
        return

    selected_candidates = [candidate_options[lbl] for lbl in selected_labels]
    # Sort selected by ATS score descending
    selected_candidates.sort(key=lambda x: x.get("ats_score", 0), reverse=True)

    # ─── Ranked Leaderboard ──────────────────────────────────────────────────
    col_rank_head, col_rank_csv = st.columns([2, 1])
    with col_rank_head:
        st.markdown("### 🏆 Automated Candidate Leaderboard")
    with col_rank_csv:
        csv_bytes = generate_candidate_rankings_csv(selected_candidates)
        st.download_button(
            "📥 Export Rankings CSV",
            data=csv_bytes,
            file_name="candidate_rankings.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
            key="btn_export_rankings_csv"
        )

    for rank, c in enumerate(selected_candidates, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏅"
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px; padding: 14px 20px; margin-bottom: 10px;
                    display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #F8FAFC;">
                {medal} Rank #{rank}: {c.get('candidate_name')}
            </div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #60A5FA;">
                Overall Score: {c.get('ats_score')}/100
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Side-by-Side Comparison Matrix ─────────────────────────────────────
    st.markdown("### ⚔️ Side-by-Side Diagnostic Comparison")

    cols = st.columns(len(selected_candidates))

    for idx, c in enumerate(selected_candidates):
        full_json = c.get("full_json", {})
        ats_breakdown = full_json.get("ATS_Breakdown", {})

        with cols[idx]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                        border-radius: 14px; padding: 16px; height: 100%;">
                <h4 style="margin: 0; color: #F8FAFC;">{c.get('candidate_name')}</h4>
                <p style="color: #94A3B8; font-size: 0.8rem;">{c.get('email')}</p>
                <div style="font-size: 1.8rem; font-weight: 800; color: #38BDF8; margin: 8px 0;">
                    {c.get('ats_score')}<span style="font-size:1rem; color:#94A3B8;">/100</span>
                </div>
                <div style="background: rgba(16,185,129,0.15); color: #34D399; padding: 4px 10px; border-radius: 10px; font-weight: 700; font-size: 0.8rem; display:inline-block; margin-bottom: 12px;">
                    {c.get('recruiter_verdict')}
                </div>
                <hr style="border-color: rgba(255,255,255,0.08); margin: 10px 0;">
                <div style="font-size: 0.85rem; color: #CBD5E1;">
                    <p><strong>Seniority Level:</strong> {c.get('candidate_level')}</p>
                    <p><strong>Hiring Probability:</strong> {c.get('hiring_probability')}</p>
                    <p><strong>Skills Score:</strong> {ats_breakdown.get('Skills_Score', 0)}%</p>
                    <p><strong>Experience Score:</strong> {ats_breakdown.get('Experience_Score', 0)}%</p>
                    <p><strong>Projects Score:</strong> {ats_breakdown.get('Projects_Score', 0)}%</p>
                    <p><strong>Formatting Score:</strong> {ats_breakdown.get('Formatting_Score', 0)}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
