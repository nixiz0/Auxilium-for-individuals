import time
from fastapi.testclient import TestClient
from CONFIG import LOCAL_LLM_TEST
from cot_api import app


client = TestClient(app)

def test_run_cot():
    """
    Tests the Chain of Thought (CoT) API with a specific model and prompt.

    This function checks if the specified model is available and downloads it if necessary. 
    Then, it sends a POST request to the CoT API with the model name and prompt, and verifies the response.

    Raises:
    AssertionError: If the API response status is not 200 or if the response does not contain the expected keys.
    """

    # Set input data for testing
    input_data = {
        "model_name": LOCAL_LLM_TEST,
        "prompt": "How much is 5 × 3 + 84 - 8 / 4 ?",
        "conversation_history": []
    }
    
    # Send a POST request to the API
    response = client.post("/cot/", json=input_data)
    
    # Check response status
    assert response.status_code == 200
    result = response.json()
    
    # Check that the response contains the "result_answer" keys
    assert "result_answer" in result
    
    # Show results for verification
    print("Answer:", result["result_answer"])
    time.sleep(4)