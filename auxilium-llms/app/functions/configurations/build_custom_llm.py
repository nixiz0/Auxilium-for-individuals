import streamlit as st
import requests
from CONFIG import OLLAMA_API, LANGUAGE
from functions.llms_system.system_instruction.modelfile_llm import show_system_instruction, rebuild_llm


def custom_llm(model_use):
    """
    Configure and update the custom language model settings.

    Parameters:
    model_use (str): The name of the model to use.
    """
    modelfile_values = {
        'system_text': "",
        'modelfile': "",
        'temperature': 0.7,
        'top_k': 40,
        'top_p': 0.90
    }

    if st.session_state.model_use != model_use:
        st.session_state.model_use = model_use
        st.session_state.system_text = show_system_instruction(model_use)
    
    for key, value in modelfile_values.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Add an input for the model name
    model_name_input = st.sidebar.text_input("Nom du modèle" if LANGUAGE == 'fr' else "Name of the model", value=st.session_state.model_use)
    
    # Display the extracted text in a text area
    modified_system_instruction = st.sidebar.text_area("Instruction Système" if LANGUAGE == 'fr' else "System Instruction", st.session_state.system_text, height=180, key='system_text_area')
    modified_system_instruction = f'"""{modified_system_instruction}"""'

    # Add a number input for temperature
    temperature = st.sidebar.number_input("Temperature", min_value=0.1, max_value=1.0, value=st.session_state.temperature, step=0.1)
    top_k = st.sidebar.number_input("Top_k", min_value=10, max_value=100, value=st.session_state.top_k, step=10)
    top_p = st.sidebar.number_input("Top_p", min_value=0.4, max_value=0.96, value=st.session_state.top_p, step=0.05)

    col1, col2 = st.sidebar.columns([1, 2])
    with col1:
        # Check if the text area content has changed
        if st.button("Créer" if LANGUAGE == 'fr' else "Create"):
            model_base = st.session_state.model_use
            model_name = model_name_input if model_name_input else st.session_state.model_use
            rebuild_llm(model_base, model_name, modified_system_instruction, temperature=temperature, top_k=top_k, top_p=top_p)
    
    with col2:
        # Delete selected model button
        if st.button("Supprimer" if LANGUAGE == 'fr' else "Delete"):
            response = requests.delete(f"{OLLAMA_API}/api/delete", json={"name": model_use})
            if response.status_code == 200:
                st.rerun()
            else:
                st.sidebar.write(f"Error deleting template: {response.status_code}, {response.text}")