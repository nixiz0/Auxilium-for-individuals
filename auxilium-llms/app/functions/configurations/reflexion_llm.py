import streamlit as st 
from CONFIG import PATH_CONFIG_FILE
from functions.update_config import update_config


def get_initial_state():
    """
    Reads the configuration file and returns the initial state.

    The configuration file is expected to have key-value pairs separated by ' = '.
    Converts the value to a boolean based on whether it is 'True' or not.

    Returns:
        dict: A dictionary containing the configuration keys and their corresponding boolean values.
    """
    config = {}
    with open(PATH_CONFIG_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            if ' = ' in line:
                key, value = line.strip().split(' = ')
                config[key] = value == 'True'
    return config

def toggle_reflection():
    """
    Toggles the reflection state in the session and updates the configuration file.

    The function inverts the current reflection state, updates the session state, 
    updates the configuration file with the new state, and triggers a rerun of the app.
    """
    new_state = not st.session_state.REFLEXION
    st.session_state.REFLEXION = new_state
    update_config('REFLEXION', new_state)
    st.rerun()