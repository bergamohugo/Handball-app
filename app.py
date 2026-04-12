import streamlit as st
import pandas as pd

# 1. Configuration et mémoire
st.set_page_config(page_title="Handball App")

if "donnees" not in st.session_state:
    st.session_state.donnees = {} # On stocke par nom de joueuse

# 2. Menu de navigation
page = st.selectbox("Menu", ["📝 Formulaire Joueuse", "📋 Espace Coach (Privé)"])

st.divider()

# --- PAGE FORMULAIRE ---
if page == "📝 Formulaire Joueuse":
    st.header("Ton bilan du jour")
    
    with st.form("bilan"):
        nom = st.text_input("Ton Prénom")
        
        st.subheader("État général (1 à 5)")
        fati = st.slider("Fatigue", 1, 5, 3)
        form = st.slider("Forme", 1, 5, 3)
        stre = st.slider("Stress", 1, 5, 3)
        mora = st.slider("Moral", 1, 5, 3)
        
        st.subheader("Infos sup")
        cycl = st.radio("Règles ?", ["Non", "Oui"])
        douleur = st.text_input("Douleurs ? (Où et quelle intensité)")
        
        if st.form_submit_button("Envoyer au coach"):
            if nom:
                # On enregistre dans la mémoire
                st.session_state.donnees[nom] = {
                    "Fatigue": fati,
                    "Forme": form,
                    "Stress": stre,
                    "Moral": mora,
                    "Règles": cycl,
                    "Douleurs": douleur
                }
                st.success("C'est envoyé !")
            else:
                st.error("N'oublie pas ton prénom")

# --- PAGE COACH ---
else:
    st.header("Suivi des joueuses")
    
    mdp = st.text_input("Code secret coach", type="password")
    
    if mdp == "1234": # Ton code secret
        if not st.session_state.donnees:
            st.info("Aucune joueuse n'a encore rempli le formulaire.")
        else:
            # Liste cliquable des joueuses
            liste_filles = list(st.session_state.donnees.keys())
            fille_choisie = st.selectbox("Sélectionne une joueuse pour voir ses infos :", liste_filles)
            
            # Affichage des infos de la joueuse sélectionnée
            infos = st.session_state.donnees[fille_choisie]
            
            st.write(f"### Bilan de {fille_choisie}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Fatigue", f"{infos['Fatigue']}/5")
                st.metric("Forme", f"{infos['Forme']}/5")
            with col2:
                st.metric("Stress", f"{infos['Stress']}/5")
                st.metric("Moral", f"{infos['Moral']}/5")
            
            st.info(f"**Règles :** {infos['Règles']}")
            st.warning(f"**Douleurs :** {infos['Douleurs']}")
            
    elif mdp != "":
        st.error("Mauvais code")
