import requests
import streamlit as st
from CONFIG import LANGUAGE, COT_API


def llm_cot(model_name=str, prompt=str, conversation_history=list):
    """
    Sends a request to the COT_API to generate a response using the specified model.

    Args:
        model_name (str): The name of the model to use for generating the response.
        prompt (str): The prompt to send to the model.

    Returns:
        str: The generated response from the model, or None if an error occurs.
    """
    url = COT_API
    data = {
        "model_name": model_name,
        "prompt": prompt,
        "conversation_history": conversation_history
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        return result["result_answer"]
    except requests.exceptions.ConnectionError:
        st.error("Veuillez démarrer et/ou installer l'outil de réflexion nécessaire." if LANGUAGE == 'fr' else 
                 "Please start and/or install the necessary reflection tool.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def build_full_prompt_reflexion(full_prompt: str, prompt_reflexion: str) -> str:
    """
    Constructs a comprehensive instruction string for an advanced language model 
    to generate the most relevant and complete response using both the user's 
    initial prompt and the intermediate reasoning generated for analysis.

    Parameters:
    full_prompt (str): The initial prompt provided by the user.
    prompt_reflexion (str): The intermediate reasoning generated to better understand and structure the response.

    Returns:
    str: A comprehensive instruction string guiding the language model to generate 
         a high-quality response that precisely addresses the user's request. The response 
         should be clear, well-structured, and leverage all useful insights from the reasoning.
    """
    full_prompt_instruction = f"""You are an advanced language model. Your goal is to generate the most relevant and complete response possible by using both the user's initial prompt and the intermediate reasoning generated for analysis.

Here is the structured process:

1. **User's initial prompt:**  
{full_prompt}  

2. **Generated reasoning to better understand and structure the response:**  
{prompt_reflexion}  

Based on these two elements, generate a final high-quality response that precisely addresses the user's request.  
Your response should be clear, well-structured, and leverage all useful insights from the reasoning.
"""
    return full_prompt_instruction