import streamlit as st
from CONFIG import LANGUAGE, PATH_LOGO_AUXILIUM
from functions._ui_custom_.page_image import display_image
from functions.update_config import update_config
from functions.configurations.download_model import download_model
from functions.configurations.choose_llm import view_install_llms
from functions.configurations.build_custom_llm import custom_llm


def menu_page():
    # ----[HEADER ELEMENTS]----
    # Initialize input field in session_state
    if 'model_name_input' not in st.session_state:
        st.session_state.model_name_input = ""

    # ----[SIDEBAR ELEMENTS]----
    language = st.sidebar.selectbox("🔠Choisissez la langue" if LANGUAGE == 'fr' else "🔠Choose language", ["fr", "en"], index=["fr", "en"].index(LANGUAGE), key='selectbox_lang')
    if st.sidebar.button("Mettre à jour" if LANGUAGE == 'fr' else "Update", key='btn_set_lang'):
        update_config('LANGUAGE', f"'{language}'")
        st.rerun()

    st.sidebar.markdown("<hr style='margin:0px;'>", unsafe_allow_html=True)

    st.sidebar.markdown("### Télécharger un modèle sur Ollama" if LANGUAGE == 'fr' else "### Download a model from Ollama")

    model_name_input = st.sidebar.text_input("Nom du modèle" if LANGUAGE == 'fr' else "Name of the model", key='model_name_input')

    if model_name_input:
        if st.sidebar.button("Télécharger" if LANGUAGE == 'fr' else "Download"):
            download_model(model_name_input)
            st.session_state.model_name_input = ""

    st.sidebar.markdown("### Construisez votre modèle" if LANGUAGE == 'fr' else "### Build your Model")

    model_names = view_install_llms()
    model_names.insert(0, "")
    model_use = st.sidebar.selectbox('🔬 Modèles' if LANGUAGE == "fr" else '🔬 Models', model_names)

    if model_use:
        custom_llm(model_use)


    # ----[PAGE ELEMENTS]----
    display_image(PATH_LOGO_AUXILIUM, 200)

    # Center title and description
    menu_txt = {
        "fr": {
            "title": "Auxilium-IA",
            "description": "Utiliser les LLMs en leur plein potentiel"
        },
        "en": {
            "title": "Auxilium-AI",
            "description": "Use LLMs to their full potential"
        }
    }

    # Select intro_content based on language
    menu_txt_content = menu_txt[LANGUAGE]
    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 5em;'>
            <h1>{menu_txt_content['title']}</h1>
            <h3>{menu_txt_content['description']}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )