import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable import RunnableSequence
from CONFIG import OLLAMA_API, COT_TEMPLATE_PROMPT, COT_CONVERSATION_TEMPLATE_PROMPT


app = FastAPI()

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

class PromptInput(BaseModel):
    model_name: str
    prompt: str
    conversation_history: list

# Creation of the PromptTemplate
prompt_default = PromptTemplate(
    input_variables=["question", "problem_understanding", "key_information", "strategy", "execution", "verification", "critical_reflection", "refinement", "final_answer"],
    template=COT_TEMPLATE_PROMPT
)

# Creation of the PromptTemplate
prompt_conversation = PromptTemplate(
    input_variables=["question", "conversation_history", "problem_understanding", "key_information", "strategy", "execution", "verification", "critical_reflection", "refinement", "final_answer"],
    template=COT_CONVERSATION_TEMPLATE_PROMPT
)

@app.post("/cot/")
async def run_cot(input: PromptInput):
    """
    Process a reasoning request using a Large Language Model (LLM) with a Chain of Thought (CoT) approach.

    This endpoint receives a prompt and a model name, structures the prompt using a predefined template, 
    and executes the reasoning process step by step before returning the final response.

    Args:
        input (PromptInput): A Pydantic model containing:
            - model_name (str): The name of the LLM model to use.
            - prompt (str): The question or problem to be processed.
            - conversation_history (list): The history of the conversation (optional).

    Returns:
        dict: A JSON response containing:
            - "result_answer" (str): The full reasoning process and final answer.
        
    Raises:
        HTTPException: If an error occurs during processing, returns a 500 error with details.
    """
    try:
        model_name = input.model_name
        conversation_history = input.conversation_history
        prompt = input.prompt

        check_and_pull_model(model_name)

        # Initialization of the LLM model with OllamaLLM
        llm = OllamaLLM(base_url=OLLAMA_API, model=model_name)  
            
        if conversation_history == []:
            # Creating the correct sequence with RunnableSequence
            chain = RunnableSequence(
                RunnableLambda(lambda x: prompt_default.format(**x)),  # Apply the prompt
                llm  # Pass formatted output to the model
            )

            # Execution
            full_output = chain.invoke({
                "question": prompt,
                "problem_understanding": "Let's first understand what the question is asking.",
                "key_information": "Identify the important elements in the question.",
                "strategy": "Determine the best approach to solve this problem.",
                "execution": "Apply the strategy step by step.",
                "verification": "Check if our solution makes sense and answers the original question.",
                "critical_reflection": "Let's critically evaluate our approach and solution.",
                "refinement": "Based on our critical reflection, let's refine our solution if necessary.",
                "final_answer": "Construction of the best final answer based on the comprehensive reflection carried out"
            })
        else: 
            # Creating the correct sequence with RunnableSequence
            chain = RunnableSequence(
                RunnableLambda(lambda x: prompt_conversation.format(**x)),  # Apply the prompt
                llm  # Pass formatted output to the model
            )

            # Execution
            full_output = chain.invoke({
                "question": prompt,
                "conversation_history": f"Here is the current history of the conversation between the user and the assistant: {conversation_history}\n\n",
                "problem_understanding": "Let's first understand what the question is asking.",
                "key_information": "Identify the important elements in the question.",
                "strategy": "Determine the best approach to solve this problem.",
                "execution": "Apply the strategy step by step.",
                "verification": "Check if our solution makes sense and answers the original question.",
                "critical_reflection": "Let's critically evaluate our approach and solution.",
                "refinement": "Based on our critical reflection, let's refine our solution if necessary.",
                "final_answer": "Construction of the best final answer based on the comprehensive reflection carried out"
            })
        
        return {
            "result_answer": full_output.strip(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))