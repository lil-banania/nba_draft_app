# components/filters.py
"""Composants de filtrage et sélection"""

import streamlit as st
import pandas as pd
from config.settings import POSITIONS

def create_position_filter(key_suffix: str = ""):
    """Create position filter with quick selection buttons - EXTRAIT DE create_enhanced_search_with_stats"""
    st.markdown("**Positions:**")
    positions = POSITIONS['all']
    
    # Boutons de sélection rapide - MÊME LOGIQUE QUE L'ORIGINAL
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    with quick_col1:
        if st.button("All Positions", key=f"all_pos_{key_suffix}"):
            st.session_state[f'selected_positions_{key_suffix}'] = positions
    with quick_col2:
        if st.button("Guards", key=f"guards_{key_suffix}"):
            st.session_state[f'selected_positions_{key_suffix}'] = POSITIONS['guards']
    with quick_col3:
        if st.button("Frontcourt", key=f"frontcourt_{key_suffix}"):
            st.session_state[f'selected_positions_{key_suffix}'] = POSITIONS['forwards'] + ['C']
    
    # Multi-select avec état persistant - EXTRAIT DE L'ORIGINAL
    session_key = f'selected_positions_{key_suffix}'
    if session_key not in st.session_state:
        st.session_state[session_key] = positions
    
    selected_positions = st.multiselect(
        "Select positions:",
        positions,
        default=st.session_state[session_key],
        key=f"position_multiselect_{key_suffix}"
    )
    st.session_state[session_key] = selected_positions
    
    return selected_positions

def create_basic_stats_filters(key_suffix: str = ""):
    """Create basic stats filters - EXTRAIT DE create_enhanced_search_with_stats"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_ppg = st.slider("Min PPG", 0, 30, 0, key=f"ppg_slider_{key_suffix}")
    
    with col2:
        min_3pt = st.slider("Min 3P%", 0.0, 0.6, 0.0, 0.05, key=f"3pt_slider_{key_suffix}")
    
    with col3:
        min_potential = st.slider("Min Potential", 0.0, 1.0, 0.0, 0.1, key=f"potential_slider_{key_suffix}")
    
    return {
        'min_ppg': min_ppg,
        'min_3pt': min_3pt,
        'min_potential': min_potential
    }

def create_advanced_filters(df: pd.DataFrame, key_suffix: str = ""):
    """Create advanced filtering options - EXTRAIT DE create_interactive_filters"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        positions = ['All'] + sorted(df['position'].unique().tolist())
        selected_position = st.selectbox("📍 Position", positions, key=f"position_select_{key_suffix}")
    
    with col2:
        colleges = ['All'] + sorted(df['college'].unique().tolist())
        selected_college = st.selectbox("🏫 College", colleges, key=f"college_select_{key_suffix}")
    
    with col3:
        if 'scout_grade' in df.columns:
            grades = ['All'] + sorted(df['scout_grade'].unique().tolist(), reverse=True)
            selected_grade = st.selectbox("⭐ Scout Grade", grades, key=f"grade_select_{key_suffix}")
        else:
            selected_grade = 'All'
    
    with col4:
        prob_min = st.slider("🎯 Min Potential", 0.0, 1.0, 0.0, 0.1, key=f"prob_slider_{key_suffix}")
    
    return {
        'position': selected_position,
        'college': selected_college,
        'grade': selected_grade,
        'prob_min': prob_min
    }

def create_search_bar(key_suffix: str = ""):
    """Create search bar component - EXTRAIT DE create_enhanced_search_with_stats"""
    search_term = st.text_input(
        "🔍 Search prospects:", 
        placeholder="Search by name, college, or keywords...",
        help="Search across player names, colleges, and archetypes",
        key=f"search_input_{key_suffix}"
    )
    return search_term

def create_age_range_filter(df: pd.DataFrame, key_suffix: str = ""):
    """Create age range filter"""
    if 'age' not in df.columns:
        return None
    
    min_age = int(df['age'].min())
    max_age = int(df['age'].max())
    
    age_range = st.slider(
        "Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
        key=f"age_range_{key_suffix}"
    )
    
    return age_range

def create_sort_options(key_suffix: str = ""):
    """Create sorting options - EXTRAIT DE create_enhanced_search_with_stats"""
    sort_options = ["Draft Rank", "PPG", "Potential", "Name", "Age"]
    sort_by = st.selectbox(
        "Sort by:",
        sort_options,
        key=f"sort_select_{key_suffix}"
    )
    return sort_by

def create_view_options(key_suffix: str = ""):
    """Create view options for different displays"""
    view_options = ["Top 14 (Lottery)", "Top 30 (First Round)", "Full Draft (60)"]
    view_range = st.selectbox(
        "View Range:",
        view_options,
        key=f"view_range_{key_suffix}"
    )
    return view_range

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply all filters to DataFrame - EXTRAIT ET CONSOLIDÉ DE L'ORIGINAL"""
    filtered_df = df.copy()
    
    # Position filter
    if 'positions' in filters and filters['positions']:
        filtered_df = filtered_df[filtered_df['position'].isin(filters['positions'])]
    
    if 'position' in filters and filters['position'] != 'All':
        filtered_df = filtered_df[filtered_df['position'] == filters['position']]
    
    # College filter
    if 'college' in filters and filters['college'] != 'All':
        filtered_df = filtered_df[filtered_df['college'] == filters['college']]
    
    # Grade filter
    if 'grade' in filters and filters['grade'] != 'All':
        filtered_df = filtered_df[filtered_df['scout_grade'] == filters['grade']]
    
    # Stats filters
    if 'min_ppg' in filters:
        filtered_df = filtered_df[filtered_df['ppg'] >= filters['min_ppg']]
    
    if 'min_3pt' in filters and 'three_pt_pct' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['three_pt_pct'] >= filters['min_3pt']]
    
    if 'min_potential' in filters:
        filtered_df = filtered_df[filtered_df['final_gen_probability'] >= filters['min_potential']]
    
    if 'prob_min' in filters:
        filtered_df = filtered_df[filtered_df['final_gen_probability'] >= filters['prob_min']]
    
    # Age range filter
    if 'age_range' in filters and filters['age_range']:
        min_age, max_age = filters['age_range']
        filtered_df = filtered_df[
            (filtered_df['age'] >= min_age) & 
            (filtered_df['age'] <= max_age)
        ]
    
    # Search term filter - MÊME LOGIQUE QUE L'ORIGINAL
    if 'search_term' in filters and filters['search_term']:
        search_term = filters['search_term'].lower()
        mask = (
            filtered_df['name'].str.lower().str.contains(search_term, na=False) |
            filtered_df['college'].str.lower().str.contains(search_term, na=False) |
            filtered_df['position'].str.lower().str.contains(search_term, na=False)
        )
        if 'archetype' in filtered_df.columns:
            mask |= filtered_df['archetype'].str.lower().str.contains(search_term, na=False)
        
        filtered_df = filtered_df[mask]
    
    return filtered_df

def create_comparison_selectors(df: pd.DataFrame, key_suffix: str = ""):
    """Create player selection for comparisons - EXTRAIT DE create_player_comparison"""
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Select Player 1:", df['name'].tolist(), key=f"comp_p1_{key_suffix}")
    
    with col2:
        available_players = [name for name in df['name'].tolist() if name != player1]
        player2 = st.selectbox("Select Player 2:", available_players, key=f"comp_p2_{key_suffix}")
    
    return player1, player2

def create_team_selector(key_suffix: str = ""):
    """Create team selector for team fit analysis"""
    from config.teams_data import NBA_TEAMS_ANALYSIS
    
    teams = sorted(list(NBA_TEAMS_ANALYSIS.keys()))
    selected_team = st.selectbox("Select Team:", teams, key=f"team_select_{key_suffix}")
    
    return selected_team

def create_historical_era_selector(key_suffix: str = ""):
    """Create historical era selector for What If simulator"""
    eras = {
        2003: "LeBron Era - Athletic Potential Premium",
        2009: "Traditional Big Man Era", 
        2014: "International/Potential Revolution",
        2018: "Pace & Space Revolution",
        2021: "Modern Positionless Era"
    }
    
    selected_year = st.selectbox(
        "Transport 2025 prospects to which historical draft?",
        list(eras.keys()),
        format_func=lambda x: f"{x} - {eras[x]}",
        key=f"era_select_{key_suffix}"

    )

def create_search_filters(df: pd.DataFrame, key_suffix: str = ""):
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_term = create_search_bar(key_suffix)
    
    with col2:
        positions = create_position_filter(key_suffix)
    
    with col3:
        stats_filters = create_basic_stats_filters(key_suffix)
    
    with col4:
        age_range = create_age_range_filter(df, key_suffix)
    
    # Combine all filters
    combined_filters = {
        'search_term': search_term,
        'positions': positions,
        'age_range': age_range,
        **stats_filters
    }
    
    return combined_filters

def create_historical_era_selector(key_suffix: str = ""):
    """Create historical era selector for What If simulator"""
    eras = {
        2003: "LeBron Era - Athletic Potential Premium",
        2009: "Traditional Big Man Era", 
        2014: "International/Potential Revolution",
        2018: "Pace & Space Revolution",
        2021: "Modern Positionless Era"
    }
    
    selected_year = st.selectbox(
        "Transport 2025 prospects to which historical draft?",
        list(eras.keys()),
        format_func=lambda x: f"{x} - {eras[x]}",
        key=f"era_select_{key_suffix}"
    )
    
    return selected_year
    

