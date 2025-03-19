import os
import requests

# ----[USER CUSTOM CONFIG]----
# App Config
LANGUAGE = 'fr'

# App LLM Config
LLM_CHOOSE = "llama3.1:latest"
LLM_REFLEXION = "wizardlm2:latest"
REFLEXION = True

# ----[SYSTEM CONFIG]----
# App Paths
PATH_CONFIG_FILE = 'app/CONFIG.py'
PATH_ICON_LOGO_AUXILIUM = 'app/ressources/auxilium-logo.png'
PATH_LOGO_AUXILIUM = 'app/ressources/auxilium-logo.png'

# History Limit length (user-assistant exchanges)
MAX_HISTORY = int(os.getenv('MAX_HISTORY', 5))
RAG_MAX_HISTORY = int(os.getenv('RAG_MAX_HISTORY', 2))

# Streamlit max upload size data file
MAX_UPLOAD_SIZE_MB = int(os.getenv('MAX_UPLOAD_SIZE_MB', 10240))

# API URL LLM System
OLLAMA_API = os.getenv('OLLAMA_API', 'http://localhost:11434')
TRANSLATE_API = os.getenv("TRANSLATE_API", "http://localhost:7995/translate")
COT_API = os.getenv("COT_API", "http://localhost:7996/cot/") if REFLEXION else None
try:
    RAG_API = None if not requests.get(os.getenv("RAG_API", "http://localhost:7997"), timeout=5).ok else os.getenv("RAG_API", "http://localhost:7997")
except requests.exceptions.RequestException:
    RAG_API = None

# Language Preprompt
PREPROMPT = "Answer only in French : \n" if LANGUAGE == 'fr' else None

# Save conversation (with a volume mounted in Docker)
SAVE_HISTORY_DIR = os.getenv("SAVE_HISTORY_DIR", "conversation")