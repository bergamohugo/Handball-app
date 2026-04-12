import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Handball Performance", layout="wide")

# Initialisation de la base de données (si vide)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Date", "Nom", "Sommeil", "Stress", "Fatigue", "Douleurs", "Règles"
    ])

st.title("🤾‍♀️ Suivi Performance & Bien-être")

menu = ["Joueuse (Saisie)", "Coach (Analyses)"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Joueuse (Saisie)":
    st.header("Formulaire Quotidien")
    
    with st.form("wellbeing_form"):
        nom = st.text_input("Prénom et Nom")
        
        st.subheader("État général (1 = Mauvais, 5 = Excellent)")
        sommeil = st.slider("Qualité du sommeil", 1, 5, 3)
        stress = st.slider("Niveau de stress", 1, 5, 3)
        fatigue = st.slider("Niveau d'énergie", 1, 5, 3)
        
        st.subheader("Douleurs & Blessures")
        zones = [
            "Aucune", "Cheville G", "Cheville D", "Genou G", "Genou D", 
            "Cuisse G", "Cuisse D", "Hanche", "Dos", "Épaule G", "Épaule D", "Autre"
        ]
        douleurs = st.multiselect("Sélectionne la ou les zones douloureuses :", zones)
        
        st.subheader("Cycle")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        
        submitted = st.form_submit_button("Envoyer mes données")
        if submitted:
            new_data = {
                "Date": datetime.now().strftime("%d/%m/%Y"),
                "Nom": nom,
                "Sommeil": sommeil,
                "Stress": stress,
                "Fatigue": fatigue,
                "Douleurs": ", ".join(douleurs),
                "Règles": "Oui" if regles else "Non"
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_data])], ignore_index=True)
            st.success("Données envoyées ! Merci coach.")

else:
    st.header("Tableau de Bord Coach")
    if not st.session_state.data.empty:
        # Affichage du tableau
        st.dataframe(st.session_state.data.style.background_gradient(cmap="RdYlGn", subset=["Sommeil", "Stress", "Fatigue"]))
        
        # Petit résumé
        st.subheader("Alertes")
        alertes = st.session_state.data[st.session_state.data["Fatigue"] <= 2]
        if not alertes.empty:
            st.warning(f"Attention, {len(alertes)} joueuse(s) sont en état de fatigue critique.")
    else:
        st.info("Aucune donnée enregistrée pour le moment.")
