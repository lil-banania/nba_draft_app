# utils/data_utils.py
"""Utilitaires pour le traitement des données"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Any
from datetime import datetime, date

def safe_numeric(value: Any, default: float = 0.0) -> float:
    """Convert value to float safely"""
    try:
        if pd.isna(value) or value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return default

def safe_string(value: Any, default: str = 'N/A') -> str:
    """Convert value to string safely"""
    try:
        if pd.isna(value) or value is None:
            return default
        return str(value)
    except (ValueError, TypeError, AttributeError):
        return default

def format_height(height_decimal: float) -> str:
    """Convert decimal height to feet'inches format"""
    if height_decimal == 0:
        return "N/A"
    feet = int(height_decimal)
    inches = int((height_decimal - feet) * 12)
    return f"{feet}'{inches}\""

def calculate_draft_grade_average(df: pd.DataFrame) -> str:
    """Calculate average draft grade from letter grades"""
    
    # Mapping des grades vers des valeurs numériques
    grade_mapping = {
        'A+': 4.3,
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'D-': 0.7,
        'F': 0.0
    }
    
    # Mapping inverse pour reconvertir en lettres
    reverse_mapping = {
        4.3: 'A+', 4.0: 'A', 3.7: 'A-',
        3.3: 'B+', 3.0: 'B', 2.7: 'B-',
        2.3: 'C+', 2.0: 'C', 1.7: 'C-',
        1.3: 'D+', 1.0: 'D', 0.7: 'D-',
        0.0: 'F'
    }
    
    # Convertir les grades en valeurs numériques
    numeric_grades = []
    for grade in df['scout_grade']:
        grade_clean = safe_string(grade).strip()
        if grade_clean in grade_mapping:
            numeric_grades.append(grade_mapping[grade_clean])
        else:
            # Grade par défaut si non reconnu
            numeric_grades.append(2.5)  # Équivalent à un "C+"
    
    # Calculer la moyenne
    if numeric_grades:
        avg_numeric = sum(numeric_grades) / len(numeric_grades)
        
        # Trouver le grade le plus proche
        closest_grade = min(reverse_mapping.keys(), key=lambda x: abs(x - avg_numeric))
        return reverse_mapping[closest_grade]
    
    return "B"  # Grade par défaut

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and clean NBA draft data"""
    try:
        # Try loading from multiple possible sources
        for filename in ['nba_prospects_2025.csv', 'complete_nba_draft_rankings.csv']:
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
    """Create comprehensive demo data with 60 prospects"""
    # Top prospects with realistic stats
    top_prospects = [
        {'name': 'Cooper Flagg', 'position': 'PF', 'college': 'Duke', 'ppg': 16.5, 'rpg': 8.2, 'apg': 4.1, 'spg': 1.8, 'bpg': 1.4, 'fg_pct': 0.478, 'three_pt_pct': 0.352, 'ft_pct': 0.765, 'ts_pct': 0.589, 'age': 18.0, 'height': 6.9, 'weight': 220, 'usage_rate': 22.5, 'ortg': 115, 'drtg': 98, 'scout_grade': 'A+', 'archetype': 'Two-Way Wing'},
        {'name': 'Ace Bailey', 'position': 'SF', 'college': 'Rutgers', 'ppg': 15.8, 'rpg': 6.1, 'apg': 2.3, 'spg': 1.2, 'bpg': 0.8, 'fg_pct': 0.445, 'three_pt_pct': 0.385, 'ft_pct': 0.825, 'ts_pct': 0.612, 'age': 18.0, 'height': 6.8, 'weight': 200, 'usage_rate': 28.2, 'ortg': 118, 'drtg': 105, 'scout_grade': 'A+', 'archetype': 'Elite Scorer'},
        {'name': 'Dylan Harper', 'position': 'SG', 'college': 'Rutgers', 'ppg': 19.2, 'rpg': 4.8, 'apg': 4.6, 'spg': 1.6, 'bpg': 0.3, 'fg_pct': 0.512, 'three_pt_pct': 0.345, 'ft_pct': 0.792, 'ts_pct': 0.595, 'age': 19.0, 'height': 6.6, 'weight': 195, 'usage_rate': 25.8, 'ortg': 112, 'drtg': 102, 'scout_grade': 'A+', 'archetype': 'Versatile Guard'},
        {'name': 'VJ Edgecombe', 'position': 'SG', 'college': 'Baylor', 'ppg': 12.1, 'rpg': 4.9, 'apg': 2.8, 'spg': 1.9, 'bpg': 0.6, 'fg_pct': 0.432, 'three_pt_pct': 0.298, 'ft_pct': 0.712, 'ts_pct': 0.501, 'age': 19.0, 'height': 6.5, 'weight': 180, 'usage_rate': 19.5, 'ortg': 105, 'drtg': 95, 'scout_grade': 'A', 'archetype': 'Athletic Defender'},
        {'name': 'Boogie Fland', 'position': 'PG', 'college': 'Arkansas', 'ppg': 14.6, 'rpg': 3.2, 'apg': 5.1, 'spg': 1.4, 'bpg': 0.2, 'fg_pct': 0.465, 'three_pt_pct': 0.368, 'ft_pct': 0.856, 'ts_pct': 0.578, 'age': 18.0, 'height': 6.2, 'weight': 175, 'usage_rate': 24.1, 'ortg': 114, 'drtg': 108, 'scout_grade': 'A', 'archetype': 'Floor General'},
    ]
    
    # Generate remaining prospects
    all_prospects = top_prospects.copy()
    
    for i in range(6, 61):
        prospect = {
            'name': f'Prospect {i}',
            'position': np.random.choice(['PG', 'SG', 'SF', 'PF', 'C']),
            'college': np.random.choice(['Duke', 'Kentucky', 'UNC', 'Kansas', 'UCLA', 'Arizona']),
            'ppg': np.random.normal(12, 4),
            'rpg': np.random.normal(5, 2),
            'apg': np.random.normal(3, 2),
            'spg': np.random.normal(1.2, 0.5),
            'bpg': np.random.normal(0.8, 0.6),
            'fg_pct': np.random.normal(0.45, 0.08),
            'three_pt_pct': np.random.normal(0.35, 0.10),
            'ft_pct': np.random.normal(0.75, 0.12),
            'ts_pct': np.random.normal(0.55, 0.08),
            'age': np.random.normal(19, 1.2),
            'height': np.random.normal(6.5, 0.5),
            'weight': np.random.normal(200, 25),
            'usage_rate': np.random.normal(22, 5),
            'ortg': np.random.normal(110, 8),
            'drtg': np.random.normal(105, 7),
            'scout_grade': np.random.choice(['B', 'B-', 'C+', 'C']),
            'archetype': np.random.choice(['Shooter', 'Defender', 'Athlete', 'Role Player'])
        }
        all_prospects.append(prospect)
    
    df = pd.DataFrame(all_prospects)
    df['final_gen_probability'] = np.random.beta(2, 3, len(df))
    df['final_rank'] = range(1, len(df) + 1)
    
    return clean_dataframe(df)

def calculate_days_until_draft() -> int:
    """Calculate days until draft day"""
    draft_date = date(2025, 6, 26)
    today = date.today()
    return (draft_date - today).days

def validate_dataframe(df: pd.DataFrame) -> bool:
    """Validate that dataframe has required columns"""
    required_cols = ['name', 'position', 'college', 'ppg', 'rpg', 'apg', 'final_rank']
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
        return False
    
    return True

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format float as percentage"""
    try:
        return f"{value:.{decimals}%}"
    except:
        return "N/A"

def format_stat(value: float, decimals: int = 1) -> str:
    """Format stat with proper decimals"""
    try:
        return f"{value:.{decimals}f}"
    except:
        return "N/A"

def calculate_age_at_draft(birthdate: str) -> float:
    """Calculate age at draft day"""
    try:
        birth = datetime.strptime(birthdate, "%Y-%m-%d").date()
        draft_date = date(2025, 6, 26)
        age = (draft_date - birth).days / 365.25
        return age
    except:
        return 20.0  # Default age
