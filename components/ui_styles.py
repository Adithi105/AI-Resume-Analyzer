import streamlit as st

def apply_custom_styles(theme: str = "dark"):
    """
    Injects custom production-ready CSS into the Streamlit application for elevated UI aesthetics.
    Includes dark/light mode CSS variables, glassmorphism cards, glowing badges, refined metrics,
    gradient buttons, smooth transitions, and responsive containers.
    """
    if theme == "light":
        bg_primary = "#F8FAFC"
        bg_secondary = "#FFFFFF"
        bg_card = "rgba(255, 255, 255, 0.9)"
        border_color = "rgba(226, 232, 240, 0.8)"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        text_muted = "#64748B"
        accent_gradient = "linear-gradient(135deg, #2563EB 0%, #4F46E5 100%)"
        accent_hover = "linear-gradient(135deg, #1D4ED8 0%, #4338CA 100%)"
        card_shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)"
        glass_border = "1px solid rgba(203, 213, 225, 0.6)"
        badge_green_bg = "#ECFDF5"
        badge_green_text = "#047857"
        badge_green_border = "#A7F3D0"
        badge_red_bg = "#FEF2F2"
        badge_red_text = "#B91C1C"
        badge_red_border = "#FECACA"
        badge_blue_bg = "#EFF6FF"
        badge_blue_text = "#1D4ED8"
        badge_blue_border = "#BFDBFE"
        tab_bg = "#F1F5F9"
        tab_active_bg = "#FFFFFF"
    else:
        # Dark Theme (Default Enterprise Dark Mode)
        bg_primary = "#0F172A"
        bg_secondary = "#1E293B"
        bg_card = "rgba(30, 41, 59, 0.75)"
        border_color = "rgba(51, 65, 85, 0.7)"
        text_primary = "#F8FAFC"
        text_secondary = "#CBD5E1"
        text_muted = "#94A3B8"
        accent_gradient = "linear-gradient(135deg, #3B82F6 0%, #6366F1 100%)"
        accent_hover = "linear-gradient(135deg, #2563EB 0%, #4F46E5 100%)"
        card_shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 15px rgba(59, 130, 246, 0.1)"
        glass_border = "1px solid rgba(255, 255, 255, 0.08)"
        badge_green_bg = "rgba(16, 185, 129, 0.15)"
        badge_green_text = "#34D399"
        badge_green_border = "rgba(52, 211, 153, 0.3)"
        badge_red_bg = "rgba(239, 68, 68, 0.15)"
        badge_red_text = "#F87171"
        badge_red_border = "rgba(248, 113, 113, 0.3)"
        badge_blue_bg = "rgba(59, 130, 246, 0.15)"
        badge_blue_text = "#60A5FA"
        badge_blue_border = "rgba(96, 165, 250, 0.3)"
        tab_bg = "rgba(15, 23, 42, 0.6)"
        tab_active_bg = "#1E293B"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* CSS Custom Variables */
    :root {{
        --bg-primary: {bg_primary};
        --bg-secondary: {bg_secondary};
        --bg-card: {bg_card};
        --border-color: {border_color};
        --text-primary: {text_primary};
        --text-secondary: {text_secondary};
        --text-muted: {text_muted};
        --accent-gradient: {accent_gradient};
        --accent-hover: {accent_hover};
        --card-shadow: {card_shadow};
        --glass-border: {glass_border};
    }}

    /* Global Document Reset */
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: {text_primary};
        background-color: {bg_primary};
    }}

    /* Main Container Padding */
    .main .block-container {{
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }}

    /* Top Application Banner Header */
    .app-header-container {{
        background: {bg_card};
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: {glass_border};
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: {card_shadow};
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, {bg_card} 0%, {bg_secondary} 100%);
    }}

    .app-header-title {{
        font-size: 1.85rem;
        font-weight: 800;
        background: {accent_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin: 0;
    }}

    .app-header-subtitle {{
        font-size: 0.95rem;
        color: {text_muted};
        margin-top: 4px;
        margin-bottom: 0;
    }}

    .enterprise-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #818CF8;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {{
        background: {bg_card};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: {glass_border};
        border-radius: 16px;
        padding: 18px 22px;
        box-shadow: {card_shadow};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.25);
    }}

    div[data-testid="stMetricLabel"] {{
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        color: {text_muted} !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    div[data-testid="stMetricValue"] {{
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: {text_primary} !important;
        margin-top: 4px;
    }}

    /* Gradient Primary Buttons */
    .stButton > button {{
        background: {accent_gradient} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stButton > button:hover {{
        background: {accent_hover} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(59, 130, 246, 0.45) !important;
    }}

    .stButton > button:active {{
        transform: translateY(0px) !important;
    }}

    /* Streamlit Tabs Styling */
    div[data-baseweb="tab-list"] {{
        background-color: {tab_bg};
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
        border: {glass_border};
    }}

    div[data-baseweb="tab"] {{
        height: 44px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.92rem;
        color: {text_muted};
        border: none !important;
        padding: 0 20px;
        transition: all 0.2s ease;
    }}

    div[aria-selected="true"] {{
        background-color: {tab_active_bg} !important;
        color: {text_primary} !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }}

    /* Custom Badges */
    .skill-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        margin: 4px 6px 6px 0px;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        transition: all 0.25s ease;
    }}

    .skill-badge:hover {{
        transform: translateY(-2px) scale(1.03);
    }}

    .skill-badge-green {{
        background-color: {badge_green_bg};
        color: {badge_green_text};
        border: 1px solid {badge_green_border};
    }}

    .skill-badge-red {{
        background-color: {badge_red_bg};
        color: {badge_red_text};
        border: 1px solid {badge_red_border};
    }}

    .skill-badge-blue {{
        background-color: {badge_blue_bg};
        color: {badge_blue_text};
        border: 1px solid {badge_blue_border};
    }}

    /* Card Containers */
    .glass-card {{
        background: {bg_card};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: {glass_border};
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: {card_shadow};
        transition: all 0.3s ease;
    }}

    .glass-card:hover {{
        border-color: rgba(99, 102, 241, 0.3);
    }}

    /* Accent Boxed Items */
    .strength-box {{
        background-color: {badge_green_bg};
        border-left: 4px solid #10B981;
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 12px;
        color: {text_primary};
        font-weight: 500;
        font-size: 0.92rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08);
    }}

    .suggestion-box {{
        background-color: {badge_blue_bg};
        border-left: 4px solid #3B82F6;
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 12px;
        color: {text_primary};
        font-weight: 500;
        font-size: 0.92rem;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
    }}

    .hero-card {{
        background: linear-gradient(135deg, {bg_card} 0%, {bg_secondary} 100%);
        border: {glass_border};
        border-radius: 18px;
        padding: 28px;
        text-align: center;
        box-shadow: {card_shadow};
        transition: all 0.3s ease;
    }}

    .hero-card:hover {{
        transform: translateY(-4px);
    }}

    /* Custom Animations */
    @keyframes pulseGlow {{
        0% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }}
        70% {{ box-shadow: 0 0 0 12px rgba(99, 102, 241, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }}
    }}

    .pulse-animation {{
        animation: pulseGlow 2s infinite;
    }}

    /* Custom Progress Bar Styling */
    .stProgress > div > div > div > div {{
        background: {accent_gradient};
        border-radius: 10px;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {bg_secondary};
        border-right: {glass_border};
    }}

    /* Responsive Media Queries */
    @media (max-width: 768px) {{
        .app-header-container {{
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
        }}
        div[data-testid="stMetricValue"] {{
            font-size: 1.3rem !important;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_badge(text: str, badge_type: str = "green", icon: str = "●") -> str:
    """
    Generates HTML string for a styled badge pill with an icon dot.
    """
    css_class = f"skill-badge skill-badge-{badge_type}"
    return f'<span class="{css_class}"><span>{icon}</span> {text}</span>'
