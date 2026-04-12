import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
from io import BytesIO

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Handball Performance", layout="centered")

# --- STYLE CSS (FOND NOIR, TEXTE BLANC & BLEU) ---
st.markdown("""
    <style>
    /* Fond de l'application en noir profond */
    .stApp {
        background-color: #000000;
    }
    /* Titres en Bleu vif */
    h1, h2, h3 {
        color: #007bff !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    /* Tous les textes (petits) en Blanc */
    p, label, span, li, div {
        color: #ffffff !important;
        font-size: 14px !important;
    }
    /* Bouton Valider (Bleu avec texte blanc) */
    .stButton>button {
        background-color: #007bff;
        color: white !important;
        border-radius: 8px;
        width: 100%;
        height: 45px;
        font-weight: bold;
        border: none;
        margin-top: 20px;
    }
    /* Champs de saisie texte */
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #007bff !important;
    }
    /* Barre latérale */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de la base de données temporaire
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Douleurs", "Règles"])

# --- TITRE PRINCIPAL ---
st.title("🤾‍♂️ SUIVI JOUEUSES")

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["📝 Formulaire", "📊 Coach"])

if menu == "📝 Formulaire":
    with st.form("form_handball_final"):
        st.subheader("Identification")
        nom = st.text_input("Prénom et Nom")
        
        st.write("---")
        st.subheader("1- État de forme (1=Mauvais, 5=Top)")
        
        # Cases à cocher horizontales (Radio)
        sommeil = st.radio("Qualité du Sommeil", [1, 2, 3, 4, 5], horizontal=True, index=2)
        stress = st.radio("Niveau de Stress", [1, 2, 3, 4, 5], horizontal=True, index=2)
        fatigue = st.radio("Niveau d'Énergie", [1, 2, 3, 4, 5], horizontal=True, index=2)
        
        st.write("---")
        st.subheader("2- Zones de douleurs (Clique sur le corps)")
        
        # Image du corps humain (Lien Wikimedia robuste)
        url_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Medical_Anatomy_Blank_Charts_Custom_2.png/400px-Medical_Anatomy_Blank_Charts_Custom_2.png"
        try:
            response = requests.get(url_img)
            img = Image.open(BytesIO(response.content))
        except:
            img = None

        # Zone de dessin (Canvas cliquable)
        canvas_result = st_canvas(
            fill_color="rgba(0, 123, 255, 0.5)", # Points bleus
            stroke_width=2,
            stroke_color="#007bff",
            background_image=img if img else None
