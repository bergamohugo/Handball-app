import streamlit as st
import pandas as pd

# Configuration pour un look moderne et sombre
st.set_page_config(page_title="Handball Performance", layout="wide")

# Style CSS pour le Fond Noir et les accents Bleus
st.markdown("""
    <style>
    /* Fond noir et texte blanc */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Titres en bleu sport */
    h1, h2, h3 { color: #3B82F6 !important; }
    
    /* Personnalisation des boutons */
    .stButton>button { 
        background-color: #1E40AF; 
        color: white; 
        border-radius: 12px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #3B82F6; border: none; }
    
    /* Cacher les lignes rouges d'erreur Streamlit */
    .stAlert { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de la base de données interne
if "db" not in st.session_state:
    st.session_state.db = {}

# Menu latéral simplifié
page = st.sidebar.radio("Menu", ["📝 Formulaire", "🔒 Coach"])

# --- PAGE JOUEUSE ---
if page == "📝 Formulaire":
    st.title("🤾‍♀️ Ton Bilan Santé")
    
    nom = st.selectbox("Sélectionne ton nom", ["Julie Ribot", "Léa Bernard", "Manon Durand"])
    
    st.write("---")
    
    # Échelle moderne avec des "Pills" au lieu de sliders
    st.subheader("📊 Ton état de forme")
    st.caption("1 = Très bas | 5 = Excellent")
    
    col1, col2 = st.columns(2)
    with col1:
        fatigue = st.segmented_control("⚡ Fatigue", options=[1, 2, 3, 4, 5], default=3)
        forme = st.segmented_control("💪 Forme Physique", options=[1, 2, 3, 4, 5], default=3)
    with col2:
        moral = st.segmented_control("🧠 Mental / Envie", options=[1, 2, 3, 4, 5], default=3)
        stress = st.segmented_control("🧘 Stress", options=[1, 2, 3, 4, 5], default=3)
    
    st.write("---")
    st.subheader("🤕 Zones de douleurs")
    douleurs = st.multiselect(
        "Coche les zones (G/D) :",
        ["Aucune", "Cheville G", "Cheville D", "Genou G", "Genou D", "Cuisse G", "Cuisse D", "Dos", "Épaule G", "Épaule D"]
    )
    
    st.write("---")
    st.subheader("📅 Cycle Menstruel")
    regles = st.radio("Période de règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
    
    if st.button("ENVOYER MON BILAN"):
        st.session_state.db[nom] = {
            "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
            "Douleurs": ", ".join(douleurs) if douleurs else "Aucune", 
            "Règles": regles
        }
        st.balloons() # Petite animation de fête pour la joueuse
        st.success(f"Enregistré ! Merci {nom}.")

# --- PAGE COACH ---
else:
    st.title("🔒 Suivi Individuel")
    code = st.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("Aucun bilan reçu aujourd'hui.")
        else:
            fille = st.selectbox("Choisir une joueuse :", list(st.session_state.db.keys()))
            infos = st.session_state.db[fille]
            
            st.header(f"Bilan de {fille}")
            
            # Affichage moderne
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Fatigue", f"{infos['Fatigue']}/5")
            c2.metric("Forme", f"{infos['Forme']}/5")
            c3.metric("Moral", f"{infos['Moral']}/5")
            c4.metric("Stress", f"{infos['Stress']}/5")
            
            st.markdown(f"""
            <div style="background-color: #1E293B; padding: 20px; border-radius: 15px; border-left: 5px solid #3B82F6;">
                <h4 style='margin-top:0;'>📍 Zones de douleurs :</h4>
                <p style='font-size: 20px;'>{infos['Douleurs']}</p>
                <hr>
                <p>📅 Cycle : {infos['Règles']}</p>
            </div>
            """, unsafe_allow_html=True)
