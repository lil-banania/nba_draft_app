import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Résultats ML - NBA Draft 2025", page_icon="🤖", layout="wide")

# Titre
st.title("🤖 Résultats du Modèle ML - NBA Draft 2025")
st.markdown("---")

# Charger les résultats
@st.cache_data
def load_results():
    """Charge les résultats du modèle"""
    try:
        with open('nba_draft_results.json', 'r') as f:
            results = json.load(f)
        return results
    except FileNotFoundError:
        st.error("❌ Fichier de résultats introuvable. Exécutez d'abord le modèle.")
        return None

@st.cache_data
def load_predictions():
    """Charge les prédictions complètes"""
    try:
        df = pd.read_csv('nba_draft_predictions.csv')
        return df
    except FileNotFoundError:
        st.warning("⚠️ Fichier de prédictions introuvable.")
        return None

@st.cache_data
def load_features():
    """Charge la liste des features"""
    try:
        with open('nba_draft_features.json', 'r') as f:
            features = json.load(f)
        return features
    except FileNotFoundError:
        return None

# Charger les données
results = load_results()
predictions = load_predictions()
features_data = load_features()

if results is None:
    st.stop()

# Sidebar - Informations du modèle
with st.sidebar:
    st.header("ℹ️ Informations")
    st.metric("Version", results['model_version'])
    st.metric("Type", results['model_type'].capitalize())
    st.metric("Meilleur modèle", results['best_model'])
    st.metric("Joueurs analysés", results['n_players'])
    st.metric("Features utilisées", results['n_features'])
    
    st.markdown("---")
    st.markdown("### 🎯 Objectif")
    st.markdown("""
    Ce modèle prédit le **draft rank** (position 1-60) de chaque joueur 
    en se basant uniquement sur des **données observables** :
    - Stats college
    - Évaluations scouting
    - Mesures physiques
    - Feature engineering
    """)

# Onglets principaux
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble",
    "🎯 Performance",
    "📈 Prédictions",
    "🔍 Feature Importance",
    "📋 Données détaillées"
])

# TAB 1: VUE D'ENSEMBLE
with tab1:
    st.header("📊 Vue d'ensemble des résultats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    perf = results['performance']
    errors = results['errors_analysis']
    
    with col1:
        st.metric(
            "MAE Ensemble",
            f"{perf['ensemble_mae']:.2f} picks",
            help="Mean Absolute Error - Erreur moyenne de prédiction"
        )
    
    with col2:
        st.metric(
            "RMSE",
            f"{perf['ensemble_rmse']:.2f} picks",
            help="Root Mean Squared Error - Pénalise les grosses erreurs"
        )
    
    with col3:
        st.metric(
            "R²",
            f"{perf['ensemble_r2']:.3f}",
            help="Coefficient de détermination - Part de variance expliquée"
        )
    
    with col4:
        st.metric(
            "Spearman",
            f"{perf['ensemble_spearman']:.3f}",
            help="Corrélation de rang - Mesure la qualité du ranking"
        )
    
    st.markdown("---")
    
    # Interprétation
    st.subheader("💡 Interprétation")
    
    mae = perf['ensemble_mae']
    spearman = perf['ensemble_spearman']
    
    # Verdict basé sur MAE
    if mae < 5:
        verdict_color = "green"
        verdict_text = "🟢 EXCELLENT"
        verdict_detail = "Prédictions très précises!"
    elif mae < 8:
        verdict_color = "blue"
        verdict_text = "🟡 BON"
        verdict_detail = "Prédictions fiables"
    elif mae < 12:
        verdict_color = "orange"
        verdict_text = "🟠 CORRECT"
        verdict_detail = "Prédictions acceptables"
    else:
        verdict_color = "red"
        verdict_text = "🔴 FAIBLE"
        verdict_detail = "Modèle à améliorer"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### Performance globale: {verdict_text}")
        st.markdown(f"*{verdict_detail}*")
        st.markdown(f"""
        - **Erreur moyenne:** {mae:.1f} picks
        - **Erreur médiane:** {errors['median_error']:.1f} picks
        - **Erreur max:** {errors['max_error']:.1f} picks
        """)
    
    with col2:
        # Verdict basé sur Spearman
        if spearman > 0.7:
            st.success(f"✅ **Excellente corrélation de rang** (Spearman = {spearman:.3f})")
            st.markdown("Le modèle range très bien les joueurs, même si les valeurs exactes ont une marge d'erreur.")
        elif spearman > 0.5:
            st.info(f"✅ **Bonne corrélation de rang** (Spearman = {spearman:.3f})")
        else:
            st.warning(f"⚠️ **Corrélation de rang modérée** (Spearman = {spearman:.3f})")
    
    st.markdown("---")
    
    # Précision par tier
    st.subheader("🎯 Précision par tier de draft")
    
    tier_data = results['tier_performance']
    
    if tier_data:
        cols = st.columns(len(tier_data))
        
        for idx, (tier_name, tier_info) in enumerate(tier_data.items()):
            with cols[idx]:
                st.metric(
                    f"{tier_name}",
                    f"{tier_info['mae']:.2f} picks",
                    delta=None,
                    help=f"Picks {tier_info['range']} ({tier_info['n_players']} joueurs)"
                )
        
        st.markdown("""
        **Note:** Il est normal que les lottery picks (1-10) soient plus difficiles à prédire 
        car ils dépendent fortement des besoins des équipes et du talent "upside" difficile à quantifier.
        """)

# TAB 2: PERFORMANCE
with tab2:
    st.header("🎯 Performance des modèles")
    
    # Comparaison des modèles
    st.subheader("📊 Comparaison des modèles individuels")
    
    model_names = list(perf['cv_mae_mean'].keys())
    
    comparison_data = {
        'Modèle': model_names,
        'CV MAE': [perf['cv_mae_mean'][name] for name in model_names],
        'CV Std': [perf['cv_mae_std'][name] for name in model_names],
        'Test MAE': [perf['test_mae'][name] for name in model_names],
        'Test RMSE': [perf['test_rmse'][name] for name in model_names],
        'R²': [perf['test_r2'][name] for name in model_names],
        'Spearman': [perf['test_spearman'][name] for name in model_names],
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Styliser le DataFrame
    st.dataframe(
        df_comparison.style.format({
            'CV MAE': '{:.2f}',
            'CV Std': '{:.2f}',
            'Test MAE': '{:.2f}',
            'Test RMSE': '{:.2f}',
            'R²': '{:.3f}',
            'Spearman': '{:.3f}',
        }).background_gradient(subset=['Test MAE'], cmap='RdYlGn_r'),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Visualisation des performances
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique MAE par modèle
        fig_mae = go.Figure()
        
        fig_mae.add_trace(go.Bar(
            x=model_names,
            y=[perf['cv_mae_mean'][name] for name in model_names],
            name='CV MAE',
            marker_color='lightblue',
            error_y=dict(
                type='data',
                array=[perf['cv_mae_std'][name] for name in model_names]
            )
        ))
        
        fig_mae.add_trace(go.Bar(
            x=model_names,
            y=[perf['test_mae'][name] for name in model_names],
            name='Test MAE',
            marker_color='darkblue'
        ))
        
        fig_mae.update_layout(
            title="MAE par modèle",
            xaxis_title="Modèle",
            yaxis_title="MAE (picks)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_mae, use_container_width=True)
    
    with col2:
        # Graphique Spearman par modèle
        fig_spearman = go.Figure()
        
        fig_spearman.add_trace(go.Bar(
            x=model_names,
            y=[perf['test_spearman'][name] for name in model_names],
            marker_color=['green' if s > 0.7 else 'orange' for s in [perf['test_spearman'][name] for name in model_names]]
        ))
        
        fig_spearman.add_hline(y=0.7, line_dash="dash", line_color="red", 
                               annotation_text="Seuil excellent (0.7)")
        
        fig_spearman.update_layout(
            title="Corrélation Spearman par modèle",
            xaxis_title="Modèle",
            yaxis_title="Spearman",
            height=400
        )
        
        st.plotly_chart(fig_spearman, use_container_width=True)
    
    st.markdown("---")
    
    # Poids de l'ensemble
    st.subheader("⚖️ Poids des modèles dans l'ensemble")
    
    weights = results['weights']
    
    fig_weights = go.Figure(data=[
        go.Pie(
            labels=list(weights.keys()),
            values=list(weights.values()),
            hole=0.3,
            textinfo='label+percent',
            marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        )
    ])
    
    fig_weights.update_layout(
        title="Contribution de chaque modèle à la prédiction finale",
        height=400
    )
    
    st.plotly_chart(fig_weights, use_container_width=True)
    
    st.info("""
    **ℹ️ Note:** Les poids sont calculés en fonction des performances en validation croisée. 
    Les modèles les plus performants ont un poids plus élevé dans la prédiction finale.
    """)

# TAB 3: PRÉDICTIONS
with tab3:
    st.header("📈 Analyse des prédictions")
    
    if predictions is not None:
        # Statistiques sur les erreurs
        st.subheader("📊 Distribution des erreurs")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Erreur médiane", f"{errors['median_error']:.2f} picks")
        with col2:
            st.metric("Erreur moyenne", f"{errors['mean_error']:.2f} picks")
        with col3:
            st.metric("Top 10 accuracy", f"{errors['top10_accuracy']*100:.1f}%")
        with col4:
            st.metric("Top 5 accuracy", f"{errors['top5_accuracy']*100:.1f}%")
        
        # Graphique scatter: Prédit vs Réel
        st.subheader("🎯 Prédictions vs Réalité")
        
        fig_scatter = go.Figure()
        
        # Ligne parfaite (y=x)
        fig_scatter.add_trace(go.Scatter(
            x=[1, 60],
            y=[1, 60],
            mode='lines',
            name='Prédiction parfaite',
            line=dict(color='red', dash='dash')
        ))
        
        # Prédictions
        fig_scatter.add_trace(go.Scatter(
            x=predictions['draft_rank'],
            y=predictions['predicted_rank_ensemble'],
            mode='markers',
            name='Prédictions',
            marker=dict(
                size=8,
                color=predictions['prediction_error'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Erreur"),
                line=dict(width=1, color='white')
            ),
            text=predictions['name'] if 'name' in predictions.columns else None,
            hovertemplate='<b>%{text}</b><br>Réel: %{x}<br>Prédit: %{y:.1f}<br>Erreur: %{marker.color:.1f}<extra></extra>'
        ))
        
        fig_scatter.update_layout(
            title="Prédictions vs Draft Rank réel",
            xaxis_title="Draft Rank réel",
            yaxis_title="Draft Rank prédit",
            height=600,
            hovermode='closest'
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Histogramme des erreurs
        st.subheader("📊 Distribution des erreurs de prédiction")
        
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Histogram(
            x=predictions['prediction_error'],
            nbinsx=20,
            marker_color='lightblue',
            marker_line_color='darkblue',
            marker_line_width=1
        ))
        
        fig_hist.update_layout(
            title="Fréquence des erreurs",
            xaxis_title="Erreur absolue (picks)",
            yaxis_title="Nombre de joueurs",
            height=400
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Meilleures et pires prédictions
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Top 5 meilleures prédictions")
            best_preds = predictions.nsmallest(5, 'prediction_error')
            
            for idx, row in best_preds.iterrows():
                with st.container():
                    st.markdown(f"""
                    **{row.get('name', f"Joueur #{idx}")}**  
                    Réel: `{row['draft_rank']:.0f}` | Prédit: `{row['predicted_rank_ensemble']:.1f}` | Erreur: `{row['prediction_error']:.1f}`
                    """)
        
        with col2:
            st.subheader("❌ Top 5 pires prédictions")
            worst_preds = predictions.nlargest(5, 'prediction_error')
            
            for idx, row in worst_preds.iterrows():
                with st.container():
                    st.markdown(f"""
                    **{row.get('name', f"Joueur #{idx}")}**  
                    Réel: `{row['draft_rank']:.0f}` | Prédit: `{row['predicted_rank_ensemble']:.1f}` | Erreur: `{row['prediction_error']:.1f}`
                    """)

# TAB 4: FEATURE IMPORTANCE
with tab4:
    st.header("🔍 Importance des features")
    
    feature_imp = pd.DataFrame(results['feature_importance'])
    
    st.subheader("🏆 Top 20 features les plus importantes")
    
    # Graphique horizontal
    top_features = feature_imp.head(20)
    
    fig_importance = go.Figure(go.Bar(
        x=top_features['importance'],
        y=top_features['feature'],
        orientation='h',
        marker=dict(
            color=top_features['importance'],
            colorscale='Blues',
            showscale=False
        )
    ))
    
    fig_importance.update_layout(
        title="Contribution de chaque feature au modèle",
        xaxis_title="Importance",
        yaxis_title="Feature",
        height=600,
        yaxis=dict(autorange="reversed")
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Analyse de la distribution
    st.markdown("---")
    st.subheader("📊 Distribution de l'importance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Top feature", feature_imp.iloc[0]['feature'])
        st.metric("Importance", f"{feature_imp.iloc[0]['importance']:.1%}")
        
        # Vérifier si dominante
        if feature_imp.iloc[0]['importance'] > 0.5:
            st.error("⚠️ Feature ultra-dominante (>50%) - Risque de surapprentissage")
        elif feature_imp.iloc[0]['importance'] > 0.3:
            st.warning("⚠️ Feature très dominante (>30%)")
        else:
            st.success("✅ Distribution équilibrée")
    
    with col2:
        # Top 3 features cumulées
        top3_cumul = feature_imp.head(3)['importance'].sum()
        st.metric("Top 3 features (cumulé)", f"{top3_cumul:.1%}")
        
        # Top 10 cumulé
        top10_cumul = feature_imp.head(10)['importance'].sum()
        st.metric("Top 10 features (cumulé)", f"{top10_cumul:.1%}")
    
    # Table complète
    st.markdown("---")
    st.subheader("📋 Table complète des features")
    
    st.dataframe(
        feature_imp.style.format({'importance': '{:.4f}'})
        .background_gradient(subset=['importance'], cmap='Blues'),
        use_container_width=True,
        height=400
    )

# TAB 5: DONNÉES DÉTAILLÉES
with tab5:
    st.header("📋 Données détaillées")
    
    if predictions is not None:
        st.subheader("🎯 Prédictions complètes")
        
        # Options de filtrage
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tier_filter = st.selectbox(
                "Filtrer par tier",
                ["Tous", "Lottery (1-10)", "First Round (11-30)", "Second Round (31-60)"]
            )
        
        with col2:
            error_threshold = st.slider(
                "Erreur max (picks)",
                0, int(predictions['prediction_error'].max()) + 1,
                int(predictions['prediction_error'].max()) + 1
            )
        
        with col3:
            sort_by = st.selectbox(
                "Trier par",
                ["Draft Rank", "Erreur (décroissant)", "Erreur (croissant)"]
            )
        
        # Appliquer les filtres
        filtered_df = predictions.copy()
        
        if tier_filter == "Lottery (1-10)":
            filtered_df = filtered_df[filtered_df['draft_rank'] <= 10]
        elif tier_filter == "First Round (11-30)":
            filtered_df = filtered_df[(filtered_df['draft_rank'] >= 11) & (filtered_df['draft_rank'] <= 30)]
        elif tier_filter == "Second Round (31-60)":
            filtered_df = filtered_df[filtered_df['draft_rank'] >= 31]
        
        filtered_df = filtered_df[filtered_df['prediction_error'] <= error_threshold]
        
        if sort_by == "Draft Rank":
            filtered_df = filtered_df.sort_values('draft_rank')
        elif sort_by == "Erreur (décroissant)":
            filtered_df = filtered_df.sort_values('prediction_error', ascending=False)
        else:
            filtered_df = filtered_df.sort_values('prediction_error')
        
        st.dataframe(
            filtered_df.style.format({
                'draft_rank': '{:.0f}',
                'predicted_rank_ensemble': '{:.1f}',
                'prediction_error': '{:.1f}'
            }).background_gradient(subset=['prediction_error'], cmap='RdYlGn_r'),
            use_container_width=True,
            height=600
        )
        
        # Téléchargement
        st.download_button(
            label="📥 Télécharger les prédictions (CSV)",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='nba_draft_predictions_filtered.csv',
            mime='text/csv'
        )
    
    # Liste des features utilisées
    if features_data:
        st.markdown("---")
        st.subheader("📝 Features utilisées dans le modèle")
        
        st.info(f"**{features_data['n_features']} features** au total")
        
        # Afficher en colonnes
        n_cols = 3
        cols = st.columns(n_cols)
        
        for idx, feature in enumerate(features_data['features']):
            with cols[idx % n_cols]:
                st.markdown(f"• `{feature}`")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🏀 NBA Draft 2025 - Modèle de Machine Learning v3 (Clean)</p>
    <p style='font-size: 0.8em; color: gray;'>
        Basé uniquement sur des données observables • Sans data leakage • 
        Features: Stats college + Scouting + Physique + Feature Engineering
    </p>
</div>
""", unsafe_allow_html=True)