import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

# 🎯 MODÈLE DE RÉGRESSION - PRÉDICTION DU DRAFT RANK
print("🎯 NBA DRAFT 2025 - MODÈLE DE RÉGRESSION (DRAFT RANK)")
print("=" * 70)

# Charger le dataset
df = pd.read_csv('nba_prospects_2025.csv')
print(f"Dataset chargé: {df.shape[0]} joueurs, {df.shape[1]} features")

# 🎯 VARIABLE CIBLE : DRAFT RANK (régression)
print("\n🎯 DÉFINITION DE LA VARIABLE CIBLE:")

# Vérifier quelle colonne contient le vrai draft rank
rank_columns = [col for col in df.columns if 'rank' in col.lower() and 'predicted' not in col.lower()]
print(f"Colonnes rank détectées: {rank_columns}")

# Utiliser la colonne appropriée (à ajuster selon votre dataset)
if 'actual_rank' in df.columns:
    target_col = 'actual_rank'
elif 'rank' in df.columns:
    target_col = 'rank'
elif 'draft_position' in df.columns:
    target_col = 'draft_position'
else:
    print("⚠️ ATTENTION: Aucune colonne rank trouvée. Utilisation de 'rank' par défaut.")
    target_col = 'rank'

# Créer la cible propre
if target_col in df.columns:
    df['draft_rank'] = df[target_col].copy()
    # Filtrer les joueurs non draftés (rank > 60 ou NaN)
    df_clean = df[df['draft_rank'].notna() & (df['draft_rank'] <= 60)].copy()
    print(f"✅ Variable cible: {target_col} → draft_rank")
    print(f"✅ Joueurs draftés (rank 1-60): {len(df_clean)}")
    print(f"📊 Distribution du rank:")
    print(f"   - Min: {df_clean['draft_rank'].min():.0f}")
    print(f"   - Max: {df_clean['draft_rank'].max():.0f}")
    print(f"   - Médiane: {df_clean['draft_rank'].median():.0f}")
    print(f"   - Moyenne: {df_clean['draft_rank'].mean():.1f}")
else:
    print(f"❌ ERREUR: Colonne '{target_col}' non trouvée!")
    print("Colonnes disponibles:", df.columns.tolist())
    # Créer une cible factice pour démonstration
    print("\n⚠️ CRÉATION D'UNE CIBLE FACTICE POUR DÉMONSTRATION")
    df_clean = df.copy()
    df_clean['draft_rank'] = np.arange(1, len(df_clean) + 1)

# 🚫 SUPPRESSION DES FEATURES LEAKY
print("\n🚫 SUPPRESSION DES FEATURES LEAKY:")

leaky_features = [
    # Tout ce qui contient le résultat final
    'final_draft_score_v21', 'score_v22', 'predicted_rank_v22', 'predicted_rank_v21',
    'ml_rank', 'rank', 'round', 'actual_rank', 'draft_position',
    'final_gen_probability', 'ml_gen_probability', 'gen_probability',
    'final_grade', 'ml_prediction', 'predicted_rank', 'predicted_grade',
    'final_score', 'base_score', 'draft_rank',  # Notre cible!
    'error_v21', 'error_v22', 'improvement', 'alert_level',
    'projected_pick', 'consensus_floor', 'mock_draft_position',
    'is_generational_talent', 'is_gen_talent',  # Dérivé du rank
    'draft_value', 'draft_probability', 'selection_order'
]

# Supprimer aussi les colonnes avec "rank" ou "draft" dans le nom (sauf features clean)
additional_leaky = [col for col in df_clean.columns 
                    if any(keyword in col.lower() for keyword in ['rank', 'draft', 'pick', 'round'])
                    and col not in ['draft_rank']]

all_leaky = list(set(leaky_features + additional_leaky))
present_leaky = [f for f in all_leaky if f in df_clean.columns and f != 'draft_rank']

print(f"✅ Features leaky détectées et supprimées: {len(present_leaky)}")
for feature in sorted(present_leaky)[:15]:  # Afficher les 15 premières
    print(f"   - {feature}")
if len(present_leaky) > 15:
    print(f"   ... et {len(present_leaky) - 15} autres")

# 📋 FEATURES CLEAN - SEULEMENT DONNÉES OBSERVABLES
print("\n📋 SÉLECTION DES FEATURES CLEAN:")

clean_features = [
    # Stats college (observables)
    'ppg', 'rpg', 'apg', 'spg', 'bpg', 'turnovers',
    'fg_pct', 'three_pt_pct', 'ts_pct', 'usage_rate_calculated',
    'fga', 'fta', 'ft_pct', 'PER', 'win_shares',
    
    # Attributs scouting (évaluations humaines)
    'shooting_skill_score', 'athleticism_score', 'bbiq_score', 
    'leadership_score', 'defensive_upside',
    'defensive_rating', 'offensive_rating',
    # Note: 'scouting_consensus_grade' EXCLU - risque de data leakage (trop corrélé au rank)
    
    # Physique (mesurables)
    'age', 'weight', 'games_played', 'minutes', 'games_started',
    # Note: 'height', 'wingspan' exclus car souvent au format texte (6-8, 7'0", etc.)
    
    # Context équipe (observables)
    'team_pace', 'team_ranking', 'conference_strength',
    
    # Bonus/malus basés sur règles (pas de leakage)
    'young_prospect_bonus', 'yang_hansen_penalty', 'youth_bonus', 
    'low_production_malus', 'high_usage_bonus'
]

# Vérifier disponibilité et qualité
available_clean_features = []
for feature in clean_features:
    if feature in df_clean.columns:
        non_null_count = df_clean[feature].notna().sum()
        non_null_pct = non_null_count / len(df_clean) * 100
        if non_null_count >= len(df_clean) * 0.5:  # Au moins 50% de données
            available_clean_features.append(feature)
        else:
            print(f"   ⚠️ {feature}: seulement {non_null_pct:.0f}% de données - EXCLU")

print(f"✅ {len(available_clean_features)} features clean disponibles")
print(f"📝 Features principales: {available_clean_features[:10]}")

# 🔍 ANALYSE DE LA FEATURE SCOUTING_CONSENSUS_GRADE (pour justifier son exclusion)
print("\n🔍 ANALYSE: SCOUTING_CONSENSUS_GRADE vs DRAFT_RANK")
print("-" * 70)

if 'scouting_consensus_grade' in df_clean.columns and 'draft_rank' in df_clean.columns:
    # Calculer la corrélation
    scouting_numeric = pd.to_numeric(df_clean['scouting_consensus_grade'], errors='coerce')
    
    if scouting_numeric.notna().sum() > 10:
        from scipy.stats import pearsonr, spearmanr
        
        # Masque des valeurs non-nulles
        mask = scouting_numeric.notna() & df_clean['draft_rank'].notna()
        
        if mask.sum() > 10:
            pearson_corr, _ = pearsonr(
                scouting_numeric[mask], 
                df_clean.loc[mask, 'draft_rank']
            )
            spearman_corr, _ = spearmanr(
                scouting_numeric[mask], 
                df_clean.loc[mask, 'draft_rank']
            )
            
            print(f"📊 Corrélation avec draft_rank:")
            print(f"   - Pearson:  {pearson_corr:+.3f}")
            print(f"   - Spearman: {spearman_corr:+.3f}")
            
            if abs(pearson_corr) > 0.8 or abs(spearman_corr) > 0.8:
                print(f"   ⚠️  ATTENTION: Corrélation très forte (> 0.8)")
                print(f"   ⚠️  Cette feature est probablement du DATA LEAKAGE!")
                print(f"   ✅ DÉCISION: Feature EXCLUE du modèle")
            elif abs(pearson_corr) > 0.6:
                print(f"   ⚠️  Corrélation forte (> 0.6) - feature dominante potentielle")
                print(f"   ✅ DÉCISION: Feature EXCLUE pour tester la vraie capacité prédictive")
            else:
                print(f"   ✅ Corrélation acceptable (< 0.6)")
        else:
            print(f"   ⚠️  Pas assez de données pour calculer la corrélation")
    else:
        print(f"   ⚠️  scouting_consensus_grade: trop de valeurs manquantes")
else:
    print(f"   ℹ️  scouting_consensus_grade ou draft_rank non disponible")

print("-" * 70)

# 📏 CONVERSION DES FEATURES PHYSIQUES (height, wingspan)
print("\n📏 CONVERSION DES FEATURES PHYSIQUES:")

def convert_height_to_inches(height_str):
    """Convertit 6-8, 6'8", ou 6-8" en pouces (80 inches)"""
    if pd.isna(height_str):
        return np.nan
    
    height_str = str(height_str).strip()
    
    try:
        # Format: 6-8 ou 6'8" ou 6'8
        if '-' in height_str:
            feet, inches = height_str.split('-')
            return int(feet) * 12 + int(inches)
        elif "'" in height_str:
            parts = height_str.replace('"', '').split("'")
            feet = int(parts[0])
            inches = float(parts[1]) if len(parts) > 1 and parts[1] else 0
            return feet * 12 + inches
        else:
            # Déjà numérique
            return float(height_str)
    except:
        return np.nan

# Convertir height si présente
if 'height' in df_clean.columns:
    df_clean['height_inches'] = df_clean['height'].apply(convert_height_to_inches)
    if df_clean['height_inches'].notna().sum() >= len(df_clean) * 0.5:
        available_clean_features.append('height_inches')
        print(f"  ✅ height → height_inches (en pouces)")
    else:
        print(f"  ⚠️ height: trop de valeurs manquantes")

# Convertir wingspan si présente
if 'wingspan' in df_clean.columns:
    df_clean['wingspan_inches'] = df_clean['wingspan'].apply(convert_height_to_inches)
    if df_clean['wingspan_inches'].notna().sum() >= len(df_clean) * 0.5:
        available_clean_features.append('wingspan_inches')
        print(f"  ✅ wingspan → wingspan_inches (en pouces)")
        
        # Feature dérivée: wingspan vs height
        if 'height_inches' in available_clean_features:
            df_clean['wingspan_advantage'] = df_clean['wingspan_inches'] - df_clean['height_inches']
            available_clean_features.append('wingspan_advantage')
            print(f"  ✅ wingspan_advantage créée (wingspan - height)")
    else:
        print(f"  ⚠️ wingspan: trop de valeurs manquantes")

print(f"📊 Features après conversion: {len(available_clean_features)}")

# 🔧 FEATURE ENGINEERING CLEAN
print("\n🔧 FEATURE ENGINEERING CLEAN:")

# Vérifier la présence des features nécessaires pour le calcul
def safe_feature_engineering(df, features_available):
    """Créer des features dérivées seulement si les features source existent"""
    new_features = []
    
    # 1. Efficacité scoring
    if 'ppg' in features_available and 'fga' in features_available:
        df['efficiency_ratio'] = df['ppg'] / (df['fga'] + 0.1)
        new_features.append('efficiency_ratio')
    
    # 2. Playmaking
    if 'apg' in features_available and 'turnovers' in features_available:
        df['playmaking_ratio'] = df['apg'] / (df['turnovers'] + 0.1)
        new_features.append('playmaking_ratio')
    
    # 3. Impact global (two-way)
    if all(f in features_available for f in ['ppg', 'rpg', 'apg', 'spg', 'bpg']):
        df['two_way_impact'] = (df['ppg'] + df['rpg'] + df['apg'] + 
                                df['spg'] + df['bpg']) / 5
        new_features.append('two_way_impact')
    
    # 4. Production ajustée au rythme
    if 'ppg' in features_available and 'team_pace' in features_available:
        df['pace_adjusted_ppg'] = df['ppg'] * (100 / (df['team_pace'] + 0.1))
        new_features.append('pace_adjusted_ppg')
    
    # 5. Efficacité par minute
    if 'ppg' in features_available and 'minutes' in features_available:
        df['minutes_efficiency'] = df['ppg'] / (df['minutes'] + 0.1)
        new_features.append('minutes_efficiency')
    
    # 6. Production ajustée à l'âge (jeunes = meilleur potentiel)
    if 'ppg' in features_available and 'age' in features_available:
        df['age_adjusted_production'] = df['ppg'] * (22 - df['age'])
        new_features.append('age_adjusted_production')
    
    # 7. Comparaisons par position
    if 'position' in df.columns and 'ppg' in features_available:
        df['ppg_vs_position'] = df['ppg'] / (df.groupby('position')['ppg'].transform('mean') + 0.1)
        new_features.append('ppg_vs_position')
    
    if 'position' in df.columns and 'ts_pct' in features_available:
        df['ts_vs_position'] = df['ts_pct'] / (df.groupby('position')['ts_pct'].transform('mean') + 0.1)
        new_features.append('ts_vs_position')
    
    # 8. Composite de skills (si disponible)
    skill_features = ['shooting_skill_score', 'athleticism_score', 'bbiq_score']
    if all(f in features_available for f in skill_features):
        df['skill_composite'] = df[skill_features].mean(axis=1)
        new_features.append('skill_composite')
    
    # 9. Volume de production
    if all(f in features_available for f in ['ppg', 'rpg', 'apg']):
        df['production_volume'] = df['ppg'] + df['rpg'] + df['apg']
        new_features.append('production_volume')
    
    # 10. Efficacité vraie (True Shooting + Volume)
    if 'ts_pct' in features_available and 'fga' in features_available:
        df['scoring_efficiency'] = df['ts_pct'] * df['fga']
        new_features.append('scoring_efficiency')
    
    return new_features

# Créer les features
new_features = safe_feature_engineering(df_clean, available_clean_features)
available_clean_features.extend(new_features)

print(f"✅ {len(new_features)} nouvelles features créées:")
for feat in new_features:
    print(f"   + {feat}")
print(f"📊 Total features: {len(available_clean_features)}")

# 🔧 PREPROCESSING
print("\n🔧 PREPROCESSING:")

# Préparer X et y
X = df_clean[available_clean_features].copy()
y = df_clean['draft_rank'].copy()

# Identifier et convertir les colonnes non-numériques
print(f"Vérification des types de données...")
non_numeric_cols = []
for col in X.columns:
    if X[col].dtype == 'object':
        non_numeric_cols.append(col)
        print(f"  ⚠️ {col} est non-numérique (type: {X[col].dtype})")
        
        # Tenter conversion en numérique
        try:
            # Essayer conversion simple
            X[col] = pd.to_numeric(X[col], errors='coerce')
            print(f"     ✅ Converti en numérique")
        except:
            # Si échec, supprimer la colonne
            print(f"     ❌ Impossible de convertir - SUPPRESSION")
            X = X.drop(columns=[col])
            available_clean_features.remove(col)

if non_numeric_cols:
    print(f"✅ Nettoyage terminé: {len(non_numeric_cols)} colonnes traitées")

# Imputation des valeurs manquantes (maintenant toutes les colonnes sont numériques)
print(f"\nImputation des valeurs manquantes...")
X_filled = X.fillna(X.median())
print(f"✅ Valeurs manquantes imputées avec la médiane")

# Vérification finale
missing_check = X_filled.isna().sum().sum()
if missing_check > 0:
    print(f"⚠️ Attention: {missing_check} valeurs manquantes restantes - remplacement par 0")
    X_filled = X_filled.fillna(0)
else:
    print(f"✅ Aucune valeur manquante restante")

# Standardisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_filled)
X_scaled = pd.DataFrame(X_scaled, columns=available_clean_features, index=X_filled.index)
print(f"✅ Features standardisées (mean=0, std=1)")

print(f"\n📊 DONNÉES FINALES:")
print(f"   - Nombre de joueurs: {len(X_scaled)}")
print(f"   - Nombre de features: {len(available_clean_features)}")
print(f"   - Range du rank: {y.min():.0f} à {y.max():.0f}")

# 🤖 MODÈLES DE RÉGRESSION
print("\n" + "="*70)
print("🤖 ENTRAÎNEMENT DES MODÈLES DE RÉGRESSION")
print("="*70)

# Split train/test pour évaluation finale
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"\n📊 Split: {len(X_train)} train / {len(X_test)} test")

# Définir les modèles
models = {
    'Random Forest': RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        min_samples_leaf=2,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    ),
    'Gradient Boosting': GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        random_state=42
    ),
    'Ridge Regression': Ridge(
        alpha=10.0,
        random_state=42
    ),
    'Lasso Regression': Lasso(
        alpha=1.0,
        random_state=42,
        max_iter=2000
    )
}

# Cross-validation
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
results = {}

print("\n🔄 VALIDATION CROISÉE (5-Fold):")
print("-" * 70)

for name, model in models.items():
    # CV avec MAE (métrique principale)
    cv_scores = -cross_val_score(
        model, X_train, y_train, 
        cv=kfold, 
        scoring='neg_mean_absolute_error'
    )
    
    results[name] = {
        'cv_mae_mean': cv_scores.mean(),
        'cv_mae_std': cv_scores.std()
    }
    
    print(f"{name:20s} | MAE: {cv_scores.mean():5.2f} (±{cv_scores.std():4.2f})")

# 🎯 ENTRAÎNEMENT ET ÉVALUATION SUR TEST SET
print("\n" + "="*70)
print("🎯 ÉVALUATION SUR TEST SET")
print("="*70)

best_model = None
best_mae = float('inf')
predictions = {}

for name, model in models.items():
    # Entraîner sur train complet
    model.fit(X_train, y_train)
    
    # Prédire sur test
    y_pred = model.predict(X_test)
    
    # Clipper les prédictions dans [1, 60]
    y_pred_clipped = np.clip(y_pred, 1, 60)
    
    # Calculer métriques
    mae = mean_absolute_error(y_test, y_pred_clipped)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred_clipped))
    r2 = r2_score(y_test, y_pred_clipped)
    spearman_corr, _ = spearmanr(y_test, y_pred_clipped)
    
    # Stocker
    predictions[name] = y_pred_clipped
    results[name].update({
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'spearman': spearman_corr
    })
    
    # Meilleur modèle
    if mae < best_mae:
        best_mae = mae
        best_model = (name, model)
    
    print(f"\n{name}:")
    print(f"  MAE:       {mae:6.2f} picks")
    print(f"  RMSE:      {rmse:6.2f} picks")
    print(f"  R²:        {r2:6.3f}")
    print(f"  Spearman:  {spearman_corr:6.3f}")

# 🏆 MEILLEUR MODÈLE
print("\n" + "="*70)
print(f"🏆 MEILLEUR MODÈLE: {best_model[0]}")
print("="*70)
print(f"✅ Erreur moyenne: {best_mae:.2f} picks")
print(f"✅ Spearman: {results[best_model[0]]['spearman']:.3f}")

# 🎯 ENSEMBLE (moyenne pondérée)
print("\n🎯 PRÉDICTION ENSEMBLE:")

# Pondérations basées sur les performances CV
weights = {}
total_inv_mae = sum(1/results[name]['cv_mae_mean'] for name in models.keys())
for name in models.keys():
    weights[name] = (1/results[name]['cv_mae_mean']) / total_inv_mae

print("Poids des modèles:")
for name, weight in weights.items():
    print(f"  {name:20s}: {weight:.3f}")

# Prédiction ensemble
y_pred_ensemble = np.zeros(len(y_test))
for name, weight in weights.items():
    y_pred_ensemble += weight * predictions[name]

y_pred_ensemble = np.clip(y_pred_ensemble, 1, 60)

# Métriques ensemble
mae_ensemble = mean_absolute_error(y_test, y_pred_ensemble)
rmse_ensemble = np.sqrt(mean_squared_error(y_test, y_pred_ensemble))
r2_ensemble = r2_score(y_test, y_pred_ensemble)
spearman_ensemble, _ = spearmanr(y_test, y_pred_ensemble)

print(f"\n📊 PERFORMANCE ENSEMBLE:")
print(f"  MAE:       {mae_ensemble:6.2f} picks")
print(f"  RMSE:      {rmse_ensemble:6.2f} picks")
print(f"  R²:        {r2_ensemble:6.3f}")
print(f"  Spearman:  {spearman_ensemble:6.3f}")

# 📊 ANALYSE DES ERREURS
print("\n" + "="*70)
print("📊 ANALYSE DES ERREURS (ENSEMBLE)")
print("="*70)

errors = np.abs(y_test.values - y_pred_ensemble)
errors_sorted_idx = np.argsort(errors)

print(f"\n📈 Distribution des erreurs:")
print(f"  Erreur médiane:  {np.median(errors):5.2f} picks")
print(f"  Erreur moyenne:  {np.mean(errors):5.2f} picks")
print(f"  Erreur max:      {np.max(errors):5.2f} picks")
print(f"  Top 10 accuracy: {(errors <= 10).mean()*100:5.1f}%")
print(f"  Top 5 accuracy:  {(errors <= 5).mean()*100:5.1f}%")

# Erreurs par tier de draft
df_test_results = df_clean.loc[X_test.index].copy()
df_test_results['predicted_rank'] = y_pred_ensemble
df_test_results['error'] = errors

print(f"\n📊 Erreurs par tier:")
tiers = [(1, 10, "Lottery"), (11, 30, "First Round"), (31, 60, "Second Round")]
for start, end, label in tiers:
    mask = (df_test_results['draft_rank'] >= start) & (df_test_results['draft_rank'] <= end)
    if mask.sum() > 0:
        tier_mae = df_test_results.loc[mask, 'error'].mean()
        print(f"  {label:15s} (picks {start:2d}-{end:2d}): MAE = {tier_mae:5.2f}")

# 🔍 MEILLEURES ET PIRES PRÉDICTIONS
print(f"\n✅ 5 MEILLEURES PRÉDICTIONS:")
for idx in errors_sorted_idx[:5]:
    actual = y_test.iloc[idx]
    pred = y_pred_ensemble[idx]
    error = errors[idx]
    player_idx = X_test.index[idx]
    player_name = df_clean.loc[player_idx, 'name'] if 'name' in df_clean.columns else f"Joueur #{player_idx}"
    print(f"  {player_name:25s} | Réel: {actual:5.1f} | Prédit: {pred:5.1f} | Erreur: {error:5.1f}")

print(f"\n❌ 5 PIRES PRÉDICTIONS:")
for idx in errors_sorted_idx[-5:]:
    actual = y_test.iloc[idx]
    pred = y_pred_ensemble[idx]
    error = errors[idx]
    player_idx = X_test.index[idx]
    player_name = df_clean.loc[player_idx, 'name'] if 'name' in df_clean.columns else f"Joueur #{player_idx}"
    print(f"  {player_name:25s} | Réel: {actual:5.1f} | Prédit: {pred:5.1f} | Erreur: {error:5.1f}")

# 🔍 FEATURE IMPORTANCE
print("\n" + "="*70)
print("🔍 FEATURE IMPORTANCE (Random Forest)")
print("="*70)

rf_model = models['Random Forest']
feature_importance = pd.DataFrame({
    'feature': available_clean_features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🏆 TOP 15 FEATURES:")
for idx, row in feature_importance.head(15).iterrows():
    print(f"  {row['feature']:30s}: {row['importance']:6.4f}")

# 💡 INTERPRÉTATION
print("\n" + "="*70)
print("💡 INTERPRÉTATION DES RÉSULTATS")
print("="*70)

print(f"\n✅ PERFORMANCE GLOBALE:")
print(f"  • Erreur moyenne: {mae_ensemble:.1f} picks")
print(f"  • Corrélation Spearman: {spearman_ensemble:.3f}")
print(f"  • R²: {r2_ensemble:.3f}")

if mae_ensemble < 5:
    verdict = "🟢 EXCELLENT - Prédictions très précises!"
elif mae_ensemble < 8:
    verdict = "🟡 BON - Prédictions fiables"
elif mae_ensemble < 12:
    verdict = "🟠 CORRECT - Prédictions acceptables"
else:
    verdict = "🔴 FAIBLE - Modèle à améliorer"

print(f"\n{verdict}")

if spearman_ensemble > 0.7:
    print(f"✅ Excellente corrélation de rang (Spearman > 0.7)")
elif spearman_ensemble > 0.5:
    print(f"✅ Bonne corrélation de rang (Spearman > 0.5)")
else:
    print(f"⚠️ Corrélation de rang modérée")

# 🎯 RECOMMANDATIONS
print(f"\n🎯 RECOMMANDATIONS:")
if mae_ensemble > 10:
    print("  1. Considérer plus de features (scouting, combine measurements)")
    print("  2. Essayer des modèles plus complexes (XGBoost, LightGBM)")
    print("  3. Améliorer le feature engineering")

if feature_importance.head(1)['importance'].values[0] > 0.3:
    top_feat = feature_importance.head(1)['feature'].values[0]
    print(f"  • Feature dominante: {top_feat} ({feature_importance.head(1)['importance'].values[0]:.1%})")
    print(f"    → Risque de surapprentissage sur cette feature")

print("\n🚀 MODÈLE DE RÉGRESSION PRÊT!")
print("="*70)

# 💾 SAUVEGARDER LE MODÈLE ET LES RÉSULTATS
print("\n💾 SAUVEGARDE DU MODÈLE ET DES RÉSULTATS:")
print("-" * 70)

import joblib
import json

# 1. Sauvegarder le meilleur modèle individuel
joblib.dump(best_model[1], 'nba_draft_model_best.pkl')
print(f"✅ Meilleur modèle ({best_model[0]}) sauvegardé: nba_draft_model_best.pkl")

# 2. Sauvegarder tous les modèles de l'ensemble
joblib.dump(models, 'nba_draft_models_ensemble.pkl')
print(f"✅ Ensemble de modèles sauvegardé: nba_draft_models_ensemble.pkl")

# 3. Sauvegarder le scaler
joblib.dump(scaler, 'nba_draft_scaler.pkl')
print(f"✅ Scaler sauvegardé: nba_draft_scaler.pkl")

# 4. Sauvegarder la liste des features
with open('nba_draft_features.json', 'w') as f:
    json.dump({
        'features': available_clean_features,
        'n_features': len(available_clean_features)
    }, f, indent=2)
print(f"✅ Liste des features sauvegardée: nba_draft_features.json")

# 5. Sauvegarder les résultats pour Streamlit
results_for_streamlit = {
    'model_version': 'v3_clean',
    'model_type': 'regression',
    'best_model': best_model[0],
    'n_players': len(df_clean),
    'n_features': len(available_clean_features),
    'performance': {
        'cv_mae_mean': {name: results[name]['cv_mae_mean'] for name in models.keys()},
        'cv_mae_std': {name: results[name]['cv_mae_std'] for name in models.keys()},
        'test_mae': {name: results[name]['mae'] for name in models.keys()},
        'test_rmse': {name: results[name]['rmse'] for name in models.keys()},
        'test_r2': {name: results[name]['r2'] for name in models.keys()},
        'test_spearman': {name: results[name]['spearman'] for name in models.keys()},
        'ensemble_mae': mae_ensemble,
        'ensemble_rmse': rmse_ensemble,
        'ensemble_r2': r2_ensemble,
        'ensemble_spearman': spearman_ensemble,
    },
    'errors_analysis': {
        'median_error': float(np.median(errors)),
        'mean_error': float(np.mean(errors)),
        'max_error': float(np.max(errors)),
        'top10_accuracy': float((errors <= 10).mean()),
        'top5_accuracy': float((errors <= 5).mean()),
    },
    'tier_performance': {},
    'feature_importance': feature_importance.to_dict('records'),
    'weights': weights,
    'predictions': df_test_results[['draft_rank', 'predicted_rank', 'error']].to_dict('records') if 'name' not in df_test_results.columns else df_test_results[['name', 'draft_rank', 'predicted_rank', 'error']].to_dict('records')
}

# Ajouter les erreurs par tier
for start, end, label in tiers:
    mask = (df_test_results['draft_rank'] >= start) & (df_test_results['draft_rank'] <= end)
    if mask.sum() > 0:
        tier_mae = df_test_results.loc[mask, 'error'].mean()
        results_for_streamlit['tier_performance'][label] = {
            'range': f"{start}-{end}",
            'mae': float(tier_mae),
            'n_players': int(mask.sum())
        }

# Sauvegarder en JSON
with open('nba_draft_results.json', 'w') as f:
    json.dump(results_for_streamlit, f, indent=2)
print(f"✅ Résultats sauvegardés: nba_draft_results.json")

# 6. Sauvegarder les prédictions complètes pour tous les joueurs
df_clean['predicted_rank_ensemble'] = np.zeros(len(df_clean))
df_clean.loc[X_test.index, 'predicted_rank_ensemble'] = y_pred_ensemble
df_clean['prediction_error'] = np.abs(df_clean['draft_rank'] - df_clean['predicted_rank_ensemble'])

# Pour les joueurs du train set, faire une prédiction (pour info seulement)
if len(X_train) > 0:
    y_train_pred = np.zeros(len(X_train))
    for name, weight in weights.items():
        model = models[name]
        y_train_pred += weight * model.predict(X_train)
    y_train_pred = np.clip(y_train_pred, 1, 60)
    df_clean.loc[X_train.index, 'predicted_rank_ensemble'] = y_train_pred
    df_clean.loc[X_train.index, 'prediction_error'] = np.abs(
        df_clean.loc[X_train.index, 'draft_rank'] - y_train_pred
    )

# Colonnes à sauvegarder
cols_to_save = ['name', 'position', 'draft_rank', 'predicted_rank_ensemble', 'prediction_error']
if 'name' not in df_clean.columns:
    cols_to_save.remove('name')
if 'position' not in df_clean.columns:
    cols_to_save.remove('position')

# Garder seulement les colonnes qui existent
cols_to_save = [col for col in cols_to_save if col in df_clean.columns]

df_predictions = df_clean[cols_to_save].copy()
df_predictions = df_predictions.sort_values('draft_rank')
df_predictions.to_csv('nba_draft_predictions.csv', index=False)
print(f"✅ Prédictions complètes sauvegardées: nba_draft_predictions.csv")

print("\n" + "="*70)
print("✅ TOUS LES FICHIERS SAUVEGARDÉS:")
print("   • nba_draft_model_best.pkl (meilleur modèle)")
print("   • nba_draft_models_ensemble.pkl (tous les modèles)")
print("   • nba_draft_scaler.pkl (standardisation)")
print("   • nba_draft_features.json (liste des features)")
print("   • nba_draft_results.json (résultats pour Streamlit)")
print("   • nba_draft_predictions.csv (prédictions complètes)")
print("="*70)