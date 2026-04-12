import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Handball Santé", layout="centered")

st.title("🤾‍♂️ FORMULAIRE SANTÉ")

# Lien direct vers l'image du corps (plus de code à rallonge !)
bg_image = "https://raw.githubusercontent.com/u-foka/handball-app/main/body_outline.png"

nom = st.text_input("Ton Prénom")

st.subheader("Zones de douleurs (Clique sur le corps)")

# Le Canvas avec l'image
canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.3)",
    stroke_width=2,
    stroke_color="#ff0000",
    background_image=None, # On peut changer ici si besoin
    background_color="#eeeeee",
    height=400,
    width=300,
    drawing_mode="point",
    key="canvas",
)

if st.button("VALIDER"):
    if nom:
        st.success(f"Merci {nom}, tes informations ont été transmises.")
    else:
        st.warning("Pense à mettre ton prénom !")
