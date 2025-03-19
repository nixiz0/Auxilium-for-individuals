import os
import re
import json
import nltk
import pandas as pd
import streamlit as st
from nltk.corpus import stopwords
from CONFIG import SAVE_HISTORY_DIR


if not os.path.exists(SAVE_HISTORY_DIR):
    os.makedirs(SAVE_HISTORY_DIR)

# Download stopwords if necessary
try:
    nltk.corpus.stopwords.words('english')
    nltk.corpus.stopwords.words('french')
except LookupError:
    nltk.download('stopwords')


def generate_filename(messages):
    """
    Generate a filename based on the content of the first message in the list.
    
    Parameters:
        messages (list): List of message dictionaries.
        
    Returns:
        str: Generated filename or default 'conversation.json'.
    """
    if messages:
        first_message = messages[0]['content']
        cleaned_message = re.sub(r'\W+', ' ', first_message).lower()
        stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))
        cleaned_message = " ".join(word for word in cleaned_message.split() if word not in stop_words)
        return "_".join(cleaned_message.split()[:5]) + ".json"
    return "conversation.json"


def save_conversation(messages, filename):
    """
    Save a list of messages to a JSON file.
    
    Parameters:
        messages (list): List of message dictionaries.
        filename (str): The name of the file to save the messages.
    """
    filepath = os.path.join(SAVE_HISTORY_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)


def load_conversation(filename):
    """
    Load messages from a JSON file.
    
    Parameters:
        filename (str): The name of the file to load messages from.
        
    Returns:
        list: List of message dictionaries.
    """
    filepath = os.path.join(SAVE_HISTORY_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def rename_conversation(old_filename, new_filename):
    """
    Rename a conversation file and clean the new filename.
    
    Parameters:
        old_filename (str): The current name of the file.
        new_filename (str): The new name of the file.
    """
    cleaned_new_filename = re.sub(r'[?!:;,]', '', new_filename)   
    old_filepath = os.path.join(SAVE_HISTORY_DIR, old_filename)
    new_filepath = os.path.join(SAVE_HISTORY_DIR, cleaned_new_filename + ".json")
    if os.path.exists(old_filepath):
        os.rename(old_filepath, new_filepath)
        
    st.session_state.selected_filename = cleaned_new_filename
    st.rerun()
    

def delete_conversation(filename):
    """
    Delete a conversation file.
    
    Parameters:
        filename (str): The name of the file to be deleted.
    """
    filepath = os.path.join(SAVE_HISTORY_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    st.session_state.selected_filename = None
    st.rerun()


def download_conversation_as_csv(messages):
    """
    Convert messages to a CSV format and return as bytes.
    
    Parameters:
        messages (list): List of message dictionaries.
        
    Returns:
        bytes: CSV formatted data as bytes.
    """
    df = pd.DataFrame(messages)
    return df.to_csv(index=False).encode('utf-8')