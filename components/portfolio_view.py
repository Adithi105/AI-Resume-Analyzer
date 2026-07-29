"""
Portfolio Analyzer Module — UI Component

Analyzes candidate GitHub profile, LinkedIn profile, and Portfolio website.
Displays score cards, Plotly radar & bar charts, Repository Quality analysis,
Project Quality, Contribution Analysis, Improvement Suggestions, and Tech Recommendations.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Callable


def _create_radar_chart(metrics: Dict[str, int]) -> go.Figure:
    """Create a sleek Plotly radar chart for portfolio quality metrics."""
    categories = [k.replace("_", " ") for k in metrics.keys()]
    values = list(metrics.values())

    # Close the radar polygon
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(99, 102, 241, 0.25)",
        line=dict(color="#6366F1", width=3),
        name="Portfolio Audit",
        marker=dict(size=6, color="#818CF8")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#94A3B8", size=10),
                gridcolor="rgba(255, 255, 255, 0.1)"
            ),
            angularaxis=dict(
                tickfont=dict(color="#F8FAFC", size=11, family="Inter, sans-serif"),
                gridcolor="rgba(255, 255, 255, 0.1)"
            ),
            bgcolor="rgba(0, 0, 0, 0)"
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=40, r=40, t=30, b=30),
        height=320,
        showlegend=False
    )
    return fig


def _create_scores_bar_chart(scores: Dict[str, int]) -> go.Figure:
    """Create horizontal bar chart comparing platform scores."""
    labels = list(scores.keys())
    vals = list(scores.values())
    colors = ["#A78BFA", "#38BDF8", "#34D399"]

    fig = go.Figure(go.Bar(
        x=vals,
        y=labels,
        orientation="h",
        marker=dict(
            color=colors[:len(labels)],
            line=dict(color="rgba(255, 255, 255, 0.2)", width=1)
        ),
        text=[f"{v}%" for v in vals],
        textposition="inside",
        insidetextfont=dict(color="#FFFFFF", size=12, family="Inter, sans-serif")
    ))

    fig.update_layout(
        xaxis=dict(range=[0, 100], gridcolor="rgba(255, 255, 255, 0.08)", tickfont=dict(color="#94A3B8")),
        yaxis=dict(tickfont=dict(color="#F8FAFC", size=12)),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=20, r=20, t=20, b=20),
        height=220
    )
    return fig


def render_portfolio_analyzer_section(
    analyze_portfolio_fn: Callable[[str, str, str, str], Dict[str, Any]]
):
    """Renders the complete Portfolio Analyzer interface."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #38BDF8, #818CF8);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌐 Developer Portfolio & Online Presence Analyzer
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Audit GitHub code quality, LinkedIn professional completeness, and Portfolio website design/responsiveness.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Form Inputs ────────────────────────────────────────────────────────
    st.markdown('<div class="glass-card" style="padding: 1.25rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.subheader("🔗 Candidate Profiles & Portfolio Links")

    col_gh, col_li, col_web = st.columns(3)

    with col_gh:
        github_url = st.text_input(
            "🐱 GitHub Profile / Username",
            placeholder="https://github.com/username",
            key="port_gh_url"
        )
    with col_li:
        linkedin_url = st.text_input(
            "💼 LinkedIn Profile URL",
            placeholder="https://linkedin.com/in/username",
            key="port_li_url"
        )
    with col_web:
        portfolio_url = st.text_input(
            "🌐 Portfolio Website URL",
            placeholder="https://myportfolio.dev",
            key="port_web_url"
        )

    candidate_notes = st.text_area(
        "📝 Candidate Bio / Project Context / Resume Excerpt (Optional)",
        height=90,
        placeholder="Add extra context about your top open-source projects, key repos, or tech stack...",
        key="port_notes"
    )

    col_btn, col_hint = st.columns([1, 2])
    with col_btn:
        analyze_clicked = st.button(
            "🌐 Analyze Portfolio & Presence",
            type="primary",
            use_container_width=True,
            key="btn_analyze_portfolio"
        )
    with col_hint:
        st.caption("AI evaluates repository structure, commit consistency, README quality, LinkedIn completeness, and UI aesthetics.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Trigger or retrieve cached portfolio data
    if analyze_clicked:
        if not any([github_url, linkedin_url, portfolio_url, candidate_notes]):
            st.warning("⚠️ Please provide at least one link (GitHub, LinkedIn, or Portfolio) or enter candidate notes to run the audit.")
        else:
            with st.spinner("🤖 Auditing GitHub repositories, LinkedIn completeness, and Portfolio design..."):
                portfolio_data = analyze_portfolio_fn(
                    github_url, linkedin_url, portfolio_url, candidate_notes
                )
                st.session_state["portfolio_data"] = portfolio_data
                st.success("🎉 Portfolio & Online Presence Audit Complete!")

    portfolio_data = st.session_state.get("portfolio_data")

    if not portfolio_data:
        st.info("👆 Enter your GitHub, LinkedIn, or Portfolio URL above and click **Analyze Portfolio & Presence** to generate your audit report.")
        return

    # ─── Executive Score Cards ──────────────────────────────────────────────
    st.markdown("### 📊 Presence & Quality Score Cards")

    overall = portfolio_data.get("Overall_Portfolio_Score", 0)
    gh_score = portfolio_data.get("GitHub_Score", 0)
    li_score = portfolio_data.get("LinkedIn_Score", 0)
    web_score = portfolio_data.get("Portfolio_Website_Score", 0)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div style="background: rgba(167, 139, 250, 0.1); border: 1px solid rgba(167, 139, 250, 0.3);
                    border-radius: 14px; padding: 18px; text-align: center;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: #A78BFA;">Overall Brand Score</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{overall}<span style="font-size:1.1rem; color:#A78BFA;">/100</span></div>
            <div style="font-size: 0.78rem; color: #94A3B8;">Combined Presence Quality</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3);
                    border-radius: 14px; padding: 18px; text-align: center;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: #38BDF8;">🐱 GitHub Score</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{gh_score}<span style="font-size:1.1rem; color:#38BDF8;">/100</span></div>
            <div style="font-size: 0.78rem; color: #94A3B8;">Code & Repositories</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3);
                    border-radius: 14px; padding: 18px; text-align: center;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: #34D399;">💼 LinkedIn Score</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{li_score}<span style="font-size:1.1rem; color:#34D399;">/100</span></div>
            <div style="font-size: 0.78rem; color: #94A3B8;">Professional Completeness</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div style="background: rgba(244, 114, 182, 0.1); border: 1px solid rgba(244, 114, 182, 0.3);
                    border-radius: 14px; padding: 18px; text-align: center;">
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; color: #F472B6;">🌐 Portfolio Score</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin: 4px 0;">{web_score}<span style="font-size:1.1rem; color:#F472B6;">/100</span></div>
            <div style="font-size: 0.78rem; color: #94A3B8;">Design & Showcase</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Visual Charts ──────────────────────────────────────────────────────
    col_radar, col_bar = st.columns([1, 1])

    with col_radar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🕸️ Multi-Dimension Quality Radar")
        mb = portfolio_data.get("Metrics_Breakdown", {})
        st.plotly_chart(_create_radar_chart(mb), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_bar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Platform Performance Comparison")
        scores_dict = {
            "🐱 GitHub": gh_score,
            "💼 LinkedIn": li_score,
            "🌐 Portfolio": web_score,
        }
        st.plotly_chart(_create_scores_bar_chart(scores_dict), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Platform Audits ───────────────────────────────────────────────────
    st.markdown("### 🔎 Detailed Diagnostic Audits")

    gh_info = portfolio_data.get("GitHub_Analysis", {})
    li_info = portfolio_data.get("LinkedIn_Analysis", {})
    web_info = portfolio_data.get("Portfolio_Website_Analysis", {})

    col_gh_card, col_li_card = st.columns(2)

    with col_gh_card:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🐱 GitHub Repository & Code Quality")
        st.markdown(f"**Repository Audit**: {gh_info.get('Repository_Quality', '')}")
        st.markdown("**Top Tech & Languages Detected**:")
        st.write(", ".join([f"`{lang}`" for lang in gh_info.get("Top_Languages", [])]))

        st.markdown("**Highlights**:")
        for h in gh_info.get("Highlights", []):
            st.markdown(f"- ✅ {h}")

        st.markdown("**Risks / Gaps**:")
        for r in gh_info.get("Risks", []):
            st.markdown(f"- ⚠️ {r}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_li_card:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💼 LinkedIn Completeness Audit")
        st.markdown(f"**Profile Completeness**: {li_info.get('Profile_Completeness', '')}")

        st.markdown("**Strengths**:")
        for s in li_info.get("Strengths", []):
            st.markdown(f"- 🌟 {s}")

        st.markdown("**Areas for Growth**:")
        for g in li_info.get("Gaps", []):
            st.markdown(f"- 📌 {g}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Portfolio Website & Contribution Analysis
    col_web_card, col_contrib_card = st.columns(2)

    with col_web_card:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🌐 Portfolio Website Design & UX")
        st.markdown(f"**Design Evaluation**: {web_info.get('Design_Quality', '')}")

        st.markdown("**Strengths**:")
        for s in web_info.get("Strengths", []):
            st.markdown(f"- 🎨 {s}")

        st.markdown("**UI/UX Improvements**:")
        for imp in web_info.get("Areas_For_Improvement", []):
            st.markdown(f"- 🛠️ {imp}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_contrib_card:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Open-Source Contribution Analysis")
        contrib_text = portfolio_data.get("Contribution_Analysis", "")
        st.write(contrib_text)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── Recommendations & Action Items ─────────────────────────────────────
    col_sug, col_rec = st.columns(2)

    with col_sug:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💡 Strategic Improvement Suggestions")
        for sug in portfolio_data.get("Improvement_Suggestions", []):
            st.markdown(f"- 🚀 {sug}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_rec:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🛠 Recommended Technologies & Tools")
        for rec in portfolio_data.get("Technology_Recommendations", []):
            st.markdown(f"- 🔧 {rec}")
        st.markdown('</div>', unsafe_allow_html=True)
