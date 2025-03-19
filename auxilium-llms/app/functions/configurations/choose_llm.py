import requests
import streamlit as st
from CONFIG import OLLAMA_API, LANGUAGE
from functions.update_config import update_config


def view_install_llms():
    """
    Retrieve and display the list of ollama installed llm.

    Returns:
    list: A list of installed LANGUAGE model names.
    """
    try:
        # Run 'ollama list' command and get the output
        response = requests.get(f"{OLLAMA_API}/api/tags")
        if response.status_code == 200:
            data = response.json()
            model_names = [model["name"] for model in data.get("models", [])]  # Retrieve only model names
        else:
            raise Exception(f"Ollama API Error: {response.status_code}, {response.text}")
        
        return model_names

    except requests.exceptions.ConnectionError as e:
        # Handle the error and display a message based on the user's LANGUAGEuage
        if LANGUAGE == 'fr':
            st.sidebar.error("Veuillez démarrer votre Ollama pour accéder à vos LLMs.")
        else:
            st.sidebar.error("Please start your Ollama to access your LLMs.")
        return []


def get_llm(constant_model, model_name):
    """
    Updates the configuration file with the selected model name and displays a success or error message.

    This function updates the 'LLM_CHOOSE' key in the configuration file with the provided model name.
    It displays a success message in the Streamlit sidebar if the update is successful, or an error message if the update fails.

    Parameters:
    model_name (str): The name of the model to be set in the configuration.

    Raises:
    Exception: If an error occurs while updating the configuration file, an error message is displayed in the Streamlit sidebar.
    """
    try:
        update_config(constant_model, f'"{model_name}"', 'app/CONFIG.py')
    except Exception as e:
        st.sidebar.error(f"Échec lors de la sélection du modèle : {e}" if LANGUAGE == 'fr' else f"Failed selecting a model : {e}")