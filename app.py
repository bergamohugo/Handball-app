import streamlit as st
import pandas as pd

# Configuration pour un look moderne
st.set_page_config(page_title="Handball Performance", layout="wide")

# Application d'un style bleu personnalisé
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3 { color: #00457C !important; }
    .stButton>button { 
        background-color: #00457C; 
        color: white; 
        border-radius: 8px;
        width: 100%;
    }
    .stSelectbox, .stSlider { color: #00457C; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de la base de données interne
if "db" not in st.session_state:
    st.session_state.db = {}

# Menu latéral
page = st.sidebar.radio("Navigation", ["📝 Formulaire Joueuse", "🔒 Espace Coach"])

# --- PAGE JOUEUSE ---
if page == "📝 Formulaire Joueuse":
    st.title("🔵 Bilan Santé Quotidien")
    
    with st.container():
        nom = st.selectbox("Sélectionne ton nom", ["Julie Ribot", "Léa Bernard", "Manon Durand"])
        
        st.write("---")
        st.subheader("📊 État de forme")
        st.caption("Note de 1 (Bas) à 5 (Top)")
        
        c1, c2 = st.columns(2)
        with c1:
            fatigue = st.select_slider("⚡ Fatigue", options=[1, 2, 3, 4, 5], value=3)
            forme = st.select_slider("💪 Forme Physique", options=[1, 2, 3, 4, 5], value=3)
        with c2:
            moral = st.select_slider("🧠 Mental / Envie", options=[1, 2, 3, 4, 5], value=3)
            stress = st.select_slider("🧘 Stress", options=[1, 2, 3, 4, 5], value=3)
        
        st.write("---")
        st.subheader("🤕 Zones de douleurs")
        # Liste précise avec Gauche/Droite
        douleurs = st.multiselect(
            "Coche les zones concernées :",
            ["Aucune", 
             "Cheville Gauche", "Cheville Droite", 
             "Genou Gauche", "Genou Droit", 
             "Cuisse Gauche", "Cuisse Droite", 
             "Hanche / Adducteurs", 
             "Dos / Lombaires", 
             "Épaule Gauche", "Épaule Droite", 
             "Coude / Main"]
        )
        
        st.write("---")
        st.subheader("📅 Cycle Menstruel")
        regles = st.radio("Es-tu dans ta période de règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
        
        if st.button("ENVOYER MON BILAN"):
            # On stocke les infos
            st.session_state.db[nom] = {
                "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
                "Douleurs": ", ".join(douleurs) if douleurs else "Aucune", 
                "Règles": regles
            }
            st.success(f"✅ Merci {nom}, tes données sont transmises au coach !")

# --- PAGE COACH ---
else:
    st.title("🔒 Espace Coach")
    code = st.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("En attente des premiers retours des joueuses...")
        else:
            fille = st.selectbox("Choisir une joueuse :", list(st.session_state.db.keys()))
            infos = st.session_state.db[fille]
            
            st.header(f"Fiche de {fille}")
            
            # Affichage en gros chiffres bleus
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Fatigue", f"{infos['Fatigue']}/5")
            c2.metric("Forme", f"{infos['Forme']}/5")
            c3.metric("Moral", f"{infos['Moral']}/5")
            c4.metric("Stress", f"{infos['Stress']}/5")
            
            st.divider()
            st.markdown(f"### 📍 Zones signalées :\n **{infos['Douleurs']}**")
            st.write(f"📅 État cycle : {infos['Règles']}")
