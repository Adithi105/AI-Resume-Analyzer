import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

def render_ats_gauge_chart(score: int):
    """
    Renders an interactive Plotly Gauge meter for the ATS score.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ATS Score Index", 'font': {'size': 20, 'color': "#1E293B"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#2563EB"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#CBD5E1",
            'steps': [
                {'range': [0, 40], 'color': '#FEE2E2'},
                {'range': [40, 60], 'color': '#FEF3C7'},
                {'range': [60, 80], 'color': '#E0F2FE'},
                {'range': [80, 100], 'color': '#D1FAE5'}
            ],
            'threshold': {
                'line': {'color': "#16A34A", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(
        height=260,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_skills_pie_chart(skills_count: int, missing_count: int, strengths_count: int):
    """
    Renders a donut chart illustrating skill breakdown.
    """
    labels = ['Skills Found', 'Missing Skills', 'Key Strengths']
    values = [max(1, skills_count), max(0, missing_count), max(0, strengths_count)]
    colors = ['#10B981', '#EF4444', '#3B82F6']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.5,
        marker_colors=colors,
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    
    fig.update_layout(
        title_text="Resume Profile Distribution",
        height=260,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_analytics_section(data: Dict[str, Any]):
    """
    Renders combined analytics charts section.
    """
    st.subheader("📈 Analytics & Visual Metrics")
    col1, col2 = st.columns(2)

    ats_score = data.get("ATS_Score", 0)
    skills = data.get("Skills", [])
    missing = data.get("Missing_Skills", [])
    strengths = data.get("Strengths", [])

    with col1:
        render_ats_gauge_chart(ats_score)

    with col2:
        render_skills_pie_chart(len(skills), len(missing), len(strengths))
