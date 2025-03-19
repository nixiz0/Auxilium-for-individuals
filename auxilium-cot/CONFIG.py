import os 
OLLAMA_API = os.getenv('OLLAMA_API', 'http://localhost:11434')

LOCAL_LLM_TEST = os.getenv('LOCAL_LLM_TEST', "llama3.2")

COT_TEMPLATE_PROMPT = """Question: {question}

Let's approach this step-by-step:

1. **Understand the problem:**  
   {problem_understanding}  

2. **Identify key information:**  
   {key_information}  

3. **Develop a strategy:**  
   {strategy}  

4. **Execute the plan:**  
   {execution}  

5. **Verify the solution:**  
   {verification}  

6. **Critical reflection and self-evaluation:**  
   {critical_reflection}
   - Are there any assumptions made that need to be challenged?
   - What are the potential limitations of this approach?
   - Are there alternative perspectives or solutions that should be considered?
   - How confident am I in this solution and why?

7. **Refinement based on reflection:**  
   {refinement}
   - Based on the critical reflection, what adjustments or improvements can be made to the solution?
   - Are there any additional factors or considerations that should be incorporated?

Construction of the best final answer based on the comprehensive reflection carried out:
{final_answer}
"""


COT_CONVERSATION_TEMPLATE_PROMPT = """Question: {question}

"Here is the current history of the conversation between the user and the assistant: {conversation_history}",

Let's approach this step-by-step:

1. **Understand the problem:**  
   {problem_understanding}  

2. **Identify key information:**  
   {key_information}  

3. **Develop a strategy:**  
   {strategy}  

4. **Execute the plan:**  
   {execution}  

5. **Verify the solution:**  
   {verification}  

6. **Critical reflection and self-evaluation:**  
   {critical_reflection}
   - Are there any assumptions made that need to be challenged?
   - What are the potential limitations of this approach?
   - Are there alternative perspectives or solutions that should be considered?
   - How confident am I in this solution and why?

7. **Refinement based on reflection:**  
   {refinement}
   - Based on the critical reflection, what adjustments or improvements can be made to the solution?
   - Are there any additional factors or considerations that should be incorporated?

Construction of the best final answer based on the comprehensive reflection carried out:
{final_answer}
"""