import streamlit as st
import os
from ollama import ChatResponse, Client
from CONFIG import *
from functions.configurations.choose_llm import view_install_llms, get_llm
from functions.configurations.reflexion_llm import get_initial_state, toggle_reflection
from functions.llms_system.translate_api import translate_text
from functions.llms_system.cot_api import llm_cot, build_full_prompt_reflexion
from functions.llms_system.manage_conversation import *


def discussion_page():
    # ----[HEADER ELEMENTS]----
    client = Client(host=OLLAMA_API)  # Ollama API URL

    # Initialize messages history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize session state for selected filename
    if "selected_filename" not in st.session_state:
        st.session_state.selected_filename = None

    # Initialize session state for model used
    st.session_state.model_use = ""

    # Initialize session state for reflexion model used
    st.session_state.model_reflexion_use = ""

    # Load the initial state of the variable from the config file
    initial_state = get_initial_state()
    if 'REFLEXION' not in st.session_state:
        st.session_state.REFLEXION = initial_state.get('REFLEXION', True)


    # ----[SIDEBAR ELEMENTS]----
    model_names = view_install_llms()
    model_names.insert(0, "")
    if st.sidebar.checkbox("Modèles Configuration" if LANGUAGE == 'fr' else "Configuration Models"):
        model_use = st.sidebar.selectbox('🔬 Modèles' if LANGUAGE == "fr" else '🔬 Models', model_names, index=model_names.index(st.session_state.model_use) if st.session_state.model_use in model_names else 0)
        if model_use:
            get_llm("LLM_CHOOSE", model_use)
        else:
            if LLM_CHOOSE:
                st.sidebar.success(f"##### Actuellement: {LLM_CHOOSE}" if LANGUAGE == 'fr' else f"##### Currently: {LLM_CHOOSE}")
            else: 
                st.sidebar.warning("##### Veuillez choisir un modèle." if LANGUAGE == 'fr' else "##### Please choose a model.")

        model_reflexion_use = st.sidebar.selectbox('🔬 Modèle de réflexion' if LANGUAGE == "fr" else '🔬 Reflexion model', model_names, index=model_names.index(st.session_state.model_reflexion_use) if st.session_state.model_reflexion_use in model_names else 0)
        if model_reflexion_use:
            get_llm("LLM_REFLEXION", model_reflexion_use)
        else:
            if LLM_REFLEXION:
                st.sidebar.success(f"##### Actuellement: {LLM_REFLEXION}" if LANGUAGE == 'fr' else f"##### Currently: {LLM_REFLEXION}")
            else: 
                st.sidebar.warning("##### Veuillez choisir un modèle." if LANGUAGE == 'fr' else "##### Please choose a model.")

    # Display the title
    st.sidebar.markdown(f"<h3 style='padding-bottom: 0.4em;'>Réflexion Avancée</h3>" if LANGUAGE == 'fr' else
                        f"<h3 style='padding-bottom: 0.4em;'>Advanced Reflexion</h3>", unsafe_allow_html=True)

    # Display the button
    if st.sidebar.button("❌" if st.session_state.REFLEXION else "✅"):
        toggle_reflection()

    st.sidebar.markdown("<hr style='margin:0px;'>", unsafe_allow_html=True)

    # Load conversation files
    if not os.path.exists(SAVE_HISTORY_DIR):
        os.makedirs(SAVE_HISTORY_DIR)

    conversation_files = os.listdir(SAVE_HISTORY_DIR)
    conversation_files.insert(0, "")

    col1, col2 = st.sidebar.columns([3, 1])

    with col1:
        selected_file = st.selectbox("Sélectionner conversation" if LANGUAGE == 'fr' else "Select conversation", conversation_files, index=0)

    with col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if selected_file == "":
            if st.button("➕"):
                st.session_state.messages = []
                st.session_state.selected_filename = None
                st.rerun()

    if selected_file:
        st.session_state.messages = load_conversation(selected_file)
        st.session_state.selected_filename = selected_file

        new_filename = st.sidebar.text_input("Renommer la conversation" if LANGUAGE == 'fr' else "Rename the conversation")
        if st.sidebar.button("Renommer" if LANGUAGE == 'fr' else "Rename") and new_filename:
            rename_conversation(st.session_state.selected_filename, new_filename)

        if st.sidebar.button("Supprimer" if LANGUAGE == 'fr' else "Delete"):
            delete_conversation(selected_file)

        if st.sidebar.button("Télécharger en CSV"if LANGUAGE == 'fr' else "Download as CSV"):
            csv = download_conversation_as_csv(load_conversation(selected_file))
            st.sidebar.download_button(label="CSV", data=csv, file_name=f"{selected_file}.csv", mime='text/csv')
        

    # ----[PAGE ELEMENTS]----
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source_documents" in message:
                with st.expander("Voir les documents sources" if LANGUAGE == 'fr' else "View source documents"):
                    for doc in message["source_documents"]:
                        st.markdown(doc)
    # Accept user input
    if prompt := st.chat_input("Que voudriez-vous demander ?" if LANGUAGE == 'fr' else "What would you like to ask ?"):
        initial_prompt = prompt

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": initial_prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(initial_prompt)

        # Build the conversation with history
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages[-MAX_HISTORY * 2:]
        ]

        # Translate or correct the prompt if text already in english
        prompt_translated = translate_text(text=prompt, input_lang=LANGUAGE)

        if PREPROMPT:
            full_prompt = PREPROMPT + prompt_translated
        else:   
            full_prompt = prompt_translated
        print(full_prompt)

        if REFLEXION:
            # Checking if there has already been a conversation therefore user and assistant or not
            conversation = any(message.get("role") == "assistant" for message in st.session_state.messages)
            if not conversation:
                # Generate assistant response using llm_cot
                result_reflexion = llm_cot(model_name=LLM_REFLEXION, prompt=prompt_translated, conversation_history=[])
            else:
                # Generate assistant response using llm_cot
                result_reflexion = llm_cot(model_name=LLM_REFLEXION, prompt=prompt_translated, conversation_history=conversation_history)        

            full_prompt_instruction = build_full_prompt_reflexion(full_prompt, result_reflexion)

            # Inject the preprompt before sending the request
            final_prompt = full_prompt_instruction
        else:
            final_prompt = full_prompt

        # Add new user message
        conversation_history.append({"role": "user", "content": final_prompt})

        # Generate response using all recent history
        response: ChatResponse = client.chat(model=LLM_CHOOSE, messages=conversation_history)

        # Extract the content from the response
        response = response['message']['content']

        if response:
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Save the conversation
            if not st.session_state.selected_filename:
                st.session_state.selected_filename = generate_filename(st.session_state.messages)

            # Add call to save function after each message addition
            save_conversation(st.session_state.messages, st.session_state.selected_filename)
        else:
            st.error("Failed to get a response from the model.")