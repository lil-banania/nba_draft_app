# pages/team_fit.py
"""Page Team Fit Analysis avec composants modulaires"""

import streamlit as st
import pandas as pd
from components.cards import display_team_fit_card
from components.charts import create_team_fit_heatmap
from components.filters import create_team_selector
from config.teams_data import NBA_TEAMS_ANALYSIS, get_teams_by_division, get_team_fit_score
from utils.helpers import safe_numeric, safe_string

def show(df: pd.DataFrame):
    """Display team fit analysis page"""
    st.markdown("## 🎯 Complete NBA Team Fit Analysis")
    st.caption("Analyzing fit with all 30 NBA teams based on roster needs and playing style")
    
    # Analysis mode selection
    analysis_mode = st.radio(
        "Analysis Mode:", 
        ["Team Perspective", "Player Perspective", "Division Matrix", "Best Fits Summary"], 
        horizontal=True
    )
    
    if analysis_mode == "Team Perspective":
        display_team_perspective_analysis(df)
    elif analysis_mode == "Player Perspective":
        display_player_perspective_analysis(df)
    elif analysis_mode == "Division Matrix":
        display_division_matrix_analysis(df)
    else:
        display_best_fits_summary(df)

def display_team_perspective_analysis(df: pd.DataFrame):
    """Display team-focused fit analysis"""
    st.markdown("### 🏀 Team Perspective Analysis")
    
    # Team selection
    selected_team = create_team_selector("team_perspective")
    
    if selected_team in NBA_TEAMS_ANALYSIS:
        team_data = NBA_TEAMS_ANALYSIS[selected_team]
        
        # Team info header
        display_team_info_header(selected_team, team_data)
        
        # Calculate and display best fits
        player_fits = calculate_team_fits(df.head(30), team_data)
        player_fits.sort(key=lambda x: x['fit_score'], reverse=True)
        
        display_team_fit_results(selected_team, player_fits[:12])
        
        # Team needs breakdown
        display_team_needs_breakdown(team_data)

def display_player_perspective_analysis(df: pd.DataFrame):
    """Display player-focused fit analysis"""
    st.markdown("### 👤 Player Perspective Analysis")
    
    # Player selection
    selected_player = st.selectbox("Select Player:", df['name'].head(20).tolist(), key="player_perspective")
    player_data = df[df['name'] == selected_player].iloc[0]
    
    # Calculate fits for all teams
    team_fits = calculate_player_team_fits(player_data)
    team_fits.sort(key=lambda x: x['fit_score'], reverse=True)
    
    # Display player info
    display_player_info_header(selected_player, player_data)
    
    # Show best fits
    st.markdown("### 🎯 Best Team Fits")
    
    col1, col2 = st.columns(2)
    
    # Top 6 fits in each column
    for i, fit in enumerate(team_fits[:12]):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            display_team_fit_card(
                fit['team'],
                fit['fit_score'],
                fit['reasons'],
                fit['context']
            )

def display_division_matrix_analysis(df: pd.DataFrame):
    """Display division-by-division matrix analysis"""
    st.markdown("### 🗺️ Division Matrix Analysis")
    
    # Division selection
    divisions = get_teams_by_division()
    selected_division = st.selectbox("Select Division:", list(divisions.keys()), key="division_matrix")
    
    division_teams = divisions[selected_division]
    top_players = df['name'].head(10).tolist()
    
    # Calculate matrix data
    matrix_data = []
    for player_name in top_players:
        player_data = df[df['name'] == player_name].iloc[0]
        row = []
        
        for team in division_teams:
            team_data = NBA_TEAMS_ANALYSIS[team]
            fit_data = calculate_player_team_fit(player_data, team_data)
            row.append(fit_data['score'])
        
        matrix_data.append(row)
    
    # Create and display heatmap
    fig = create_team_fit_heatmap(
        matrix_data,
        top_players,
        division_teams,
        f"{selected_division} Division - Team/Player Fit Matrix (%)"
    )
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Division insights
    display_division_insights(selected_division, division_teams)

def display_best_fits_summary(df: pd.DataFrame):
    """Display summary of best fits across the draft"""
    st.markdown("### 📊 Best Fits Summary")
    
    # Calculate all fits
    all_fits = []
    
    for _, player in df.head(20).iterrows():
        for team_name, team_data in NBA_TEAMS_ANALYSIS.items():
            fit_data = calculate_player_team_fit(player, team_data)
            
            all_fits.append({
                'Player': player['name'],
                'Team': team_name,
                'Fit Score': fit_data['score'],
                'Rank': player['final_rank'],
                'Position': player['position'],
                'Division': team_data.get('division', 'Unknown')
            })
    
    # Convert to DataFrame for analysis
    fits_df = pd.DataFrame(all_fits)
    
    # Display top matches
    display_top_matches_summary(fits_df)
    
    # Position-specific insights
    display_position_fit_insights(fits_df)

def display_team_info_header(team_name: str, team_data: dict):
    """Display team information header"""
    st.markdown(f"### {team_name}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"**Team Context:** {team_data['team_context']}")
        st.write(f"**Priority:** {team_data.get('priority', 'Balanced approach')}")
        st.write(f"**Division:** {team_data.get('division', 'Unknown')}")
    
    with col2:
        # Top positional needs
        pos_needs = team_data['positional_needs']
        top_need = max(pos_needs.items(), key=lambda x: x[1])
        st.metric("Biggest Need", top_need[0], f"{top_need[1]:.0%} priority")

def display_player_info_header(player_name: str, player_data: pd.Series):
    """Display player information header"""
    st.markdown(f"### {player_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Position", safe_string(player_data.get('position')))
    with col2:
        st.metric("College", safe_string(player_data.get('college')))
    with col3:
        st.metric("Draft Rank", f"#{int(safe_numeric(player_data.get('final_rank', 0)))}")
    with col4:
        st.metric("Potential", f"{safe_numeric(player_data.get('final_gen_probability', 0.5)):.1%}")

def display_team_fit_results(team_name: str, player_fits: list):
    """Display team fit results"""
    st.markdown("### 🎯 Best Fits for This Team")
    
    for i, fit in enumerate(player_fits):
        if fit['fit_score'] > 70:
            color = '#10b981'
            tier = "Excellent Fit"
        elif fit['fit_score'] > 50:
            color = '#f59e0b'
            tier = "Good Fit"
        else:
            color = '#6b7280'
            tier = "Moderate Fit"
        
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
                        #{fit['rank']} {fit['name']} ({fit['position']})
                    </strong>
                    <div style="font-size: 1rem; color: #666; margin-top: 0.5rem;">
                        {' • '.join(fit['reasons']) if fit['reasons'] else 'Good overall fit'}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: {color};">
                        {fit['fit_score']:.0f}%
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">{tier}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_team_needs_breakdown(team_data: dict):
    """Display detailed team needs breakdown"""
    st.markdown("### 📋 Team Needs Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📍 Positional Needs")
        pos_needs = team_data['positional_needs']
        for pos, priority in sorted(pos_needs.items(), key=lambda x: x[1], reverse=True):
            priority_text = "🔴 High" if priority > 0.7 else "🟡 Medium" if priority > 0.4 else "🟢 Low"
            st.write(f"**{pos}:** {priority_text} ({priority:.0%})")
    
    with col2:
        st.markdown("#### 🎯 Skill Priorities")
        skill_needs = team_data['skill_needs']
        for skill, priority in sorted(skill_needs.items(), key=lambda x: x[1], reverse=True):
            priority_text = "🔴 High" if priority > 0.7 else "🟡 Medium" if priority > 0.4 else "🟢 Low"
            st.write(f"**{skill.title()}:** {priority_text} ({priority:.0%})")

def calculate_team_fits(players_df: pd.DataFrame, team_data: dict) -> list:
    """Calculate fit scores for multiple players with a team"""
    player_fits = []
    
    for _, player in players_df.iterrows():
        fit_data = calculate_player_team_fit(player, team_data)
        player_fits.append({
            'name': safe_string(player['name']),
            'position': safe_string(player['position']),
            'fit_score': fit_data['score'],
            'reasons': fit_data['reasons'],
            'rank': safe_numeric(player.get('final_rank', 0))
        })
    
    return player_fits

def calculate_player_team_fits(player: pd.Series) -> list:
    """Calculate fit scores for a player with all teams"""
    team_fits = []
    
    for team_name, team_data in NBA_TEAMS_ANALYSIS.items():
        fit_data = calculate_player_team_fit(player, team_data)
        team_fits.append({
            'team': team_name,
            'fit_score': fit_data['score'],
            'reasons': fit_data['reasons'],
            'context': team_data['team_context']
        })
    
    return team_fits

def calculate_player_team_fit(player: pd.Series, team_data: dict) -> dict:
    """Calculate detailed fit score between a player and team"""
    fit_score = 0
    fit_reasons = []
    
    # Position fit (40% weight)
    position = safe_string(player['position'])
    if position in team_data['positional_needs']:
        pos_score = team_data['positional_needs'][position] * 40
        fit_score += pos_score
        if pos_score > 20:
            fit_reasons.append(f"Fills {position} need")
    
    # Skills fit (60% weight)
    ppg = safe_numeric(player.get('ppg', 0))
    three_pt = safe_numeric(player.get('three_pt_pct', 0))
    apg = safe_numeric(player.get('apg', 0))
    rpg = safe_numeric(player.get('rpg', 0))
    
    # Scoring
    if ppg > 15 and team_data['skill_needs']['scoring'] > 0.6:
        skill_score = team_data['skill_needs']['scoring'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Elite scorer ({ppg:.1f} PPG)")
    
    # Shooting
    if three_pt > 0.35 and team_data['skill_needs']['shooting'] > 0.6:
        skill_score = team_data['skill_needs']['shooting'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Good shooter ({three_pt:.1%})")
    
    # Playmaking
    if apg > 5 and team_data['skill_needs']['playmaking'] > 0.6:
        skill_score = team_data['skill_needs']['playmaking'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Elite playmaker ({apg:.1f} APG)")
    
    # Rebounding
    if rpg > 7 and team_data['skill_needs']['rebounding'] > 0.6:
        skill_score = team_data['skill_needs']['rebounding'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Strong rebounder ({rpg:.1f} RPG)")
    
    # Normalize score
    fit_score = min(100, max(0, fit_score))
    
    return {'score': fit_score, 'reasons': fit_reasons}

def display_top_matches_summary(fits_df: pd.DataFrame):
    """Display top matches summary"""
    st.markdown("#### 🏆 Perfect Matches (90%+ Fit)")
    
    perfect_matches = fits_df[fits_df['Fit Score'] >= 90].sort_values('Fit Score', ascending=False)
    
    if len(perfect_matches) > 0:
        for _, match in perfect_matches.head(10).iterrows():
            st.success(f"**#{match['Rank']} {match['Player']}** → **{match['Team']}** ({match['Fit Score']:.0f}%)")
    else:
        st.info("No perfect matches (90%+) found in current analysis")

def display_position_fit_insights(fits_df: pd.DataFrame):
    """Display position-specific fit insights"""
    st.markdown("#### 📊 Position Fit Analysis")
    
    position_avg = fits_df.groupby('Position')['Fit Score'].mean().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Average Fit by Position:**")
        for pos, avg_fit in position_avg.items():
            st.write(f"**{pos}:** {avg_fit:.1f}% average fit")
    
    with col2:
        best_pos_match = fits_df.loc[fits_df['Fit Score'].idxmax()]
        st.metric(
            "Best Single Match",
            f"{best_pos_match['Player']} → {best_pos_match['Team']}",
            f"{best_pos_match['Fit Score']:.0f}%"
        )

def display_division_insights(division: str, teams: list):
    """Display insights about the division"""
    st.markdown(f"#### 💡 {division} Division Insights")
    
    division_contexts = {
        'Atlantic': "Competitive division with mix of contenders and rebuilders",
        'Central': "Balanced division with varying team philosophies", 
        'Southeast': "Young division focused on development",
        'Northwest': "High-powered offense division",
        'Pacific': "Star-heavy division with championship aspirations",
        'Southwest': "Physical, defensive-minded division"
    }
    
    context = division_contexts.get(division, "Diverse division with varying needs")
    st.info(f"**Division Character:** {context}")
    
    st.markdown("**Teams in Division:**")
    for team in teams:
        team_data = NBA_TEAMS_ANALYSIS[team]
        priority = team_data.get('priority', 'balanced')
        st.write(f"• **{team}:** {priority} approach")
