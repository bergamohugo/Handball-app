import streamlit as st
import pandas as pd

# Configuration simple
st.set_page_config(page_title="Handball Suivi", layout="wide")

# Initialisation de la mémoire interne
if "db" not in st.session_state:
    st.session_state.db = {}

# Menu de navigation
page = st.sidebar.radio("Navigation", ["📝 Formulaire Joueuse", "🔒 Espace Coach"])

# --- PAGE JOUEUSE ---
if page == "📝 Formulaire Joueuse":
    st.title("🔵 Bilan de Santé")
    
    with st.form("bilan"):
        nom = st.selectbox("Sélectionne ton nom", ["Julie Ribot", "Léa Bernard", "Manon Durand"])
        
        st.subheader("État de forme (1 à 5)")
        fatigue = st.select_slider("⚡ Fatigue", options=[1, 2, 3, 4, 5], value=3)
        forme = st.select_slider("💪 Forme Physique", options=[1, 2, 3, 4, 5], value=3)
        moral = st.select_slider("🧠 Mental", options=[1, 2, 3, 4, 5], value=3)
        
        st.subheader("Santé")
        douleurs = st.multiselect("Zones de douleurs", ["Aucune", "Cheville", "Genou", "Cuisse", "Dos", "Épaule"])
        regles = st.radio("Période de règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
        
        if st.form_submit_button("Envoyer"):
            st.session_state.db[nom] = {
                "Fatigue": fatigue, "Forme": forme, "Moral": moral,
                "Douleurs": ", ".join(douleurs), "Règles": regles
            }
            st.success(f"Merci {nom}, c'est enregistré !")

# --- PAGE COACH ---
else:
    st.title("🔒 Suivi des Joueuses")
    code = st.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("Aucune donnée reçue.")
        else:
            fille = st.selectbox("Choisir une joueuse :", list(st.session_state.db.keys()))
            infos = st.session_state.db[fille]
            
            st.header(f"Fiche de {fille}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Fatigue", f"{infos['Fatigue']}/5")
            c2.metric("Forme", f"{infos['Forme']}/5")
            c3.metric("Moral", f"{infos['Moral']}/5")
            
            st.info(f"📍 Douleurs : {infos['Douleurs']}")
            st.write(f"📅 Règles : {infos['Règles']}")
