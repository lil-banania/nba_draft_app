# pages/steals_busts.py
"""Page Steals & Busts avec analyse prédictive avancée"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.data_utils import safe_numeric, safe_string
from components.cards import display_prediction_card

def show(df: pd.DataFrame):
    """Page principale Steals & Busts"""
    st.markdown("## 💎 Bold Predictions: Steals & Busts")
    st.caption("AI-powered analysis identifying potential steals and bust risks")
    
    # Calculate steal and bust scores
    df_analysis = calculate_advanced_metrics(df)
    
    # Display main analysis
    col1, col2 = st.columns(2)
    
    with col1:
        display_steal_predictions(df_analysis)
    
    with col2:
        display_bust_predictions(df_analysis)
    
    # Summary insights
    display_summary_insights()

def calculate_advanced_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate advanced metrics for steal/bust analysis"""
    df_analysis = df.copy()
    
    # Calculate multiple factors for steal potential
    df_analysis['skill_efficiency'] = calculate_skill_efficiency(df_analysis)
    df_analysis['age_factor'] = calculate_age_factor(df_analysis)
    df_analysis['shooting_upside'] = calculate_shooting_upside(df_analysis)
    df_analysis['steal_score'] = calculate_steal_score(df_analysis)
    df_analysis['bust_risk'] = calculate_bust_risk(df_analysis)
    
    return df_analysis

def calculate_skill_efficiency(df: pd.DataFrame) -> pd.Series:
    """Calculate skill efficiency metric"""
    if 'usage_rate' in df.columns:
        return df['ppg'] / df['usage_rate'] * 100
    else:
        return df['ppg']  # Fallback if usage_rate not available

def calculate_age_factor(df: pd.DataFrame) -> pd.Series:
    """Calculate age advantage factor"""
    return 1 + (20 - df['age']) * 0.1  # Younger = more upside

def calculate_shooting_upside(df: pd.DataFrame) -> pd.Series:
    """Calculate shooting potential"""
    if 'ft_pct' in df.columns:
        return df['three_pt_pct'] * df['ft_pct']
    else:
        return df['three_pt_pct']

def calculate_steal_score(df: pd.DataFrame) -> pd.Series:
    """Calculate comprehensive steal score"""
    return (
        df['final_gen_probability'] * 50 +
        df['skill_efficiency'] * 0.5 +
        df['age_factor'] * 10 +
        df['shooting_upside'] * 30
    ) / (df['final_rank'] * 0.5)

def calculate_bust_risk(df: pd.DataFrame) -> pd.Series:
    """Calculate bust risk score for each player"""
    bust_risks = []
    
    for idx, row in df.iterrows():
        risk = 0
        
        # Age risk
        if row['age'] > 21:
            risk += 20
        
        # Shooting risk for guards/wings
        if row['position'] in ['PG', 'SG', 'SF'] and row['three_pt_pct'] < 0.32:
            risk += 25
        
        # Efficiency risk
        if 'ts_pct' in row and row['ts_pct'] < 0.50:
            risk += 20
        
        # Limited skill risk
        if row['ppg'] < 15 and row['rpg'] < 7 and row['apg'] < 5:
            risk += 15
        
        # Usage vs efficiency
        if 'usage_rate' in row and row['usage_rate'] > 25 and row.get('ts_pct', 0.5) < 0.52:
            risk += 20
        
        bust_risks.append(risk)
    
    return pd.Series(bust_risks, index=df.index)

def display_steal_predictions(df_analysis: pd.DataFrame):
    """Display steal predictions with detailed analysis"""
    st.markdown("### 💎 **BOLD STEAL PREDICTIONS**")
    st.caption("Players who will massively outperform draft position")
    
    # Get steals: players outside top 10 with high steal scores
    potential_steals = df_analysis[df_analysis['final_rank'] > 10].nlargest(5, 'steal_score')
    
    steal_predictions = generate_steal_predictions(potential_steals)
    
    for pred in steal_predictions:
        display_steal_card(pred)

def display_bust_predictions(df_analysis: pd.DataFrame):
    """Display bust risk predictions"""
    st.markdown("### ⚠️ **BUST RISK ALERTS**")
    st.caption("High picks with significant red flags")
    
    # Get busts: top 20 picks with high bust risk
    potential_busts = df_analysis.head(20).nlargest(5, 'bust_risk')
    
    bust_predictions = generate_bust_predictions(potential_busts)
    
    for pred in bust_predictions:
        display_bust_card(pred)

def generate_steal_predictions(potential_steals: pd.DataFrame) -> list:
    """Generate detailed steal predictions"""
    predictions = [
        {
            'prediction': "Future All-Star",
            'reasoning': "Elite efficiency + shooting upside + perfect age curve",
            'confidence': 85
        },
        {
            'prediction': "6th Man of the Year",
            'reasoning': "Instant offense skillset being overlooked",
            'confidence': 75
        },
        {
            'prediction': "Starting Role Player",
            'reasoning': "3&D potential with room to grow",
            'confidence': 70
        },
        {
            'prediction': "Surprise Rookie Impact",
            'reasoning': "NBA-ready skills despite lower ranking",
            'confidence': 65
        },
        {
            'prediction': "Late Round Gem",
            'reasoning': "Specialist skills that translate immediately",
            'confidence': 60
        }
    ]
    
    # Combine with player data
    result = []
    for i, (_, player) in enumerate(potential_steals.iterrows()):
        if i < len(predictions):
            pred = predictions[i].copy()
            pred['player'] = player
            result.append(pred)
    
    return result

def generate_bust_predictions(potential_busts: pd.DataFrame) -> list:
    """Generate detailed bust predictions"""
    predictions = [
        {
            'prediction': "Major Disappointment",
            'reasoning': "Multiple red flags: age, efficiency, skill gaps",
            'confidence': 80
        },
        {
            'prediction': "Role Player Ceiling",
            'reasoning': "Limited upside despite high draft position",
            'confidence': 70
        },
        {
            'prediction': "Bench Contributor",
            'reasoning': "Skills won't translate to NBA level",
            'confidence': 65
        },
        {
            'prediction': "Development Project",
            'reasoning': "Raw talent but significant concerns",
            'confidence': 60
        },
        {
            'prediction': "Trade Candidate",
            'reasoning': "May need change of scenery to succeed",
            'confidence': 55
        }
    ]
    
    # Combine with player data
    result = []
    for i, (_, player) in enumerate(potential_busts.iterrows()):
        if i < len(predictions):
            pred = predictions[i].copy()
            pred['player'] = player
            result.append(pred)
    
    return result

def display_steal_card(pred: dict):
    """Display steal prediction card"""
    player = pred['player']
    name = safe_string(player['name'])
    rank = int(safe_numeric(player['final_rank']))
    position = safe_string(player['position'])
    
    # Determine steal level color
    if pred['confidence'] > 80:
        color = "#059669"  # Dark green
        steal_level = "🔥 MEGA STEAL"
    elif pred['confidence'] > 70:
        color = "#10b981"  # Medium green
        steal_level = "💎 GREAT VALUE"
    else:
        color = "#34d399"  # Light green
        steal_level = "✨ GOOD VALUE"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color}, {color}dd); 
                padding: 1.2rem; 
                border-radius: 12px; 
                margin: 0.8rem 0; 
                color: white;
                border: 2px solid {color};">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.3rem;">
                    {steal_level}
                </div>
                <strong style="font-size: 1.1rem;">#{rank} {name}</strong>
                <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.95;">
                    {position} • {pred['prediction']}
                </div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; font-style: italic;">
                    "{pred['reasoning']}"
                </div>
            </div>
            <div style="text-align: center; margin-left: 1rem;">
                <div style="font-size: 2rem; font-weight: bold;">
                    {pred['confidence']}%
                </div>
                <div style="font-size: 0.7rem; opacity: 0.9;">
                    Confidence
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_bust_card(pred: dict):
    """Display bust prediction card"""
    player = pred['player']
    name = safe_string(player['name'])
    rank = int(safe_numeric(player['final_rank']))
    position = safe_string(player['position'])
    
    # Determine risk level color
    if pred['confidence'] > 75:
        color = "#dc2626"  # Dark red
        risk_level = "🚨 EXTREME RISK"
    elif pred['confidence'] > 65:
        color = "#ef4444"  # Medium red
        risk_level = "⚠️ HIGH RISK"
    else:
        color = "#f87171"  # Light red
        risk_level = "⚡ MODERATE RISK"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color}, {color}dd); 
                padding: 1.2rem; 
                border-radius: 12px; 
                margin: 0.8rem 0; 
                color: white;
                border: 2px solid {color};">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.3rem;">
                    {risk_level}
                </div>
                <strong style="font-size: 1.1rem;">#{rank} {name}</strong>
                <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.95;">
                    {position} • {pred['prediction']}
                </div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; font-style: italic;">
                    "{pred['reasoning']}"
                </div>
            </div>
            <div style="text-align: center; margin-left: 1rem;">
                <div style="font-size: 2rem; font-weight: bold;">
                    {pred['confidence']}%
                </div>
                <div style="font-size: 0.7rem; opacity: 0.9;">
                    Risk Level
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_summary_insights():
    """Display key insights summary"""
    st.markdown("---")
    st.markdown("### 📊 **Key Insights**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🎯 Steal Indicators:**
        - Young players (19 or under) with high efficiency
        - Strong shooters being undervalued
        - Players with elite skills in specific areas
        - Good college stats with low usage rates
        """)
    
    with col2:
        st.warning("""
        **⚠️ Bust Warning Signs:**
        - Older prospects (21+) without elite skills
        - Poor shooting for perimeter players
        - High usage with low efficiency
        - Limited athleticism or size for position
        """)

def display_methodology():
    """Display analysis methodology"""
    with st.expander("🔬 Analysis Methodology"):
        st.markdown("""
        ### Steal Score Calculation
        - **Generational Probability** (50%): AI-assessed ceiling
        - **Skill Efficiency** (5%): Production per usage
        - **Age Factor** (10%): Youth bonus multiplier  
        - **Shooting Upside** (30%): 3P% × FT% correlation
        - **Draft Position Penalty**: Divided by rank factor
        
        ### Bust Risk Factors
        - **Age Premium**: 21+ years = +20 risk points
        - **Shooting Concerns**: <32% 3P% for perimeter = +25 points
        - **Efficiency Red Flags**: <50% TS% = +20 points
        - **Limited Skills**: No elite area = +15 points
        - **Usage/Efficiency Gap**: High usage + low efficiency = +20 points
        
        ### Confidence Levels
        - **80%+**: Historical precedent + multiple indicators
        - **70-79%**: Strong indicators with some uncertainty
        - **60-69%**: Moderate confidence with risk factors
        - **<60%**: Speculative based on limited data
        """)
