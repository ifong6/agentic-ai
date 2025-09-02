from langchain_core.messages import AIMessage
from pydantic import BaseModel

from agent_config.AgentState import agentState
from utils.invoke_llm import invoke_llm

routing_prompt_template = """
    You are a planning agent responsible for determining the next best agent(s) to handle the task, 
    based on the user's intents and feedback from a human reviewer.

    ---

    Detected Intents:
        {intents}

    Info Items:
        {info_items}
    ---

    ## Agent Capabilities:
        - `"quote_pdf_agent"`: Handles creating one more multiple quotations.
        - `"invoice_pdf_agent"`: issues one more multiple invoices.
        - `"final_response_agent"`: confirm with user before closes the conversation.

    ---

    ## Instructions:
        1. Prioritize create quotation before issuing invoice, if both are needed.
        2. If **no specific intent applies** route to `"final_response_agent"`.

    ---

    ## Output Format:
        Output ONLY valid JSON. Do not include explanations or formatting. The JSON must strictly follow this schema:
        ```json
            {{
                "next_agents": ["<a list of next agents to invoke with sorted priorities per your analysis>"],
                "messages": "<Explaining your reasoning and thought process of your planning result>"
            }}
 
"""

class PlanningResultOutput(BaseModel):
    feedback_outcome: str
    next_agents: list[str]
    messages: str

def planning_agent_node(state: agentState):
    print("- [INVOKE] [planning_agent_node]")

    system_prompt = routing_prompt_template.format(
        intents=state.intents,
        info_items=state.info_items
    )
    parsed_response = invoke_llm(system_prompt, PlanningResultOutput)

    try:
        next_agents = parsed_response.get("next_agents", [])  # the next agents per planning result
        messages = parsed_response.get("messages", "")[-1]

        return {
            "next_agents": next_agents,
            "messages": [AIMessage(content=messages)]
        }

    except Exception as e:
        print(f"[ERROR][planning_agent_node] {e}")
        return {
            "messages": [AIMessage(content=f"[PlanningAgent Error] {e}")]
        }

