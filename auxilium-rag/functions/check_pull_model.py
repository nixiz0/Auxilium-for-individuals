import requests
from CONFIG import OLLAMA_API


def check_and_pull_model(model_name):
    """
    Checks if the model is present locally. If not, it downloads the model.

    Parameters:
    - model_name (str): Name of the model to check and download if necessary.
    """
    response = requests.get(f"{OLLAMA_API}/api/tags")
    if response.status_code == 200:
        data = response.json()
        ollama_models_list = [model["name"] for model in data.get("models", [])]
        if model_name not in ollama_models_list:
            print(f"Model {model_name} isn't present. Download in progress...")
            requests.post(f"{OLLAMA_API}/api/pull", json={"name": model_name})
        else:
            pass
    else:
        raise Exception(f"Ollama API Error: {response.status_code}, {response.text}")