import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration
st.set_page_config(page_title="Handball Suivi", layout="centered")

# CSS pour un style Bleu Marine et lisible
st.markdown("""
    <style>
    /* Couleur des titres */
    h1, h2, h3 { color: #003366 !important; font-weight: bold; }
    
    /* Style du bouton Valider */
    .stButton>button { 
        background-color: #003366; 
        color: white; 
        width: 100%; 
        height: 50px;
        font-size: 20px;
        border-radius: 10px;
    }
    
    /* Rendre les chiffres des boutons radio plus gros */
    .stRadio label { font-size: 18px !important; color: #000000; }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Douleurs", "Règles"])

st.title("🤾‍♂️ SUIVI JOUEUSES")

menu = st.sidebar.radio("Navigation", ["📝 Formulaire", "📊 Dashboard Coach"])

if menu == "📝 Formulaire":
    st.header("État de forme")
    
    with st.form("form_wellness"):
        nom = st.text_input("Prénom de la joueuse")
        
        st.write("---")
        st.subheader("Notes (1 = Mauvais, 5 = Excellent)")
        
        # Chiffres bien visibles
        sommeil = st.radio("Qualité du Sommeil", [1, 2, 3, 4, 5], horizontal=True)
        stress = st.radio("Niveau de Stress", [1, 2, 3, 4, 5], horizontal=True)
        fatigue = st.radio("Niveau d'Énergie", [1, 2, 3, 4, 5], horizontal=True)
        
        st.write("---")
        st.subheader("Zones de douleurs")
        
        col1, col2 = st.columns(2)
        with col1:
            d_epaule = st.checkbox("Épaule")
            d_coude = st.checkbox("Coude / Main")
            d_dos = st.checkbox("Dos")
        with col2:
            d_hanche = st.checkbox("Hanche")
            d_genou = st.checkbox("Genou")
            d_cheville = st.checkbox("Cheville / Pied")
            
        st.write("---")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        
        submit = st.form_submit_button("VALIDER L'ENVOI")
        
        if submit:
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
            st.success("Données enregistrées !")

else:
    st.header("📊 Tableau du Coach")
    if not st.session_state.data.empty:
        # Tableau bien contrasté
        st.dataframe(st.session_state.data, use_container_width=True)
    else:
        st.info("En attente de saisies...")
