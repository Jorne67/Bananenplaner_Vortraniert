import streamlit as st
import requests
import base64

st.set_page_config(page_title="Banana Ripeness Detection", page_icon="🍌")

st.title("🍌 Banana Ripeness Detection – Roboflow")

ROBOFLOW_TO_STUFE = {
    "unripe":      "🟢 Stufe 1 – Grün",
    "freshunripe": "🟡🟢 Stufe 2/3 – Mehr grün als gelb",
    "freshripe":   "🟡 Stufe 4 – Gelb mit grünen Spitzen ⭐ Optimal",
    "ripe":        "🟡 Stufe 5 – Vollgelb ⭐ Optimal",
    "overripe":    "🟡🟤 Stufe 6 – Vollgelb mit braunen Punkten",
    "rotten":      "🟤 Stufe 7 – Braun",
}

uploaded_file = st.file_uploader(
    "Lade ein Bild einer Banane hoch",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    st.image(uploaded_file, caption="Hochgeladenes Bild", use_container_width=True)

    with st.spinner("🔍 Analyse läuft..."):

        api_key = st.secrets["ROBOFLOW_API_KEY"]

        img_bytes = uploaded_file.read()

        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        response = requests.post(
            "https://classify.roboflow.com/banana-ripeness-classification/5",
            params={
                "api_key": api_key
            },
            data=img_base64,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        result = response.json()

    st.divider()
    st.subheader("📊 Ergebnis")

    # DEBUG ANZEIGE
    with st.expander("Technische API-Antwort"):
        st.json(result)

    if "top" in result:

        top_class = result["top"]
        confidence = result["confidence"]

        label = ROBOFLOW_TO_STUFE.get(top_class, top_class)

        st.success(f"Erkannter Reifegrad: {label}")

        st.write(f"Konfidenz: {confidence:.0%}")

        st.divider()
        st.subheader("📈 Alle Wahrscheinlichkeiten")

        predictions = result.get("predictions", {})

        if isinstance(predictions, dict):

            for key, pred in predictions.items():

                if isinstance(pred, dict):
                    st.write(
                        f"{pred.get('class', key)}: "
                        f"{pred.get('confidence', 0):.0%}"
                    )

    else:

        st.error("❌ Fehler bei der Analyse")

        if "message" in result:
            st.write(f"API Meldung: {result['message']}")

        st.write("Bitte überprüfe:")
        st.write("- API-Key korrekt?")
        st.write("- Modell-Version korrekt?")
        st.write("- Modell deployed?")
