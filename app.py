import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
from io import BytesIO

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Handball Suivi", layout="centered")

# --- STYLE CSS (FOND BLEU, TEXTE BLANC) ---
st.markdown("""
    <style>
    /* Fond bleu foncé */
    .stApp {
        background-color: #00264d;
    }
    /* Tout le texte en blanc et plus petit */
    p, label, span, div, h1, h2, h3 {
        color: white !important;
        font-size: 14px !important;
    }
    /* Titres un peu plus grands mais blancs */
    h1 { font-size: 24px !important; }
    h2 { font-size: 20px !important; }
    
    /* Bouton Valider (Jaune pour être visible) */
    .stButton>button {
        background-color: #FFCC00;
        color: black !important;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    /* Cacher le menu Streamlit pour faire plus "App" */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Points_Douleur", "Règles"])

# --- TITRE ---
st.title("🤾‍♂️ SUIVI PERFORMANCE")

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["📝 Formulaire", "📊 Coach"])

if menu == "📝 Formulaire":
    with st.form("form_v4"):
        nom = st.text_input("Prénom de la joueuse")
        
        st.write("---")
        st.subheader("1- État de forme (1=Mauvais, 5=Top)")
        
        # Sélection par cases horizontales
        sommeil = st.radio("Qualité du Sommeil", [1, 2, 3, 4, 5], horizontal=True, index=2)
        stress = st.radio("Niveau de Stress", [1, 2, 3, 4, 5], horizontal=True, index=2)
        fatigue = st.radio("Niveau d'Énergie", [1, 2, 3, 4, 5], horizontal=True, index=2)
        
        st.write("---")
        st.subheader("2- Zones de douleurs (Clique sur le corps)")
        
        # Chargement de l'image du corps humain
        url_img = "https://www.dummies.com/wp-content/uploads/439266.image0.jpg"
        try:
            response = requests.get(url_img)
            img = Image.open(BytesIO(response.content))
        except:
            img = None

        # Zone de dessin (Canvas)
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.6)", 
            stroke_width=2,
            stroke_color="red",
            background_image=img if img else None,
            update_streamlit=True,
            height=400,
            width=300, # Format portrait pour mobile
            drawing_mode="point",
            key="canvas",
        )
        
        # Récupération des points
        nb_douleurs = 0
        if canvas_result.json_data is not None:
            nb_douleurs = len([obj for obj in canvas_result.json_data["objects"] if obj["type"] == "circle"])

        st.write("---")
        st.subheader("3- Cycle")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        
        st.write("")
        submit = st.form_submit_button("VALIDER")
        
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
            st.success("Données envoyées !")

else:
    st.header("📊 Espace Coach")
    if not st.session_state.data.empty:
        st.dataframe(st.session_state.data)
    else:
        st.write("Aucune donnée enregistrée.")
