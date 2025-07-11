# config/settings.py
"""Configuration et constantes de l'application NBA Draft"""

import streamlit as st
from datetime import date

# Configuration Streamlit
def configure_streamlit():
    """Configure les paramètres Streamlit"""
    st.set_page_config(
        page_title="🏀 NBA Draft 2025 AI",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# Constantes de l'application
APP_CONFIG = {
    'title': "🏀 NBA Draft 2025 AI",
    'subtitle': "AI-Powered Prospect Analysis & Draft Simulator",
    'version': "2.0",
    'author': "NBA Draft Intelligence"
}

# Métriques d'affichage
DISPLAY_METRICS = {
    'prospects_count': 60,
    'ml_accuracy': 84.7,
    'nba_teams_count': 30
}

# Configuration des couleurs
COLORS = {
    'primary': '#FF6B35',
    'secondary': '#F7931E', 
    'accent': '#FFD23F',
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
    'gray': '#6B7280'
}

# Configuration des grades
GRADE_MAPPING = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

REVERSE_GRADE_MAPPING = {v: k for k, v in GRADE_MAPPING.items()}

GRADE_COLORS = {
    'A+': '🟢', 'A': '🟢', 'A-': '🟢',
    'B+': '🟡', 'B': '🟡', 'B-': '🟡', 
    'C+': '🟠', 'C': '🟠', 'C-': '🟠',
    'D+': '🔴', 'D': '🔴', 'D-': '🔴',
    'F': '⚫'
}

# Configuration des colonnes de données
DATA_COLUMNS = {
    'numeric': ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'age', 'final_rank', 
               'final_gen_probability', 'fg_pct', 'three_pt_pct', 'ft_pct', 
               'ts_pct', 'height', 'weight', 'usage_rate', 'ortg', 'drtg'],
    'string': ['name', 'position', 'college', 'scout_grade', 'archetype'],
    'display': ['final_rank', 'name', 'position', 'college', 'ppg', 'rpg', 'apg', 
               'three_pt_pct', 'scout_grade', 'final_gen_probability']
}

# Configuration des onglets
MAIN_TABS = [
    "🏠 Dashboard",
    "📊 Compare Players", 
    "🔍 Enhanced Search",
    "🎯 Live Big Board",
    "💎 Steals & Busts",
    "📈 5-Year Projections", 
    "📊 Historical Intelligence",
    "🎯 Team Fit Analysis"
]

# Dates importantes
DRAFT_DATE = date(2025, 6, 26)
DRAFT_LOCATION = "Brooklyn, NY"

# Configuration des tiers
DRAFT_TIERS = {
    'elite': {'min': 1, 'max': 5, 'name': '🏆 Elite', 'color': '#FFD700'},
    'lottery': {'min': 6, 'max': 14, 'name': '🎰 Lottery', 'color': '#FF6B35'},
    'first': {'min': 15, 'max': 30, 'name': '🏀 First', 'color': '#4361EE'},
    'second': {'min': 31, 'max': 60, 'name': '⚡ Second', 'color': '#6B7280'}
}

# Configuration des positions
POSITIONS = {
    'all': ['PG', 'SG', 'SF', 'PF', 'C'],
    'guards': ['PG', 'SG'],
    'wings': ['SG', 'SF'],
    'forwards': ['SF', 'PF'],
    'bigs': ['PF', 'C']
}

# Configuration des fichiers de données
DATA_FILES = [
    'complete_nba_draft_rankings.csv',
    'final_nba_draft_rankings.csv', 
    'ml_nba_draft_predictions.csv'
]

# Configuration des seuils
THRESHOLDS = {
    'elite_prospect': 0.7,
    'good_prospect': 0.5,
    'elite_scorer': 20.0,
    'good_scorer': 15.0,
    'elite_shooter': 0.38,
    'good_shooter': 0.33,
    'elite_playmaker': 6.0,
    'good_playmaker': 4.0,
    'young_prospect': 19.0
}