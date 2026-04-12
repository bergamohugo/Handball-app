import streamlit as st
import pandas as pd
from datetime import date

# Configuration de la page
st.set_page_config(page_title="Handball Performance", layout="wide")

# --- SIMULATION DE BASE DE DONNÉES (Pour le test) ---
if 'data' not in st.session_state:
    st.session_state.data = []
if 'commentaires' not in st.session_state:
    st.session_state.commentaires = {}

# --- BARRE LATÉRALE (Navigation) ---
st.sidebar.title("🤾 Menu")
role = st.sidebar.radio("Tu es :", ["Joueuse", "Coach"])
equipe = st.sidebar.selectbox("Choisir l'équipe :", ["Séniors Féminines", "U18 Filles"])

# --- INTERFACE JOUEUSE ---
if role == "Joueuse":
    st.header(f"Formulaire Quotidien - {equipe}")
    nom = st.text_input("Ton nom et prénom")
    
    col1, col2 = st.columns(2)
    with col1:
        fatigue = st.slider("Niveau de fatigue", 1, 5, 2, help="1: Fraîche, 5: Épuisée")
        sommeil = st.slider("Qualité du sommeil", 1, 5, 4)
    with col2:
        stress = st.slider("Niveau de stress", 1, 5, 1)
        douleur = st.selectbox("Douleur particulière ?", ["Aucune", "Cheville", "Genou", "Épaule", "Dos", "Autre"])

    st.subheader("🩸 Suivi du Cycle")
    regles = st.checkbox("J'ai mes règles aujourd'hui")
    symptomes = st.multiselect("Symptômes éventuels :", ["Crampes", "Maux de tête", "Baisse d'énergie", "Douleurs dos"])

    if st.button("Envoyer mes données"):
        if nom:
            # Enregistrement des données
            entree = {
                "Date": date.today(),
                "Equipe": equipe,
                "Nom": nom,
                "Fatigue": fatigue,
                "Sommeil": sommeil,
                "Stress": stress,
                "Douleur": douleur,
                "Regles": "Oui" if regles else "Non",
                "Symptomes": ", ".join(symptomes)
            }
            st.session_state.data.append(entree)
            st.success(f"Merci {nom}, tes données sont transmises au coach !")
        else:
            st.error("N'oublie pas de mettre ton nom !")

# --- INTERFACE COACH ---
else:
    st.header(f"Tableau de Bord Coach - {equipe}")
    
    if not st.session_state.data:
        st.info("Aucune donnée enregistrée pour le moment.")
    else:
        df = pd.DataFrame(st.session_state.data)
        df_filtre = df[df['Equipe'] == equipe]
        
        # Affichage du tableau de suivi
        st.subheader("État de forme des joueuses")
        st.dataframe(df_filtre)

        # Section Commentaires du Coach
        st.divider()
        st.subheader("💬 Ajouter un commentaire de suivi")
        joueuse_sel = st.selectbox("Sélectionner une joueuse", df_filtre['Nom'].unique())
        com_texte = st.text_area(f"Note pour {joueuse_sel} :")
        
        if st.button("Enregistrer le commentaire"):
            st.session_state.commentaires[joueuse_sel] = com_texte
            st.success("Commentaire enregistré.")

        # Affichage des commentaires existants
        if joueuse_sel in st.session_state.commentaires:
            st.info(f"**Dernière note :** {st.session_state.commentaires[joueuse_sel]}")
