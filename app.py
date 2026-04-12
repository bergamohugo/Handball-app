import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page avec un layout large
st.set_page_config(page_title="Handball Performance", layout="wide")

# --- STYLE PERSONNALISÉ (Bleu Moderne) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #00457C;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_all_choices=True)

# 1. BASE DE DONNÉES FICTIVE
LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand"]

# 2. INITIALISATION DE LA MÉMOIRE
if "db_handball" not in st.session_state:
    st.session_state.db_handball = {}

# 3. NAVIGATION
st.sidebar.title("🤾‍♂️ Handball App")
mode = st.sidebar.radio("Aller vers :", ["📝 Formulaire Joueuse", "📊 Tableau de Bord Coach"])

# --- MODE 1 : FORMULAIRE JOUEUSE ---
if mode == "📝 Formulaire Joueuse":
    st.title("🔵 Ton Bilan Quotidien")
    
    with st.container():
        nom_joueuse = st.selectbox("Sélectionne ton nom", [""] + LISTE_JOUEUSES)
        
        if nom_joueuse:
            st.divider()
            
            # --- SECTION ETAT DE FORME ---
            st.subheader("📊 Ton état de forme")
            st.info("Note de 1 (Bas) à 5 (Excellent)")
            
            c1, c2 = st.columns(2)
            with c1:
                fatigue = st.select_slider("⚡ Niveau de Fatigue", options=[1, 2, 3, 4, 5], value=3)
                moral = st.select_slider("🧠 Mental / Motivation", options=[1, 2, 3, 4, 5], value=3)
            with c2:
                forme = st.select_slider("💪 Forme Physique", options=[1, 2, 3, 4, 5], value=3)
                stress = st.select_slider("🧘 Niveau de Stress", options=[1, 2, 3, 4, 5], value=3)
                
            st.divider()
            
            # --- SECTION SANTÉ ---
            st.subheader("🤕 Santé & Blessures")
            # Choix prédéfinis pour aller plus vite
            choix_douleurs = st.multiselect(
                "Localisation des douleurs :",
                ["Aucune", "Cheville Gauche", "Cheville Droite", "Genou Gauche", "Genou Droit", 
                 "Cuisse / Ischios", "Dos / Lombaires", "Épaule", "Coude / Poignet"]
            )
            precisions = st.text_input("Précisions (optionnel)", placeholder="Ex: Gêne sur les sauts")
            
            st.divider()
            
            # --- SECTION RÈGLES ---
            st.subheader("📅 Cycle Menstruel")
            regles = st.radio(
                "Es-tu dans ta période de règles ?",
                ["Non", "Oui", "Pas de réponse"],
                horizontal=True
            )
            
            if st.button("ENVOYER MON BILAN"):
                # Sauvegarde
                infos = {
                    "Date": datetime.now().strftime("%d/%m/%Y"),
                    "Fatigue": fatigue,
                    "Forme": forme,
                    "Moral": moral,
                    "Stress": stress,
                    "Douleurs": ", ".join(choix_douleurs) if choix_douleurs else "Aucune",
                    "Notes": precisions,
                    "Règles": regles
                }
                
                if nom_joueuse not in st.session_state.db_handball:
                    st.session_state.db_handball[nom_joueuse] = []
                
                st.session_state.db_handball[nom_joueuse].append(infos)
                st.success(f"✅ Merci {nom_joueuse}, tes données ont été transmises.")

# --- MODE 2 : ESPACE COACH ---
else:
    st.title("🔒 Suivi Individuel")
    code = st.sidebar.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db_handball:
            st.info("En attente des premiers bilans...")
        else:
            joueuse_sel = st.selectbox("Sélectionner une joueuse :", list(st.session_state.db_handball.keys()))
            
            if joueuse_sel:
                data = st.session_state.db_handball[joueuse_sel]
                df = pd.DataFrame(data)
                
                # Header personnalisé
                st.header(f"Fiche de {joueuse_sel}")
                
                # Chiffres clés (Dernière saisie)
                derniere = data[-1]
                cols = st.columns(4)
                # Utilisation de couleurs bleues pour les metrics
                cols[0].metric("Fatigue", f"{derniere['Fatigue']}/5")
                cols[1].metric("Forme", f"{derniere['Forme']}/5")
                cols[2].metric("Moral", f"{derniere['Moral']}/5")
                cols[3].metric("Stress", f"{derniere['Stress']}/5")
                
                st.info(f"📍 **Douleurs signalées :** {derniere['Douleurs']} ({derniere['Notes']})")
                st.caption(f"📅 État cycle : {derniere['Règles']}")
                
                st.divider()
                st.subheader("📈 Historique Journalier")
                st.dataframe(df.set_index("Date"), use_container_width=True)
                
    elif code != "":
        st.error("Accès refusé")
