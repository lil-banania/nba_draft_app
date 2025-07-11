# config/teams_data.py
"""Données et analyse des besoins des équipes NBA"""

NBA_TEAMS_ANALYSIS = {
    # Atlantic Division
    'Boston Celtics': {
        'division': 'Atlantic',
        'positional_needs': {'PG': 0.3, 'SG': 0.4, 'SF': 0.2, 'PF': 0.4, 'C': 0.6},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.4, 'defense': 0.5, 'rebounding': 0.5},
        'team_context': 'Championship team looking for depth',
        'priority': 'depth'
    },
    'Brooklyn Nets': {
        'division': 'Atlantic',
        'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.8, 'PF': 0.4, 'C': 0.5},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Rebuilding with focus on young talent',
        'priority': 'youth'
    },
    'New York Knicks': {
        'division': 'Atlantic',
        'positional_needs': {'PG': 0.5, 'SG': 0.4, 'SF': 0.6, 'PF': 0.3, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.6, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Looking for versatile contributors',
        'priority': 'versatility'
    },
    'Philadelphia 76ers': {
        'division': 'Atlantic',
        'positional_needs': {'PG': 0.8, 'SG': 0.6, 'SF': 0.4, 'PF': 0.3, 'C': 0.2},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
        'team_context': 'Need playmaking and shooting around stars',
        'priority': 'playmaking'
    },
    'Toronto Raptors': {
        'division': 'Atlantic',
        'positional_needs': {'PG': 0.6, 'SG': 0.5, 'SF': 0.4, 'PF': 0.7, 'C': 0.3},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.6, 'defense': 0.7, 'rebounding': 0.5},
        'team_context': 'Young core needs complementary pieces',
        'priority': 'development'
    },
    
    # Central Division
    'Chicago Bulls': {
        'division': 'Central',
        'positional_needs': {'PG': 0.7, 'SG': 0.3, 'SF': 0.6, 'PF': 0.5, 'C': 0.4},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.8, 'defense': 0.5, 'rebounding': 0.4},
        'team_context': 'Need floor general and outside shooting',
        'priority': 'playmaking'
    },
    'Cleveland Cavaliers': {
        'division': 'Central',
        'positional_needs': {'PG': 0.3, 'SG': 0.6, 'SF': 0.7, 'PF': 0.5, 'C': 0.4},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Need wing depth and perimeter shooting',
        'priority': 'wings'
    },
    'Detroit Pistons': {
        'division': 'Central',
        'positional_needs': {'PG': 0.3, 'SG': 0.8, 'SF': 0.7, 'PF': 0.3, 'C': 0.4},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.3},
        'team_context': 'Need perimeter scoring and shooting',
        'priority': 'shooting'
    },
    'Indiana Pacers': {
        'division': 'Central',
        'positional_needs': {'PG': 0.3, 'SG': 0.5, 'SF': 0.6, 'PF': 0.4, 'C': 0.7},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.8},
        'team_context': 'Need interior defense and rebounding',
        'priority': 'defense'
    },
    'Milwaukee Bucks': {
        'division': 'Central',
        'positional_needs': {'PG': 0.7, 'SG': 0.5, 'SF': 0.3, 'PF': 0.4, 'C': 0.6},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.8, 'playmaking': 0.7, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Need secondary playmaker and shooting',
        'priority': 'playmaking'
    },
    
    # Southeast Division
    'Atlanta Hawks': {
        'division': 'Southeast',
        'positional_needs': {'PG': 0.2, 'SG': 0.6, 'SF': 0.7, 'PF': 0.8, 'C': 0.6},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.3, 'defense': 0.9, 'rebounding': 0.7},
        'team_context': 'Need defense and size around Trae Young',
        'priority': 'defense'
    },
    'Charlotte Hornets': {
        'division': 'Southeast',
        'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.5, 'PF': 0.6, 'C': 0.9},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.8, 'rebounding': 0.9},
        'team_context': 'Need interior presence and defense',
        'priority': 'interior'
    },
    'Miami Heat': {
        'division': 'Southeast',
        'positional_needs': {'PG': 0.6, 'SG': 0.4, 'SF': 0.5, 'PF': 0.7, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.8, 'rebounding': 0.5},
        'team_context': 'Culture fit and two-way players preferred',
        'priority': 'culture'
    },
    'Orlando Magic': {
        'division': 'Southeast',
        'positional_needs': {'PG': 0.4, 'SG': 0.8, 'SF': 0.3, 'PF': 0.4, 'C': 0.2},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.4, 'rebounding': 0.3},
        'team_context': 'Need perimeter scoring and shooting',
        'priority': 'scoring'
    },
    'Washington Wizards': {
        'division': 'Southeast',
        'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.8, 'PF': 0.7, 'C': 0.3},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.5, 'defense': 0.8, 'rebounding': 0.6},
        'team_context': 'Rebuilding - need versatile two-way players',
        'priority': 'youth'
    },
    
    # Northwest Division
    'Denver Nuggets': {
        'division': 'Northwest',
        'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.4, 'PF': 0.3, 'C': 0.2},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.3},
        'team_context': 'Need perimeter depth around Jokic',
        'priority': 'depth'
    },
    'Minnesota Timberwolves': {
        'division': 'Northwest',
        'positional_needs': {'PG': 0.6, 'SG': 0.7, 'SF': 0.3, 'PF': 0.2, 'C': 0.3},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.8, 'playmaking': 0.6, 'defense': 0.4, 'rebounding': 0.3},
        'team_context': 'Need perimeter scoring and playmaking',
        'priority': 'scoring'
    },
    'Oklahoma City Thunder': {
        'division': 'Northwest',
        'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.5, 'PF': 0.6, 'C': 0.8},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.6, 'rebounding': 0.8},
        'team_context': 'Need veteran presence and interior size',
        'priority': 'interior'
    },
    'Portland Trail Blazers': {
        'division': 'Northwest',
        'positional_needs': {'PG': 0.9, 'SG': 0.3, 'SF': 0.6, 'PF': 0.4, 'C': 0.2},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
        'team_context': 'Desperate need for franchise point guard',
        'priority': 'playmaking'
    },
    'Utah Jazz': {
        'division': 'Northwest',
        'positional_needs': {'PG': 0.4, 'SG': 0.7, 'SF': 0.6, 'PF': 0.5, 'C': 0.3},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Rebuilding with young core',
        'priority': 'youth'
    },
    
    # Pacific Division
    'Golden State Warriors': {
        'division': 'Pacific',
        'positional_needs': {'PG': 0.4, 'SG': 0.3, 'SF': 0.7, 'PF': 0.6, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.5},
        'team_context': 'Need youth and athleticism',
        'priority': 'youth'
    },
    'Los Angeles Clippers': {
        'division': 'Pacific',
        'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.4, 'PF': 0.5, 'C': 0.6},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.5},
        'team_context': 'Need depth and versatility',
        'priority': 'depth'
    },
    'Los Angeles Lakers': {
        'division': 'Pacific',
        'positional_needs': {'PG': 0.6, 'SG': 0.5, 'SF': 0.4, 'PF': 0.3, 'C': 0.7},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.8, 'playmaking': 0.6, 'defense': 0.7, 'rebounding': 0.6},
        'team_context': 'Need role players around aging stars',
        'priority': 'experience'
    },
    'Phoenix Suns': {
        'division': 'Pacific',
        'positional_needs': {'PG': 0.3, 'SG': 0.4, 'SF': 0.6, 'PF': 0.7, 'C': 0.5},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.6},
        'team_context': 'Need complementary pieces around core',
        'priority': 'depth'
    },
    'Sacramento Kings': {
        'division': 'Pacific',
        'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.6, 'PF': 0.7, 'C': 0.8},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.9, 'rebounding': 0.8},
        'team_context': 'Need frontcourt defense and size',
        'priority': 'defense'
    },
    
    # Southwest Division
    'Dallas Mavericks': {
        'division': 'Southwest',
        'positional_needs': {'PG': 0.3, 'SG': 0.6, 'SF': 0.5, 'PF': 0.4, 'C': 0.7},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.8, 'rebounding': 0.6},
        'team_context': 'Need defense and complementary pieces',
        'priority': 'defense'
    },
    'Houston Rockets': {
        'division': 'Southwest',
        'positional_needs': {'PG': 0.3, 'SG': 0.5, 'SF': 0.8, 'PF': 0.6, 'C': 0.4},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.8, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
        'team_context': 'Young team building around core',
        'priority': 'youth'
    },
    'Memphis Grizzlies': {
        'division': 'Southwest',
        'positional_needs': {'PG': 0.2, 'SG': 0.6, 'SF': 0.7, 'PF': 0.4, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.3, 'defense': 0.7, 'rebounding': 0.5},
        'team_context': 'Need shooting and wing depth',
        'priority': 'shooting'
    },
    'New Orleans Pelicans': {
        'division': 'Southwest',
        'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.6, 'PF': 0.3, 'C': 0.4},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Need consistency and depth',
        'priority': 'depth'
    },
    'San Antonio Spurs': {
        'division': 'Southwest',
        'positional_needs': {'PG': 0.3, 'SG': 0.7, 'SF': 0.4, 'PF': 0.2, 'C': 0.6},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
        'team_context': 'Need shooting and scoring around Wembanyama',
        'priority': 'scoring'
    }
}

# Fonctions utilitaires pour les équipes
def get_teams_by_division():
    """Retourne les équipes groupées par division"""
    divisions = {}
    for team, data in NBA_TEAMS_ANALYSIS.items():
        division = data['division']
        if division not in divisions:
            divisions[division] = []
        divisions[division].append(team)
    return divisions

def get_teams_by_priority(priority):
    """Retourne les équipes avec une priorité donnée"""
    return [team for team, data in NBA_TEAMS_ANALYSIS.items() 
            if data['priority'] == priority]

def get_team_fit_score(player_position, player_skills, team_name):
    """Calculate team fit score for a player"""
    if team_name not in NBA_TEAMS_ANALYSIS:
        return 0.0
    
    team_data = NBA_TEAMS_ANALYSIS[team_name]
    
    # Position fit (40% weight)
    position_score = team_data['positional_needs'].get(player_position, 0.1) * 40
    
    # Skills fit (60% weight) 
    skills_score = 0
    for skill, value in player_skills.items():
        if skill in team_data['skill_needs']:
            skills_score += value * team_data['skill_needs'][skill] * 10
    
    return min(100, position_score + skills_score)
