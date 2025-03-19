import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from CONFIG import *


def ensure_vectorstore_dir():
    if not os.path.exists(VECTORSTORE_DIR):
        os.makedirs(VECTORSTORE_DIR)

def load_existing_collections(collections, document_store):
    ensure_vectorstore_dir()
    for collection_name in os.listdir(VECTORSTORE_DIR):
        collection_path = os.path.join(VECTORSTORE_DIR, collection_name)
        if os.path.isdir(collection_path):
            embeddings = OllamaEmbeddings(base_url=OLLAMA_API, model=MODEL_VECTOR)
            try:
                vector_store = FAISS.load_local(collection_path, embeddings, allow_dangerous_deserialization=True)
                collections[collection_name] = vector_store
                document_store[collection_name] = {}
                print(f"Loaded collection: {collection_name}")
            except Exception as e:
                print(f"Error loading collection {collection_name}: {str(e)}")