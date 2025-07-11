# components/charts.py
"""Graphiques et visualisations réutilisables"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.helpers import safe_numeric, safe_string

def create_position_distribution_chart(df: pd.DataFrame):
    """Create position distribution pie chart"""
    if 'position' not in df.columns:
        return None
    
    position_counts = df['position'].value_counts()
    fig_pie = px.pie(
        values=position_counts.values,
        names=position_counts.index,
        title="Distribution by Position",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_layout(height=400)
    return fig_pie

def create_potential_bar_chart(df: pd.DataFrame, top_n: int = 10):
    """Create top prospects potential bar chart"""
    if 'final_gen_probability' not in df.columns:
        return None
    
    top_potential = df.nlargest(top_n, 'final_gen_probability')
    fig_bar = px.bar(
        top_potential,
        x='name',
        y='final_gen_probability',
        title=f"Top {top_n} by Generational Talent Probability",
        color='final_gen_probability',
        color_continuous_scale='Viridis',
        labels={'final_gen_probability': 'Potential'}
    )
    fig_bar.update_xaxes(tickangle=45)
    fig_bar.update_yaxes(tickformat='.0%')
    fig_bar.update_layout(height=500)
    return fig_bar

def create_comparison_radar(p1_data: pd.Series, p2_data: pd.Series, 
                           player1: str, player2: str):
    """Create radar chart for player comparison - EXTRAIT DE L'ORIGINAL"""
    categories = ['Scoring', 'Shooting', 'Rebounding', 'Playmaking', 
                 'Defense', 'Efficiency', 'Potential']
    
    # Calculate normalized values - MÊME LOGIQUE QUE L'ORIGINAL
    p1_values = [
        min(100, safe_numeric(p1_data['ppg']) / 30 * 100),
        safe_numeric(p1_data.get('three_pt_pct', 0)) * 200,
        min(100, safe_numeric(p1_data['rpg']) / 15 * 100),
        min(100, safe_numeric(p1_data['apg']) / 10 * 100),
        min(100, (safe_numeric(p1_data.get('spg', 0)) + safe_numeric(p1_data.get('bpg', 0))) / 4 * 100),
        safe_numeric(p1_data.get('ts_pct', 0.5)) * 100,
        safe_numeric(p1_data.get('final_gen_probability', 0.5)) * 100
    ]
    
    p2_values = [
        min(100, safe_numeric(p2_data['ppg']) / 30 * 100),
        safe_numeric(p2_data.get('three_pt_pct', 0)) * 200,
        min(100, safe_numeric(p2_data['rpg']) / 15 * 100),
        min(100, safe_numeric(p2_data['apg']) / 10 * 100),
        min(100, (safe_numeric(p2_data.get('spg', 0)) + safe_numeric(p2_data.get('bpg', 0))) / 4 * 100),
        safe_numeric(p2_data.get('ts_pct', 0.5)) * 100,
        safe_numeric(p2_data.get('final_gen_probability', 0.5)) * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1_values + [p1_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player1,
        line=dict(color='#FF6B35', width=3),
        fillcolor='rgba(255, 107, 53, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=p2_values + [p2_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player2,
        line=dict(color='#4361EE', width=3),
        fillcolor='rgba(67, 97, 238, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )
        ),
        showlegend=True,
        title=f"Skill Comparison: {player1} vs {player2}",
        height=500,
        font=dict(size=14)
    )
    
    return fig

def create_movement_visualization(current_df: pd.DataFrame, historical_rankings: list, year: int):
    """Create movement visualization for What If simulator - EXTRAIT DE L'ORIGINAL"""
    # Prepare data for visualization
    movement_data = []
    for player in historical_rankings:
        movement_data.append({
            'Player': player['name'][:15] + ('...' if len(player['name']) > 15 else ''),
            'Current Rank': player['current_rank'],
            'Historical Rank': player['historical_rank'],
            'Change': player['rank_change'],
            'Position': player['position'],
            'Era Fit': player['era_fit']
        })
    
    # Create slope chart - MÊME LOGIQUE QUE L'ORIGINAL
    fig = go.Figure()
    
    # Add lines for each player
    for player in movement_data:
        color = (
            '#10b981' if player['Change'] > 2 else  # Green for risers
            '#ef4444' if player['Change'] < -2 else  # Red for fallers
            '#6b7280'  # Gray for stable
        )
        
        fig.add_trace(go.Scatter(
            x=[1, 2],
            y=[player['Current Rank'], player['Historical Rank']],
            mode='lines+markers',
            name=player['Player'],
            line=dict(color=color, width=2),
            marker=dict(size=8, color=color),
            hovertemplate=(
                f"<b>{player['Player']}</b><br>"
                f"Position: {player['Position']}<br>"
                f"2025 Rank: #{player['Current Rank']}<br>"
                f"{year} Rank: #{player['Historical Rank']}<br>"
                f"Change: {player['Change']:+d}<br>"
                f"Era Fit: {player['Era Fit']}<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))
    
    fig.update_layout(
        title=f"Draft Position Changes: 2025 → {year}",
        xaxis=dict(
            tickvals=[1, 2],
            ticktext=['2025 Draft', f'{year} Draft'],
            range=[0.8, 2.8]
        ),
        yaxis=dict(
            title="Draft Position",
            autorange="reversed",
            tickmode='linear',
            tick0=1,
            dtick=2
        ),
        height=600,
        showlegend=False,
        hovermode='closest'
    )
    
    return fig

def create_projection_timeline_chart(years: list, projected_ppg: list, projected_rpg: list, 
                                   projected_apg: list, player_name: str):
    """Create 5-year projection timeline - EXTRAIT DE create_realistic_projections"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Points Per Game', 'Rebounds Per Game', 'Assists Per Game', 'Overall Development'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Add traces - MÊME LOGIQUE QUE L'ORIGINAL
    fig.add_trace(
        go.Scatter(x=years, y=projected_ppg, mode='lines+markers', name='PPG',
                  line=dict(color='#FF6B35', width=4), marker=dict(size=12)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=projected_rpg, mode='lines+markers', name='RPG',
                  line=dict(color='#4361EE', width=4), marker=dict(size=12)),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=projected_apg, mode='lines+markers', name='APG',
                  line=dict(color='#10B981', width=4), marker=dict(size=12)),
        row=2, col=1
    )
    
    # Overall impact
    overall_impact = [(p*1.5 + r + a*1.2) / 3.7 for p, r, a in zip(projected_ppg, projected_rpg, projected_apg)]
    fig.add_trace(
        go.Scatter(x=years, y=overall_impact, mode='lines+markers', name='Overall',
                  line=dict(color='#8B5CF6', width=4), marker=dict(size=12)),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600, 
        title=f"{player_name} - Realistic 5-Year Development Projection",
        showlegend=False
    )
    fig.update_xaxes(title_text="NBA Season", tickvals=years, ticktext=[f"Year {y}" for y in years])
    
    return fig

def create_team_fit_heatmap(matrix_data: list, players: list, teams: list, title: str):
    """Create team-player fit heatmap - EXTRAIT DE display_team_player_matrix"""
    fig = px.imshow(
        matrix_data,
        labels=dict(x="Team", y="Player", color="Fit Score"),
        x=[team.split()[-1] for team in teams],
        y=players,
        color_continuous_scale="RdYlGn",
        title=title,
        aspect="auto"
    )
    
    fig.update_layout(height=500, font=dict(size=12))
    fig.update_coloraxes(colorbar_title="Fit Score %")
    
    return fig

def create_steals_busts_scatter(df: pd.DataFrame):
    """Create scatter plot for steals and busts analysis"""
    if not all(col in df.columns for col in ['final_rank', 'final_gen_probability']):
        return None
    
    # Color based on potential vs rank
    df['category'] = 'Average'
    df.loc[(df['final_rank'] > 15) & (df['final_gen_probability'] > 0.6), 'category'] = 'Potential Steal'
    df.loc[(df['final_rank'] <= 10) & (df['final_gen_probability'] < 0.4), 'category'] = 'Bust Risk'
    
    fig = px.scatter(
        df,
        x='final_rank',
        y='final_gen_probability',
        color='category',
        hover_data=['name', 'position', 'college'],
        title="Steals & Busts Analysis: Rank vs Potential",
        labels={
            'final_rank': 'Draft Rank',
            'final_gen_probability': 'Generational Talent Probability'
        },
        color_discrete_map={
            'Potential Steal': '#10B981',
            'Bust Risk': '#EF4444',
            'Average': '#6B7280'
        }
    )
    
    fig.update_layout(height=500)
    fig.update_yaxes(tickformat='.0%')
    
    return fig
