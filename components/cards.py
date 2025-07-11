# components/cards.py
"""Cartes de joueurs et composants d'affichage"""

import streamlit as st
import pandas as pd
from utils.helpers import safe_numeric, safe_string, format_height
from config.settings import COLORS

def display_player_card(player: pd.Series):
    """Display a properly formatted player card - EXTRAIT DE L'ORIGINAL"""
    name = safe_string(player['name'])
    position = safe_string(player['position'])
    college = safe_string(player['college'])
    archetype = safe_string(player.get('archetype', 'N/A'))
    
    # Stats
    ppg = safe_numeric(player['ppg'])
    rpg = safe_numeric(player['rpg'])
    apg = safe_numeric(player['apg'])
    fg_pct = safe_numeric(player.get('fg_pct', 0))
    three_pt_pct = safe_numeric(player.get('three_pt_pct', 0))
    ts_pct = safe_numeric(player.get('ts_pct', 0))
    
    # Physical
    age = safe_numeric(player.get('age', 0))
    height = format_height(safe_numeric(player.get('height', 0)))
    weight = safe_numeric(player.get('weight', 0))
    
    grade = safe_string(player['scout_grade'])
    prob = safe_numeric(player.get('final_gen_probability', 0.5))
    
    # Card header - MÊME STRUCTURE QUE L'ORIGINAL
    st.markdown(f"""
    <div style="background: white; 
                border: 2px solid {COLORS['primary']}; 
                border-left: 6px solid {COLORS['primary']};
                padding: 2rem; 
                border-radius: 15px; 
                margin: 1.5rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div>
                <h3 style="margin: 0 0 0.5rem 0; color: #333; font-size: 1.4rem;">{name}</h3>
                <div style="color: #666; font-size: 1rem;">
                    {position} • {college} • {archetype}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="background: {COLORS['primary']}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                    Grade: {grade}
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;">
                    Projection: {prob:.1%}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit metrics for stats - COMME DANS L'ORIGINAL
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("PPG", f"{ppg:.1f}")
    with col2:
        st.metric("RPG", f"{rpg:.1f}")
    with col3:
        st.metric("APG", f"{apg:.1f}")
    with col4:
        st.metric("FG%", f"{fg_pct:.1%}")
    with col5:
        st.metric("3P%", f"{three_pt_pct:.1%}")
    with col6:
        st.metric("TS%", f"{ts_pct:.1%}")
    
    # Physical attributes - MÊME FORMAT QUE L'ORIGINAL
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
        <span style="margin: 0 1rem;"><strong>Age:</strong> {age:.0f}</span>
        <span style="margin: 0 1rem;"><strong>Height:</strong> {height}</span>
        <span style="margin: 0 1rem;"><strong>Weight:</strong> {weight:.0f} lbs</span>
    </div>
    """, unsafe_allow_html=True)

def display_leader_card(title: str, player_name: str, stat_value: str, description: str, color: str = None):
    """Display a leader category card - EXTRAIT DE create_leaders_section"""
    if color is None:
        color = COLORS['primary']
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa, #ffffff); 
                border: 2px solid {color}; 
                border-left: 6px solid {color};
                padding: 1.5rem; 
                border-radius: 12px; 
                margin: 1rem 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                color: #333;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="color: #333; font-size: 1.2rem;">
                    {title}
                </strong>
                <div style="font-size: 1.1rem; color: #333; margin: 0.5rem 0;">
                    <strong>{player_name}</strong>
                </div>
                <div style="font-size: 0.9rem; color: #666;">
                    {description}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2.5rem; font-weight: bold; color: {color};">
                    {stat_value}
                </div>
                <div style="font-size: 0.9rem; color: #666;">Peak</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_comparison_card(player1_name: str, player2_name: str, player1_data: dict, player2_data: dict):
    """Display side-by-side comparison card"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']}); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <h3 style="margin: 0 0 1rem 0;">{player1_name}</h3>
            <div style="font-size: 0.9rem; opacity: 0.9;">
                {player1_data.get('position', 'N/A')} • {player1_data.get('college', 'N/A')}
            </div>
            <div style="margin-top: 1.5rem;">
                <div>{player1_data.get('ppg', 0):.1f} PPG</div>
                <div>{player1_data.get('rpg', 0):.1f} RPG</div>
                <div>{player1_data.get('apg', 0):.1f} APG</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['info']}, #2563EB); 
                    padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
            <h3 style="margin: 0 0 1rem 0;">{player2_name}</h3>
            <div style="font-size: 0.9rem; opacity: 0.9;">
                {player2_data.get('position', 'N/A')} • {player2_data.get('college', 'N/A')}
            </div>
            <div style="margin-top: 1.5rem;">
                <div>{player2_data.get('ppg', 0):.1f} PPG</div>
                <div>{player2_data.get('rpg', 0):.1f} RPG</div>
                <div>{player2_data.get('apg', 0):.1f} APG</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_team_fit_card(team_name: str, fit_score: float, reasons: list, context: str):
    """Display team fit analysis card - EXTRAIT DE display_player_perspective_analysis"""
    if fit_score > 70:
        color = COLORS['success']
        tier = "Excellent Fit"
    elif fit_score > 50:
        color = COLORS['warning']
        tier = "Good Fit"
    else:
        color = COLORS['error']
        tier = "Poor Fit"
    
    st.markdown(f"""
    <div style="background: white; 
                border: 2px solid {color}; 
                border-left: 6px solid {color};
                padding: 1.5rem; 
                border-radius: 12px; 
                margin: 1rem 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <strong style="color: #333; font-size: 1.2rem;">
                    {team_name}
                </strong>
                <div style="font-size: 0.9rem; color: #666; margin: 0.5rem 0; font-style: italic;">
                    {context}
                </div>
                <div style="font-size: 1rem; color: #666;">
                    {' • '.join(reasons) if reasons else 'General fit'}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 2.5rem; font-weight: bold; color: {color};">
                    {fit_score:.0f}%
                </div>
                <div style="font-size: 0.9rem; color: #666;">{tier}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_prospect_summary_card(rank: int, name: str, position: str, grade: str, potential: float):
    """Display prospect summary card for tables"""
    tier_color = COLORS['primary'] if rank <= 5 else COLORS['warning'] if rank <= 14 else COLORS['info']
    
    return f"""
    <div style="display: flex; align-items: center; padding: 0.5rem;">
        <div style="background: {tier_color}; color: white; padding: 0.2rem 0.5rem; 
                    border-radius: 15px; margin-right: 1rem; font-weight: bold; min-width: 30px; text-align: center;">
            #{rank}
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 600; color: #333;">{name}</div>
            <div style="font-size: 0.8rem; color: #666;">{position} • Grade {grade} • {potential:.1%} potential</div>
        </div>
    </div>
    """

def display_steal_bust_card(player_name: str, prediction: str, reasoning: str, 
                           confidence: int, card_type: str = "steal"):
    """Display steal or bust prediction card - EXTRAIT DE create_steals_busts_analysis"""
    if card_type == "steal":
        if confidence > 80:
            color = "#059669"
            level = "🔥 MEGA STEAL"
        elif confidence > 70:
            color = "#10b981"
            level = "💎 GREAT VALUE"
        else:
            color = "#34d399"
            level = "✨ GOOD VALUE"
    else:  # bust
        if confidence > 75:
            color = "#dc2626"
            level = "🚨 EXTREME RISK"
        elif confidence > 65:
            color = "#ef4444"
            level = "⚠️ HIGH RISK"
        else:
            color = "#f87171"
            level = "⚡ MODERATE RISK"
    
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
                    {level}
                </div>
                <strong style="font-size: 1.1rem;">{player_name}</strong>
                <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.95;">
                    {prediction}
                </div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; font-style: italic;">
                    "{reasoning}"
                </div>
            </div>
            <div style="text-align: center; margin-left: 1rem;">
                <div style="font-size: 2rem; font-weight: bold;">
                    {confidence}%
                </div>
                <div style="font-size: 0.7rem; opacity: 0.9;">
                    {'Confidence' if card_type == 'steal' else 'Risk Level'}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
def display_intel_card(title: str, items: list, card_type: str = "info"):
    """Display intelligence card with items"""
    colors = {
        "info": "#3B82F6",
        "success": "#10B981", 
        "warning": "#F59E0B",
        "error": "#EF4444"
    }
    
    color = colors.get(card_type, colors["info"])
    
    st.markdown(f"""
    <div style="background: {color}20; 
                border-left: 4px solid {color}; 
                padding: 1rem; 
                border-radius: 8px; 
                margin: 0.5rem 0;">
        <h4 style="margin: 0 0 0.5rem 0; color: {color};">{title}</h4>
        {"".join([f"<div style='margin: 0.2rem 0;'>• {item}</div>" for item in items])}
    </div>
    """, unsafe_allow_html=True)

def display_prediction_card(prediction_type: str, player_name: str, rank: int, 
                          position: str, prediction: str, reasoning: str, 
                          confidence: int):
    """Display prediction card for steals/busts"""
    
    if prediction_type == "steal":
        if confidence > 80:
            color = "#059669"
            level = "🔥 MEGA STEAL"
        elif confidence > 70:
            color = "#10b981"
            level = "💎 GREAT VALUE"
        else:
            color = "#34d399"
            level = "✨ GOOD VALUE"
    else:  # bust
        if confidence > 75:
            color = "#dc2626"
            level = "🚨 EXTREME RISK"
        elif confidence > 65:
            color = "#ef4444"
            level = "⚠️ HIGH RISK"
        else:
            color = "#f87171"
            level = "⚡ MODERATE RISK"
    
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
                    {level}
                </div>
                <strong style="font-size: 1.1rem;">#{rank} {player_name}</strong>
                <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.95;">
                    {position} • {prediction}
                </div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; font-style: italic;">
                    "{reasoning}"
                </div>
            </div>
            <div style="text-align: center; margin-left: 1rem;">
                <div style="font-size: 2rem; font-weight: bold;">
                    {confidence}%
                </div>
                <div style="font-size: 0.7rem; opacity: 0.9;">
                    {"Confidence" if prediction_type == "steal" else "Risk Level"}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
