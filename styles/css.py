# styles/css.py
"""Styles CSS pour l'application NBA Draft"""

import streamlit as st
from config.settings import COLORS

def inject_custom_css():
    """Inject custom CSS for styling"""
    st.markdown(f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main {{ 
            font-family: 'Inter', sans-serif; 
        }}
        
        .hero-header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 50%, {COLORS['accent']} 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
            color: white;
        }}
        
        .hero-title {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .prospect-card {{
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-left: 5px solid {COLORS['primary']};
        }}
        
        .countdown-container {{
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
        }}
        
        .leader-card {{
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #FFD700;
            color: #333;
        }}
        
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        .stat-box {{
            background: #f8f9fa;
            padding: 0.8rem;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            color: #666;
        }}
        
        .tier-elite {{
            background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']});
            color: white;
            border-radius: 8px;
            padding: 0.3rem 0.8rem;
            font-weight: bold;
        }}
        
        .tier-lottery {{
            background: linear-gradient(135deg, {COLORS['warning']}, #e97c07);
            color: white;
            border-radius: 8px;
            padding: 0.3rem 0.8rem;
            font-weight: bold;
        }}
        
        .tier-first {{
            background: linear-gradient(135deg, {COLORS['info']}, #1d4ed8);
            color: white;
            border-radius: 8px;
            padding: 0.3rem 0.8rem;
            font-weight: bold;
        }}
        
        .comparison-card {{
            background: white;
            border: 2px solid {COLORS['primary']};
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        .strength-card {{
            background: linear-gradient(135deg, {COLORS['success']}, #059669);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        }}
        
        .weakness-card {{
            background: linear-gradient(135deg, {COLORS['warning']}, #d97706);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        }}
        
        .opportunity-card {{
            background: linear-gradient(135deg, {COLORS['info']}, #2563eb);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }}
        
        .threat-card {{
            background: linear-gradient(135deg, {COLORS['error']}, #dc2626);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
        }}
        
        .search-results-card {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.2rem;
            margin: 0.8rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }}
        
        .search-results-card:hover {{
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .grade-a {{
            background: {COLORS['success']};
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: bold;
        }}
        
        .grade-b {{
            background: {COLORS['warning']};
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: bold;
        }}
        
        .grade-c {{
            background: {COLORS['error']};
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: bold;
        }}
        
        .fit-excellent {{
            color: {COLORS['success']};
            font-weight: bold;
        }}
        
        .fit-good {{
            color: {COLORS['warning']};
            font-weight: bold;
        }}
        
        .fit-poor {{
            color: {COLORS['error']};
            font-weight: bold;
        }}
        
        .projection-high {{
            background: linear-gradient(135deg, {COLORS['success']}, #059669);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .projection-medium {{
            background: linear-gradient(135deg, {COLORS['warning']}, #d97706);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .projection-low {{
            background: linear-gradient(135deg, {COLORS['error']}, #dc2626);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }}
        
    </style>""", unsafe_allow_html=True)

def get_grade_style_class(grade: str) -> str:
    """Get CSS class for grade styling"""
    grade_upper = grade.upper()
    if grade_upper.startswith('A'):
        return 'grade-a'
    elif grade_upper.startswith('B'):
        return 'grade-b'
    else:
        return 'grade-c'

def get_tier_style_class(rank: int) -> str:
    """Get CSS class for tier styling"""
    if rank <= 5:
        return 'tier-elite'
    elif rank <= 14:
        return 'tier-lottery'
    else:
        return 'tier-first'

def get_fit_style_class(fit_score: float) -> str:
    """Get CSS class for team fit styling"""
    if fit_score >= 70:
        return 'fit-excellent'
    elif fit_score >= 50:
        return 'fit-good'
    else:
        return 'fit-poor'

def get_projection_style_class(projection: float) -> str:
    """Get CSS class for projection styling"""
    if projection >= 0.7:
        return 'projection-high'
    elif projection >= 0.5:
        return 'projection-medium'
    else:
        return 'projection-low'
