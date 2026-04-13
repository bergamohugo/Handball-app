import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Handball Performance Lab",
    page_icon="🤾‍♀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BASE DE DONNÉES FICTIVE (Pour l'exemple)
if "db" not in st.session_state:
    st.session_state.db = {}
    
LISTE_JOUEUSES = ["Julie Ribot", "Léa Bernard", "Manon Durand"]

# 3. LE DESIGN PRO ET FRAIS (Nouveau style)
st.markdown("""
    <style>
    /* Importation d'une police plus moderne */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #F0F4F8; /* Fond gris très clair frais */
    }

    /* Supprimer les éléments de base Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Le titre principal */
    .title-app {
        font-size: 32px;
        font-weight: 600;
        color: #0F172A; /* Bleu très foncé */
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 3px solid #06B6D4; /* Ligne cyan frais */
    }
    
    /* Les cartes de formulaire (Design moderne) */
    .stForm, .card-coach {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.01);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    
    /* Les titres de section */
    h2, h3 {
        color: #06B6D4 !important; /* Cyan Électrique */
        font-weight: 600;
        margin-top: 15px;
    }
    
    /* Style du bouton envoyer */
    .stButton>button {
        background-color: #06B6D4; /* Cyan */
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0891B2;
        box-shadow: 0 4px 6px rgba(6, 182, 212, 0.4);
    }
    
    /* Personnalisation des Pills et Segmented Control */
    .stHorizontal {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 5px;
    }
    [data-testid="stBaseButton-segmented_control_option"] {
        background-color: white !important;
        border: 2px solid #E2E8F0 !important;
        color: #64748B !important;
        border-radius: 10px !important;
    }
    [data-testid="stBaseButton-segmented_control_option"][aria-selected="true"] {
        background-color: #06B6D4 !important; /* Cyan */
        color: white !important;
        border-color: #06B6D4 !important;
    }
    
    /* Style du menu latéral */
    .st-emotion-cache-1cypcdb {
        background-color: #0F172A;
        color: white;
    }
    [data-testid="stSidebarRadioButton"] label {
        color: white;
    }
    
    </style>
""", unsafe_allow_html=True)

# 4. BARRE LATÉRALE (Navigation secrète)
page = st.sidebar.radio("Navigation 🤾‍♀️", ["📝 Formulaire", "🔒 Coach"])

# --- PAGE 1 : LE FORMULAIRE JOUERUSE (Le nouveau look) ---
if page == "📝 Formulaire":
    st.markdown('<h1 class="title-app">Handball <span style="color:#06B6D4">Performance Lab</span></h1>', unsafe_allow_html=True)
    
    with st.form("bilan_frais", clear_on_submit=True):
        st.subheader("Identification")
        nom = st.selectbox("Sélectionne ton nom :", [""] + LISTE_JOUEUSES)
        
        if nom:
            st.write("---")
            st.subheader("📊 État de forme")
            st.caption("Note de 1 (Très bas) à 5 (Excellent)")
            
            c1, c2 = st.columns(2)
            with c1:
                fatigue = st.segmented_control("⚡ Fatigue", options=[1, 2, 3, 4, 5], default=3)
                forme = st.segmented_control("💪 Forme Physique", options=[1, 2, 3, 4, 5], default=3)
            with c2:
                moral = st.segmented_control("🧠 Mental / Envie", options=[1, 2, 3, 4, 5], default=3)
                stress = st.segmented_control("🧘 Stress", options=[1, 2, 3, 4, 5], default=3)
            
            st.write("---")
            st.subheader("🤕 Zones de douleurs précises")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("**Haut & Tronc**")
                haut = st.multiselect("Zones (D/G) :", ["Cou/Nuque", "Épaule G", "Épaule D", "Abdominaux", "Dos (Haut)", "Dos (Lombaires)"])
            with c2:
                st.write("**Bras & Mains**")
                bras = st.multiselect("Zones (D/G) :", ["Coude G", "Coude D", "Poignet/Main G", "Poignet/Main D"])
            with c3:
                st.write("**Bas du corps**")
                bas = st.multiselect("Zones (D/G) :", ["Hanche G", "Hanche D", "Adducteurs G", "Adducteurs D", "Cuisse G", "Cuisse D", "Genou G", "Genou D", "Mollet G", "Mollet D", "Cheville G", "Cheville D", "Pied G", "Pied D"])
            
            toutes_douleurs = haut + bras + bas
            intensite = 0
            if toutes_douleurs:
                intensite = st.select_slider("🔥 Intensité globale de la douleur", options=range(1, 11), value=1)
                st.caption("1 = Gêne | 10 = Douleur insupportable")
            
            st.write("---")
            st.subheader("📅 Cycle Menstruel")
            regles = st.radio("Période de règles ?", ["Non", "Oui", "Pas de réponse"], horizontal=True)
            
            st.write("---")
            envoyer = st.form_submit_button("VALIDER MON BILAN DU JOUR")
            
            if envoyer:
                # Sauvegarde
                infos = {
                    "Date": datetime.now().strftime("%d/%m/%Y"),
                    "Time": datetime.now().strftime("%H:%M"),
                    "Fatigue": fatigue, "Forme": forme, "Moral": moral, "Stress": stress,
                    "Douleurs": ", ".join(toutes_douleurs) if toutes_douleurs else "Aucune", 
                    "Intensité": intensite,
                    "Règles": regles
                }
                
                if nom not in st.session_state.db:
                    st.session_state.db[nom] = []
                
                st.session_state.db[nom].append(infos)
                st.success(f"✅ Merci {nom}, tes données sont transmises au coach !")

# --- PAGE 2 : ESPACE COACH (Plus complet et clair) ---
else:
    st.markdown('<h1 class="title-app">🔒 Espace Coach</h1>', unsafe_allow_html=True)
    code = st.sidebar.text_input("Code Secret", type="password")
    
    if code == "COACH24":
        if not st.session_state.db:
            st.info("Aucun bilan reçu aujourd'hui. Partagez le lien avec l'équipe !")
        else:
            joueuses_dispos = list(st.session_state.db.keys())
            fille = st.selectbox("📊 Voir le suivi de :", joueuses_dispos)
            
            if fille:
                data = st.session_state.db[fille]
                derniere = data[-1]
                st.header(f"Fiche Individuelle de {fille}")
                
                # NOUVEAU : Visuel Coach (Météo du jour en gros chiffres)
                c1, c2, c3, c4 = st.columns(4)
                
                # Fonction pour colorer selon la note
                def get_color(note):
                    return "#EF4444" if note <= 2 else "#EAB308" if note == 3 else "#22C55E"

                # Métriques stylisées
                st.markdown(f"""
                <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 30px;">
                    <div class="card-coach" style="flex: 1; text-align: center; border-left: 5px solid {get_color(6-derniere['Fatigue'])};">
                        <p style="font-size: 16px; color: #64748B; margin:0;">Fatigue</p>
                        <p style="font-size: 40px; font-weight: 600; color: #0F172A; margin:0;">{derniere['Fatigue']}<span style="font-size: 18px; color: #94A3B8;">/5</span></p>
                    </div>
                    <div class="card-coach" style="flex: 1; text-align: center; border-left: 5px solid {get_color(derniere['Forme'])};">
                        <p style="font-size: 16px; color: #64748B; margin:0;">Forme</p>
                        <p style="font-size: 40px; font-weight: 600; color: #0F172A; margin:0;">{derniere['Forme']}<span style="font-size: 18px; color: #94A3B8;">/5</span></p>
                    </div>
                    <div class="card-coach" style="flex: 1; text-align: center; border-left: 5px solid {get_color(derniere['Moral'])};">
                        <p style="font-size: 16px; color: #64748B; margin:0;">Moral</p>
                        <p style="font-size: 40px; font-weight: 600; color: #0F172A; margin:0;">{derniere['Moral']}<span style="font-size: 18px; color: #94A3B8;">/5</span></p>
                    </div>
                    <div class="card-coach" style="flex: 1; text-align: center; border-left: 5px solid {get_color(6-derniere['Stress'])};">
                        <p style="font-size: 16px; color: #64748B; margin:0;">Stress</p>
                        <p style="font-size: 40px; font-weight: 600; color: #0F172A; margin:0;">{derniere['Stress']}<span style="font-size: 18px; color: #94A3B8;">/5</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # --- SANTÉ ---
                # Code couleur douleur
                d_color = "#3B82F6" if derniere['Intensité'] < 4 else "#EAB308" if derniere['Intensité'] < 7 else "#EF4444"
                
                st.markdown(f"""
                <div class="card-coach" style="border-left: 10px solid {d_color};">
                    <h4 style='margin-top:0;'>🤕 Alerte Blessure :</h4>
                    <p style='font-size: 18px; color: #0F172A;'>{derniere['Douleurs']}</p>
                    <p style='font-size: 22px; font-weight: bold; color: {d_color};'>Niveau : {derniere['Intensité']}/10</p>
                    <hr style='border: 0.5px solid #E2E8F0;'>
                    <p style='color: #64748B;'>📅 Cycle Menstruel : {derniere['Règles']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # --- HISTORIQUE (Tableau clean) ---
                st.divider()
                st.subheader("📅 Historique Complet")
                df = pd.DataFrame(data)
                # Trier par date inverse
                df = df.sort_index(ascending=False)
                st.dataframe(df.set_index("Date"), use_container_width=True)
                
    elif code != "":
        st.error("Code incorrect.")
