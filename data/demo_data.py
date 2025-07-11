# data/demo_data.py
"""Génération de données de démonstration pour l'application"""

import pandas as pd
import numpy as np
from data.processor import clean_dataframe

def create_demo_data() -> pd.DataFrame:
    """Create comprehensive demo data with 60 prospects"""
    
    # Top 5 prospects avec des données réalistes
    top_prospects = [
        {
            'name': 'Cooper Flagg', 'position': 'PF', 'college': 'Duke', 
            'ppg': 16.5, 'rpg': 8.2, 'apg': 4.1, 'spg': 1.8, 'bpg': 1.4,
            'fg_pct': 0.478, 'three_pt_pct': 0.352, 'ft_pct': 0.765, 'ts_pct': 0.589,
            'age': 18.0, 'height': 6.9, 'weight': 220, 'usage_rate': 22.5,
            'ortg': 115, 'drtg': 98, 'scout_grade': 'A+', 'archetype': 'Two-Way Wing'
        },
        {
            'name': 'Ace Bailey', 'position': 'SF', 'college': 'Rutgers',
            'ppg': 15.8, 'rpg': 6.1, 'apg': 2.3, 'spg': 1.2, 'bpg': 0.8,
            'fg_pct': 0.445, 'three_pt_pct': 0.385, 'ft_pct': 0.825, 'ts_pct': 0.612,
            'age': 18.0, 'height': 6.8, 'weight': 200, 'usage_rate': 28.2,
            'ortg': 118, 'drtg': 105, 'scout_grade': 'A+', 'archetype': 'Elite Scorer'
        },
        {
            'name': 'Dylan Harper', 'position': 'SG', 'college': 'Rutgers',
            'ppg': 19.2, 'rpg': 4.8, 'apg': 4.6, 'spg': 1.6, 'bpg': 0.3,
            'fg_pct': 0.512, 'three_pt_pct': 0.345, 'ft_pct': 0.792, 'ts_pct': 0.595,
            'age': 19.0, 'height': 6.6, 'weight': 195, 'usage_rate': 25.8,
            'ortg': 112, 'drtg': 102, 'scout_grade': 'A+', 'archetype': 'Versatile Guard'
        },
        {
            'name': 'VJ Edgecombe', 'position': 'SG', 'college': 'Baylor',
            'ppg': 12.1, 'rpg': 4.9, 'apg': 2.8, 'spg': 1.9, 'bpg': 0.6,
            'fg_pct': 0.432, 'three_pt_pct': 0.298, 'ft_pct': 0.712, 'ts_pct': 0.501,
            'age': 19.0, 'height': 6.5, 'weight': 180, 'usage_rate': 19.5,
            'ortg': 105, 'drtg': 95, 'scout_grade': 'A', 'archetype': 'Athletic Defender'
        },
        {
            'name': 'Boogie Fland', 'position': 'PG', 'college': 'Arkansas',
            'ppg': 14.6, 'rpg': 3.2, 'apg': 5.1, 'spg': 1.4, 'bpg': 0.2,
            'fg_pct': 0.465, 'three_pt_pct': 0.368, 'ft_pct': 0.856, 'ts_pct': 0.578,
            'age': 18.0, 'height': 6.2, 'weight': 175, 'usage_rate': 24.1,
            'ortg': 114, 'drtg': 108, 'scout_grade': 'A', 'archetype': 'Floor General'
        }
    ]
    
    # Générer les prospects restants (6-60)
    all_prospects = top_prospects.copy()
    
    # Noms réalistes pour les prospects générés
    prospect_names = [
        'Tre Johnson', 'Jeremiah Fears', 'Noa Essengue', 'Kasparas Jakucionis', 'Kon Knueppel',
        'Khaman Maluach', 'Collin Murray-Boyles', 'Derik Queen', 'Asa Newell', 'Liam McNeeley',
        'Cedric Coward', 'Carter Bryant', 'Egor Demin', 'Will Riley', 'Jase Richardson',
        'Rasheer Fleming', 'Nique Clifford', 'Maxime Raynaud', 'Walter Clayton Jr', 'Thomas Sorber',
        'Joan Beringer', 'Drake Powell', 'Nolan Traore', 'Danny Wolf', 'Noah Penda',
        'Ben Saraf', 'Alex Johnson', 'Marcus Williams', 'James Davis', 'Michael Brown',
        'David Wilson', 'Chris Miller', 'Anthony Garcia', 'Tyler Martinez', 'Jason Rodriguez',
        'Kevin Lewis', 'Brian Walker', 'Daniel Hall', 'Ryan Young', 'Justin Allen',
        'Brandon King', 'Cameron Wright', 'Jordan Lopez', 'Austin Hill', 'Trevor Green',
        'Sean Adams', 'Nathan Baker', 'Caleb Nelson', 'Lucas Carter', 'Mason Mitchell',
        'Owen Perez', 'Ethan Roberts', 'Noah Turner', 'Liam Phillips', 'William Campbell',
        'Jacob Parker', 'Alexander Evans', 'Benjamin Edwards', 'Samuel Collins'
    ]
    
    # Colleges variés
    colleges = [
        'Duke', 'Kentucky', 'UNC', 'Kansas', 'UCLA', 'Arizona', 'Gonzaga', 'Villanova',
        'Michigan State', 'Syracuse', 'Florida', 'Texas', 'Arkansas', 'Auburn', 'Alabama',
        'Tennessee', 'LSU', 'Georgia', 'South Carolina', 'Virginia', 'Virginia Tech',
        'Wake Forest', 'NC State', 'Miami', 'Georgia Tech', 'Clemson', 'Louisville',
        'Pittsburgh', 'Boston College', 'Notre Dame', 'Marquette', 'Creighton', 'Xavier',
        'Butler', 'Providence', 'St. John\'s', 'Seton Hall', 'DePaul', 'Georgetown'
    ]
    
    # Archétypes variés
    archetypes = [
        'Elite Scorer', 'Floor General', 'Two-Way Wing', 'Athletic Defender', 'Elite Shooter',
        'Rim Protector', 'Stretch Big', 'Point Forward', 'Combo Guard', 'Role Player',
        'Energy Big', 'Defensive Specialist', 'Shooter', 'Playmaker', 'Athlete'
    ]
    
    # Grades variés avec distribution réaliste
    grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D']
    grade_weights = [0.02, 0.05, 0.08, 0.12, 0.18, 0.20, 0.15, 0.10, 0.07, 0.02, 0.01]
    
    # Générer prospects 6-60
    for i in range(55):  # 55 prospects supplémentaires
        # Décliner graduellement les stats en fonction du rang
        rank_factor = max(0.3, 1.0 - (i / 60))  # Facteur de déclin
        
        prospect = {
            'name': prospect_names[i] if i < len(prospect_names) else f'Prospect {i+6}',
            'position': np.random.choice(['PG', 'SG', 'SF', 'PF', 'C'], 
                                       p=[0.15, 0.25, 0.25, 0.20, 0.15]),
            'college': np.random.choice(colleges),
            'ppg': max(3, np.random.normal(12 * rank_factor, 4)),
            'rpg': max(1, np.random.normal(5 * rank_factor, 2)),
            'apg': max(0.5, np.random.normal(3 * rank_factor, 2)),
            'spg': max(0.2, np.random.normal(1.2 * rank_factor, 0.5)),
            'bpg': max(0, np.random.normal(0.8 * rank_factor, 0.6)),
            'fg_pct': np.clip(np.random.normal(0.45 * rank_factor, 0.08), 0.25, 0.65),
            'three_pt_pct': np.clip(np.random.normal(0.35 * rank_factor, 0.10), 0.15, 0.55),
            'ft_pct': np.clip(np.random.normal(0.75, 0.12), 0.50, 0.95),
            'ts_pct': np.clip(np.random.normal(0.55 * rank_factor, 0.08), 0.40, 0.70),
            'age': np.clip(np.random.normal(19.5, 1.2), 18, 23),
            'height': np.clip(np.random.normal(6.5, 0.5), 5.8, 7.2),
            'weight': np.clip(np.random.normal(200, 25), 160, 280),
            'usage_rate': np.clip(np.random.normal(22, 5), 10, 35),
            'ortg': np.clip(np.random.normal(110 * rank_factor, 8), 85, 125),
            'drtg': np.clip(np.random.normal(105, 7), 90, 120),
            'scout_grade': np.random.choice(grades, p=grade_weights),
            'archetype': np.random.choice(archetypes)
        }
        
        all_prospects.append(prospect)
    
    # Créer le DataFrame
    df = pd.DataFrame(all_prospects)
    
    # Ajouter les probabilités et rangs
    df['final_gen_probability'] = np.random.beta(2, 3, len(df))
    
    # Ajuster les probabilités pour les top prospects
    df.loc[:4, 'final_gen_probability'] = np.random.uniform(0.75, 0.95, 5)
    df.loc[5:14, 'final_gen_probability'] = np.random.uniform(0.55, 0.75, 10)
    df.loc[15:29, 'final_gen_probability'] = np.random.uniform(0.35, 0.55, 15)
    
    # Assigner les rangs
    df['final_rank'] = range(1, len(df) + 1)
    
    # Nettoyer et retourner
    return clean_dataframe(df)

def create_simplified_demo_data(num_prospects: int = 30) -> pd.DataFrame:
    """Create a simplified version with fewer prospects for testing"""
    full_data = create_demo_data()
    return full_data.head(num_prospects)

def add_mock_historical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add mock historical comparison data"""
    df_with_history = df.copy()
    
    # Comparaisons historiques simulées
    historical_comps = [
        'LeBron James', 'Kevin Durant', 'Stephen Curry', 'Giannis Antetokounmpo',
        'Luka Doncic', 'Jayson Tatum', 'Ja Morant', 'Zion Williamson',
        'Paolo Banchero', 'Scottie Barnes', 'Evan Mobley', 'Cade Cunningham',
        'Jalen Green', 'Franz Wagner', 'Josh Giddey', 'Herbert Jones'
    ]
    
    # Ajouter des comparaisons aléatoires
    df_with_history['historical_comp'] = np.random.choice(
        historical_comps, size=len(df), replace=True
    )
    
    # Ajouter scores de similarité
    df_with_history['similarity_score'] = np.random.uniform(0.6, 0.9, len(df))
    
    return df_with_history

def generate_mock_workout_data(df: pd.DataFrame) -> pd.DataFrame:
    """Generate mock NBA workout/combine data"""
    df_workout = df.copy()
    
    # Mesures physiques
    df_workout['wingspan'] = df_workout['height'] + np.random.uniform(-0.2, 0.4, len(df))
    df_workout['standing_reach'] = df_workout['height'] * 1.33 + np.random.uniform(-0.1, 0.1, len(df))
    df_workout['body_fat_pct'] = np.random.uniform(0.05, 0.15, len(df))
    
    # Tests athlétiques
    df_workout['vertical_leap'] = np.random.uniform(28, 42, len(df))
    df_workout['lane_agility'] = np.random.uniform(10.5, 12.5, len(df))
    df_workout['sprint_3_4'] = np.random.uniform(3.0, 3.8, len(df))
    
    # Tests de tir
    df_workout['spot_up_shooting'] = np.random.uniform(0.6, 0.9, len(df))
    df_workout['off_dribble_shooting'] = np.random.uniform(0.4, 0.8, len(df))
    
    return df_workout
