import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
from io import BytesIO

# --- CONFIGURATION & DESIGN ---
st.set_page_config(page_title="Handball Performance", layout="centered")

# CSS pour fond Bleu Foncé et Texte Blanc
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp {
        background-color: #00264d;
        color: white;
    }
    /* Forcer le texte en blanc pour presque tout */
    .stApp p, .stApp label, .stApp span, .stApp div, .stApp h1, .stApp h2, .stApp h3 {
        color: white !important;
    }
    /* Style du bouton Valider (Texte Noir pour contraste) */
    .stButton>button {
        background-color: #ffcc00; /* Jaune pour bien voir */
        color: black !important;
        width: 100%;
        height: 50px;
        font-size: 20px;
        border-radius: 10px;
        font-weight: bold;
    }
    /* Style du Menu Latéral */
    .css-163utfM, .css-145kmo2 {
        background-color: #003366 !important;
        color: white !important;
    }
    /* Style des Inputs (Texte Noir pour écrire) */
    .stTextInput>div>div>input {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES TEMPORAIRE ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Points_Douleur", "Règles"])

# --- MENU NAVIGATION ---
st.sidebar.markdown("# <span style='color: white;'>Menu</span>", unsafe_allow_html=True)
menu = st.sidebar.radio("", ["📝 Formulaire", "📊 Dashboard Coach"])

# --- ÉCRAN : FORMULAIRE JOUEUSE ---
if menu == "📝 Formulaire":
    st.title("🤾‍♂️ SUIVI JOUEUSES")
    st.write("C'est rapide, c'est pour ta perf !")

    with st.form("wellbeing_form"):
        nom = st.text_input("Ton Prénom")
        
        st.write("---")
        st.subheader("1- Ton état de forme (1=Mauvais, 5=Top)")
        
        # Notes 1 à 5 bien visibles
        sommeil = st.radio("Qualité de ton Sommeil", [1, 2, 3, 4, 5], horizontal=True)
        stress = st.radio("Niveau de Stress", [1, 2, 3, 4, 5], horizontal=True)
        fatigue = st.radio("Niveau d'Énergie", [1, 2, 3, 4, 5], horizontal=True)
        
        st.write("---")
        st.subheader("2- Tes douleurs (Clic sur le schéma)")
        
        # Image du corps humain (front & back)
        url_img = "https://raw.githubusercontent.com/bergamohugo/Handball-app/main/body_front_back.png"
        try:
            # Téléchargement de l'image pour le canvas
            response = requests.get(url_img)
            img_original = Image.open(BytesIO(response.content))
        except:
            st.error("L'image du corps humain n'a pas pu être chargée. As-tu bien ajouté body_front_back.png à ton GitHub ?")
            img_original = Image.new('RGB', (600, 400), color=(0, 38, 77)) # Image par défaut

        # --- LE CANVAS DU CORPS HUMAIN ---
        st.write("Appuie sur tes zones douloureuses :")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.5)",  # Couleur des points (Rouge transparent)
            stroke_width=3,
            stroke_color="red",
            background_image=img_original,
            update_streamlit=True,
            height=400,
            width=600,
            drawing_mode="point", # On clique pour mettre un point
            key="canvas_douleurs",
        )
        
        # Récupération des points cliqués
        zones_douleurs = ""
        if canvas_result.image_data is not None:
            # On va stocker les coordonnées des points cliqués
            # Pour faire simple ici on stocke juste le nombre de points
            # Une version finale coderait les coordonnées par zone (épaule, genou...)
            points_cliques = [shape for shape in canvas_result.json_data["objects"] if shape["type"] == "circle"]
            if len(points_cliques) > 0:
                # zones_douleurs = f"{len(points_cliques)} points de douleur"
                # Alternative : stocker les coordonnées pour analyse précise
                points_coords = [(int(p['left']), int(p['top'])) for p in points_cliques]
                zones_douleurs = str(points_coords)

        st.write("---")
        st.subheader("3- Cycle")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        
        submit = st.form_submit_button("VALIDER ET ENVOYER")
        
        if submit:
            new_row = {
                "Date": datetime.now().strftime("%d/%m"),
                "Nom": nom,
                "Sommeil": sommeil,
                "Stress": stress,
                "Fatigue": fatigue,
                "Points_Douleur": zones_douleurs if zones_douleurs else "Aucune",
                "Règles": "Oui" if regles else "Non"
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("C'est enregistré ! Merci.")

# --- ÉCRAN : DASHBOARD COACH ---
else:
    st.header("📊 Tableau du Coach")
    st.write("Visualisation des données du groupe")
    
    # Affichage en blanc (le style CSS s'applique)
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data, use_container_width=True)
    else:
        st.info("En attente de saisies...")
