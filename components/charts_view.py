import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def render_ats_gauge_chart(score: int, theme: str = "dark"):
    """
    Renders an interactive Plotly Gauge meter for the ATS score with theme support.
    """
    is_dark = (theme == "dark")
    text_color = "#F8FAFC" if is_dark else "#0F172A"
    axis_tick_color = "#94A3B8" if is_dark else "#64748B"
    bg_step_red = "rgba(239, 68, 68, 0.2)" if is_dark else "#FEE2E2"
    bg_step_yellow = "rgba(245, 158, 11, 0.2)" if is_dark else "#FEF3C7"
    bg_step_blue = "rgba(59, 130, 246, 0.2)" if is_dark else "#E0F2FE"
    bg_step_green = "rgba(16, 185, 129, 0.25)" if is_dark else "#D1FAE5"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%", 'font': {'size': 38, 'color': text_color, 'family': 'Plus Jakarta Sans, sans-serif'}},
        title={'text': "Circular ATS Readiness Gauge", 'font': {'size': 18, 'color': text_color, 'family': 'Plus Jakarta Sans, sans-serif'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': axis_tick_color, 'dtick': 20},
            'bar': {'color': "#6366F1", 'thickness': 0.3},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1.5,
            'bordercolor': "rgba(148, 163, 184, 0.3)",
            'steps': [
                {'range': [0, 40], 'color': bg_step_red},
                {'range': [40, 60], 'color': bg_step_yellow},
                {'range': [60, 80], 'color': bg_step_blue},
                {'range': [80, 100], 'color': bg_step_green}
            ],
            'threshold': {
                'line': {'color': "#10B981", 'width': 4},
                'thickness': 0.8,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_ats_breakdown_bar_chart(breakdown: Dict[str, int], theme: str = "dark"):
    """
    Renders a horizontal bar chart of the 8 weighted ATS category scores.
    """
    is_dark = (theme == "dark")
    text_color = "#F8FAFC" if is_dark else "#0F172A"

    categories = [
        'Skills', 'Experience', 'Projects', 'Keywords',
        'Education', 'Formatting', 'Certifications', 'Readability'
    ]
    scores = [
        breakdown.get("Skills_Score", 0),
        breakdown.get("Experience_Score", 0),
        breakdown.get("Projects_Score", 0),
        breakdown.get("Keyword_Match_Score", 0),
        breakdown.get("Education_Score", 0),
        breakdown.get("Formatting_Score", 0),
        breakdown.get("Certifications_Score", 0),
        breakdown.get("Readability_Score", 0)
    ]

    colors_list = [
        '#10B981' if s >= 80 else '#3B82F6' if s >= 60 else '#F59E0B' if s >= 40 else '#EF4444'
        for s in scores
    ]

    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker=dict(color=colors_list, line=dict(width=0)),
        text=[f"{s}%" for s in scores],
        textposition='auto',
        textfont=dict(color="#FFFFFF", family="Plus Jakarta Sans, sans-serif", size=11)
    ))

    fig.update_layout(
        title_text="Category Score Comparison Matrix",
        title_font=dict(size=18, color=text_color, family="Plus Jakarta Sans, sans-serif"),
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 100], showgrid=True, gridcolor="rgba(148, 163, 184, 0.15)", tickfont=dict(color=text_color)),
        yaxis=dict(autorange="reversed", tickfont=dict(color=text_color, size=11, family="Plus Jakarta Sans, sans-serif")),
        font=dict(family="Plus Jakarta Sans, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_skills_pie_chart(skills_count: int, missing_count: int, strengths_count: int, theme: str = "dark"):
    """
    Renders a sleek donut chart illustrating skill breakdown.
    """
    is_dark = (theme == "dark")
    text_color = "#F8FAFC" if is_dark else "#0F172A"

    labels = ['Skills Found', 'Missing Skills', 'Key Strengths']
    values = [max(1, skills_count), max(0, missing_count), max(0, strengths_count)]
    colors = ['#10B981', '#EF4444', '#3B82F6']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.6,
        marker_colors=colors,
        textinfo='label+percent',
        insidetextorientation='radial',
        textfont=dict(size=12, color="#FFFFFF" if is_dark else "#0F172A", family="Plus Jakarta Sans, sans-serif")
    )])
    
    fig.update_layout(
        title_text="Resume Skill Matrix Breakdown",
        title_font=dict(size=18, color=text_color, family="Plus Jakarta Sans, sans-serif"),
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            font=dict(color=text_color, family="Plus Jakarta Sans, sans-serif"),
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        font=dict(family="Plus Jakarta Sans, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_analytics_section(data: Dict[str, Any], theme: str = "dark"):
    """
    Renders combined analytics charts section inside glass containers.
    """
    st.subheader("📈 ATS Analytics & Visual Metrics")
    col1, col2 = st.columns(2)

    ats_score = data.get("ATS_Score", 0)
    breakdown = data.get("ATS_Breakdown", {})

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_ats_gauge_chart(ats_score, theme=theme)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_ats_breakdown_bar_chart(breakdown, theme=theme)
        st.markdown('</div>', unsafe_allow_html=True)
