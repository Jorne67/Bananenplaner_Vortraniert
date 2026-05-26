import streamlit as st
from inference_sdk import InferenceHTTPClient

st.title("🍌 Banana Ripeness Detection")

uploaded_file = st.file_uploader(
    "Lade ein Bananenbild hoch",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="OJPob1K0te2vvBOc175w"
    )

    result = client.run_workflow(
        workspace_name="jarnes-workspace",
        workflow_id="detect-and-classify-3",
        images={
            "image": "temp.jpg"
        },
        use_cache=True
    )

    st.image(uploaded_file)

    st.subheader("Ergebnis")

    st.json(result)
