# pages/search.py
"""Page de recherche avancée avec composants modulaires"""

import streamlit as st
import pandas as pd
from components.filters import create_search_filters, apply_filters, create_sort_options
from components.tables import display_search_results_table  # ✅ CORRIGÉ
from components.charts import create_position_distribution_chart
from utils.helpers import safe_numeric, safe_string

def show(df: pd.DataFrame):
    """Display enhanced search page"""
    st.markdown("## 🔍 Player Database")
    st.caption("Advanced search and filtering system")
    
    # Search and filter section
    filtered_df = create_search_section(df)
    
    # Results summary
    display_results_summary(filtered_df, df)
    
    # Quick statistics for filtered results
    if len(filtered_df) > 0:
        display_filtered_stats(filtered_df)
    
    # Main results table
    display_search_results_table(filtered_df.head(50))  # Limit to 50 results
    
    # Quick actions
    display_search_actions(filtered_df)

def create_search_section(df: pd.DataFrame) -> pd.DataFrame:
    """Create comprehensive search section"""
    st.markdown("### 🔍 Search & Filter")
    
    # Main search bar
    search_term = st.text_input(
        "Search prospects:", 
        placeholder="Search by name, college, or keywords...",
        help="Search across player names, colleges, and archetypes"
    )
    
    # Advanced filters in expandable section
    with st.expander("🔧 Advanced Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Position filter
            st.markdown("**Positions:**")
            positions = ['PG', 'SG', 'SF', 'PF', 'C']
            selected_positions = st.multiselect(
                "Select positions:",
                positions,
                default=positions,
                key="search_positions"
            )
        
        with col2:
            # Stats filters
            st.markdown("**Performance:**")
            min_ppg = st.slider("Min PPG", 0, 30, 0, key="search_ppg")
            min_3pt = st.slider("Min 3P%", 0.0, 0.6, 0.0, 0.05, key="search_3pt")
        
        with col3:
            # College and grade filters
            st.markdown("**Background:**")
            colleges = ['All'] + sorted(df['college'].unique().tolist())
            selected_college = st.selectbox("College", colleges, key="search_college")
            
            if 'scout_grade' in df.columns:
                grades = ['All'] + sorted(df['scout_grade'].unique().tolist(), reverse=True)
                selected_grade = st.selectbox("Scout Grade", grades, key="search_grade")
            else:
                selected_grade = 'All'
        
        with col4:
            # Potential and age
            st.markdown("**Projection:**")
            min_potential = st.slider("Min Potential", 0.0, 1.0, 0.0, 0.1, key="search_potential")
            
            if 'age' in df.columns:
                min_age = int(df['age'].min())
                max_age = int(df['age'].max())
                age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age), key="search_age")
            else:
                age_range = None
    
    # Apply all filters
    filtered_df = df.copy()
    
    # Search term filter
    if search_term:
        mask = (
            filtered_df['name'].str.contains(search_term, case=False, na=False) |
            filtered_df['college'].str.contains(search_term, case=False, na=False) |
            filtered_df['position'].str.contains(search_term, case=False, na=False)
        )
        if 'archetype' in filtered_df.columns:
            mask |= filtered_df['archetype'].str.contains(search_term, case=False, na=False)
        filtered_df = filtered_df[mask]
    
    # Position filter
    if selected_positions:
        filtered_df = filtered_df[filtered_df['position'].isin(selected_positions)]
    
    # Stats filters
    filtered_df = filtered_df[filtered_df['ppg'] >= min_ppg]
    if 'three_pt_pct' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['three_pt_pct'] >= min_3pt]
    
    # College filter
    if selected_college != 'All':
        filtered_df = filtered_df[filtered_df['college'] == selected_college]
    
    # Grade filter
    if selected_grade != 'All' and 'scout_grade' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['scout_grade'] == selected_grade]
    
    # Potential filter
    filtered_df = filtered_df[filtered_df['final_gen_probability'] >= min_potential]
    
    # Age filter
    if age_range and 'age' in filtered_df.columns:
        min_age_sel, max_age_sel = age_range
        filtered_df = filtered_df[
            (filtered_df['age'] >= min_age_sel) & 
            (filtered_df['age'] <= max_age_sel)
        ]
    
    return filtered_df

def display_results_summary(filtered_df: pd.DataFrame, original_df: pd.DataFrame):
    """Display search results summary"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Results Found", len(filtered_df), f"of {len(original_df)} total")
    
    with col2:
        if len(filtered_df) > 0:
            sort_by = st.selectbox(
                "Sort by:",
                ["Draft Rank", "PPG", "Potential", "Name", "Age"],
                key="search_sort"
            )
            
            # Apply sorting
            if sort_by == "Draft Rank":
                filtered_df = filtered_df.sort_values('final_rank')
            elif sort_by == "PPG":
                filtered_df = filtered_df.sort_values('ppg', ascending=False)
            elif sort_by == "Potential":
                filtered_df = filtered_df.sort_values('final_gen_probability', ascending=False)
            elif sort_by == "Name":
                filtered_df = filtered_df.sort_values('name')
            elif sort_by == "Age":
                filtered_df = filtered_df.sort_values('age')
    
    with col3:
        if len(filtered_df) > 0:
            avg_potential = filtered_df['final_gen_probability'].mean()
            st.metric("Avg Potential", f"{avg_potential:.1%}")

def display_filtered_stats(df: pd.DataFrame):
    """Display quick statistics for filtered results"""
    if len(df) == 0:
        return
    
    st.markdown("### 📊 Filtered Results Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Position breakdown chart
        if len(df) > 0 and 'position' in df.columns:
            fig = create_position_distribution_chart(df)
            if fig:
                fig.update_layout(title="Position Distribution (Filtered)", height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Key statistics
        st.markdown("#### 📈 Key Stats")
        
        if len(df) > 0:
            stats_data = {
                "Metric": ["Top Scorer", "Best Potential", "Youngest", "Most Experienced"],
                "Player": [
                    df.loc[df['ppg'].idxmax(), 'name'] if 'ppg' in df.columns else 'N/A',
                    df.loc[df['final_gen_probability'].idxmax(), 'name'],
                    df.loc[df['age'].idxmin(), 'name'] if 'age' in df.columns else 'N/A',
                    df.loc[df['age'].idxmax(), 'name'] if 'age' in df.columns else 'N/A'
                ],
                "Value": [
                    f"{df['ppg'].max():.1f} PPG" if 'ppg' in df.columns else 'N/A',
                    f"{df['final_gen_probability'].max():.1%}",
                    f"{df['age'].min():.0f} years" if 'age' in df.columns else 'N/A',
                    f"{df['age'].max():.0f} years" if 'age' in df.columns else 'N/A'
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)

def display_search_actions(df: pd.DataFrame):
    """Display search actions and export options"""
    if len(df) > 0:
        st.markdown("### 🎯 Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Export Results"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="nba_draft_search_results.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🔄 Reset Filters"):
                st.rerun()
        
        with col3:
            st.metric("Export Ready", f"{len(df)} prospects")
