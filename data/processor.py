# data/processor.py
"""Traitement et nettoyage des données"""

import pandas as pd
import numpy as np
from config.settings import DATA_COLUMNS
from utils.helpers import safe_numeric, safe_string

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe with proper type conversions"""
    df_clean = df.copy()
    
    # Clean numeric columns
    for col in DATA_COLUMNS['numeric']:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
    
    # Clean string columns
    for col in DATA_COLUMNS['string']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).fillna('N/A')
    
    # Additional cleaning
    df_clean = validate_data_ranges(df_clean)
    df_clean = add_calculated_columns(df_clean)
    
    return df_clean

def validate_data_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and cap data ranges to realistic values"""
    df_validated = df.copy()
    
    # Cap statistical values to realistic ranges
    stat_caps = {
        'ppg': (0, 50),
        'rpg': (0, 20),
        'apg': (0, 15),
        'spg': (0, 5),
        'bpg': (0, 5),
        'fg_pct': (0, 1),
        'three_pt_pct': (0, 1),
        'ft_pct': (0, 1),
        'ts_pct': (0, 1),
        'age': (16, 25),
        'height': (5.5, 8.0),
        'weight': (150, 350),
        'usage_rate': (0, 50),
        'final_gen_probability': (0, 1)
    }
    
    for col, (min_val, max_val) in stat_caps.items():
        if col in df_validated.columns:
            df_validated[col] = df_validated[col].clip(min_val, max_val)
    
    return df_validated

def add_calculated_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add calculated columns for enhanced analysis"""
    df_calc = df.copy()
    
    # Add efficiency metrics
    if 'ppg' in df_calc.columns and 'usage_rate' in df_calc.columns:
        df_calc['scoring_efficiency'] = df_calc['ppg'] / (df_calc['usage_rate'] + 1) * 100
    
    # Add versatility score
    if all(col in df_calc.columns for col in ['ppg', 'rpg', 'apg']):
        df_calc['versatility_score'] = (
            df_calc['ppg'] * 0.4 + 
            df_calc['rpg'] * 0.3 + 
            df_calc['apg'] * 0.3
        )
    
    # Add defensive impact
    if all(col in df_calc.columns for col in ['spg', 'bpg']):
        df_calc['defensive_impact'] = df_calc['spg'] + df_calc['bpg']
    
    # Add age-adjusted potential
    if all(col in df_calc.columns for col in ['final_gen_probability', 'age']):
        age_factor = 1 + (22 - df_calc['age']) * 0.05
        df_calc['age_adjusted_potential'] = (
            df_calc['final_gen_probability'] * age_factor
        ).clip(0, 1)
    
    # Add shooting grade
    if 'three_pt_pct' in df_calc.columns:
        df_calc['shooting_grade'] = pd.cut(
            df_calc['three_pt_pct'],
            bins=[0, 0.25, 0.33, 0.38, 0.45, 1.0],
            labels=['Poor', 'Below Avg', 'Average', 'Good', 'Elite'],
            include_lowest=True
        )
    
    return df_calc

def filter_prospects(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply filters to prospects DataFrame"""
    filtered_df = df.copy()
    
    # Position filter
    if 'positions' in filters and filters['positions']:
        filtered_df = filtered_df[filtered_df['position'].isin(filters['positions'])]
    
    # Age range filter
    if 'age_range' in filters:
        min_age, max_age = filters['age_range']
        filtered_df = filtered_df[
            (filtered_df['age'] >= min_age) & 
            (filtered_df['age'] <= max_age)
        ]
    
    # Stats filters
    stat_filters = {
        'min_ppg': 'ppg',
        'min_rpg': 'rpg', 
        'min_apg': 'apg',
        'min_3pt': 'three_pt_pct',
        'min_potential': 'final_gen_probability'
    }
    
    for filter_key, column in stat_filters.items():
        if filter_key in filters and column in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[column] >= filters[filter_key]]
    
    # College filter
    if 'colleges' in filters and filters['colleges']:
        filtered_df = filtered_df[filtered_df['college'].isin(filters['colleges'])]
    
    # Grade filter
    if 'grades' in filters and filters['grades']:
        filtered_df = filtered_df[filtered_df['scout_grade'].isin(filters['grades'])]
    
    # Search term filter
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

def sort_prospects(df: pd.DataFrame, sort_by: str, ascending: bool = True) -> pd.DataFrame:
    """Sort prospects by specified criteria"""
    if sort_by not in df.columns:
        return df
    
    return df.sort_values(sort_by, ascending=ascending).reset_index(drop=True)

def get_prospect_summary_stats(df: pd.DataFrame) -> dict:
    """Get summary statistics for prospects"""
    summary = {}
    
    if not df.empty:
        numeric_columns = ['ppg', 'rpg', 'apg', 'three_pt_pct', 'age', 'final_gen_probability']
        
        for col in numeric_columns:
            if col in df.columns:
                summary[col] = {
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max()
                }
        
        # Categorical summaries
        if 'position' in df.columns:
            summary['position_counts'] = df['position'].value_counts().to_dict()
        
        if 'college' in df.columns:
            summary['top_colleges'] = df['college'].value_counts().head(10).to_dict()
        
        if 'scout_grade' in df.columns:
            summary['grade_distribution'] = df['scout_grade'].value_counts().to_dict()
    
    return summary

def identify_outliers(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """Identify statistical outliers in the dataset"""
    if columns is None:
        columns = ['ppg', 'rpg', 'apg', 'three_pt_pct', 'final_gen_probability']
    
    outliers = df.copy()
    outliers['is_outlier'] = False
    outliers['outlier_reasons'] = ''
    
    for col in columns:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            col_outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            outliers.loc[col_outliers, 'is_outlier'] = True
            
            # Add reason for outlier
            high_outliers = df[col] > upper_bound
            low_outliers = df[col] < lower_bound
            
            outliers.loc[high_outliers, 'outlier_reasons'] += f'High {col}, '
            outliers.loc[low_outliers, 'outlier_reasons'] += f'Low {col}, '
    
    # Clean up outlier reasons
    outliers['outlier_reasons'] = outliers['outlier_reasons'].str.rstrip(', ')
    
    return outliers[outliers['is_outlier'] == True]

def prepare_display_dataframe(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """Prepare DataFrame for display with proper formatting"""
    if columns is None:
        columns = DATA_COLUMNS['display']
    
    # Select available columns
    available_columns = [col for col in columns if col in df.columns]
    display_df = df[available_columns].copy()
    
    # Format numeric columns
    format_mapping = {
        'ppg': '{:.1f}',
        'rpg': '{:.1f}',
        'apg': '{:.1f}',
        'spg': '{:.1f}',
        'bpg': '{:.1f}',
        'three_pt_pct': '{:.1%}',
        'fg_pct': '{:.1%}',
        'ft_pct': '{:.1%}',
        'ts_pct': '{:.1%}',
        'final_gen_probability': '{:.1%}',
        'age': '{:.0f}',
        'height': '{:.1f}',
        'weight': '{:.0f}'
    }
    
    for col, fmt in format_mapping.items():
        if col in display_df.columns:
            if col.endswith('_pct') or col == 'final_gen_probability':
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1%}")
            elif col in ['age', 'weight', 'final_rank']:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.0f}")
            else:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}")
    
    return display_df
