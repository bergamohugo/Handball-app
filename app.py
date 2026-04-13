import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Handball Performance Lab",
    page_icon="🤾‍♀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BASE DE DONNÉES FICTIVE
if "db" not in st.session_state:
    st.session_state.db = {}
    
LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand"]

# 3. DESIGN FRAIS & MODERNE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; background-color: #F0F4F8; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .title-app { font-size: 32px; font-weight: 600; color: #0F172A; text-align: center; padding-bottom: 20px; border-bottom: 3px solid #06B6D4; }
    .card-coach { background-color: #FFFFFF; padding: 20px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    h2, h3 { color: #06B6D4 !important; font-weight: 600; }
    .stButton>button { background-color: #06B6D4; color: white; border-radius: 12px; width: 100%; font-weight: 600; height: 3em; }
    </style>
""", unsafe_allow_html=True)

# 4. NAVIGATION
page = st.sidebar.radio("Navigation", ["📝 Formulaire", "🔒 Coach"])

# --- PAGE 1 : LE FORMULAIRE ---
if page == "📝 Formulaire":
    st.markdown('<h1 class="title-app">Handball <span style="color:#06B6D4">Performance Lab</span></h1>', unsafe_allow_html=True)
    
    # On sort le selectbox du formulaire pour plus de stabilité
    nom = st.selectbox("👤 Sélectionne ton nom :", [""] + LISTE_JOUEUSES)
    
    if nom:
        with st.form("bilan_final"):
            st.subheader("📊 État de forme")
            c1, c2 = st.columns(2)
            with c1:
                fatigue = st.segmented_control("⚡ Fatigue", options=[1, 2, 3, 4, 5], default=3)
                forme = st.segmented_control("💪 Forme Physique", options=[1, 2, 3, 4, 5], default=3)
            with c2:
                moral = st.segmented_control("🧠 Mental / Envie", options=[1, 2, 3, 4, 5], default=3)
                stress = st.segmented_control("🧘 Stress", options=[1, 2, 3, 4, 5], default=3)
            
            st.divider()
            st.subheader("🤕 Zones de douleurs")
            c1, c2, c3 = st.columns(3)
            with c1:
                haut = st.multiselect("Haut & Tronc :", ["Cou", "Épaule G", "Épaule D", "Dos (Haut)", "Dos (Bas)"])
            with c2:
                bras = st.multiselect("Bras :", ["Coude G", "Coude D", "Poignet G", "Poignet D"])
            with c3:
                bas = st.multiselect("Bas :", ["Hanche G", "Hanche D", "Cuisse G", "Cuisse D", "Genou G", "Genou D", "Cheville G", "Cheville D"])
            
            toutes_douleurs = haut + bras + bas
            intensite = st.select_slider("🔥 Intensité (si douleur)", options=range(0, 11), value=0)
            
            st.divider()
            st.subheader("📅 Cycle Menstruel")
            regles = st.radio("Période de règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
            
            envoyer = st.form_submit_button("VALIDER MON BILAN")
            
            if envoyer:
                infos = {
                    "Date": datetime.now().strftime("%d/%m/%Y"),
                    "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
                    "Douleurs": ", ".join(toutes_douleurs) if toutes_douleurs else "Aucune", 
                    "Intensité": intensite, "Règles": regles
                }
                if nom not in st.session_state.db: st.session_state.db[nom] = []
                st.session_state.db[nom].append(infos)
                st.balloons()
                st.success("✅ Bilan enregistré !")

# --- PAGE 2 : COACH ---
else:
    st.markdown('<h1 class="title-app">🔒 Espace Coach</h1>', unsafe_allow_html=True)
    code = st.sidebar.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("Aucune donnée pour le moment.")
        else:
            fille = st.selectbox("📊 Suivi de :", list(st.session_state.db.keys()))
            if fille:
                derniere = st.session_state.db[fille][-1]
                
                # Cartes de stats
                cols = st.columns(4)
                metrics = [("Fatigue", "Fatigue"), ("Forme", "Forme"), ("Moral", "Moral"), ("Stress", "Stress")]
                for i, (label, key) in enumerate(metrics):
                    cols[i].markdown(f"""
                        <div class="card-coach" style="text-align:center;">
                            <p style="color:#64748B; margin:0;">{label}</p>
                            <p style="font-size:30px; font-weight:600; margin:0;">{derniere[key]}/5</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Carte Douleur
                color = "#22C55E" if derniere['Intensité'] < 2 else "#EAB308" if derniere['Intensité'] < 5 else "#EF4444"
                st.markdown(f"""
                    <div class="card-coach" style="border-left: 10px solid {color};">
                        <h4>🤕 Santé :</h4>
                        <p><b>Zones :</b> {derniere['Douleurs']}</p>
                        <p><b>Intensité :</b> {derniere['Intensité']}/10</p>
                        <p><b>Cycle :</b> {derniere['Règles']}</p>
                    </div>
                """, unsafe_allow_html=True)
    elif code != "":
        st.error("Code incorrect")
