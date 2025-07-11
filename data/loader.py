# data/loader.py
"""Chargement des données - Version simplifiée"""

import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and clean NBA draft data with caching"""
    try:
        # Try loading from multiple possible sources
        filenames = [
            'complete_nba_draft_rankings.csv', 
            'final_nba_draft_rankings.csv', 
            'ml_nba_draft_predictions.csv'
        ]
        
        for filename in filenames:
            try:
                df = pd.read_csv(filename)
                st.success(f"✅ Data loaded from {filename}")
                return clean_dataframe(df)
            except FileNotFoundError:
                continue
        
        # If no file found, create demo data
        st.info("📋 Using demonstration data")
        return create_demo_data()
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return create_demo_data()

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe with proper type conversions"""
    df_clean = df.copy()
    
    # Numeric columns
    numeric_cols = ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'age', 'final_rank', 
                   'final_gen_probability', 'fg_pct', 'three_pt_pct', 'ft_pct', 
                   'ts_pct', 'height', 'weight', 'usage_rate', 'ortg', 'drtg']
    
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
    
    # String columns
    string_cols = ['name', 'position', 'college', 'scout_grade', 'archetype']
    
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).fillna('N/A')
    
    return df_clean

def create_demo_data() -> pd.DataFrame:
    """Create demo data for testing"""
    # Top prospects avec données réalistes
    prospects = []
    
    # Top 5 réalistes
    top_5 = [
        {'name': 'Cooper Flagg', 'position': 'PF', 'college': 'Duke', 'ppg': 16.5, 'rpg': 8.2, 'apg': 4.1, 'scout_grade': 'A+', 'archetype': 'Two-Way Wing'},
        {'name': 'Ace Bailey', 'position': 'SF', 'college': 'Rutgers', 'ppg': 15.8, 'rpg': 6.1, 'apg': 2.3, 'scout_grade': 'A+', 'archetype': 'Elite Scorer'},
        {'name': 'Dylan Harper', 'position': 'SG', 'college': 'Rutgers', 'ppg': 19.2, 'rpg': 4.8, 'apg': 4.6, 'scout_grade': 'A+', 'archetype': 'Versatile Guard'},
        {'name': 'VJ Edgecombe', 'position': 'SG', 'college': 'Baylor', 'ppg': 12.1, 'rpg': 4.9, 'apg': 2.8, 'scout_grade': 'A', 'archetype': 'Athletic Defender'},
        {'name': 'Boogie Fland', 'position': 'PG', 'college': 'Arkansas', 'ppg': 14.6, 'rpg': 3.2, 'apg': 5.1, 'scout_grade': 'A', 'archetype': 'Floor General'}
    ]
    
    prospects.extend(top_5)
    
    # Ajouter 25 prospects générés
    colleges = ['Duke', 'Kentucky', 'UNC', 'Kansas', 'UCLA', 'Arizona', 'Gonzaga', 'Michigan', 'Texas', 'Auburn']
    positions = ['PG', 'SG', 'SF', 'PF', 'C']
    grades = ['A-', 'B+', 'B', 'B-', 'C+', 'C']
    archetypes = ['Scorer', 'Shooter', 'Defender', 'Playmaker', 'Athlete', 'Role Player']
    
    for i in range(5, 30):
        prospect = {
            'name': f'Prospect {i+1}',
            'position': np.random.choice(positions),
            'college': np.random.choice(colleges),
            'ppg': max(5, np.random.normal(12, 4)),
            'rpg': max(1, np.random.normal(5, 2)),
            'apg': max(0.5, np.random.normal(3, 2)),
            'spg': max(0.3, np.random.normal(1.2, 0.5)),
            'bpg': max(0, np.random.normal(0.8, 0.6)),
            'three_pt_pct': np.clip(np.random.normal(0.35, 0.10), 0.15, 0.55),
            'fg_pct': np.clip(np.random.normal(0.45, 0.08), 0.25, 0.65),
            'ft_pct': np.clip(np.random.normal(0.75, 0.12), 0.50, 0.95),
            'ts_pct': np.clip(np.random.normal(0.55, 0.08), 0.40, 0.70),
            'age': np.clip(np.random.normal(19.5, 1.2), 18, 23),
            'height': np.clip(np.random.normal(6.5, 0.5), 5.8, 7.2),
            'weight': np.clip(np.random.normal(200, 25), 160, 280),
            'scout_grade': np.random.choice(grades),
            'archetype': np.random.choice(archetypes)
        }
        prospects.append(prospect)
    
    df = pd.DataFrame(prospects)
    
    # Ajouter colonnes calculées
    df['final_rank'] = range(1, len(df) + 1)
    df['final_gen_probability'] = np.random.beta(2, 3, len(df))
    
    # Ajuster les probabilités pour les top prospects
    df.loc[:4, 'final_gen_probability'] = np.random.uniform(0.75, 0.95, 5)
    
    return clean_dataframe(df)

def validate_data(df: pd.DataFrame) -> bool:
    """Validate loaded data"""
    if df is None or df.empty:
        return False
    required_cols = ['name', 'position', 'ppg', 'final_rank']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.warning(f"Missing required columns: {missing_cols}")
        return False
    return True
