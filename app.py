import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="Handball Lab", layout="wide")

# STYLE ELITE NEON
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%); color: #f8fafc; }
    header, footer, #MainMenu {visibility: hidden;}
    .main-title { font-size: 30px; font-weight: 800; text-align: center; color: #06b6d4; text-shadow: 0 0 15px rgba(6, 182, 212, 0.5); margin-bottom: 20px; }
    .card-stats { background: rgba(255,255,255,0.05); padding:15px; border-radius:15px; text-align:center; border: 1px solid #06b6d4; }
    /* Style pour les boutons de changement de mode */
    .mode-button { text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); }
    </style>
""", unsafe_allow_html=True)

# 2. INITIALISATION
if "db" not in st.session_state: st.session_state.db = {}
if "page_actuelle" not in st.session_state: st.session_state.page_actuelle = "Joueuse"

LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand", "Camille Petit", "Sarah Lopez"]

# --- LOGIQUE DE NAVIGATION (SANS BARRE LATÉRALE) ---
if st.session_state.page_actuelle == "Joueuse":
    # --- PAGE JOUEUSE ---
    st.markdown('<p class="main-title">PERFORMANCE LAB</p>', unsafe_allow_html=True)
    
    nom = st.selectbox("👤 SÉLECTIONNE TON NOM", [""] + LISTE_JOUEUSES)
    
    if nom:
        with st.form("form_final"):
            st.markdown("### ⚡ ÉTAT DE FORME")
            c1, c2 = st.columns(2)
            with c1:
                fatigue = st.segmented_control("Fatigue", options=[1, 2, 3, 4, 5], default=3)
                forme = st.segmented_control("Physique", options=[1, 2, 3, 4, 5], default=3)
            with c2:
                moral = st.segmented_control("Mental", options=[1, 2, 3, 4, 5], default=3)
                stress = st.segmented_control("Stress", options=[1, 2, 3, 4, 5], default=3)
            
            st.write("---")
            st.markdown("### 🤕 SANTÉ PRÉCISE")
            ca, cb, cc = st.columns(3)
            with ca: haut = st.multiselect("Haut :", ["Cou", "Épaule G", "Épaule D", "Dos Haut", "Lombaires"])
            with cb: bras = st.multiselect("Bras :", ["Coude G", "Coude D", "Poignet G", "Poignet D"])
            with cc: bas = st.multiselect("Bas :", ["Hanche G", "Hanche D", "Adducteurs", "Cuisse G", "Cuisse D", "Genou G", "Genou D", "Cheville G", "Cheville D", "Pied G", "Pied D"])
            
            intensite = st.select_slider("🔥 Intensité douleur (0 si rien)", options=range(11), value=0)
            regles = st.radio("Règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
            
            if st.form_submit_button("ENVOYER MON BILAN"):
                data = {
                    "Date": datetime.now().strftime("%d/%m %H:%M"),
                    "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
                    "Douleurs": ", ".join(haut+bras+bas) if (haut+bras+bas) else "Aucune",
                    "Intensité": intensite, "Règles": regles
                }
                if nom not in st.session_state.db: st.session_state.db[nom] = []
                st.session_state.db[nom].append(data)
                st.balloons()
                st.success("Transmis !")

    # BOUTON DISCRET POUR PASSER AU MODE COACH (Tout en bas)
    st.write("#")
    if st.button("⚙️ Accès Administration Coach"):
        st.session_state.page_actuelle = "Coach"
        st.rerun()

else:
    # --- PAGE COACH ---
    st.markdown('<p class="main-title">DASHBOARD COACH</p>', unsafe_allow_html=True)
    
    if st.button("⬅️ Retour au Formulaire"):
        st.session_state.page_actuelle = "Joueuse"
        st.rerun()

    pwd = st.text_input("Entre le code secret :", type="password")
    
    if pwd == "COACH24":
        if not st.session_state.db:
            st.warning("Aucun bilan reçu pour le moment.")
        else:
            # TABLEAU GÉNÉRAL
            st.subheader("📋 État de l'équipe")
            recap = []
            for j, bilans in st.session_state.db.items():
                dernier = bilans[-1]
                recap.append({"Joueuse": j, "Fatigue": dernier["Fatigue"], "Forme": dernier["Forme"], "Douleurs": dernier["Douleurs"], "Intensité": dernier["Intensité"]})
            st.dataframe(pd.DataFrame(recap), use_container_width=True, hide_index=True)
            
            # ZOOM JOUEUSE
            st.write("---")
            fille_sel = st.selectbox("🔍 Détail par joueuse :", list(st.session_state.db.keys()))
            if fille_sel:
                d = st.session_state.db[fille_sel][-1]
                c1, c2, c3, c4 = st.columns(4)
                c1.markdown(f'<div class="card-stats"><small>Fatigue</small><br><b>{d["Fatigue"]}/5</b></div>', unsafe_allow_html=True)
                c2.markdown(f'<div class="card-stats"><small>Physique</small><br><b>{d["Forme"]}/5</b></div>', unsafe_allow_html=True)
                c3.markdown(f'<div class="card-stats"><small>Douleur</small><br><b>{d["Intensité"]}/10</b></div>', unsafe_allow_html=True)
                c4.markdown(f'<div class="card-stats"><small>Règles</small><br><b>{d["Règles"]}</b></div>', unsafe_allow_html=True)
    elif pwd != "":
        st.error("Code incorrect")
