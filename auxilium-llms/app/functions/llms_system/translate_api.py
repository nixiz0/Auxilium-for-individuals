import requests
from CONFIG import TRANSLATE_API


def translate_text(text=str, input_lang=str):
    """
    Translates the given text using an external translation API.

    Args:
        text (str): The text to be translated.

    Returns:
        str: The translated text if the API call is successful.
        None: If there is an error during the API call.

    Raises:
        HTTPError: An error occurs from the API call, and the status code is returned.
    """
    url = TRANSLATE_API
    payload = {"text": text, "input_lang": input_lang}
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        translated_text = response.json().get("translated_text")
        return translated_text
    else:
        print(f"Error: {response.status_code} - {response.json().get('detail')}")
        return None