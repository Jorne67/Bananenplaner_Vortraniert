import streamlit as st
import requests
import base64
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Banana Ripeness Planner",
    page_icon="🍌",
    layout="centered"
)

st.title("🍌 Banana Ripeness Planner")

# =========================================================
# REIFEGRAD TEXTE
# =========================================================

ROBOFLOW_TO_STUFE = {
    "unripe":      "🟢 Stufe 1 – Grün",
    "freshunripe": "🟡🟢 Stufe 2/3 – Mehr grün als gelb",
    "freshripe":   "🟡 Stufe 4 – Gelb mit grünen Spitzen ⭐ Optimal",
    "ripe":        "🟡 Stufe 5 – Vollgelb ⭐ Optimal",
    "overripe":    "🟡🟤 Stufe 6 – Vollgelb mit braunen Punkten",
    "rotten":      "🟤 Stufe 7 – Braun",
}

# =========================================================
# TAGE BIS OPTIMAL
# =========================================================

TAGE_BIS_OPTIMAL = {
    "unripe": 5,
    "freshunripe": 3,
    "freshripe": 1,
    "ripe": 0,
    "overripe": -1,
    "rotten": -2
}

# =========================================================
# WIE LANGE OPTIMAL?
# =========================================================

OPTIMAL_DAUER = {
    "unripe": 0,
    "freshunripe": 1,
    "freshripe": 2,
    "ripe": 1,
    "overripe": 0,
    "rotten": 0
}

# =========================================================
# SESSION STORAGE
# =========================================================

if "bananas" not in st.session_state:
    st.session_state.bananas = []

# =========================================================
# UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Lade ein Bild einer Banane hoch",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Hochgeladenes Bild",
        use_container_width=True
    )

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
    st.subheader("📊 Analyse")

    if "top" in result:

        top_class = result["top"]
        confidence = result["confidence"]

        label = ROBOFLOW_TO_STUFE.get(top_class, top_class)

        st.success(f"🍌 Erkannter Reifegrad: {label}")
        st.write(f"Konfidenz: {confidence:.0%}")

        tage = TAGE_BIS_OPTIMAL[top_class]

        st.divider()
        st.subheader("⏳ Wann perfekt essbar?")

        if tage > 0:
            st.info(f"Diese Banane wird in ungefähr **{tage} Tagen** perfekt essbar sein.")

        elif tage == 0:
            st.success("✅ Diese Banane ist heute perfekt essbar!")

        else:
            st.warning("⚠️ Diese Banane ist bereits über dem optimalen Reifegrad.")

        # =========================================================
        # SPEICHERN
        # =========================================================

        st.session_state.bananas.append({
            "class": top_class,
            "days_until_optimal": tage,
            "optimal_duration": OPTIMAL_DAUER[top_class]
        })

# =========================================================
# KALENDER
# =========================================================

if st.session_state.bananas:

    st.divider()
    st.subheader("📅 Nächste 7 Tage")

    today = datetime.now()

    for i in range(7):

        current_day = today + timedelta(days=i)

        banana_available = False

        for banana in st.session_state.bananas:

            start = banana["days_until_optimal"]
            ende = start + banana["optimal_duration"]

            if start <= i <= ende:
                banana_available = True

        if banana_available:

            st.markdown(
                f"""
                <div style="
                    background-color:#9BE39B;
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:10px;
                    color:black;
                    font-weight:bold;
                ">
                ✅ {current_day.strftime('%d.%m.%Y')}<br>
                Perfekte Banane verfügbar
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    background-color:#FF9B9B;
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:10px;
                    color:black;
                    font-weight:bold;
                ">
                ❌ {current_day.strftime('%d.%m.%Y')}<br>
                Keine perfekte Banane
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# EMPFEHLUNG
# =========================================================

    st.divider()
    st.subheader("🛒 Welche Banane heute kaufen?")

    fehlende_tage = []

    for i in range(7):

        found = False

        for banana in st.session_state.bananas:

            start = banana["days_until_optimal"]
            ende = start + banana["optimal_duration"]

            if start <= i <= ende:
                found = True

        if not found:
            fehlende_tage.append(i)

    if len(fehlende_tage) == 0:

        st.success("🎉 Für alle nächsten 7 Tage ist eine perfekte Banane vorhanden!")

    else:

        erster_fehlender_tag = fehlende_tage[0]

        if erster_fehlender_tag >= 5:
            empfehlung = "🟢 Stufe 1 – Grün"

        elif erster_fehlender_tag >= 3:
            empfehlung = "🟡🟢 Stufe 2/3 – Mehr grün als gelb"

        elif erster_fehlender_tag >= 1:
            empfehlung = "🟡 Stufe 4 – Gelb mit grünen Spitzen"

        else:
            empfehlung = "🟡 Stufe 5 – Vollgelb"

        st.info(
            f"Du solltest heute folgende Banane kaufen:\n\n"
            f"### {empfehlung}"
        )

# =========================================================
# RESET
# =========================================================

st.divider()

if st.button("🗑️ Alle gespeicherten Bananen löschen"):

    st.session_state.bananas = []
    st.rerun()
