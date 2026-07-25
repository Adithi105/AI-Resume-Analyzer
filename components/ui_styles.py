import streamlit as st

def apply_custom_styles():
    """
    Injects custom production-ready CSS into the Streamlit application for elevated UI aesthetics.
    Includes glassmorphism cards, glowing badges, refined metrics, and responsive containers.
    """
    css = """
    <style>
    /* Global Container Padding & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* Custom Badges */
    .skill-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px 4px 6px 0px;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    .skill-badge-green {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }

    .skill-badge-red {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }

    .skill-badge-blue {
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
    }

    /* Card Containers */
    .custom-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .dark-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }

    /* Green Strength Box */
    .strength-box {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #15803D;
        font-weight: 500;
    }

    /* AI Suggestion Box */
    .suggestion-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
        color: #0369A1;
        font-weight: 500;
    }

    /* Custom Progress Bar Color */
    .stProgress > div > div > div > div {
        border-radius: 10px;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_badge(text: str, badge_type: str = "green") -> str:
    """
    Generates HTML string for a styled badge pill.
    """
    css_class = f"skill-badge skill-badge-{badge_type}"
    return f'<span class="{css_class}">{text}</span>'
