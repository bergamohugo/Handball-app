import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="Handball Lab", layout="wide", initial_sidebar_state="collapsed")

# 2. BASE DE DONNÉES
if "db" not in st.session_state:
    st.session_state.db = {}
LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand"]

# 3. DESIGN "NEON SPORT" (Le gros changement est ici)
st.markdown("""
    <style>
    /* Fond dégradé sombre type salle de sport futuriste */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Masquer le surplus */
    header, footer, #MainMenu {visibility: hidden;}

    /* Titre Stylisé */
    .main-title {
        font-size: 40px;
        font-weight: 800;
        background: -webkit-linear-gradient(#06b6d4, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Cartes effet "Verre" (Glassmorphism) */
    div[data-testid="stVerticalBlock"] > div:has(div.stForm), .custom-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }

    /* Bouton type "Gaming" */
    .stButton>button {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        height: 3.5rem !important;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
    }

    /* Inputs et Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. NAVIGATION
page = st.sidebar.radio("Navigation", ["📝 Formulaire", "🔒 Coach"])

# --- INTERFACE JOUEUSE ---
if page == "📝 Formulaire":
    st.markdown('<p class="main-title">Performance Lab</p>', unsafe_allow_html=True)
    
    nom = st.selectbox("Qui es-tu ?", [""] + LISTE_JOUEUSES)
    
    if nom:
        with st.form("bilan_neon"):
            st.markdown("### ⚡ État de forme")
            c1, c2 = st.columns(2)
            with c1:
                fatigue = st.segmented_control("Niveau de Fatigue", options=[1, 2, 3, 4, 5], default=3)
                forme = st.segmented_control("Forme Physique", options=[1, 2, 3, 4, 5], default=3)
            with c2:
                moral = st.segmented_control("Moral / Envie", options=[1, 2, 3, 4, 5], default=3)
                stress = st.segmented_control("Stress global", options=[1, 2, 3, 4, 5], default=3)
            
            st.markdown("### 🤕 Santé")
            c3, c4 = st.columns(2)
            with c3:
                zones = st.multiselect("Zones douloureuses :", ["Cou", "Dos", "Épaule", "Coude", "Poignet", "Hanche", "Cuisse", "Genou", "Cheville", "Pied"])
            with c4:
                intensite = st.select_slider("Intensité", options=range(11))
            
            st.markdown("### 📅 Cycle")
            regles = st.radio("Période de règles ?", ["Non", "Oui", "Privé"], horizontal=True)
            
            if st.form_submit_button("VALIDER LE BILAN"):
                # Stockage rapide
                data = {"Date": datetime.now().strftime("%d/%m"), "Fatigue": fatigue, "Forme": forme, "Zones": ", ".join(zones), "Score": intensite, "Regles": regles}
                if nom not in st.session_state.db: st.session_state.db[nom] = []
                st.session_state.db[nom].append(data)
                st.balloons()
                st.success("Bilan transmis !")

# --- INTERFACE COACH ---
else:
    st.markdown('<p class="main-title">Dashboard Coach</p>', unsafe_allow_html=True)
    code = st.sidebar.text_input("Accès", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("En attente de données...")
        else:
            selection = st.selectbox("Sélectionne une joueuse", list(st.session_state.db.keys()))
            if selection:
                last = st.session_state.db[selection][-1]
                
                # Grille de stats façon tableau de bord de voiture
                st.markdown(f"## Suivi de {selection}")
                c1, c2, c3, c4 = st.columns(4)
                for col, (lab, val) in zip([c1, c2, c3, c4], [("Fatigue", last['Fatigue']), ("Forme", last['Forme']), ("Score Douleur", last['Score']), ("Règles", last['Regles'])]):
                    col.markdown(f"""
                        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; text-align:center; border: 1px solid rgba(255,255,255,0.1)">
                            <p style="margin:0; color:#94a3b8;">{lab}</p>
                            <p style="margin:0; font-size:28px; font-weight:bold; color:#06b6d4;">{val}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top:20px; background:rgba(6, 182, 212, 0.1); padding:20px; border-radius:15px; border-left: 5px solid #06b6d4;">
                        <h4 style="margin:0;">📍 Localisation des douleurs :</h4>
                        <p style="font-size:20px; margin:5px 0;">{last['Zones'] if last['Zones'] else 'Aucune'}</p>
                    </div>
                """, unsafe_allow_html=True)
