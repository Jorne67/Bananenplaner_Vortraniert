import streamlit as st
import base64
from inference_sdk import InferenceHTTPClient

st.title("🍌 Banana Ripeness Detection – Roboflow")

# Klassen auf unsere Skala mappen
ROBOFLOW_TO_STUFE = {
    "unripe":      (1, "🟢 Stufe 1 – Grün"),
    "freshunripe": (2, "🟡🟢 Stufe 2 – Mehr grün als gelb"),
    "freshripe":   (3, "🟡🟢 Stufe 3 – Mehr gelb als grün / Gelb mit grünen Spitzen ⭐ Optimal"),
    "ripe":        (4, "🟡 Stufe 5 – Vollgelb ⭐ Optimal"),
    "overripe":    (5, "🟡🟤 Stufe 6 – Vollgelb mit braunen Punkten"),
    "rotten":      (6, "🟤 Stufe 7 – Braun"),
}

uploaded_file = st.file_uploader("Lade ein Bild hoch", type=["jpg","jpeg","png"])

if uploaded_file:
    st.image(uploaded_file)

    with st.spinner("🔍 Analyse läuft..."):
        api_key = st.secrets["ROBOFLOW_API_KEY"]

        client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=api_key
        )

        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        result = client.infer(
            img_base64,
            model_id="banana-ripeness-classification/3"
        )

    st.divider()
    st.subheader("📊 Ergebnis")

    top_class = result["top"]
    confidence = result["confidence"]

    stufe_nr, stufe_label = ROBOFLOW_TO_STUFE.get(top_class, (0, top_class))

    st.success(f"**Erkannter Reifegrad:** {stufe_label}")
    st.write(f"Konfidenz: {confidence:.0%}")

    st.divider()
    st.subheader("Alle Wahrscheinlichkeiten")
    for pred in result["predictions"]:
        st.write(f"{pred['class']}: {pred['confidence']:.0%}")
