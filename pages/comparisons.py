# pages/comparisons.py
"""Page de comparaison des joueurs avec composants modulaires"""

import streamlit as st
import pandas as pd
from components.charts import create_comparison_radar
from components.cards import display_comparison_card
from components.filters import create_comparison_selectors
from components.tables import create_detailed_comparison_table  # ✅ CORRIGÉ
from utils.helpers import safe_numeric, safe_string

def show(df: pd.DataFrame):
    """Display player comparison page"""
    st.markdown("## 📊 Enhanced Player Comparison")
    
    if len(df) < 2:
        st.warning("Need at least 2 prospects for comparison")
        return
    
    # Player selection using modular component
    player1, player2 = create_comparison_selectors(df, "comparison_page")
    
    if player1 == player2:
        st.warning("Please select different players")
        return
    
    # Get player data
    p1_data = df[df['name'] == player1].iloc[0]
    p2_data = df[df['name'] == player2].iloc[0]
    
    # Display comparison cards
    display_player_comparison_cards(p1_data, p2_data, player1, player2)
    
    # Create radar chart
    create_comparison_radar_section(p1_data, p2_data, player1, player2)
    
    # Detailed stats comparison
    create_detailed_comparison_table(p1_data, p2_data, player1, player2)
    
    # Comparison insights
    display_comparison_insights(p1_data, p2_data, player1, player2)

def display_player_comparison_cards(p1_data: pd.Series, p2_data: pd.Series, 
                                   player1: str, player2: str):
    """Display comparison cards for both players"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6B35, #F7931E); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <h3 style="margin: 0 0 1rem 0;">{player1}</h3>
            <div style="font-size: 0.9rem; opacity: 0.9;">
                {safe_string(p1_data.get('position', 'N/A'))} • {safe_string(p1_data.get('college', 'N/A'))}
            </div>
            <div style="margin-top: 1.5rem;">
                <div>{safe_numeric(p1_data.get('ppg', 0)):.1f} PPG</div>
                <div>{safe_numeric(p1_data.get('rpg', 0)):.1f} RPG</div>
                <div>{safe_numeric(p1_data.get('apg', 0)):.1f} APG</div>
                <div style="margin-top: 1rem; font-size: 0.8rem;">
                    Grade: {safe_string(p1_data.get('scout_grade', 'N/A'))}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4361EE, #2563EB); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <h3 style="margin: 0 0 1rem 0;">{player2}</h3>
            <div style="font-size: 0.9rem; opacity: 0.9;">
                {safe_string(p2_data.get('position', 'N/A'))} • {safe_string(p2_data.get('college', 'N/A'))}
            </div>
            <div style="margin-top: 1.5rem;">
                <div>{safe_numeric(p2_data.get('ppg', 0)):.1f} PPG</div>
                <div>{safe_numeric(p2_data.get('rpg', 0)):.1f} RPG</div>
                <div>{safe_numeric(p2_data.get('apg', 0)):.1f} APG</div>
                <div style="margin-top: 1rem; font-size: 0.8rem;">
                    Grade: {safe_string(p2_data.get('scout_grade', 'N/A'))}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_comparison_radar_section(p1_data: pd.Series, p2_data: pd.Series, 
                                   player1: str, player2: str):
    """Create radar chart section"""
    st.markdown("### 📊 Skill Comparison Radar")
    
    try:
        fig = create_comparison_radar(p1_data, p2_data, player1, player2)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Unable to create radar chart - insufficient data")
    except Exception as e:
        st.error(f"Error creating radar chart: {e}")

def display_comparison_insights(p1_data: pd.Series, p2_data: pd.Series, 
                               player1: str, player2: str):
    """Display comparison insights and recommendations"""
    st.markdown("### 💡 Comparison Insights")
    
    # Calculate key metrics
    p1_potential = safe_numeric(p1_data.get('final_gen_probability', 0.5))
    p2_potential = safe_numeric(p2_data.get('final_gen_probability', 0.5))
    
    p1_age = safe_numeric(p1_data.get('age', 20))
    p2_age = safe_numeric(p2_data.get('age', 20))
    
    p1_ppg = safe_numeric(p1_data.get('ppg', 0))
    p2_ppg = safe_numeric(p2_data.get('ppg', 0))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Key Advantages")
        
        advantages_p1 = []
        if p1_potential > p2_potential:
            advantages_p1.append(f"Higher ceiling ({p1_potential:.1%} vs {p2_potential:.1%})")
        if p1_age < p2_age:
            advantages_p1.append(f"Younger age ({p1_age:.0f} vs {p2_age:.0f})")
        if p1_ppg > p2_ppg:
            advantages_p1.append(f"Better scorer ({p1_ppg:.1f} vs {p2_ppg:.1f} PPG)")
        
        if advantages_p1:
            st.success(f"**{player1} advantages:**")
            for adv in advantages_p1:
                st.write(f"• {adv}")
        else:
            st.info(f"**{player1}** - No major statistical advantages")
    
    with col2:
        advantages_p2 = []
        if p2_potential > p1_potential:
            advantages_p2.append(f"Higher ceiling ({p2_potential:.1%} vs {p1_potential:.1%})")
        if p2_age < p1_age:
            advantages_p2.append(f"Younger age ({p2_age:.0f} vs {p1_age:.0f})")
        if p2_ppg > p1_ppg:
            advantages_p2.append(f"Better scorer ({p2_ppg:.1f} vs {p1_ppg:.1f} PPG)")
        
        if advantages_p2:
            st.success(f"**{player2} advantages:**")
            for adv in advantages_p2:
                st.write(f"• {adv}")
        else:
            st.info(f"**{player2}** - No major statistical advantages")
    
    # Overall recommendation
    st.markdown("#### 🏆 Draft Recommendation")
    
    if p1_potential > p2_potential + 0.1:
        recommendation = f"**{player1}** has significantly higher ceiling and should be drafted first"
    elif p2_potential > p1_potential + 0.1:
        recommendation = f"**{player2}** has significantly higher ceiling and should be drafted first"
    elif abs(p1_age - p2_age) > 1:
        younger = player1 if p1_age < p2_age else player2
        recommendation = f"**{younger}** gets the edge due to age and development potential"
    else:
        recommendation = "Very close comparison - draft based on team needs and fit"
    
    st.info(recommendation)
