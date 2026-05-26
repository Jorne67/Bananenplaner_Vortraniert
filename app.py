import streamlit as st
import requests
import base64

st.title("🍌 Banana Ripeness Detection – Roboflow")

uploaded_file = st.file_uploader("Lade ein Bild hoch", type=["jpg","jpeg","png"])

if uploaded_file:
    st.image(uploaded_file)

    # Bild zu base64 konvertieren
    img_bytes = uploaded_file.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # Roboflow API aufrufen
    api_key = st.secrets["OJPob1K0te2vvBOc175w"]
    url = "https://classify.roboflow.com/banana-ripeness-classification/3"
    
    response = requests.post(
        url,
        params={"api_key": api_key},
        json={"image": img_base64}
    )

    result = response.json()
    st.subheader("Ergebnis")
    st.json(result)
