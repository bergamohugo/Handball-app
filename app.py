import streamlit as st
import pandas as pd

# Configuration look "Pro Dark"
st.set_page_config(page_title="Handball Performance", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #3B82F6 !important; }
    .stButton>button { 
        background-color: #1E40AF; 
        color: white; 
        border-radius: 12px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

if "db" not in st.session_state:
    st.session_state.db = {}

page = st.sidebar.radio("Menu", ["📝 Formulaire", "🔒 Coach"])

# --- PAGE JOUEUSE ---
if page == "📝 Formulaire":
    st.title("🤾‍♀️ Bilan Santé Détaillé")
    nom = st.selectbox("Sélectionne ton nom", ["Julie Ribot", "Léa Bernard", "Manon Durand"])
    
    st.write("---")
    
    # État de forme
    st.subheader("📊 État de forme")
    c1, c2 = st.columns(2)
    with c1:
        fatigue = st.segmented_control("⚡ Fatigue", options=[1, 2, 3, 4, 5], default=3)
        forme = st.segmented_control("💪 Forme Physique", options=[1, 2, 3, 4, 5], default=3)
    with c2:
        moral = st.segmented_control("🧠 Mental", options=[1, 2, 3, 4, 5], default=3)
        stress = st.segmented_control("🧘 Stress", options=[1, 2, 3, 4, 5], default=3)
    
    st.write("---")
    
    # ZONES DE DOULEURS DÉTAILLÉES
    st.subheader("🤕 Localisation précise des douleurs")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.write("**Haut & Tronc**")
        haut = st.multiselect("Zones :", ["Cou/Nuque", "Épaule G", "Épaule D", "Pectoraux", "Abdominaux", "Dos (Haut)", "Dos (Bas/Lombaires)"])
        
    with col_b:
        st.write("**Bras & Mains**")
        bras = st.multiselect("Zones :", ["Biceps G", "Biceps D", "Triceps G", "Triceps D", "Coude G", "Coude D", "Avant-bras G", "Avant-bras D", "Poignet/Main G", "Poignet/Main D"])
        
    with col_c:
        st.write("**Bas du corps**")
        bas = st.multiselect("Zones :", ["Hanche G", "Hanche D", "Adducteurs G", "Adducteurs D", "Cuisse Devant G", "Cuisse Devant D", "Ischios (Arrière) G", "Ischios (Arrière) D", "Genou G", "Genou D", "Mollet G", "Mollet D", "Cheville G", "Cheville D", "Pied G", "Pied D"])

    toutes_douleurs = haut + bras + bas
    
    # Précision sur l'intensité
    intensite = 0
    if toutes_douleurs:
        intensite = st.select_slider("🔥 Intensité globale de la douleur", options=range(1, 11), value=1)
        st.caption("1 = Gêne légère | 10 = Douleur insupportable")

    st.write("---")
    st.subheader("📅 Cycle Menstruel")
    regles = st.radio("Période de règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
    
    if st.button("ENVOYER MON BILAN"):
        st.session_state.db[nom] = {
            "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
            "Douleurs": ", ".join(toutes_douleurs) if toutes_douleurs else "Aucune", 
            "Intensité": intensite,
            "Règles": regles
        }
        st.balloons()
        st.success("Enregistré !")

# --- PAGE COACH ---
else:
    st.title("🔒 Suivi Individuel")
    code = st.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("Aucun bilan reçu.")
        else:
            fille = st.selectbox("Choisir une joueuse :", list(st.session_state.db.keys()))
            infos = st.session_state.db[fille]
            
            st.header(f"Fiche de {fille}")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Fatigue", f"{infos['Fatigue']}/5")
            c2.metric("Forme", f"{infos['Forme']}/5")
            c3.metric("Moral", f"{infos['Moral']}/5")
            c4.metric("Stress", f"{infos['Stress']}/5")
            
            # Affichage stylisé des douleurs
            color = "#3B82F6" if infos['Intensité'] < 4 else "#EAB308" if infos['Intensité'] < 7 else "#EF4444"
            
            st.markdown(f"""
            <div style="background-color: #1E293B; padding: 20px; border-radius: 15px; border-left: 10px solid {color};">
                <h4 style='margin-top:0;'>📍 Zones touchées :</h4>
                <p style='font-size: 18px;'>{infos['Douleurs']}</p>
                <p style='font-size: 22px; font-weight: bold; color: {color};'>Niveau de douleur : {infos['Intensité']}/10</p>
                <hr style='border: 0.5px solid #475569;'>
                <p>📅 Cycle : {infos['Règles']}</p>
            </div>
            """, unsafe_allow_html=True)
