# main_progressive.py
"""Application principale avec refactorisation progressive"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from utils.data_utils import load_data, safe_numeric
from components.layout import inject_custom_css, display_hero_header, display_draft_countdown, display_footer

def main():
    """Application principale"""
    # Configuration
    st.set_page_config(
        page_title="🏀 NBA Draft 2025 AI",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Chargement des données
    df = load_data()
    if df is None or df.empty:
        st.error("❌ Unable to load data")
        st.stop()
    
    # Styles et header
    inject_custom_css()
    display_hero_header()
    display_draft_countdown()
    
    # Navigation avec modules refactorisés
    tabs = st.tabs([
        "🏠 Dashboard",      # ✅ Module refactorisé
        "📊 Compare Players", 
        "🔍 Enhanced Search", 
        "🎯 Live Big Board",  
        "🎯 Team Fit",       
        "💎 Steals & Busts", 
        "📈 Projections",   
        "📊 Historical",      
        " ML Analytics"
    ])
    
    # MODULES REFACTORISÉS ✅
    with tabs[0]:  # Dashboard
        try:
            from pages.dashboard import show
            show(df)
            st.success("✅ Dashboard: Module refactorisé avec composants")
        except Exception as e:
            st.error(f"Dashboard error: {e}")
            fallback_dashboard(df)
    
    with tabs[1]:  # Compare Players
        try:
            from pages.comparisons import show
            show(df)
            st.success("✅ Comparisons: Module refactorisé avec radar charts")
        except Exception as e:
            st.error(f"Comparisons error: {e}")
            fallback_comparison(df)
    
    with tabs[2]:  # Enhanced Search
        try:
            from pages.search import show
            show(df)
            st.success("✅ Search: Module refactorisé avec filtres avancés")
        except Exception as e:
            st.error(f"Search error: {e}")
            fallback_search(df)
    
    with tabs[3]:  # Live Big Board
        try:
            from pages.live_board import show
            show(df)
            st.success("✅ Live Big Board: Module refactorisé avec intel")
        except Exception as e:
            st.error(f"Live Big Board error: {e}")
            fallback_big_board(df)
    
    with tabs[4]:  # Team Fit Analysis
        try:
            from pages.team_fit import show
            show(df)
            st.success("✅ Team Fit: Module refactorisé avec matrices")
        except Exception as e:
            st.error(f"Team Fit error: {e}")
            fallback_team_fit(df)
    
    # PHASES SUIVANTES: Modules refactorisés
    with tabs[5]:  # Steals & Busts
        try:
            from pages.steals_busts import show
            show(df)
            st.success("✅ Steals & Busts: Module refactorisé avec analyse prédictive")
        except Exception as e:
            st.error(f"Steals & Busts error: {e}")
            fallback_steals_busts(df)
    
    with tabs[6]:  # Projections
        try:
            from pages.projections import show
            show(df)
            st.success("✅ 5-Year Projections: Module refactorisé avec courbes de développement")
        except Exception as e:
            st.error(f"Projections error: {e}")
            fallback_projections(df)
    
    with tabs[7]:  # Historical Intelligence
        try:
            from pages.historical import show
            show(df)
            st.success("✅ Historical Intelligence: Module refactorisé avec 6 sous-modules")
        except Exception as e:
            st.error(f"Historical Intelligence error: {e}")
            fallback_historical(df)
            
    with tabs[8]:  # ML Analytics
        try:
            from pages.ml_analytics import show
            show(df)
            st.success("✅ ML Analytics: Module refactorisé avec 6 sous-modules")
        except Exception as e:
            st.error(f"ML Analytics error: {e}")
            fallback_ml_analytics(df)
    
    # Footer
    display_footer()

# FALLBACKS pour les modules non refactorisés
def fallback_dashboard(df: pd.DataFrame):
    """Fallback simple pour le dashboard"""
    st.warning("Mode fallback activé")
    st.dataframe(df.head(10))

def fallback_comparison(df: pd.DataFrame):
    """Fallback simple pour les comparaisons"""
    st.warning("Mode fallback activé")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Player 1", df['name'].head(10))
    with col2:
        st.selectbox("Player 2", df['name'].head(10))

def fallback_search(df: pd.DataFrame):
    """Fallback simple pour la recherche"""
    st.warning("Mode fallback activé")
    search_term = st.text_input("Search players")
    if search_term:
        filtered = df[df['name'].str.contains(search_term, case=False, na=False)]
        st.dataframe(filtered)

def fallback_big_board(df: pd.DataFrame):
    """Fallback simple pour le big board"""
    st.warning("Mode fallback activé")
    st.dataframe(df[['name', 'position', 'college', 'ppg', 'scout_grade']].head(30))

def fallback_historical(df: pd.DataFrame):
    """Fallback simple pour historical intelligence"""
    st.warning("Mode fallback activé")

def fallback_ml_analytics(df: pd.DataFrame):
    """Fallback simple pour ml analytics"""
    st.warning("Mode fallback activé")
    
    # Tabs simplifiés
    tab1, tab2 = st.columns(2)
    
    with tab1:
        st.markdown("### 🎯 Quick Comparisons")
        player = st.selectbox("Select Player", df['name'].head(5), key="hist_fallback_select")
        if player:
            st.info(f"{player} comparison analysis coming soon")
    
    with tab2:
        st.markdown("### 📈 Success Patterns")
        st.info("Historical success pattern analysis in development")

if __name__ == "__main__":
    main()
