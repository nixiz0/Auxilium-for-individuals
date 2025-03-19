import streamlit as st
import os
from CONFIG import *
from functions.llms_system.manage_conversation import *
from functions.rag_system.rag_api import *


def documents_page():
    # ----[HEADER ELEMENTS]----
    # Initialize messages history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize session state for selected filename
    if "selected_filename" not in st.session_state:
        st.session_state.selected_filename = None


    # ----[SIDEBAR ELEMENTS]----
    config_profil_check = st.sidebar.checkbox("Configuration Profils" if LANGUAGE == 'fr' else "Profils Configuration")

    st.sidebar.markdown("<hr style='margin:0px;'>", unsafe_allow_html=True)

    profils = list_collections().get("collections", [])

    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        profil_name = st.selectbox("Sélectionnez un Profil" if LANGUAGE == 'fr' else "Select a Profil", [""] + profils)
    
    with col2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if profil_name:
            if st.button("❌", key="button_del_profil"):
                result = delete_collection(profil_name)
                st.write(result)
                st.rerun()

    if profil_name == "":
        col3, col4 = st.sidebar.columns([3, 1])
        with col3:
            new_profil_name = st.text_input("Nom du nouveau Profil" if LANGUAGE == 'fr' else "Name of the new Profil")

        with col4:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("➕", key="button_add_profil"):
                if new_profil_name.strip():
                    result = create_collection(new_profil_name)
                    st.rerun()
                else:
                    st.sidebar.warning("Veuillez saisir un nom valide pour le profil." if LANGUAGE == 'fr' else "Please enter a valid profile name.")

    else:
        new_name = st.sidebar.text_input("Nouveau Nom du Profil" if LANGUAGE == 'fr' else "New Profil Name")
        if st.sidebar.button("Renommer le Profil" if LANGUAGE == 'fr' else "Rename Profil"):
            if new_name.strip():
                result = rename_collection(profil_name, new_name)
                st.rerun()
            else:
                st.sidebar.warning("Veuillez saisir un nom valide pour le profil." if LANGUAGE == 'fr' else "Please enter a valid profile name.")

    st.sidebar.markdown("<hr style='margin:0px;'>", unsafe_allow_html=True)

    # Load conversation files
    if not os.path.exists(SAVE_HISTORY_DIR):
        os.makedirs(SAVE_HISTORY_DIR)

    conversation_files = os.listdir(SAVE_HISTORY_DIR)
    conversation_files.insert(0, "")

    col1, col2 = st.sidebar.columns([3, 1])

    if not config_profil_check:
        with col1:
            selected_file = st.selectbox("Sélectionner conversation" if LANGUAGE == 'fr' else "Select conversation", conversation_files, index=0)

    if profil_name and not config_profil_check:
        with col2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if selected_file == "":
                if st.button("➕"):
                    st.session_state.messages = []
                    st.session_state.selected_filename = None
                    st.rerun()

    if not config_profil_check:
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
    if config_profil_check:
        if profil_name:
            st.header("Téléchargement de Document" if LANGUAGE == 'fr' else "Document Upload")
            uploaded_files = st.file_uploader("Choisissez des fichiers" if LANGUAGE == 'fr' else 
                                            "Choose files", type=["txt", "pdf", "docx"], accept_multiple_files=True)

            if uploaded_files:
                if st.button("Télécharger Documents" if LANGUAGE == 'fr' else "Download Documents"):
                    for file in uploaded_files:
                        result = upload_document(profil_name, file)
                        st.success(f"Upload de {file.name}: {result}" if LANGUAGE == 'fr' else f"Upload of {file.name}: {result}")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source_documents" in message:
                with st.expander("Voir les documents sources" if LANGUAGE == 'fr' else "View source documents"):
                    for doc in message["source_documents"]:
                        st.markdown(doc)

    if profil_name and not config_profil_check:
        # Accept user input
        if prompt := st.chat_input("Que voudriez-vous demander sur vos documents ?" if LANGUAGE == 'fr' else "What would you like to ask on your documents ?"):
            initial_prompt = prompt

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": initial_prompt})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(initial_prompt)

            # Build the conversation with history
            conversation_history = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages[-RAG_MAX_HISTORY * 2:]
            ]

            # Add new user message
            conversation_history.append({"role": "user", "content": initial_prompt})

            rag_conversation_history = any(message.get("role") == "assistant" for message in st.session_state.messages)
            if rag_conversation_history:
                rag_conversation_history = conversation_history
            else:
                rag_conversation_history = None

            # Call to LLM RAG with conversation history
            response = query_collection(profil_name, initial_prompt, rag_conversation_history)

            # Extract the content from the response
            response_content = response['result']
            source_documents = response['source_documents']

            if response_content:
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response_content)

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_content,
                    "source_documents": source_documents
                })

                # Save the conversation
                if not st.session_state.selected_filename:
                    st.session_state.selected_filename = generate_filename(st.session_state.messages)

                # Add call to save function after each message addition
                save_conversation(st.session_state.messages, st.session_state.selected_filename)
                st.rerun()
            else:
                st.error("Failed to get a response from the model.")