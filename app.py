import streamlit as st
import pandas as pd
from datetime import datetime

# Config de la page et style Bleu
st.set_page_config(page_title="Handball Suivi", layout="centered")

# CSS pour forcer un peu de bleu
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; }
    h1, h2, h3 { color: #004a99; }
    .stButton>button { background-color: #004a99; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Douleurs", "Règles"])

st.title("🤾‍♂️ Handball Wellness - Bleu")

# Menu
menu = st.sidebar.radio("Navigation", ["📝 Formulaire Joueuse", "📊 Espace Coach"])

if menu == "📝 Formulaire Joueuse":
    st.header("Ton état de forme")
    
    with st.form("form_wellness"):
        nom = st.text_input("Ton Prénom")
        
        # Système de cases (1 à 5)
        st.subheader("Sommeil, Stress & Fatigue")
        st.write("*(1 = Très mauvais, 5 = Top)*")
        
        sommeil = st.radio("Qualité de ton sommeil :", [1, 2, 3, 4, 5], horizontal=True, index=2)
        stress = st.radio("Niveau de stress :", [1, 2, 3, 4, 5], horizontal=True, index=2)
        fatigue = st.radio("Niveau d'énergie (forme) :", [1, 2, 3, 4, 5], horizontal=True, index=2)
        
        st.divider()
        
        # Système de douleurs par zones
        st.subheader("Zones de douleurs")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Haut du corps**")
            d_epaule = st.checkbox("Épaule")
            d_coude = st.checkbox("Coude / Poignet")
            d_dos = st.checkbox("Dos / Cervicales")
        
        with col2:
            st.write("**Bas du corps**")
            d_hanche = st.checkbox("Hanche")
            d_genou = st.checkbox("Genou")
            d_cheville = st.checkbox("Cheville / Pied")
            
        st.divider()
        
        st.subheader("Cycle")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        
        submit = st.form_submit_button("VALIDER")
        
        if submit:
            # Récupération des zones cochées
            selection = []
            if d_epaule: selection.append("Épaule")
            if d_coude: selection.append("Bras")
            if d_dos: selection.append("Dos")
            if d_hanche: selection.append("Hanche")
            if d_genou: selection.append("Genou")
            if d_cheville: selection.append("Cheville")
            
            new_row = {
                "Date": datetime.now().strftime("%d/%m"),
                "Nom": nom,
                "Sommeil": sommeil,
                "Stress": stress,
                "Fatigue": fatigue,
                "Douleurs": ", ".join(selection) if selection else "Aucune",
                "Règles": "Oui" if regles else "Non"
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("C'est enregistré ! Bon entraînement.")

else:
    st.header("📊 Suivi du groupe")
    if not st.session_state.data.empty:
        # Affichage simplifié en bleu
        st.table(st.session_state.data)
    else:
        st.info("Aucune donnée pour le moment.")
