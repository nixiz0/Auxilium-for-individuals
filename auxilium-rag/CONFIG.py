import os 
OLLAMA_API = os.getenv('OLLAMA_API', 'http://localhost:11434')
RAG_API_TEST = os.getenv('RAG_API_TEST', 'http://localhost:7997')

# Models for RAG config
MODEL_RESPONSE = os.getenv('MODEL_RESPONSE', 'llama3.1')
MODEL_VECTOR = os.getenv('MODEL_VECTOR', 'nomic-embed-text')

VECTORSTORE_DIR = os.getenv('VECTORSTORE_DIR', os.path.join(os.getcwd(), "./vectorstore"))

# RAG Config
CHUNCK_SIZE = int(os.getenv('CHUNCK_SIZE', 1500))
CHUNCK_OVERLAP = int(os.getenv('CHUNCK_OVERLAP', 120))
K_NUMBER_DOC_RETRIEVE = int(os.getenv('K_NUMBER_DOC_RETRIEVE', 5))