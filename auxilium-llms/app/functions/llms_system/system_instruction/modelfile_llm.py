import streamlit as st
import requests
from CONFIG import OLLAMA_API, LANGUAGE


def show_system_instruction(model_use):
    """
    Display the model file content for the specified llm.

    Parameters:
    model_use (str): The name of the model to display.

    Returns:
    tuple: A tuple containing the system text, model file content, temperature, top_k, and top_p values.
    """
    response = requests.post(f"{OLLAMA_API}/api/show", json={"name": model_use})
    if response.status_code == 200:
        output = response.json()
    else:
        raise Exception(f"Ollama API Error: {response.status_code}, {response.text}")
    
    # Extract the system text
    system_text = output.get("system", "")
    
    return system_text


def rebuild_llm(model_base, model_name, modified_system_text, temperature=None, top_k=None, top_p=None):
    """
    Rebuild the LLM with the modified system text and model file content.

    Parameters:
    model_base (str): The base model to use.
    model_name (str): The name of the model to rebuild.
    modified_system_text (str): The modified system instruction to include.
    modelfile (str): The original model file content.
    temperature (float, optional): Sampling temperature.
    top_k (int, optional): Top-K sampling.
    top_p (float, optional): Top-P sampling.
    """

    # Construct the API request payload
    payload = {
        "model": model_name,
        "from": model_base,
        "system": modified_system_text,
        "parameters": {}  # Parameters dictionary
    }

    # Add parameters if provided
    if temperature is not None:
        payload["parameters"]["temperature"] = temperature
    if top_k is not None:
        payload["parameters"]["top_k"] = top_k
    if top_p is not None:
        payload["parameters"]["top_p"] = top_p

    # Remove parameters key if it's empty
    if not payload["parameters"]:
        del payload["parameters"]

    # Send request to Ollama to create the model
    response = requests.post(f"{OLLAMA_API}/api/create", json=payload)
    
    if response.status_code == 200:
        st.sidebar.write("Modèle créé avec succès." if LANGUAGE == 'fr' else "Model created successfully.")
    else:
        st.sidebar.write(f"Erreur lors de la création du modèle: {response.status_code}, {response.text}" if LANGUAGE == 'fr' else 
                         f"Error creating model: {response.status_code}, {response.text}")