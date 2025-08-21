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

    Human Feedback:
        {human_feedback}

    ---

    ## Agent Capabilities:
        - quotation_agent: Handles creating quotation.
        - invoice_agent: issues invoice
        - result_summary_agent: generate result summary.
        - final_response_agent: confirm with user before closes the conversation.

    ---

    ## Instructions:
        1. Read the human feedback carefully. If it indicates confirmation (e.g. "approved", "finalized"), proceed with planning.
        2. Set `"feedback_outcome"` to one of the following values:
            - `"approved"`: if the human feedback confirms all key information and approves the plan.
            - `"edit"`: if the human asked for changes, clarification, or flagged issues.
            - `"unclear"`: if the feedback is vague or insufficient to proceed.
            - `"rejected"`: if the feedback indicates a complete rejection of the plan or request.
            - `"done"`: if the human feedback indicates the conversation is complete and no further action is needed.

        3. If `"feedback_outcome"` is `"approved"`, choose one or more relevant assistant agents in `"next_agents"` based on the intent(s).
        4. Prioritize create quotation before issuing invoice, if both are needed.
        5. If **no specific intent applies** or **human request is "done"**, route to `"final_response_agent"`.

    ---

    ## Output Format:
        Output ONLY valid JSON. Do not include explanations or formatting. The JSON must strictly follow this schema:
        ```json
            {{
                "feedback_outcome": "<the feedback outcome you analyzed from the human feedback>",
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
        human_feedback=state.human_feedback[-1] if state.human_feedback else "No feedback"
    )
    parsed_response = invoke_llm(system_prompt, PlanningResultOutput)

    try:
        feedback_outcome = parsed_response.get("feedback_outcome", "").lower()
        next_agents = parsed_response.get("next_agents", [])  # the next agents per planning result
        reasoning = parsed_response.get("reasoning", "")
        messages = parsed_response.get("messages", [])[-1].get("content", "")

        return {
            "feedback_outcome": [feedback_outcome],
            "next_agents": next_agents,
            "reasoning": reasoning,
            "messages": [AIMessage(content=messages)]
        }

    except Exception as e:
        print(f"[ERROR][planning_agent_node] {e}")
        return {
            "messages": [AIMessage(content=f"[PlanningAgent Error] {e}")]
        }

