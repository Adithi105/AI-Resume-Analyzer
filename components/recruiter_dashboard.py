"""
Recruiter Dashboard Module — Candidate database management, ATS score filter, recruiter verdict filter, search, and CSV export.
"""
import streamlit as st
from database.db import get_all_resumes
from helpers.export_helper import generate_candidates_csv
from typing import List, Dict, Any


def render_recruiter_dashboard():
    """Renders the Recruiter Candidate Management Dashboard."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #3B82F6, #6366F1);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            💼 Recruiter Candidate Management Portal
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Search, filter, rank, and export audited candidate resumes stored in the enterprise database.
        </p>
    </div>
    """, unsafe_allow_html=True)

    candidates = get_all_resumes()

    if not candidates:
        st.info("ℹ️ No candidate resumes currently stored in the database. Upload a resume in **AI Resume Analyzer** to populate records.")
        return

    # ─── Filter Bar ─────────────────────────────────────────────────────────
    st.markdown('<div class="glass-card" style="padding: 1.25rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("🔍 Filter & Search Candidates")

    col_search, col_verdict, col_score = st.columns([2, 1, 1])

    with col_search:
        search_query = st.text_input("Search Candidate Name / Email", placeholder="Type to search...", key="rec_search_query")
    with col_verdict:
        verdict_filter = st.selectbox("Recruiter Verdict", options=["All Verdicts", "Strong Hire", "Shortlist / Interview", "Borderline Candidate", "Reject / Re-align", "Under Review"], key="rec_verdict_filter")
    with col_score:
        min_score = st.slider("Min ATS Score", 0, 100, 0, key="rec_min_score")

    st.markdown('</div>', unsafe_allow_html=True)

    # Filter Logic
    filtered = []
    for c in candidates:
        name = c.get("candidate_name", "").lower()
        email = c.get("email", "").lower()
        query = search_query.lower().strip()
        v = c.get("recruiter_verdict", "")
        score = c.get("ats_score", 0)

        if query and (query not in name and query not in email):
            continue
        if verdict_filter != "All Verdicts" and v != verdict_filter:
            continue
        if score < min_score:
            continue
        filtered.append(c)

    # ─── Action Bar (CSV Export) ──────────────────────────────────────────────
    col_count, col_exp = st.columns([2, 1])
    with col_count:
        st.markdown(f"### 📋 Candidate Records ({len(filtered)} of {len(candidates)})")
    with col_exp:
        csv_bytes = generate_candidates_csv(filtered)
        st.download_button(
            "📥 Export Candidates CSV",
            data=csv_bytes,
            file_name="candidate_records_export.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
            key="btn_export_candidates_csv"
        )

    # ─── Candidate Cards / Table ─────────────────────────────────────────────
    for idx, c in enumerate(filtered, 1):
        score = c.get("ats_score", 0)
        verdict = c.get("recruiter_verdict", "Under Review")
        hiring_prob = c.get("hiring_probability", "0%")
        level = c.get("candidate_level", "Not Specified")

        v_color = "#10B981" if "Strong" in verdict or "Shortlist" in verdict else "#F59E0B" if "Borderline" in verdict else "#EF4444"

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 14px; padding: 16px; margin-bottom: 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="font-size:1.1rem; color:#F8FAFC;">#{idx} {c.get('candidate_name', 'Candidate')}</strong>
                    <span style="color:#94A3B8; font-size:0.85rem; margin-left:8px;">({c.get('email', 'N/A')})</span>
                </div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <span style="background:rgba(59,130,246,0.15); color:#60A5FA; padding:4px 12px; border-radius:12px; font-weight:700; font-size:0.85rem;">
                        ATS Score: {score}/100
                    </span>
                    <span style="background:{v_color}22; color:{v_color}; border:1px solid {v_color}44; padding:4px 12px; border-radius:12px; font-weight:700; font-size:0.85rem;">
                        {verdict}
                    </span>
                </div>
            </div>
            <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1; display:flex; gap:20px;">
                <span>🎯 Seniority: <strong>{level}</strong></span>
                <span>🔥 Hiring Prob: <strong>{hiring_prob}</strong></span>
                <span>📅 Date: <strong>{c.get('created_at', '')[:10]}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"🔍 Expand Details & Full AI Audit for #{idx} {c.get('candidate_name')}", expanded=False):
            full_json = c.get("full_json", {})
            st.markdown(f"**Executive Summary**: {full_json.get('Executive_Summary', 'N/A')}")
            st.markdown(f"**Technical Strengths**: {', '.join(full_json.get('Technical_Strengths', []))}")
            st.markdown(f"**Missing Skills**: {', '.join(full_json.get('Missing_Skills', []))}")
