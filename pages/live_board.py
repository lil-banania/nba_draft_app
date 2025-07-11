# pages/live_board.py
"""Page Live Big Board avec composants modulaires"""

import streamlit as st
import pandas as pd
import numpy as np
from components.tables import create_big_board_table
from components.filters import create_view_options
from utils.helpers import safe_numeric, safe_string, get_tier_info
from config.settings import DRAFT_TIERS

def show(df: pd.DataFrame):
    """Display live big board page"""
    st.markdown("## 🎯 NBA Draft 2025 Live Big Board")
    st.caption("Updated with latest intel and team needs • Real-time draft projections")
    
    # Board controls
    display_board_controls(df)
    
    # Latest intel banner
    display_draft_intel()
    
    # Create draft variance for realistic predictions
    draft_order = create_draft_predictions(df)
    
    # Filter and display options
    filtered_board = apply_board_filters(draft_order)
    
    # Main big board table
    create_big_board_table(filtered_board)
    
    # Draft insights
    display_draft_insights(filtered_board)
    
    # Real-time updates section
    display_recent_updates()

def display_board_controls(df: pd.DataFrame):
    """Display board control options"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        view_range = st.selectbox(
            "View Range:",
            ["Top 14 (Lottery)", "Top 30 (First Round)", "Top 60 (Full Draft)"],
            key="board_view_range"
        )
        st.session_state['board_view_range'] = view_range
    
    with col2:
        sort_option = st.selectbox(
            "Sort by:",
            ["Big Board Rank", "Consensus Rank", "Upside", "Floor", "Team Fit"],
            key="board_sort"
        )
        st.session_state['board_sort'] = sort_option
    
    with col3:
        position_filter = st.selectbox(
            "Position Filter:",
            ["All Positions", "Guards (PG/SG)", "Wings (SG/SF)", "Forwards (SF/PF)", "Bigs (PF/C)", "PG", "SG", "SF", "PF", "C"],
            key="board_position"
        )
        st.session_state['board_position'] = position_filter
    
    with col4:
        tier_filter = st.selectbox(
            "Tier Filter:",
            ["All Tiers", "Elite (1-5)", "Lottery (6-14)", "First Round (15-30)", "Second Round (31-60)"],
            key="board_tier"
        )
        st.session_state['board_tier'] = tier_filter

def display_draft_intel():
    """Display latest draft intelligence"""
    intel_data = get_latest_draft_intel()
    
    st.markdown("### 🚨 Latest Draft Intel")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"**Last Updated:** {intel_data['last_updated']}")
        
        with st.expander("📰 Recent News & Movements", expanded=True):
            for news in intel_data['major_moves']:
                st.markdown(f"• {news}")
    
    with col2:
        st.markdown("**🔥 Trending:**")
        for trend in intel_data.get('trending', ['Cooper Flagg #1 Lock', 'Guard-heavy lottery', 'International surge']):
            st.markdown(f"• {trend}")

def create_draft_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """Create realistic draft predictions with variance"""
    draft_order = df.copy()
    
    # Add realistic variance based on prospect uncertainty
    np.random.seed(42)  # For consistent results
    
    # Higher uncertainty for lower-ranked prospects
    uncertainty_factor = np.clip(draft_order['final_rank'] / 10, 0.5, 3.0)
    draft_variance = np.random.normal(0, uncertainty_factor, len(draft_order))
    
    # Apply variance but keep top prospects more stable
    stability_factor = np.where(draft_order['final_rank'] <= 5, 0.3, 1.0)
    draft_order['board_variance'] = draft_variance * stability_factor
    
    # Calculate new board position
    draft_order['big_board_rank'] = draft_order['final_rank'] + draft_order['board_variance']
    draft_order['big_board_rank'] = np.clip(draft_order['big_board_rank'], 1, len(draft_order))
    
    # Sort by new board rank
    draft_order = draft_order.sort_values('big_board_rank').reset_index(drop=True)
    draft_order['board_position'] = range(1, len(draft_order) + 1)
    
    # Calculate movement
    draft_order['movement'] = draft_order['final_rank'] - draft_order['board_position']
    
    return draft_order

def apply_board_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply board filters based on user selection"""
    filtered_df = df.copy()
    
    # View range filter
    view_range = st.session_state.get('board_view_range', 'Top 30 (First Round)')
    if view_range == "Top 14 (Lottery)":
        filtered_df = filtered_df.head(14)
    elif view_range == "Top 30 (First Round)":
        filtered_df = filtered_df.head(30)
    elif view_range == "Top 60 (Full Draft)":
        filtered_df = filtered_df.head(60)
    
    # Position filter
    position_filter = st.session_state.get('board_position', 'All Positions')
    if position_filter == "Guards (PG/SG)":
        filtered_df = filtered_df[filtered_df['position'].isin(['PG', 'SG'])]
    elif position_filter == "Wings (SG/SF)":
        filtered_df = filtered_df[filtered_df['position'].isin(['SG', 'SF'])]
    elif position_filter == "Forwards (SF/PF)":
        filtered_df = filtered_df[filtered_df['position'].isin(['SF', 'PF'])]
    elif position_filter == "Bigs (PF/C)":
        filtered_df = filtered_df[filtered_df['position'].isin(['PF', 'C'])]
    elif position_filter in ['PG', 'SG', 'SF', 'PF', 'C']:
        filtered_df = filtered_df[filtered_df['position'] == position_filter]
    
    # Tier filter
    tier_filter = st.session_state.get('board_tier', 'All Tiers')
    if tier_filter == "Elite (1-5)":
        filtered_df = filtered_df[filtered_df['board_position'] <= 5]
    elif tier_filter == "Lottery (6-14)":
        filtered_df = filtered_df[(filtered_df['board_position'] >= 6) & (filtered_df['board_position'] <= 14)]
    elif tier_filter == "First Round (15-30)":
        filtered_df = filtered_df[(filtered_df['board_position'] >= 15) & (filtered_df['board_position'] <= 30)]
    elif tier_filter == "Second Round (31-60)":
        filtered_df = filtered_df[filtered_df['board_position'] >= 31]
    
    return filtered_df

def display_draft_insights(df: pd.DataFrame):
    """Display key insights from the big board"""
    st.markdown("### 📊 Big Board Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Biggest risers
        biggest_riser = df.loc[df['movement'].idxmax()] if len(df) > 0 else None
        if biggest_riser is not None:
            st.metric(
                "📈 Biggest Riser", 
                safe_string(biggest_riser['name']),
                f"+{biggest_riser['movement']:.0f} spots"
            )
    
    with col2:
        # Biggest fallers
        biggest_faller = df.loc[df['movement'].idxmin()] if len(df) > 0 else None
        if biggest_faller is not None:
            st.metric(
                "📉 Biggest Faller", 
                safe_string(biggest_faller['name']),
                f"{biggest_faller['movement']:.0f} spots"
            )
    
    with col3:
        # Position breakdown
        if len(df) > 0 and 'position' in df.columns:
            guards_count = len(df[df['position'].isin(['PG', 'SG'])])
            st.metric("Guards in Range", guards_count)
    
    with col4:
        # Average potential
        if len(df) > 0:
            avg_potential = df['final_gen_probability'].mean()
            st.metric("Avg Potential", f"{avg_potential:.1%}")

def display_recent_updates():
    """Display recent updates and movements"""
    st.markdown("### 🔄 Recent Board Movements")
    
    # Simulated recent updates
    updates = [
        {"time": "2 hours ago", "update": "Cooper Flagg locks in #1 spot after Hawks workout", "impact": "🔒"},
        {"time": "6 hours ago", "update": "VJ Edgecombe rising after athletic testing", "impact": "📈"},
        {"time": "1 day ago", "update": "International prospects gaining momentum", "impact": "🌍"},
        {"time": "2 days ago", "update": "Teams prioritizing shooting over athleticism", "impact": "🎯"}
    ]
    
    for update in updates:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #FF6B35;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{update['update']}</strong>
                    <div style="font-size: 0.8rem; color: #666; margin-top: 0.3rem;">{update['time']}</div>
                </div>
                <div style="font-size: 1.5rem;">{update['impact']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_latest_draft_intel():
    """Get latest draft intelligence"""
    return {
        'last_updated': 'June 25, 2025 - 3:30 PM ET',
        'major_moves': [
            "Cooper Flagg dominant in individual workouts with multiple teams",
            "Ace Bailey impressing scouts with improved shot selection",
            "International prospect surge continues with strong showings",
            "Teams reaching consensus on guard-heavy lottery",
            "Medical concerns emerging for some projected lottery picks"
        ],
        'trending': [
            "Cooper Flagg #1 consensus",
            "Guard run in top 10", 
            "International talent surge",
            "Shooting premium rising"
        ]
    }
