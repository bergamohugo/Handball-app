import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION & STYLE
st.set_page_config(page_title="Handball Lab", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Fond Ultra Dark avec dégradé */
    .stApp {
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }
    header, footer, #MainMenu {visibility: hidden;}

    /* Titre Néon */
    .main-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        color: #06b6d4;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
        letter-spacing: 3px;
        margin-bottom: 30px;
    }

    /* Cartes Glassmorphism */
    div[data-testid="stVerticalBlock"] > div:has(div.stForm) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
    }

    /* Boutons de sélection (Pills) */
    button[data-testid="stBaseButton-segmented_control_option"] {
        border: 1px solid rgba(6, 182, 212, 0.3) !important;
        background-color: transparent !important;
    }
    button[data-testid="stBaseButton-segmented_control_option"][aria-selected="true"] {
        background: #06b6d4 !important;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.6);
    }

    /* Bouton Valider */
    .stButton>button {
        background: linear-gradient(90deg, #06b6d4, #3b82f6) !important;
        border: none !important;
        height: 60px !important;
        font-size: 20px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 20px rgba(6, 182, 212, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. INITIALISATION
if "db" not in st.session_state: st.session_state.db = {}
LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand"]

# 3. NAVIGATION
page = st.sidebar.radio("Navigation", ["📝 Formulaire", "🔒 Coach"])

if page == "📝 Formulaire":
    st.markdown('<p class="main-title">PERFORMANCE LAB</p>', unsafe_allow_html=True)
    
    nom = st.selectbox("👤 JOUEUSE", [""] + LISTE_JOUEUSES)
    
    if nom:
        with st.form("form_elite"):
            st.markdown("### ⚡ ÉTAT DE FORME")
            c1, c2 = st.columns(2)
            with c1:
                fatigue = st.segmented_control("Fatigue", options=[1, 2, 3, 4, 5], default=3)
                forme = st.segmented_control("Physique", options=[1, 2, 3, 4, 5], default=3)
            with c2:
                moral = st.segmented_control("Mental", options=[1, 2, 3, 4, 5], default=3)
                stress = st.segmented_control("Stress", options=[1, 2, 3, 4, 5], default=3)
            
            st.write("---")
            st.markdown("### 🤕 SANTÉ & PRÉCISION")
            
            # Retour des zones détaillées
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.write("**Haut**")
                haut = st.multiselect("Zones :", ["Cou", "Épaule G", "Épaule D", "Dos Haut", "Lombaires"])
            with col_b:
                st.write("**Bras**")
                bras = st.multiselect("Zones :", ["Coude G", "Coude D", "Poignet G", "Poignet D"])
            with col_c:
                st.write("**Bas**")
                bas = st.multiselect("Zones :", ["Hanche G", "Hanche D", "Adducteurs G", "Adducteurs D", "Cuisse G", "Cuisse D", "Ischios G", "Ischios D", "Genou G", "Genou D", "Mollet G", "Mollet D", "Cheville G", "Cheville D", "Pied G", "Pied D"])
            
            toutes_douleurs = haut + bras + bas
            intensite = st.select_slider("🔥 Niveau de douleur", options=range(11), value=0)
            
            st.write("---")
            st.markdown("### 📅 CYCLE")
            regles = st.radio("Règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
            
            if st.form_submit_button("ENVOYER LE BILAN"):
                data = {
                    "Date": datetime.now().strftime("%d/%m"),
                    "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
                    "Douleurs": ", ".join(toutes_douleurs) if toutes_douleurs else "Aucune",
                    "Intensité": intensite, "Règles": regles
                }
                if nom not in st.session_state.db: st.session_state.db[nom] = []
                st.session_state.db[nom].append(data)
                st.balloons()
                st.success("Bilan transmis au coach !")

else:
    st.markdown('<p class="main-title">COACH DASHBOARD</p>', unsafe_allow_html=True)
    code = st.sidebar.text_input("Accès", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("Aucune donnée enregistrée.")
        else:
            fille = st.selectbox("Choisir une joueuse", list(st.session_state.db.keys()))
            if fille:
                last = st.session_state.db[fille][-1]
                st.markdown(f"## Fiche de {fille}")
                
                # Metrics Néon
                c1, c2, c3, c4 = st.columns(4)
                for col, (lab, val) in zip([c1, c2, c3, c4], [("Fatigue", last['Fatigue']), ("Forme", last['Forme']), ("Douleur", f"{last['Intensité']}/10"), ("Cycle", last['Règles'])]):
                    col.markdown(f"""
                        <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:20px; text-align:center; border: 1px solid #06b6d4;">
                            <p style="color:#94a3b8; margin:0; font-size:14px;">{lab}</p>
                            <p style="color:#06b6d4; font-size:24px; font-weight:bold; margin:0;">{val}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top:20px; padding:20px; border-radius:20px; background:rgba(6,182,212,0.1); border: 1px solid #06b6d4;">
                        <h4 style="margin:0; color:#06b6d4;">📍 Localisation :</h4>
                        <p style="font-size:18px; color:white;">{last['Douleurs']}</p>
                    </div>
                """, unsafe_allow_html=True)
