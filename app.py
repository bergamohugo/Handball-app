import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de l'application
st.set_page_config(page_title="Handball Performance", layout="wide")

# 1. BASE DE DONNÉES FICTIVE (Liste des joueuses)
# Tu pourras ajouter les autres noms ici plus tard
LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand"]

# 2. INITIALISATION DE LA MÉMOIRE
# On crée un dictionnaire pour stocker l'historique par joueuse
if "db_handball" not in st.session_state:
    st.session_state.db_handball = {}

# 3. BARRE LATÉRALE (Navigation)
st.sidebar.title("🤾‍♂️ Handball App")
mode = st.sidebar.radio("Aller vers :", ["📝 Formulaire Joueuse", "📊 Tableau de Bord Coach"])

# --- MODE 1 : FORMULAIRE JOUEUSE ---
if mode == "📝 Formulaire Joueuse":
    st.title("Bilan de Santé Quotidien")
    
    with st.form("form_sante"):
        nom_joueuse = st.selectbox("Sélectionne ton nom", LISTE_JOUEUSES)
        
        st.divider()
        st.subheader("Ton état de forme (1 = Mauvais, 5 = Excellent)")
        
        col1, col2 = st.columns(2)
        with col1:
            fatigue = st.select_slider("Niveau de Fatigue", options=[1, 2, 3, 4, 5], value=3)
            moral = st.select_slider("Moral / Motivation", options=[1, 2, 3, 4, 5], value=3)
        with col2:
            forme = st.select_slider("Forme Physique", options=[1, 2, 3, 4, 5], value=3)
            stress = st.select_slider("Niveau de Stress", options=[1, 2, 3, 4, 5], value=3)
            
        st.divider()
        st.subheader("Santé & Blessures")
        douleurs = st.text_area("Localisation des douleurs (si besoin)", placeholder="Ex: Cheville droite, légère gêne...")
        regles = st.radio("As-tu tes règles ?", ["Non", "Oui"])
        
        valider = st.form_submit_button("Envoyer mon bilan")
        
        if valider:
            # Création de la ligne de données
            infos = {
                "Date": datetime.now().strftime("%d/%m/%Y"),
                "Fatigue": fatigue,
                "Forme": forme,
                "Moral": moral,
                "Stress": stress,
                "Douleurs": douleurs if douleurs else "Aucune",
                "Règles": regles
            }
            
            # On ajoute l'info dans l'historique de la joueuse
            if nom_joueuse not in st.session_state.db_handball:
                st.session_state.db_handball[nom_joueuse] = []
            
            st.session_state.db_handball[nom_joueuse].append(infos)
            st.success(f"Bilan enregistré pour {nom_joueuse} !")

# --- MODE 2 : ESPACE COACH ---
else:
    st.title("Tableau de Bord Coach")
    
    code = st.sidebar.text_input("Code Secret", type="password")
    
    if code == "COACH2024": # Ton mot de passe
        if not st.session_state.db_handball:
            st.info("Aucune donnée enregistrée pour le moment.")
        else:
            # SÉLECTION DE LA JOUEUSE
            joueuse_sel = st.selectbox("Choisir une joueuse pour voir son suivi :", list(st.session_state.db_handball.keys()))
            
            if joueuse_sel:
                data = st.session_state.db_handball[joueuse_sel]
                df = pd.DataFrame(data)
                
                st.header(f"Suivi de {joueuse_sel}")
                
                # 1. DERNIÈRES INFOS (Résumé)
                derniere = data[-1]
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Fatigue", f"{derniere['Fatigue']}/5")
                c2.metric("Forme", f"{derniere['Forme']}/5")
                c3.metric("Moral", f"{derniere['Moral']}/5")
                c4.metric("Stress", f"{derniere['Stress']}/5")
                
                st.warning(f"**Notes Santé :** {derniere['Douleurs']}")
                
                st.divider()
                
                # 2. HISTORIQUE (Tableau)
                st.subheader("Historique des réponses")
                st.table(df) # Affiche toutes les dates avec les notes
                
    elif code != "":
        st.error("Code incorrect")
