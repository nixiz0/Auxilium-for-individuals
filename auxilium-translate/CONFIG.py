import os

# ----[Translation Model Config]----
TRANSLATION_MODEL = os.getenv('TRANSLATION_MODEL', "facebook/nllb-200-distilled-1.3B")
MODEL_HF_CACHE_DIR = os.getenv('MODEL_HF_CACHE_DIR', os.path.join(os.getcwd(), "./hf_model"))

CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 150))

# ----[Translation Languages Config]----
LANGUAGE_TARGET_MAPPING = {
    'fr': 'fra_Latn',  # French
    'en': 'eng_Latn',  # English
    'es': 'spa_Latn',  # Spanish
    'de': 'deu_Latn',  # German
    'ja': 'jpn_Jpan',  # Japanese
    'it': 'ita_Latn',  # Italian
    'zh-cn': 'zho_Hans',  # Chinese Simplified (langdetect uses 'zh-cn' for Simplified Chinese)
    'ko': 'kor_Hang',  # Korean
    'pt': 'por_Latn',  # Portuguese
    'ar': 'arb_Arab',  # Arabic
}

LANGUAGE_RESULT = os.getenv('LANGUAGE_RESULT', "eng_Latn")