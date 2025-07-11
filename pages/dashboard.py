# pages/dashboard.py
"""Page Dashboard avec composants modulaires"""

import streamlit as st
import pandas as pd
from components.charts import create_position_distribution_chart, create_potential_bar_chart
from components.cards import display_leader_card
from components.filters import create_advanced_filters, apply_filters
from components.tables import display_prospects_table  # ✅ CORRIGÉ
from utils.helpers import calculate_draft_grade_average, safe_numeric, safe_string
from config.settings import THRESHOLDS

def show(df: pd.DataFrame):
    """Display dashboard page with modular components"""
    st.markdown("## 📈 Dashboard Overview")
    
    # Leaders section
    create_leaders_section(df)
    
    # Key metrics
    display_key_metrics(df)
    
    # Interactive filters
    filtered_df = create_interactive_filters_section(df)
    
    # Visualizations
    display_dashboard_charts(filtered_df)
    
    # Prospects table
    display_prospects_table(filtered_df)

def create_leaders_section(df: pd.DataFrame):
    """Display category leaders - REFACTORISÉ avec composants"""
    st.markdown("### 🏆 Category Leaders (Projected Potential)")
    
    try:
        # Calculate projections - MÊME LOGIQUE QUE L'ORIGINAL
        df = df.copy()  # Éviter les warnings pandas
        df['projected_scorer'] = df['ppg'] * (1 + df['final_gen_probability'] * 0.3)
        df['projected_scorer'] = df['projected_scorer'].clip(upper=32)
        
        df['projected_shooter'] = df['three_pt_pct'] * (1 + df['final_gen_probability'] * 0.15)
        df['projected_shooter'] = df['projected_shooter'].clip(upper=0.43)
        
        df['projected_rebounder'] = df['rpg'] * (1 + df['final_gen_probability'] * 0.3)
        df['projected_rebounder'] = df['projected_rebounder'].clip(upper=15)
        
        df['projected_playmaker'] = df['apg'] * (1 + df['final_gen_probability'] * 0.35)
        df['projected_playmaker'] = df['projected_playmaker'].clip(upper=12)
        
        # Defensive impact (gestion des colonnes manquantes)
        spg = df.get('spg', pd.Series([1.0] * len(df)))
        bpg = df.get('bpg', pd.Series([0.5] * len(df)))
        df['projected_defender'] = (spg + bpg) * (1 + df['final_gen_probability'] * 0.25)
        df['projected_defender'] = df['projected_defender'].clip(upper=4)
        
        df['immediate_impact'] = (
            df['ppg'] * 0.25 +
            df['rpg'] * 0.15 +
            df['apg'] * 0.20 +
            (df['three_pt_pct'] * 100) * 0.15 +
            (22 - df['age']) * 2 +
            df['final_gen_probability'] * 30
        )
        
        # Find leaders
        best_scorer = df.loc[df['projected_scorer'].idxmax()]
        best_shooter = df.loc[df['projected_shooter'].idxmax()]
        best_rebounder = df.loc[df['projected_rebounder'].idxmax()]
        best_playmaker = df.loc[df['projected_playmaker'].idxmax()]
        best_defender = df.loc[df['projected_defender'].idxmax()]
        most_immediate_impact = df.loc[df['immediate_impact'].idxmax()]
        
        # Display using modular cards - NOUVEAU: UTILISE LES COMPOSANTS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            display_leader_card(
                "🎯 Best Scoring Potential",
                safe_string(best_scorer['name']),
                f"{safe_numeric(best_scorer['projected_scorer']):.1f}",
                f"Projected peak PPG (Current: {safe_numeric(best_scorer['ppg']):.1f})",
                "#FF6B35"
            )
            
            display_leader_card(
                "🏀 Best Rebounding Potential", 
                safe_string(best_rebounder['name']),
                f"{safe_numeric(best_rebounder['projected_rebounder']):.1f}",
                f"Projected peak RPG (Current: {safe_numeric(best_rebounder['rpg']):.1f})",
                "#4361EE"
            )
        
        with col2:
            display_leader_card(
                "🎯 Best Shooting Potential",
                safe_string(best_shooter['name']),
                f"{safe_numeric(best_shooter['projected_shooter']):.1%}",
                f"Projected peak 3P% (Current: {safe_numeric(best_shooter['three_pt_pct']):.1%})",
                "#10B981"
            )
            
            display_leader_card(
                "🛡️ Best Defensive Potential",
                safe_string(best_defender['name']),
                f"{safe_numeric(best_defender['projected_defender']):.1f}",
                f"Projected STL+BLK peak",
                "#8B5CF6"
            )
        
        with col3:
            display_leader_card(
                "🎯 Best Playmaking Potential",
                safe_string(best_playmaker['name']),
                f"{safe_numeric(best_playmaker['projected_playmaker']):.1f}",
                f"Projected peak APG (Current: {safe_numeric(best_playmaker['apg']):.1f})",
                "#F59E0B"
            )
            
            display_leader_card(
                "⚡ Most Immediate Impact",
                safe_string(most_immediate_impact['name']),
                "Ready",
                f"Year 1 contributor - {safe_numeric(most_immediate_impact['ppg']):.1f} PPG, Age {safe_numeric(most_immediate_impact['age']):.0f}",
                "#EF4444"
            )
        
    except Exception as e:
        st.error(f"Error in leaders section: {e}")

def display_key_metrics(df: pd.DataFrame):
    """Display key dashboard metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Prospects", len(df))
    
    with col2:
        elite_count = len(df[df['final_gen_probability'] > 0.7])  # Utilise valeur fixe au lieu de THRESHOLDS
        st.metric("Elite Prospects", elite_count)
    
    with col3:
        gen_count = len(df[df['final_gen_probability'] > 0.9])
        st.metric("Generational Talents", gen_count)
    
    with col4:
        draft_grade = calculate_draft_grade_average(df)
        from config.settings import GRADE_COLORS
        color_emoji = GRADE_COLORS.get(draft_grade, '🟡')
        st.metric("Draft Class Grade", f"{color_emoji} {draft_grade}", "Scout consensus average")

def create_interactive_filters_section(df: pd.DataFrame) -> pd.DataFrame:
    """Create interactive filters section using modular components"""
    st.markdown("### 🔍 Interactive Filters")
    
    # Use modular filter components - NOUVEAU: UTILISE LES COMPOSANTS
    filters = create_advanced_filters(df, "dashboard")
    
    # Apply filters using modular function - NOUVEAU: UTILISE LES COMPOSANTS
    filtered_df = apply_filters(df, filters)
    
    st.success(f"📊 {len(filtered_df)} prospects match your filters")
    return filtered_df

def display_dashboard_charts(df: pd.DataFrame):
    """Display dashboard visualizations using modular charts"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Use modular chart component - NOUVEAU: UTILISE LES COMPOSANTS
        fig_pie = create_position_distribution_chart(df)
        if fig_pie:
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Use modular chart component - NOUVEAU: UTILISE LES COMPOSANTS  
        fig_bar = create_potential_bar_chart(df, 10)
        if fig_bar:
            st.plotly_chart(fig_bar, use_container_width=True)