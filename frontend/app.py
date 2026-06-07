
# ═══════════════════════════════════════════════════════════
# ESG Intelligence Platform — Frontend Streamlit
# Projet PFA 2025-2026 · ENSIAS
# Yasmine LAHYAN & Rim LAHRECH
# ═══════════════════════════════════════════════════════════
 
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import random
 
# ───────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Intelligence Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
BACKEND_URL = "http://127.0.0.1:8000"
 
# ───────────────────────────────────────────────────────────
# DONNÉES DE RÉFÉRENCE
# ───────────────────────────────────────────────────────────
INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Energy",
    "Consumer Goods", "Industrials", "Utilities",
    "Real Estate", "Telecommunications", "Materials",
    "Transportation",
]
REGIONS = [
    "North America", "Europe", "Asia-Pacific",
    "Middle East & Africa", "Latin America",
]
 
CLASS_INFO = {
    0: {"label": "Très faible", "color": "#dc2626", "bg": "#fef2f2", "icon": "🔴", "range": "< 30"},
    1: {"label": "Faible",      "color": "#ea580c", "bg": "#fff7ed", "icon": "🟠", "range": "30 – 45"},
    2: {"label": "Moyen",       "color": "#ca8a04", "bg": "#fefce8", "icon": "🟡", "range": "45 – 60"},
    3: {"label": "Bon",         "color": "#16a34a", "bg": "#f0fdf4", "icon": "🟢", "range": "60 – 75"},
    4: {"label": "Excellent",   "color": "#15803d", "bg": "#ecfdf5", "icon": "🌟", "range": "≥ 75"},
}
 
# Mapping pour gérer l'encodage cassé de Rim
LABEL_TO_CLASS = {
    "Très faible": 0, "TrÃ¨s faible": 0,
    "Faible": 1, "Moyen": 2, "Bon": 3, "Excellent": 4,
}
 
# Distribution approximative du dataset pour les percentiles
CLASS_DISTRIBUTION = {
    0: 0.07,   # 7% des entreprises
    1: 0.14,   # 14%
    2: 0.29,   # 29%
    3: 0.32,   # 32%
    4: 0.18,   # 18%
}
 
 
# ───────────────────────────────────────────────────────────
# CSS — Minimaliste, Lisible, Bon contraste
# ───────────────────────────────────────────────────────────
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
 
    /* ── Base ── */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #fafafa !important;
        color: #171717 !important;
    }
    #MainMenu, footer, header {visibility: hidden;}
 
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e5e5 !important;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #404040 !important;
    }
    section[data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.6rem 1rem !important;
        border-radius: 8px !important;
        margin-bottom: 0.2rem !important;
        font-size: 0.95rem !important;
        color: #404040 !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background-color: #f0faf4 !important;
    }
    section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background-color: #d1f2e0 !important;
        color: #1a3a2b !important;
        font-weight: 600 !important;
    }
 
    /* ── Typographie ── */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #171717 !important;
        letter-spacing: -0.03em !important;
    }
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #262626 !important;
        letter-spacing: -0.02em !important;
    }
    h3 {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #262626 !important;
    }
    p, li, .stMarkdown {
        font-size: 0.95rem !important;
        color: #404040 !important;
        line-height: 1.65 !important;
    }
 
    /* ── Boutons ── */
    .stButton > button {
        background-color: #16a34a !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #15803d !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(22, 163, 74, 0.3) !important;
    }
 
    /* ── Inputs ── */
    .stNumberInput input, .stSelectbox > div > div,
    .stTextInput input {
        border-radius: 8px !important;
        border: 1.5px solid #d4d4d4 !important;
        font-family: 'Inter', sans-serif !important;
        color: #171717 !important;
        font-size: 0.95rem !important;
    }
    label {
        color: #404040 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }
 
    /* ── Cartes ── */
    .card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.8rem;
        border: 1px solid #e5e5e5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    .card-header {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #737373;
        font-weight: 600;
        margin-bottom: 0.6rem;
    }
 
    /* ── Métrique ── */
    .stat-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.4rem;
        border: 1px solid #e5e5e5;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #16a34a;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.78rem;
        color: #737373;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.4rem;
        font-weight: 500;
    }
 
    /* ── Score résultat ── */
    .result-score {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0.5rem 0;
    }
    .result-subtitle {
        font-size: 1rem;
        color: #525252;
        font-weight: 400;
    }
 
    /* ── Info box ── */
    .info-box {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        border-radius: 0 10px 10px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #14532d;
        font-size: 0.92rem;
        line-height: 1.6;
    }
 
    /* ── Model card ── */
    .model-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #e5e5e5;
        text-align: center;
        transition: transform 0.15s ease;
    }
    .model-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .model-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #262626;
        margin-bottom: 0.4rem;
    }
    .model-accuracy {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
    }
    .model-badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
 
    /* ── Feature tag ── */
    .feature-tag {
        display: inline-block;
        background: #f0fdf4;
        color: #14532d;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.2rem;
        border: 1px solid #d1f2e0;
    }
 
    /* ── Divider ── */
    .divider {
        height: 1px;
        background: #e5e5e5;
        margin: 2rem 0;
        border: none;
    }
 
    /* ── Percentile bar ── */
    .percentile-bar-bg {
        background: #f0f0f0;
        border-radius: 10px;
        height: 24px;
        position: relative;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    .percentile-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.8s ease;
    }
    .percentile-text {
        font-size: 1.3rem;
        font-weight: 700;
        color: #171717;
    }
    </style>
    """, unsafe_allow_html=True)
 
 
# ───────────────────────────────────────────────────────────
# UTILITAIRES
# ───────────────────────────────────────────────────────────
 
def get_percentile(prediction):
    """Calcule le percentile approximatif basé sur la distribution."""
    # Somme les % des classes en dessous + moitié de la classe actuelle
    below = sum(CLASS_DISTRIBUTION[i] for i in range(prediction))
    current = CLASS_DISTRIBUTION[prediction]
    percentile = (below + current / 2) * 100
    return round(percentile)
 
 
def get_companies_comparison(prediction):
    """Retourne des stats de comparaison simulées."""
    below = sum(CLASS_DISTRIBUTION[i] for i in range(prediction)) * 100
    same = CLASS_DISTRIBUTION[prediction] * 100
    above = sum(CLASS_DISTRIBUTION[i] for i in range(prediction + 1, 5)) * 100
    return round(below), round(same), round(above)
 
 
# ───────────────────────────────────────────────────────────
# GRAPHIQUES
# ───────────────────────────────────────────────────────────
 
def create_scale_chart(prediction):
    """Échelle visuelle avec la position du score."""
    fig = go.Figure()
 
    for i in range(5):
        info = CLASS_INFO[i]
        fig.add_trace(go.Bar(
            x=[1], y=[info["label"]],
            orientation="h",
            marker=dict(
                color=info["color"],
                opacity=1.0 if i == prediction else 0.12,
                line=dict(width=2, color=info["color"]) if i == prediction else dict(width=0),
            ),
            showlegend=False,
            hoverinfo="skip",
        ))
 
    # Flèche pour indiquer la position
    fig.add_annotation(
        x=1.15, y=CLASS_INFO[prediction]["label"],
        text=f"◀  Votre entreprise",
        showarrow=False,
        font=dict(size=13, color=CLASS_INFO[prediction]["color"],
                  family="Inter", weight=700),
        xanchor="left",
    )
 
    fig.update_layout(
        height=230,
        margin=dict(l=5, r=140, t=5, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, 1.6]),
        yaxis=dict(autorange="reversed",
                   tickfont=dict(family="Inter", size=13, color="#404040")),
        bargap=0.35,
    )
    return fig
 
 
def create_percentile_chart(prediction):
    """Graphique montrant la position en percentile parmi toutes les entreprises."""
    percentile = get_percentile(prediction)
    color = CLASS_INFO[prediction]["color"]
 
    fig = go.Figure()
 
    # Barre de distribution
    positions = []
    for i in range(5):
        start = sum(CLASS_DISTRIBUTION[j] for j in range(i)) * 100
        width = CLASS_DISTRIBUTION[i] * 100
        opacity = 0.9 if i == prediction else 0.15
        fig.add_shape(
            type="rect",
            x0=start, x1=start + width, y0=0, y1=1,
            fillcolor=CLASS_INFO[i]["color"],
            opacity=opacity,
            line=dict(width=0),
            layer="below",
        )
        positions.append((start, width, CLASS_INFO[i]["label"]))
 
    # Marqueur de position
    fig.add_trace(go.Scatter(
        x=[percentile], y=[0.5],
        mode="markers+text",
        marker=dict(size=18, color=color, symbol="diamond",
                    line=dict(width=2, color="white")),
        text=[f"{percentile}e"],
        textposition="top center",
        textfont=dict(size=14, family="Inter", color=color, weight=700),
        showlegend=False,
        hoverinfo="skip",
    ))
 
    fig.update_layout(
        height=100,
        margin=dict(l=0, r=0, t=30, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            tickvals=[0, 25, 50, 75, 100],
            ticktext=["0%", "25%", "50%", "75%", "100%"],
            tickfont=dict(family="Inter", size=11, color="#a3a3a3"),
        ),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[-0.2, 1.5]),
    )
    return fig
 
 
def create_radar_chart(data):
    """Radar chart des données de l'entreprise."""
    # Normaliser les valeurs pour le radar (0-100)
    categories = ["Revenue", "Marge", "Capitalisation",
                   "Croissance", "CO₂ (inv.)", "Eau (inv.)", "Énergie (inv.)"]
 
    # Inversés pour les émissions (moins = mieux)
    max_vals = [100000, 50, 100000, 30, 200000, 500000, 500000]
    values = [
        min(data["Revenue"] / max_vals[0] * 100, 100),
        min(data["ProfitMargin"] / max_vals[1] * 100, 100),
        min(data["MarketCap"] / max_vals[2] * 100, 100),
        min(data["GrowthRate"] / max_vals[3] * 100, 100),
        max(100 - data["CarbonEmissions"] / max_vals[4] * 100, 0),
        max(100 - data["WaterUsage"] / max_vals[5] * 100, 0),
        max(100 - data["EnergyConsumption"] / max_vals[6] * 100, 0),
    ]
 
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(22, 163, 74, 0.1)",
        line=dict(color="#16a34a", width=2),
        marker=dict(size=6, color="#16a34a"),
    ))
 
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                            gridcolor="#e5e5e5"),
            angularaxis=dict(tickfont=dict(size=11, family="Inter", color="#404040"),
                             gridcolor="#e5e5e5"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        height=320,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
 
 
def create_model_comparison_chart():
    """Bar chart comparatif des modèles."""
    models = ["Random Forest", "KNN", "Rég. Logistique"]
    accuracy = [66.9, 65.6, 41.1]
    colors = ["#16a34a", "#86efac", "#d4d4d4"]
 
    fig = go.Figure(go.Bar(
        x=models, y=accuracy,
        marker_color=colors,
        text=[f"{a}%" for a in accuracy],
        textposition="outside",
        textfont=dict(family="Inter", size=14, color="#404040", weight=600),
        width=0.5,
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(family="Inter", size=13, color="#404040")),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", range=[0, 85],
                   tickfont=dict(family="Inter", size=11, color="#a3a3a3")),
    )
    return fig
 
 
def create_class_distribution_chart():
    """Distribution des 5 classes ESG dans le dataset."""
    classes = [CLASS_INFO[i]["label"] for i in range(5)]
    counts = [800, 1500, 3200, 3500, 2000]
    colors = [CLASS_INFO[i]["color"] for i in range(5)]
 
    fig = go.Figure(go.Bar(
        x=classes, y=counts,
        marker_color=colors,
        text=counts,
        textposition="outside",
        textfont=dict(family="Inter", size=13),
        width=0.55,
    ))
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(family="Inter", size=12, color="#404040")),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0",
                   tickfont=dict(family="Inter", size=11, color="#a3a3a3")),
    )
    return fig
 
 
# ───────────────────────────────────────────────────────────
# PAGE : ACCUEIL
# ───────────────────────────────────────────────────────────
def page_home():
    st.markdown("")
 
    # Hero
    col_spacer1, col_hero, col_spacer2 = st.columns([1, 3, 1])
    with col_hero:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem 0 1rem 0;">
            <div style="display:inline-block; background:#d1f2e0; color:#14532d;
                        padding:0.35rem 1.2rem; border-radius:20px; font-size:0.82rem;
                        font-weight:600; letter-spacing:0.04em; margin-bottom:1.5rem;">
                🌿 PFA 2025-2026 · ENSIAS
            </div>
            <h1 style="font-size:3.2rem !important; letter-spacing:-0.04em !important;
                       margin-bottom:0.3rem !important;">
                ESG Intelligence Platform
            </h1>
            <p style="font-size:1.15rem !important; color:#737373 !important;
                      font-weight:300 !important; max-width:550px; margin:0 auto;
                      line-height:1.7 !important;">
                Prédiction intelligente des scores ESG d'entreprises
                grâce au Machine Learning — Random Forest, KNN
                et Régression Logistique.
            </p>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("")
 
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("11 000+", "Entreprises"),
        ("27", "Variables"),
        ("66.9%", "Précision"),
        ("5", "Classes ESG"),
    ]
    for col, (num, lbl) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # 3 étapes
    col1, col2, col3 = st.columns(3)
    steps = [
        ("01", "Saisie des données",
         "Renseignez les indicateurs financiers et environnementaux "
         "de l'entreprise à analyser."),
        ("02", "Analyse par le modèle",
         "Le Random Forest traite 17 variables et "
         "calcule les features engineered automatiquement."),
        ("03", "Score et positionnement",
         "Obtenez la classe ESG prédite et découvrez "
         "où l'entreprise se situe parmi 11 000 autres."),
    ]
    for col, (num, title, desc) in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
            <div class="card">
                <div style="font-size:2rem; font-weight:800; color:#d1f2e0;
                            margin-bottom:0.5rem;">{num}</div>
                <div style="font-size:1.05rem; font-weight:600; color:#171717;
                            margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.88rem; color:#525252; line-height:1.6;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown("""
    <div style="text-align:center; margin-top:2rem;">
        <p style="color:#737373 !important; font-size:0.9rem !important;">
            👈 Utilisez le menu latéral pour accéder à la <b>Prédiction</b>
            ou au <b>Dashboard</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
 
 
# ───────────────────────────────────────────────────────────
# PAGE : PRÉDICTION
# ───────────────────────────────────────────────────────────
def page_predict():
    st.markdown("## 🔍 Prédiction ESG")
    st.markdown(
        "Renseignez les données de l'entreprise ci-dessous. "
        "Le modèle calcule automatiquement les features engineered "
        "(intensités, taille, efficacité) avant de prédire."
    )
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    with st.form("prediction_form"):
 
        # ── Infos générales ──
        st.markdown("##### Informations générales")
        col1, col2, col3 = st.columns(3)
        with col1:
            industry = st.selectbox("Secteur d'activité", INDUSTRIES)
        with col2:
            region = st.selectbox("Région", REGIONS)
        with col3:
            year = st.number_input("Année", min_value=2015,
                                   max_value=2026, value=2024, step=1)
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        # ── Financier ──
        st.markdown("##### Données financières")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            revenue = st.number_input("Revenue ($M)",
                                      min_value=0.0, value=5000.0, step=100.0)
        with col2:
            profit_margin = st.number_input("Marge bénéficiaire (%)",
                                            value=15.0, step=0.5)
        with col3:
            market_cap = st.number_input("Capitalisation ($M)",
                                         min_value=0.0, value=20000.0, step=500.0)
        with col4:
            growth_rate = st.number_input("Taux de croissance (%)",
                                          value=5.0, step=0.5)
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        # ── Environnemental ──
        st.markdown("##### Données environnementales")
        col1, col2, col3 = st.columns(3)
        with col1:
            carbon = st.number_input("Émissions CO₂ (tonnes)",
                                     min_value=0.0, value=50000.0, step=1000.0)
        with col2:
            water = st.number_input("Consommation d'eau (m³)",
                                    min_value=0.0, value=100000.0, step=5000.0)
        with col3:
            energy = st.number_input("Énergie consommée (MWh)",
                                     min_value=0.0, value=200000.0, step=5000.0)
 
        st.markdown("")
        submitted = st.form_submit_button(
            "🔍  Analyser le score ESG", use_container_width=True)
 
    # ── Résultats ──
    if submitted:
        payload = {
            "Revenue": revenue, "ProfitMargin": profit_margin,
            "MarketCap": market_cap, "GrowthRate": growth_rate,
            "CarbonEmissions": carbon, "WaterUsage": water,
            "EnergyConsumption": energy, "Industry": industry,
            "Region": region, "Year": float(year),
        }
 
        with st.spinner("Analyse en cours..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/predict",
                                     json=payload, timeout=30)
                result = resp.json()
 
                if resp.status_code == 200:
                    raw_label = result["label"]
                    pred = LABEL_TO_CLASS.get(raw_label, result.get("prediction", 2))
                    info = CLASS_INFO[pred]
                    percentile = get_percentile(pred)
                    below, same, above = get_companies_comparison(pred)
 
                    st.markdown('<div class="divider"></div>',
                                unsafe_allow_html=True)
 
                    # ── Score principal ──
                    st.markdown("## Résultat de l'analyse")
                    col_score, col_scale = st.columns([1, 1])
 
                    with col_score:
                        st.markdown(f"""
                        <div class="card" style="text-align:center;
                                    border-left: 5px solid {info['color']};">
                            <div class="card-header">Score ESG prédit</div>
                            <div class="result-score" style="color:{info['color']};">
                                {info['icon']} {info['label']}
                            </div>
                            <div class="result-subtitle">
                                Plage ESG : {info['range']} / 100
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
 
                    with col_scale:
                        st.markdown("""
                        <div class="card">
                            <div class="card-header">Position sur l'échelle</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.plotly_chart(create_scale_chart(pred),
                                        use_container_width=True)
 
                    # ── Percentile ──
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-header">
                            Positionnement parmi 11 000 entreprises
                        </div>
                        <div style="display:flex; align-items:baseline; gap:0.8rem;
                                    margin-bottom:0.5rem;">
                            <span class="percentile-text">
                                {percentile}e percentile
                            </span>
                            <span style="color:#737373; font-size:0.9rem;">
                                — Cette entreprise fait mieux que
                                <b style="color:#171717;">{below}%</b> des
                                entreprises du dataset
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
 
                    st.plotly_chart(create_percentile_chart(pred),
                                    use_container_width=True)
 
                    # ── Comparaison ──
                    col1, col2, col3 = st.columns(3)
                    comparisons = [
                        (f"{below}%", "Font moins bien", "#ef4444", "#fef2f2"),
                        (f"{same}%", "Même catégorie", info["color"], info["bg"]),
                        (f"{above}%", "Font mieux", "#16a34a", "#f0fdf4"),
                    ]
                    for col, (val, lbl, clr, bg) in zip(
                        [col1, col2, col3], comparisons
                    ):
                        with col:
                            st.markdown(f"""
                            <div class="stat-card" style="border-top: 3px solid {clr};
                                        background: {bg};">
                                <div class="stat-number" style="color:{clr};">
                                    {val}
                                </div>
                                <div class="stat-label">{lbl}</div>
                            </div>
                            """, unsafe_allow_html=True)
 
                    st.markdown("")
 
                    # ── Radar ──
                    st.markdown("""
                    <div class="card">
                        <div class="card-header">Profil de l'entreprise</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.plotly_chart(create_radar_chart(payload),
                                    use_container_width=True)
 
                    # ── Détails ──
                    with st.expander("📋 Données envoyées au modèle"):
                        dc1, dc2, dc3 = st.columns(3)
                        with dc1:
                            st.markdown("**Général**")
                            st.markdown(f"Secteur : {industry}")
                            st.markdown(f"Région : {region}")
                            st.markdown(f"Année : {year}")
                        with dc2:
                            st.markdown("**Financier**")
                            st.markdown(f"Revenue : ${revenue:,.0f}M")
                            st.markdown(f"Marge : {profit_margin}%")
                            st.markdown(f"Cap. : ${market_cap:,.0f}M")
                            st.markdown(f"Croissance : {growth_rate}%")
                        with dc3:
                            st.markdown("**Environnemental**")
                            st.markdown(f"CO₂ : {carbon:,.0f} t")
                            st.markdown(f"Eau : {water:,.0f} m³")
                            st.markdown(f"Énergie : {energy:,.0f} MWh")
 
                else:
                    st.error(f"Erreur : {result.get('detail', 'Inconnue')}")
 
            except requests.exceptions.ConnectionError:
                st.error(
                    "⚠️ Connexion impossible au backend. "
                    "Vérifie que FastAPI tourne sur http://127.0.0.1:8000\n\n"
                    "Commande : `cd backendrim/backend && uvicorn app:app --reload`"
                )
            except Exception as e:
                st.error(f"Erreur : {str(e)}")
 
 
# ───────────────────────────────────────────────────────────
# PAGE : DASHBOARD — MODÈLES & DONNÉES
# ───────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown("## 📈 Dashboard — Modèles & Données")
    st.markdown(
        "Vue d'ensemble de la méthodologie, des modèles entraînés "
        "et des données utilisées."
    )
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ══════════ Section 1 : Pourquoi ces modèles ? ══════════
    st.markdown("### 🤖 Pourquoi ces trois modèles ?")
 
    st.markdown("""
    <div class="info-box">
        Le choix des modèles repose sur un critère clé : la <b>classification
        multi-classes</b> avec des données tabulaires mixtes (numériques +
        catégorielles). Les trois algorithmes testés offrent des approches
        complémentaires.
    </div>
    """, unsafe_allow_html=True)
 
    col1, col2, col3 = st.columns(3)
 
    with col1:
        st.markdown(f"""
        <div class="model-card">
            <div style="font-size:2rem; margin-bottom:0.5rem;">🌲</div>
            <div class="model-name">Random Forest</div>
            <div class="model-accuracy" style="color:#16a34a;">66.9%</div>
            <div class="model-badge"
                 style="background:#d1f2e0; color:#14532d;">
                ✅ MODÈLE RETENU
            </div>
            <div style="text-align:left; margin-top:1rem; font-size:0.85rem;
                        color:#525252; line-height:1.6;">
                Ensemble de 100 arbres de décision.
                Robuste au bruit, gère naturellement les features
                non-linéaires et les interactions. Pas de
                normalisation requise.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    with col2:
        st.markdown(f"""
        <div class="model-card">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📐</div>
            <div class="model-name">K-Nearest Neighbors</div>
            <div class="model-accuracy" style="color:#737373;">65.6%</div>
            <div class="model-badge"
                 style="background:#f5f5f5; color:#737373;">
                COMPARABLE
            </div>
            <div style="text-align:left; margin-top:1rem; font-size:0.85rem;
                        color:#525252; line-height:1.6;">
                Classifie par similarité avec les K voisins
                les plus proches. Simple et intuitif,
                mais sensible à la dimensionnalité
                et au scaling des variables.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    with col3:
        st.markdown(f"""
        <div class="model-card">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📊</div>
            <div class="model-name">Régression Logistique</div>
            <div class="model-accuracy" style="color:#d4d4d4;">41.1%</div>
            <div class="model-badge"
                 style="background:#fef2f2; color:#dc2626;">
                INSUFFISANT
            </div>
            <div style="text-align:left; margin-top:1rem; font-size:0.85rem;
                        color:#525252; line-height:1.6;">
                Modèle linéaire étendu à la multi-classe.
                Performant quand les relations sont
                linéaires, mais les interactions complexes
                du scoring ESG le limitent ici.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ══════════ Section 2 : Comparaison graphique ══════════
    st.markdown("### 📊 Comparaison des performances")
 
    col_chart, col_explain = st.columns([1.2, 1])
 
    with col_chart:
        st.plotly_chart(create_model_comparison_chart(),
                        use_container_width=True)
 
    with col_explain:
        st.markdown("""
        <div class="card">
            <div class="card-header">Pourquoi Random Forest gagne ?</div>
            <div style="font-size:0.9rem; color:#404040; line-height:1.7;">
                <b>1. Relations non-linéaires</b> — Le score ESG dépend
                d'interactions complexes entre les variables financières
                et environnementales.<br><br>
                <b>2. Robustesse</b> — Le bagging (bootstrap aggregating)
                réduit la variance et l'overfitting.<br><br>
                <b>3. class_weight='balanced'</b> — Compense le déséquilibre
                des classes dans le dataset.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ══════════ Section 3 : Dataset ══════════
    st.markdown("### 📁 Le Dataset")
 
    col1, col2, col3 = st.columns(3)
    ds_stats = [
        ("11 000", "Lignes"),
        ("27", "Colonnes"),
        ("310", "Entreprises réelles"),
    ]
    for col, (num, lbl) in zip([col1, col2, col3], ds_stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown("")
 
    col_dist, col_info = st.columns([1.2, 1])
 
    with col_dist:
        st.markdown("**Distribution des classes ESG**")
        st.plotly_chart(create_class_distribution_chart(),
                        use_container_width=True)
 
    with col_info:
        st.markdown("""
        <div class="card">
            <div class="card-header">Les 5 classes ESG</div>
        </div>
        """, unsafe_allow_html=True)
 
        for i in range(5):
            info = CLASS_INFO[i]
            pct = int(CLASS_DISTRIBUTION[i] * 100)
            st.markdown(f"""
            <div style="display:flex; align-items:center; padding:0.5rem 0.8rem;
                        margin:0.3rem 0; border-radius:8px; background:{info['bg']};">
                <span style="font-size:1.1rem; margin-right:0.6rem;">
                    {info['icon']}
                </span>
                <span style="font-weight:600; color:{info['color']};
                             font-size:0.9rem; min-width:100px;">
                    {info['label']}
                </span>
                <span style="color:#737373; font-size:0.82rem;">
                    Score {info['range']} — {pct}% du dataset
                </span>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ══════════ Section 4 : Feature Engineering ══════════
    st.markdown("### ⚙️ Feature Engineering")
    st.markdown(
        "Le modèle utilise 17 variables en entrée. "
        "En plus des données brutes, le backend calcule "
        "automatiquement des features dérivées :"
    )
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">Variables d'entrée (saisie utilisateur)</div>
        </div>
        """, unsafe_allow_html=True)
        raw_features = [
            "Revenue", "ProfitMargin", "MarketCap", "GrowthRate",
            "CarbonEmissions", "WaterUsage", "EnergyConsumption",
            "Industry", "Region", "Year",
        ]
        tags = "".join(
            f'<span class="feature-tag">{f}</span>' for f in raw_features
        )
        st.markdown(tags, unsafe_allow_html=True)
 
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-header">Features calculées (automatique)</div>
        </div>
        """, unsafe_allow_html=True)
        eng_features = {
            "Profit_Growth": "GrowthRate × ProfitMargin",
            "Size": "log(1 + MarketCap)",
            "Efficiency": "Revenue / (Energy + 1)",
            "Year_norm": "Year / 2025",
            "Revenue_growth": "Revenue × GrowthRate",
            "ESG_Avg": "Moyenne CO₂, Eau, Énergie",
            "ESG_Std": "Écart-type CO₂, Eau, Énergie",
            "Industry_enc": "LabelEncoder",
            "Region_enc": "LabelEncoder",
        }
        for feat, formula in eng_features.items():
            st.markdown(
                f'<span class="feature-tag">{feat}</span> '
                f'<span style="color:#a3a3a3; font-size:0.8rem;">= {formula}</span>',
                unsafe_allow_html=True,
            )
 
    # ══════════ Section 5 : Pipeline ══════════
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🔧 Pipeline ML")
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="display:flex; justify-content:center; align-items:center;
                    flex-wrap:wrap; gap:0.5rem; font-size:0.9rem;">
            <span style="background:#d1f2e0; color:#14532d; padding:0.5rem 1rem;
                         border-radius:8px; font-weight:600;">
                📥 Données brutes
            </span>
            <span style="color:#a3a3a3; font-size:1.2rem;">→</span>
            <span style="background:#dbeafe; color:#1e40af; padding:0.5rem 1rem;
                         border-radius:8px; font-weight:600;">
                🔧 Feature Engineering
            </span>
            <span style="color:#a3a3a3; font-size:1.2rem;">→</span>
            <span style="background:#fef3c7; color:#92400e; padding:0.5rem 1rem;
                         border-radius:8px; font-weight:600;">
                📏 StandardScaler
            </span>
            <span style="color:#a3a3a3; font-size:1.2rem;">→</span>
            <span style="background:#fce7f3; color:#9d174d; padding:0.5rem 1rem;
                         border-radius:8px; font-weight:600;">
                🌲 Random Forest
            </span>
            <span style="color:#a3a3a3; font-size:1.2rem;">→</span>
            <span style="background:#d1f2e0; color:#14532d; padding:0.5rem 1rem;
                         border-radius:8px; font-weight:600;">
                🎯 Classe ESG
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
 
# ───────────────────────────────────────────────────────────
# APPLICATION PRINCIPALE
# ───────────────────────────────────────────────────────────
def main():
    load_css()
 
    # ── Sidebar Navigation ──
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:1rem 0;">
            <div style="font-size:1.6rem; font-weight:700; color:#171717;
                        letter-spacing:-0.03em;">
                🌿 ESG
            </div>
            <div style="font-size:0.75rem; color:#a3a3a3; font-weight:400;
                        letter-spacing:0.04em;">
                INTELLIGENCE PLATFORM
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        page = st.radio(
            "Navigation",
            ["🏠  Accueil", "🔍  Prédiction", "📈  Dashboard"],
            label_visibility="collapsed",
        )
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        st.markdown("""
        <div style="font-size:0.75rem; color:#a3a3a3; text-align:center;
                    line-height:1.6; padding-top:1rem;">
            PFA 2025-2026 · ENSIAS<br>
            Yasmine LAHYAN<br>
            Rim LAHRECH<br><br>
            Encadrée par<br>
            <b style="color:#737373;">Mme Nabila HAMDOUN</b>
        </div>
        """, unsafe_allow_html=True)
 
    # ── Routage ──
    if "Accueil" in page:
        page_home()
    elif "Prédiction" in page:
        page_predict()
    elif "Dashboard" in page:
        page_dashboard()
 
 
if __name__ == "__main__":
    main() 