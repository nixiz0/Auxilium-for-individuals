import re
import requests
import unicodedata
from typing import List
from CONFIG import RAG_API


def clean_collection_name(name):
    # Replace spaces with _ & Remove accents & prohibited special characters
    name = name.replace(" ", "_")
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return name

# ----[Manage Collection Functions]----
def create_collection(collection_name):
    collection_name = clean_collection_name(collection_name)
    response = requests.post(f"{RAG_API}/create_collection/", json={"collection_name": collection_name})
    return response.json()

def delete_collection(collection_name):
    response = requests.delete(f"{RAG_API}/delete_collection/", json={"collection_name": collection_name})
    return response.json()

def rename_collection(old_name, new_name):
    new_name = clean_collection_name(new_name)
    response = requests.put(f"{RAG_API}/rename_collection/", json={"old_name": old_name, "new_name": new_name})
    return response.json()

def list_collections():
    response = requests.get(f"{RAG_API}/list_collections/")
    return response.json()

def upload_document(collection_name, file):
    files = {"file": file}
    response = requests.post(f"{RAG_API}/upload_document/?collection_name={collection_name}", files=files)
    return response.json()

def query_collection(collection_name, query, history: List[dict] = None):
    if history is None:
        history = []
    
    # Format history as a list of strings
    formatted_history = [f"{msg['role']}: {msg['content']}" for msg in history]
        
    response = requests.post(f"{RAG_API}/query_collection/", json={
        "collection_name": collection_name,
        "query": query,
        "history": formatted_history
    })
    return response.json()