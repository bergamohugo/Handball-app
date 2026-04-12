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
    /* Fond de l'application en noir */
    .stApp {
        background-color: #000000;
    }
    /* Titres en Bleu */
    h1, h2, h3 {
        color: #007bff !important;
        font-weight: bold !important;
    }
    /* Tous les textes et labels en Blanc */
    p, label, span, li {
        color: #ffffff !important;
        font-size: 15px !important;
    }
    /* Ajustement des cases à cocher et boutons radio en blanc */
    .stCheckbox label, .stRadio label {
        color: #ffffff !important;
    }
    /* Bouton Valider (Bleu avec texte blanc) */
    .stButton>button {
        background-color: #007bff;
        color: white !important;
        border-radius: 8px;
        width: 100%;
        border: none;
        height: 45px;
        font-weight: bold;
    }
    /* Inputs (champs texte) avec fond gris très foncé pour rester lisible */
    input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #007bff !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Points_Douleur", "Règles"])

# --- TITRE PRINCIPAL ---
st.title("🤾‍♂️ SUIVI HANDBALL")

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["📝 Formulaire", "📊 Coach"])

if menu == "📝 Formulaire":
    with st.form("form_wellness_dark"):
        st.subheader("Identification")
        nom = st.text_input("Prénom de la joueuse")
        
        st.write("---")
        st.subheader("1- État de forme (1=Mauvais, 5=Top)")
        
        sommeil = st.radio("Qualité du Sommeil", [1, 2, 3, 4, 5], horizontal=True, index=2)
        stress = st.radio("Niveau de Stress", [1, 2, 3, 4, 5], horizontal=True, index=2)
        fatigue = st.radio("Niveau d'Énergie", [1, 2, 3, 4, 5], horizontal=True, index=2)
        
        st.write("---")
        st.subheader("2- Zones de douleurs (Clique sur le corps)")
        
        # Image du corps humain
        url_img = "https://www.dummies.com/wp-content/uploads/439266.image0.jpg"
        try:
            response = requests.get(url_img)
            img = Image.open(BytesIO(response.content))
        except:
            img = None

        # Zone de dessin
        canvas_result = st_canvas(
            fill_color="rgba(0, 123, 255, 0.5)", # Points bleus transparents
            stroke_width=2,
            stroke_color="#007bff",
            background_image=img if img else None,
            update_streamlit=True,
            height=400,
            width=300,
            drawing_mode="point",
            key="canvas_black",
        )
        
        nb_douleurs = 0
        if canvas_result.json_data is not None:
            nb_douleurs = len([obj for obj in canvas_result.json_data["objects"] if obj["type"] == "circle"])

        st.write("---")
        st.subheader("3- Cycle")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        
        st.write("")
        submit = st.form_submit_button("ENVOYER LES DONNÉES")
        
        if submit:
            new_row = {
                "Date": datetime.now().strftime("%d/%m"),
                "Nom": nom,
                "Sommeil": sommeil,
                "Stress": stress,
                "Fatigue": fatigue,
                "Points_Douleur": f"{nb_douleurs} zone(s)",
                "Règles": "Oui" if regles else "Non"
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("C'est envoyé !")

else:
    st.header("📊 Espace Coach")
    #
