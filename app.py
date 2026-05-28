import streamlit as st
import requests
import base64

st.title("🍌 Banana Ripeness Detection – Roboflow")

ROBOFLOW_TO_STUFE = {
    "unripe":      "🟢 Stufe 1 – Grün",
    "freshunripe": "🟡🟢 Stufe 2/3 – Mehr grün als gelb",
    "freshripe":   "🟡 Stufe 4 – Gelb mit grünen Spitzen ⭐ Optimal",
    "ripe":        "🟡 Stufe 5 – Vollgelb ⭐ Optimal",
    "overripe":    "🟡🟤 Stufe 6 – Vollgelb mit braunen Punkten",
    "rotten":      "🟤 Stufe 7 – Braun",
}

uploaded_file = st.file_uploader("Lade ein Bild hoch", type=["jpg","jpeg","png"])

if uploaded_file:
    st.image(uploaded_file)

    with st.spinner("🔍 Analyse läuft..."):
        api_key = st.secrets["ROBOFLOW_API_KEY"]
        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        response = requests.post(
    f"https://classify.roboflow.com/banana-ripeness-classification/5",
            params={"api_key": api_key},
            data=img_base64,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        result = response.json()
    
st.write(result)
    st.divider()
    st.subheader("📊 Ergebnis")

    if "top" in result:
        top_class = result["top"]
        confidence = result["confidence"]
        label = ROBOFLOW_TO_STUFE.get(top_class, top_class)
        st.success(f"**Erkannter Reifegrad:** {label}")
        st.write(f"Konfidenz: {confidence:.0%}")

        st.divider()
        st.subheader("Alle Wahrscheinlichkeiten")
        for pred in result.get("predictions", {}).values():
            st.write(f"{pred['class']}: {pred['confidence']:.0%}")
    else:
        st.error("Fehler bei der Analyse")
        st.json(result)
