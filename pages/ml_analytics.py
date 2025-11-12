# pages/ml_analytics.py
"""Page ML Analytics - Chargement depuis models/"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
from pathlib import Path

def show(df: pd.DataFrame):
    """Display ML analytics page"""
    st.markdown("## 🤖 ML Model Analytics")
    st.caption("Regression Model Performance - Clean (No Data Leakage)")
    
    # Load model results
    results = load_model_results()
    predictions = load_predictions()
    features = load_features()
    
    if results:
        st.success("✅ **Model v3 (Clean)**: Regression model trained on observable data only")
        
        # Core performance metrics
        display_performance_overview(results)
        
        # Performance details
        display_model_comparison(results)
        
        # Predictions analysis
        if predictions is not None:
            display_predictions_analysis(predictions, results)
        
        # Feature importance
        if results.get('feature_importance'):
            display_feature_importance(results['feature_importance'])
        
        # Model info
        display_model_info(results, features)
    else:
        st.error("❌ Fichier de résultats introuvable. Exécutez d'abord le modèle.")
        st.info("""
        Pour générer les résultats:
        1. Exécutez `python model_v3.py`
        2. Vérifiez que les fichiers sont dans `models/`
        3. Rafraîchissez cette page
        """)

@st.cache_data
def load_model_results():
    """Load model results from JSON"""
    try:
        # Essayer models/
        path = Path('models/nba_draft_results.json')
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        
        # Essayer racine
        path = Path('nba_draft_results.json')
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        
        return None
    except Exception as e:
        st.error(f"Erreur de chargement: {e}")
        return None

@st.cache_data
def load_predictions():
    """Load predictions CSV"""
    try:
        # Essayer models/
        path = Path('models/nba_draft_predictions.csv')
        if path.exists():
            return pd.read_csv(path)
        
        # Essayer racine
        path = Path('nba_draft_predictions.csv')
        if path.exists():
            return pd.read_csv(path)
        
        return None
    except Exception as e:
        st.warning(f"⚠️ Fichier de prédictions introuvable: {e}")
        return None

@st.cache_data
def load_features():
    """Load features list"""
    try:
        # Essayer models/
        path = Path('models/nba_draft_features.json')
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        
        # Essayer racine
        path = Path('nba_draft_features.json')
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        
        return None
    except Exception as e:
        return None

def display_performance_overview(results):
    """Display key performance metrics"""
    st.markdown("### 📊 Performance Overview")
    
    perf = results['performance']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "MAE Ensemble",
            f"{perf['ensemble_mae']:.2f} picks",
            help="Mean Absolute Error"
        )
    
    with col2:
        st.metric(
            "RMSE",
            f"{perf['ensemble_rmse']:.2f} picks",
            help="Root Mean Squared Error"
        )
    
    with col3:
        st.metric(
            "R²",
            f"{perf['ensemble_r2']:.3f}",
            help="Coefficient of determination"
        )
    
    with col4:
        st.metric(
            "Spearman",
            f"{perf['ensemble_spearman']:.3f}",
            help="Rank correlation"
        )
    
    # Interpretation
    mae = perf['ensemble_mae']
    spearman = perf['ensemble_spearman']
    
    if mae < 5:
        verdict = "🟢 EXCELLENT"
    elif mae < 8:
        verdict = "🟡 BON"
    else:
        verdict = "🟠 CORRECT"
    
    st.success(f"{verdict} - Erreur moyenne de {mae:.1f} picks")
    
    if spearman > 0.7:
        st.success(f"✅ Excellente corrélation de rang (Spearman = {spearman:.3f})")

def display_model_comparison(results):
    """Display comparison between models"""
    st.markdown("### 🎯 Comparaison des modèles")
    
    perf = results['performance']
    
    # Create comparison dataframe
    models = list(perf['test_mae'].keys())
    
    comparison_data = {
        'Modèle': models,
        'CV MAE': [perf['cv_mae_mean'][m] for m in models],
        'Test MAE': [perf['test_mae'][m] for m in models],
        'Test R²': [perf['test_r2'][m] for m in models],
        'Spearman': [perf['test_spearman'][m] for m in models]
    }
    
    df_comp = pd.DataFrame(comparison_data)
    
    # Display table
    st.dataframe(
        df_comp.style.format({
            'CV MAE': '{:.2f}',
            'Test MAE': '{:.2f}',
            'Test R²': '{:.3f}',
            'Spearman': '{:.3f}'
        }).background_gradient(subset=['Test MAE'], cmap='RdYlGn_r'),
        use_container_width=True,
        hide_index=True
    )
    
    # Chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=models,
        y=[perf['test_mae'][m] for m in models],
        name='Test MAE',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title='MAE par modèle (Test Set)',
        xaxis_title='Modèle',
        yaxis_title='MAE (picks)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Best model
    best = results['best_model']
    st.info(f"🏆 Meilleur modèle: **{best}**")

def display_predictions_analysis(predictions, results):
    """Display predictions analysis"""
    st.markdown("### 📈 Analyse des prédictions")
    
    errors = results['errors_analysis']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Erreur médiane", f"{errors['median_error']:.2f} picks")
    with col2:
        st.metric("Erreur max", f"{errors['max_error']:.2f} picks")
    with col3:
        st.metric("Top 5 accuracy", f"{errors['top5_accuracy']*100:.1f}%")
    
    # Scatter plot
    st.markdown("#### Prédictions vs Réalité")
    
    fig = go.Figure()
    
    # Perfect line
    fig.add_trace(go.Scatter(
        x=[1, 60],
        y=[1, 60],
        mode='lines',
        name='Prédiction parfaite',
        line=dict(color='red', dash='dash')
    ))
    
    # Predictions
    fig.add_trace(go.Scatter(
        x=predictions['draft_rank'],
        y=predictions['predicted_rank_ensemble'],
        mode='markers',
        name='Prédictions',
        marker=dict(
            size=8,
            color=predictions['prediction_error'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Erreur")
        ),
        text=predictions['name'] if 'name' in predictions.columns else None,
        hovertemplate='<b>%{text}</b><br>Réel: %{x}<br>Prédit: %{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title="Draft Rank réel",
        yaxis_title="Draft Rank prédit",
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top/Worst predictions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Top 5 meilleures")
        best = predictions.nsmallest(5, 'prediction_error')
        for _, row in best.iterrows():
            st.text(f"{row.get('name', 'N/A')}: {row['prediction_error']:.1f}")
    
    with col2:
        st.markdown("#### ❌ Top 5 pires")
        worst = predictions.nlargest(5, 'prediction_error')
        for _, row in worst.iterrows():
            st.text(f"{row.get('name', 'N/A')}: {row['prediction_error']:.1f}")

def display_feature_importance(feature_importance):
    """Display feature importance"""
    st.markdown("### 🔍 Importance des features")
    
    # Convert to dataframe
    df_imp = pd.DataFrame(feature_importance)
    
    # Top 15
    top15 = df_imp.head(15)
    
    fig = go.Figure(go.Bar(
        x=top15['importance'],
        y=top15['feature'],
        orientation='h',
        marker=dict(
            color=top15['importance'],
            colorscale='Blues'
        )
    ))
    
    fig.update_layout(
        title='Top 15 features les plus importantes',
        xaxis_title='Importance',
        yaxis_title='Feature',
        height=600,
        yaxis=dict(autorange="reversed")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Check dominance
    top_importance = df_imp.iloc[0]['importance']
    top_feature = df_imp.iloc[0]['feature']
    
    if top_importance > 0.5:
        st.error(f"⚠️ Feature ultra-dominante: **{top_feature}** ({top_importance:.1%})")
    elif top_importance > 0.3:
        st.warning(f"⚠️ Feature très dominante: **{top_feature}** ({top_importance:.1%})")
    else:
        st.success(f"✅ Distribution équilibrée (top feature: {top_importance:.1%})")

def display_model_info(results, features):
    """Display model information"""
    st.markdown("### ℹ️ Informations du modèle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Configuration**")
        st.text(f"Version: {results['model_version']}")
        st.text(f"Type: {results['model_type']}")
        st.text(f"Joueurs: {results['n_players']}")
        st.text(f"Features: {results['n_features']}")
    
    with col2:
        st.markdown("**Ensemble**")
        weights = results['weights']
        for model, weight in weights.items():
            st.text(f"{model}: {weight:.1%}")
    
    # Tier performance
    if 'tier_performance' in results:
        st.markdown("#### Performance par tier")
        
        tiers = results['tier_performance']
        tier_data = []
        for tier_name, tier_info in tiers.items():
            tier_data.append({
                'Tier': tier_name,
                'Range': tier_info['range'],
                'MAE': tier_info['mae'],
                'Joueurs': tier_info['n_players']
            })
        
        df_tiers = pd.DataFrame(tier_data)
        st.dataframe(
            df_tiers.style.format({'MAE': '{:.2f}'}),
            use_container_width=True,
            hide_index=True
        )

# Fonction principale appelée depuis app.py
if __name__ == "__main__":
    # Pour tests
    show(None)
