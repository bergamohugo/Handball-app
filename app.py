import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
from io import BytesIO

# --- CONFIGURATION ---
st.set_page_config(page_title="Handball Suivi", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { color: #007bff !important; }
    p, label, span { color: #ffffff !important; font-size: 14px !important; }
    .stButton>button { background-color: #007bff; color: white !important; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Sommeil", "Stress", "Fatigue", "Douleurs", "Règles"])

st.title("🤾‍♂️ SUIVI HANDBALL")
menu = st.sidebar.radio("MENU", ["📝 Formulaire", "📊 Coach"])

if menu == "📝 Formulaire":
    with st.form("form_final"):
        nom = st.text_input("Prénom de la joueuse")
        st.write("---")
        st.subheader("1- État de forme (1=Mauvais, 5=Top)")
        sommeil = st.radio("Sommeil", [1, 2, 3, 4, 5], horizontal=True, index=2)
        stress = st.radio("Stress", [1, 2, 3, 4, 5], horizontal=True, index=2)
        fatigue = st.radio("Énergie", [1, 2, 3, 4, 5], horizontal=True, index=2)
        
        st.write("---")
        st.subheader("2- Douleurs (Clique sur le corps)")
        url_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Medical_Anatomy_Blank_Charts_Custom_2.png/400px-Medical_Anatomy_Blank_Charts_Custom_2.png"
        try:
            resp = requests.get(url_img)
            img = Image.open(BytesIO(resp.content))
        except:
            img = None

        canvas_result = st_canvas(
            fill_color="rgba(0, 123, 255, 0.5)",
            stroke_width=2,
            stroke_color="#007bff",
            background_image=img,
            background_color="#1a1a1a",
            height=450,
            width=300,
            drawing_mode="point",
            key="canvas",
        )
        
        st.write("---")
        regles = st.checkbox("J'ai mes règles aujourd'hui")
        submit = st.form_submit_button("ENVOYER")
        
        if submit:
            nb_p = len(canvas_result.json_data["objects"]) if canvas_result.json_data else 0
            new_row = {"Date": datetime.now().strftime("%d/%m"), "Nom": nom, "Sommeil": sommeil, "Stress": stress, "Fatigue": fatigue, "Douleurs": f"{nb_p} zone(s)", "Règles": "Oui" if regles else "Non"}
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Envoyé !")

else:
    st.header("📊 Espace Coach")
    st.dataframe(st.session_state.data)
