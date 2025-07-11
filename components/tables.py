# components/tables.py
"""Tableaux et affichages de données réutilisables"""

import streamlit as st
import pandas as pd
from utils.helpers import safe_numeric, safe_string

def display_search_results_table(df: pd.DataFrame):
    """Display search results in a clean table format - EXTRAIT DE L'ORIGINAL"""
    if len(df) == 0:
        st.info("🔍 No prospects match your search criteria. Try adjusting your filters.")
        return
    
    # Prepare display columns - MÊME LOGIQUE QUE L'ORIGINAL
    display_cols = ['final_rank', 'name', 'position', 'college', 'ppg', 'rpg', 'apg', 
                   'three_pt_pct', 'scout_grade', 'final_gen_probability']
    
    # Check which columns exist
    available_cols = [col for col in display_cols if col in df.columns]
    table_df = df[available_cols].copy()
    
    # Format columns safely - EXTRAIT DE L'ORIGINAL
    if 'three_pt_pct' in table_df.columns:
        table_df['three_pt_pct'] = table_df['three_pt_pct'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    if 'final_gen_probability' in table_df.columns:
        table_df['final_gen_probability'] = table_df['final_gen_probability'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    if 'ppg' in table_df.columns:
        table_df['ppg'] = table_df['ppg'].round(1)
    if 'rpg' in table_df.columns:
        table_df['rpg'] = table_df['rpg'].round(1)
    if 'apg' in table_df.columns:
        table_df['apg'] = table_df['apg'].round(1)
    
    # Rename columns for display - EXTRAIT DE L'ORIGINAL
    column_mapping = {
        'final_rank': 'Rank',
        'name': 'Name',
        'position': 'Pos',
        'college': 'College',
        'ppg': 'PPG',
        'rpg': 'RPG',
        'apg': 'APG',
        'three_pt_pct': '3P%',
        'scout_grade': 'Grade',
        'final_gen_probability': 'Potential'
    }
    
    # Apply renaming only for columns that exist
    rename_dict = {old: new for old, new in column_mapping.items() if old in table_df.columns}
    table_df = table_df.rename(columns=rename_dict)
    
    # Display with enhanced styling - EXTRAIT DE L'ORIGINAL
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d") if "Rank" in table_df.columns else None,
            "PPG": st.column_config.NumberColumn("PPG", format="%.1f") if "PPG" in table_df.columns else None,
            "RPG": st.column_config.NumberColumn("RPG", format="%.1f") if "RPG" in table_df.columns else None,
            "APG": st.column_config.NumberColumn("APG", format="%.1f") if "APG" in table_df.columns else None,
            "Grade": st.column_config.TextColumn("Grade") if "Grade" in table_df.columns else None,
            "Potential": st.column_config.TextColumn("Potential") if "Potential" in table_df.columns else None,
            "3P%": st.column_config.TextColumn("3P%") if "3P%" in table_df.columns else None,
        }
    )

def create_big_board_table(df: pd.DataFrame):
    """Create the main Big Board table - EXTRAIT DE create_big_board_table"""
    # Prepare data for display
    board_data = []
    
    for idx, player in df.iterrows():
        # Extract key info - MÊME LOGIQUE QUE L'ORIGINAL
        rank = int(safe_numeric(player.get('final_rank', idx + 1)))
        name = safe_string(player['name'])
        pos = safe_string(player['position'])
        college = safe_string(player['college'])
        
        # Stats
        ppg = safe_numeric(player['ppg'])
        rpg = safe_numeric(player['rpg'])
        apg = safe_numeric(player['apg'])
        
        # Projections
        grade = safe_string(player['scout_grade'])
        potential = safe_numeric(player.get('final_gen_probability', 0.5))
        
        # Physical
        age = safe_numeric(player.get('age', 0))
        height = f"{safe_numeric(player.get('height', 0)):.1f}" if safe_numeric(player.get('height', 0)) > 0 else "N/A"
        
        # Tier and movement - EXTRAIT DE L'ORIGINAL
        if rank <= 5:
            tier = "🏆 Elite"
        elif rank <= 14:
            tier = "🎰 Lottery"
        elif rank <= 30:
            tier = "🏀 First"
        else:
            tier = "⚡ Second"
        
        board_data.append({
            'Rank': rank,
            'Player': name,
            'Pos': pos,
            'College': college,
            'Age': f"{age:.0f}",
            'Height': height,
            'PPG': f"{ppg:.1f}",
            'RPG': f"{rpg:.1f}",
            'APG': f"{apg:.1f}",
            'Grade': grade,
            'Potential': f"{potential:.0%}",
            'Tier': tier
        })
    
    # Convert to DataFrame
    board_df = pd.DataFrame(board_data)
    
    # Display with custom styling - EXTRAIT DE L'ORIGINAL
    st.dataframe(
        board_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Player": st.column_config.TextColumn("Player", width="large"),
            "Pos": st.column_config.TextColumn("Pos", width="small"),
            "College": st.column_config.TextColumn("College", width="medium"),
            "Age": st.column_config.TextColumn("Age", width="small"),
            "Height": st.column_config.TextColumn("Height", width="small"),
            "PPG": st.column_config.TextColumn("PPG", width="small"),
            "RPG": st.column_config.TextColumn("RPG", width="small"),
            "APG": st.column_config.TextColumn("APG", width="small"),
            "Grade": st.column_config.TextColumn("Grade", width="small"),
            "Potential": st.column_config.TextColumn("Potential", width="small"),
            "Tier": st.column_config.TextColumn("Tier", width="medium")
        }
    )

def create_detailed_comparison_table(p1: pd.Series, p2: pd.Series, name1: str, name2: str):
    """Create detailed comparison tables - EXTRAIT DE L'ORIGINAL"""
    st.markdown("### 📋 Comprehensive Stats Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        basic_stats = pd.DataFrame({
            'Stat': ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
            name1: [
                f"{safe_numeric(p1['ppg']):.1f}",
                f"{safe_numeric(p1['rpg']):.1f}",
                f"{safe_numeric(p1['apg']):.1f}",
                f"{safe_numeric(p1.get('spg', 0)):.1f}",
                f"{safe_numeric(p1.get('bpg', 0)):.1f}"
            ],
            name2: [
                f"{safe_numeric(p2['ppg']):.1f}",
                f"{safe_numeric(p2['rpg']):.1f}",
                f"{safe_numeric(p2['apg']):.1f}",
                f"{safe_numeric(p2.get('spg', 0)):.1f}",
                f"{safe_numeric(p2.get('bpg', 0)):.1f}"
            ]
        })
        st.dataframe(basic_stats, use_container_width=True, hide_index=True)
    
    with col2:
        shooting_stats = pd.DataFrame({
            'Stat': ['FG%', '3P%', 'FT%', 'TS%'],
            name1: [
                f"{safe_numeric(p1.get('fg_pct', 0)):.1%}",
                f"{safe_numeric(p1.get('three_pt_pct', 0)):.1%}",
                f"{safe_numeric(p1.get('ft_pct', 0)):.1%}",
                f"{safe_numeric(p1.get('ts_pct', 0)):.1%}"
            ],
            name2: [
                f"{safe_numeric(p2.get('fg_pct', 0)):.1%}",
                f"{safe_numeric(p2.get('three_pt_pct', 0)):.1%}",
                f"{safe_numeric(p2.get('ft_pct', 0)):.1%}",
                f"{safe_numeric(p2.get('ts_pct', 0)):.1%}"
            ]
        })
        st.dataframe(shooting_stats, use_container_width=True, hide_index=True)
    
    with col3:
        from utils.helpers import format_height
        physical_stats = pd.DataFrame({
            'Stat': ['Age', 'Height', 'Weight', 'Position'],
            name1: [
                f"{safe_numeric(p1.get('age', 0)):.0f}",
                format_height(safe_numeric(p1.get('height', 0))),
                f"{safe_numeric(p1.get('weight', 0)):.0f} lbs",
                safe_string(p1.get('position'))
            ],
            name2: [
                f"{safe_numeric(p2.get('age', 0)):.0f}",
                format_height(safe_numeric(p2.get('height', 0))),
                f"{safe_numeric(p2.get('weight', 0)):.0f} lbs",
                safe_string(p2.get('position'))
            ]
        })
        st.dataframe(physical_stats, use_container_width=True, hide_index=True)

def display_prospects_table(df: pd.DataFrame, num_prospects: int = 20):
    """Display formatted prospects table - EXTRAIT DE L'ORIGINAL"""
    st.markdown("### 📋 Top Prospects")
    
    display_cols = ['name', 'position', 'college', 'ppg', 'rpg', 'apg', 
                   'three_pt_pct', 'scout_grade', 'final_gen_probability']
    
    # Check available columns
    available_cols = [col for col in display_cols if col in df.columns]
    table_df = df[available_cols].head(num_prospects).copy()
    
    # Format columns - MÊME LOGIQUE QUE L'ORIGINAL
    if 'three_pt_pct' in table_df.columns:
        table_df['three_pt_pct'] = table_df['three_pt_pct'].apply(lambda x: f"{x:.1%}")
    if 'final_gen_probability' in table_df.columns:
        table_df['final_gen_probability'] = table_df['final_gen_probability'].apply(lambda x: f"{x:.1%}")
    if 'ppg' in table_df.columns:
        table_df['ppg'] = table_df['ppg'].round(1)
    if 'rpg' in table_df.columns:
        table_df['rpg'] = table_df['rpg'].round(1)
    if 'apg' in table_df.columns:
        table_df['apg'] = table_df['apg'].round(1)
    
    # Rename columns
    table_df.columns = ['Name', 'Pos', 'College', 'PPG', 'RPG', 'APG', '3P%', 'Grade', 'Potential'][:len(table_df.columns)]
    
    st.dataframe(table_df, use_container_width=True, hide_index=True)

def create_historical_validation_table(validation_results: list):
    """Create historical validation table - EXTRAIT DE create_historical_validation"""
    val_df = pd.DataFrame(validation_results)
    
    # Style the dataframe - EXTRAIT DE L'ORIGINAL
    def style_confidence(val):
        if isinstance(val, str) and '%' in val:
            num = float(val.strip('%'))
            if num >= 80:
                return 'background-color: #10B98130'
            elif num >= 60:
                return 'background-color: #F59E0B30'
            else:
                return 'background-color: #EF444430'
        return ''
    
    styled_df = val_df.style.applymap(style_confidence, subset=['Historical Confidence'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

def create_team_fit_results_table(player_fits: list):
    """Create team fit results table"""
    fit_data = []
    for fit in player_fits:
        fit_data.append({
            'Rank': fit['rank'],
            'Player': fit['name'],
            'Position': fit['position'],
            'Fit Score': f"{fit['fit_score']:.0f}%",
            'Key Reasons': ' • '.join(fit['reasons'][:2]) if fit['reasons'] else 'General fit'
        })
    
    fit_df = pd.DataFrame(fit_data)
    
    st.dataframe(
        fit_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Player": st.column_config.TextColumn("Player", width="medium"),
            "Position": st.column_config.TextColumn("Pos", width="small"),
            "Fit Score": st.column_config.TextColumn("Fit Score", width="small"),
            "Key Reasons": st.column_config.TextColumn("Key Reasons", width="large")
        }
    )

def display_quick_actions(df: pd.DataFrame, filename: str = "nba_draft_results.csv"):
    """Display quick actions section - EXTRAIT DE L'ORIGINAL"""
    if len(df) > 0:
        st.markdown("### 🎯 Quick Actions")
        
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Export Results", key="export_results"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=filename,
                        mime="text/csv"
                    )
            
            with col2:
                st.metric("Total Results", len(df))
                
        except Exception as e:
            st.error(f"Error in quick actions: {e}")
            # Fallback simple
            if st.button("💾 Export Results (Simple)", key="export_results_simple"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=filename,
                    mime="text/csv"
                )

