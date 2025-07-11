# components/layout.py
"""Composants de mise en page et style"""

import streamlit as st
from datetime import datetime, date

def inject_custom_css():
    """Inject custom CSS for styling"""
    st.markdown("""<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main { font-family: 'Inter', sans-serif; }
        
        .hero-header {
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
            color: white;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .prospect-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #FF6B35;
        }
        
        .countdown-container {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
        }
        
        .leader-card {
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #FFD700;
            color: #333;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .stat-box {
            background: #f8f9fa;
            padding: 0.8rem;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #666;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-header {
                padding: 2rem 1rem;
            }
        }
        
        /* Custom button styles */
        .stButton > button {
            background: linear-gradient(135deg, #FF6B35, #F7931E);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #E55A2B, #E8851A);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 53, 0.4);
        }
        
        /* Custom metric styling */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border: 1px solid #e9ecef;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #FF6B35, #F7931E);
        }
    </style>""", unsafe_allow_html=True)

def display_hero_header():
    """Display hero header section"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🏀 NBA DRAFT 2025</h1>
        <p style="font-size: 1.3rem; margin-bottom: 2rem;">AI-Powered Prospect Analysis & Draft Simulator</p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">60</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Prospects</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">84.7%</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">ML Accuracy</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">30</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">NBA Teams</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_draft_countdown():
    """Display countdown to draft day"""
    draft_date = date(2025, 6, 26)
    today = date.today()
    days_left = (draft_date - today).days
    
    if days_left > 0:
        st.markdown(f"""
        <div class="countdown-container">
            <div style="font-size: 4rem; font-weight: 700; color: #333; line-height: 1;">{days_left}</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-top: 0.5rem;">
                Days Until NBA Draft 2025
            </div>
            <div style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.5rem;">
                June 26, 2025 • Brooklyn, NY
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="countdown-container">
            <div style="font-size: 4rem; font-weight: 700; color: #333; line-height: 1;">🏀</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-top: 0.5rem;">
                NBA Draft 2025 Complete!
            </div>
            <div style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.5rem;">
                Results and Analysis Available
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_footer():
    """Display application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        🏀 <strong>NBA Draft 2025 AI Dashboard</strong> | Historical Intelligence Edition<br>
        <small>Featuring 60 prospects with ML projections, 15 years of historical validation, and comprehensive team analysis</small>
    </div>
    """, unsafe_allow_html=True)

def display_section_header(title: str, subtitle: str = "", icon: str = ""):
    """Display styled section header"""
    icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''
    subtitle_html = f'<p style="font-size: 1.1rem; color: #666; margin: 0.5rem 0 2rem 0;">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div style="margin: 2rem 0;">
        <h2 style="color: #333; font-size: 2rem; font-weight: 600; margin-bottom: 0.5rem;">
            {icon_html}{title}
        </h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def display_status_badge(status: str, type: str = "info"):
    """Display status badge"""
    colors = {
        "success": {"bg": "#10B981", "text": "white"},
        "warning": {"bg": "#F59E0B", "text": "white"},
        "error": {"bg": "#EF4444", "text": "white"},
        "info": {"bg": "#3B82F6", "text": "white"},
        "neutral": {"bg": "#6B7280", "text": "white"}
    }
    
    color = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div style="display: inline-block; 
                background: {color['bg']}; 
                color: {color['text']}; 
                padding: 0.3rem 1rem; 
                border-radius: 20px; 
                font-size: 0.9rem; 
                font-weight: 600;
                margin: 0.5rem 0;">
        {status}
    </div>
    """, unsafe_allow_html=True)

def create_two_column_layout():
    """Create responsive two-column layout"""
    return st.columns([1, 1], gap="large")

def create_three_column_layout():
    """Create responsive three-column layout"""
    return st.columns([1, 1, 1], gap="medium")

def create_four_column_layout():
    """Create responsive four-column layout"""
    return st.columns([1, 1, 1, 1], gap="small")

def display_loading_spinner(message: str = "Loading..."):
    """Display loading spinner with message"""
    with st.spinner(message):
        st.empty()

def display_success_message(message: str):
    """Display success message with custom styling"""
    st.success(f"✅ {message}")

def display_warning_message(message: str):
    """Display warning message with custom styling"""
    st.warning(f"⚠️ {message}")

def display_error_message(message: str):
    """Display error message with custom styling"""
    st.error(f"❌ {message}")

def display_info_message(message: str):
    """Display info message with custom styling"""
    st.info(f"ℹ️ {message}")

def create_sidebar_layout():
    """Create and configure sidebar layout"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="color: white; margin-bottom: 1rem;">🏀 NBA Draft 2025</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                AI-Powered Basketball Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return st.sidebar

def display_progress_bar(progress: float, label: str = ""):
    """Display custom progress bar"""
    st.progress(progress, text=label)

def create_expandable_section(title: str, expanded: bool = False):
    """Create expandable section with custom styling"""
    return st.expander(f"🔍 {title}", expanded=expanded)