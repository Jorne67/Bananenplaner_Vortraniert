import streamlit as st
import requests

st.title("🍌 Banana Ripeness Detection")

uploaded_file = st.file_uploader(
    "Lade ein Bild hoch",
    type=["jpg","jpeg","png"]
)

if uploaded_file:

    st.image(uploaded_file)

    url = "https://serverless.roboflow.com/workflows/jarnes-workspace/detect-and-classify-3"

    response = requests.post(
        url,
        params={
            "api_key":"OJPob1K0te2vvBOc175w"
        },
        files={
            "image": uploaded_file
        }
    )

    result = response.json()

    st.subheader("Ergebnis")
    st.json(result)
