import requests
import streamlit as st
from CONFIG import OLLAMA_API, LANGUAGE


def download_model(model_name):
    # Create the payload for the POST request
    payload = {
        "name": model_name
    }

    st.sidebar.write("Modèle en cours de téléchargement, veuillez patienter." if LANGUAGE == 'fr' else "Model downloading, please wait.")

    # Run POST request to pull the model
    response = requests.post(f"{OLLAMA_API}/api/pull", json=payload)
    
    # Check response status and view result
    if response.status_code == 200:
        print("Model downloaded successfully.")
        st.rerun()
    else:
        print(f"Error downloading model: {response.status_code}, {response.text}")
        st.sidebar.error("Un soucis a été détecté durant le téléchargement." if LANGUAGE == 'fr' else "A problem was detected during the download.")