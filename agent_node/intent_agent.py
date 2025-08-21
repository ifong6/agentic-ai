from agent_config.AgentState import agentState
from pydantic import BaseModel
from typing import Literal
from utils.invoke_llm import invoke_llm
from langchain_core.messages import AIMessage

intent_prompt_template = """
    You are an AI assistant that analyzes user's input and identifies their underlying request intent(s).
  
    Your task:
    Step 1: Read the following email:
        ```text
        {user_input}

    Step 2: Identify what the sender is asking for. You only support the following two types of requests:
        - **Create** quotation 
        - **Issue** a new or replacement invoice due to loss

        Possible intents include:
            - create_quotation
            - issue_invoice

        **IMPORTANT NOTES:**
            - Customers may not use these exact words.
            - Their emails may be long, conversational, or unclear.
            - You must infer their true intent(s) from context, even if not explicitly stated.

        ------------------------------

        Examples:
        **Example 1:**  
        - **Input**: "Create a new quotation for a new customer."  
        - **Intents**: ["create_quotation"]  
        - **messages**: Explicitly asks to generate a quotation; no mention of invoice.  
        
        **Example 2:**  
        - **Input**: "Send ACME an invoice for order #123."  
        - **Intents**: ["create_invoice"]  
        - **messages**: Direct request to send an invoice for a specific order.  
        
        **Example 3:**  
        - **Input**: "First prepare a quote, then invoice after approval."  
        - **Intents**: ["create_quotation", "create_invoice"]  
        - **messages**: User asks for both steps — first a quotation, then an invoice.  
        
        **Example 4:**  
        - **Input**: "What are your rates?"  
        - **Intents**: []  
        - **messages**: Inquiry about pricing, not a request to create a quotation or invoice. 

    Step 3: Output ONLY valid JSON. REMOVE extra response, explanations or formatting. The JSON **MUST** strictly follow this schema:
        {{
            "intents": ["<all inquiry intents you identified>"],
            "messages": ["<your reasoning for the identified intents>"]
        }}
        
        **Example of the required format:**
        ```json 
        {{
          "intents": ["create_quotation"],
          "messages": ["Explicitly asks to generate a quotation; no mention of invoice."]
        }}
"""


class IntentClassifierOutput(BaseModel):
    intents: list[Literal['create_quotation', 'issue_invoice']]
    messages: str # any reasoning
    
def intent_agent_node(state: agentState):
    print("[INVOKE][intent_agent_node]")
  
    system_prompt = intent_prompt_template.format(user_input=state.user_input)
    parsed_response = invoke_llm(system_prompt, IntentClassifierOutput)

    try:
        intents = parsed_response.get("intents", []) or ["unknown"]
        llm_result_msg = parsed_response.get("messages", [])[-1].get("content", "")

    except Exception as e:
        return {
            "intents": ["unknown"],
            "messages": [AIMessage(content="[Error][intent_agent_node]: " + str(e))],
        }

    return {
        "intents": intents,
        "messages": [AIMessage(content=llm_result_msg)]
    }

    
  
    