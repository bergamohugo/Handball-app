import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# Configuration
st.set_page_config(page_title="Handball Suivi", layout="centered")

# Style Noir et Blanc/Bleu
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    h1, h2, h3, label, p { color: white !important; }
    .stButton>button { background-color: #007bff; color: white !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Nom", "Douleurs"])

st.title("🤾‍♂️ FORMULAIRE SANTÉ")

with st.form("form_simple"):
    nom = st.text_input("Ton Prénom")
    
    st.subheader("Zones de douleurs")
    st.write("Clique sur le carré ci-dessous pour marquer tes douleurs :")
    
    # Un canvas vide (gris foncé) où on peut cliquer
    canvas_result = st_canvas(
        fill_color="rgba(0, 123, 255, 0.5)",
        stroke_width=2,
        stroke_color="#007bff",
        background_color="#262626", # Fond gris pour cliquer dessus
        height=300,
        width=300,
        drawing_mode="point",
        key="canvas_simple",
    )
    
    submit = st.form_submit_button("VALIDER")
    
    if submit:
        nb_points = len(canvas_result.json_data["objects"]) if canvas_result.json_data else 0
        new_row = {"Date": datetime.now().strftime("%d/%m"), "Nom": nom, "Douleurs": f"{nb_points} zone(s)"}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Enregistré !")

st.write("---")
if st.checkbox("Voir les résultats (Coach)"):
    st.dataframe(st.session_state.data)
