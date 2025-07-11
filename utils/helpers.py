# utils/helpers.py
"""Fonctions utilitaires génériques"""

import pandas as pd
import numpy as np
from typing import Any, Union, Dict, List
from config.settings import GRADE_MAPPING, REVERSE_GRADE_MAPPING, DRAFT_TIERS

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

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format number as percentage"""
    return f"{value:.{decimals}%}"

def format_stat(value: float, decimals: int = 1) -> str:
    """Format statistical value"""
    return f"{value:.{decimals}f}"

def calculate_age_factor(age: float) -> float:
    """Calculate age factor for projections"""
    return 1.0 + max(0, (20 - age) * 0.05)

def validate_dataframe_columns(df: pd.DataFrame, required_columns: list) -> bool:
    """Validate that DataFrame has required columns"""
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return False
    return True

def get_tier_info(rank: int) -> tuple[str, str]:
    """Get tier name and color based on draft rank"""
    for tier_name, tier_data in DRAFT_TIERS.items():
        if tier_data['min'] <= rank <= tier_data['max']:
            return tier_data['name'], tier_data['color']
    return "⚡ Second", "#6B7280"

def calculate_similarity_score(player1: dict, player2: dict, weights: dict = None) -> float:
    """Calculate similarity score between two players"""
    if weights is None:
        weights = {
            'ppg': 0.3, 'rpg': 0.2, 'apg': 0.2,
            'three_pt_pct': 0.15, 'age': 0.15
        }
    
    score = 0.0
    total_weight = 0.0
    
    for stat, weight in weights.items():
        if stat in player1 and stat in player2:
            val1 = safe_numeric(player1[stat])
            val2 = safe_numeric(player2[stat])
            
            # Normalize difference (assuming max reasonable difference)
            max_diff = {
                'ppg': 30, 'rpg': 15, 'apg': 10,
                'three_pt_pct': 0.5, 'age': 5
            }.get(stat, 10)
            
            diff = abs(val1 - val2) / max_diff
            similarity = max(0, 1 - diff)
            score += similarity * weight
            total_weight += weight
    
    return score / total_weight if total_weight > 0 else 0.0

def calculate_draft_grade_average(df: pd.DataFrame) -> str:
    """Calculate average draft grade from letter grades"""
    numeric_grades = []
    for grade in df['scout_grade']:
        grade_clean = safe_string(grade).strip()
        if grade_clean in GRADE_MAPPING:
            numeric_grades.append(GRADE_MAPPING[grade_clean])
        else:
            numeric_grades.append(2.5)  # Default grade
    
    if numeric_grades:
        avg_numeric = sum(numeric_grades) / len(numeric_grades)
        closest_grade = min(REVERSE_GRADE_MAPPING.keys(), 
                           key=lambda x: abs(x - avg_numeric))
        return REVERSE_GRADE_MAPPING[closest_grade]
    
    return "B"

def get_performance_tier(value: float, thresholds: Dict[str, float]) -> str:
    """Get performance tier based on value and thresholds"""
    if value >= thresholds.get('elite', 0.8):
        return 'Elite'
    elif value >= thresholds.get('good', 0.6):
        return 'Good'
    elif value >= thresholds.get('average', 0.4):
        return 'Average'
    else:
        return 'Below Average'

def calculate_overall_impact(player_stats: Dict[str, float]) -> float:
    """Calculate overall impact score from player stats"""
    weights = {
        'ppg': 0.25, 'rpg': 0.15, 'apg': 0.20,
        'three_pt_pct': 0.15, 'ts_pct': 0.10,
        'final_gen_probability': 0.15
    }
    
    impact_score = 0.0
    for stat, weight in weights.items():
        if stat in player_stats:
            value = safe_numeric(player_stats[stat])
            # Normalize different stats to same scale
            if stat == 'ppg':
                normalized = min(value / 30, 1.0)
            elif stat in ['rpg', 'apg']:
                normalized = min(value / 12, 1.0)
            elif stat in ['three_pt_pct', 'ts_pct']:
                normalized = min(value / 0.6, 1.0)
            else:  # final_gen_probability
                normalized = value
            
            impact_score += normalized * weight
    
    return impact_score

def get_position_group(position: str) -> str:
    """Get position group from individual position"""
    position_groups = {
        'PG': 'Guards',
        'SG': 'Guards', 
        'SF': 'Wings',
        'PF': 'Forwards',
        'C': 'Bigs'
    }
    return position_groups.get(position, 'Unknown')
