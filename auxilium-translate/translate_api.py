import torch
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from CONFIG import *


# Check if CUDA is available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Download and load the template and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(TRANSLATION_MODEL, cache_dir=MODEL_HF_CACHE_DIR).to(device)
tokenizer = AutoTokenizer.from_pretrained(TRANSLATION_MODEL, cache_dir=MODEL_HF_CACHE_DIR)

# Configure the translation pipeline
translator = pipeline('translation', model=model, tokenizer=tokenizer, max_length=400, device=0 if device == 'cuda' else -1)

def chunk_text(text, chunk_size):
    tokens = text.split()
    return [" ".join(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]

# FastAPI application
app = FastAPI()

class TextPayload(BaseModel):
    text: str
    input_lang: str

@app.post("/translate")
def translate_text(payload: TextPayload):
    """
    Translate the provided text to LANGUAGE_RESULT.

    Args:
        payload (TextPayload): The input text to be translated.

    Returns:
        dict: Dictionary with translated text in LANGUAGE_RESULT user want.

    Raises:
        HTTPException: If the detected language is unsupported.
    """
    text = payload.text
    input_lang = payload.input_lang

    # Check if the input language is in the mapping
    if input_lang not in LANGUAGE_TARGET_MAPPING:
        raise HTTPException(status_code=300, detail=f"Unsupported language: {input_lang}")

    # Determine the source language for the translation
    language_target = LANGUAGE_TARGET_MAPPING[input_lang]

    # Divide the text into chunks if it's too long
    chunks = chunk_text(text, CHUNK_SIZE)

    # Translate each chunk individually
    translated_chunks = []
    for chunk in chunks:
        translation = translator(chunk, src_lang=language_target, tgt_lang=LANGUAGE_RESULT)
        translated_chunks.append(translation[0]['translation_text'])

    # Combine the translated chunks into the final translated text
    translated_text = ' '.join(translated_chunks)

    return {"translated_text": translated_text}