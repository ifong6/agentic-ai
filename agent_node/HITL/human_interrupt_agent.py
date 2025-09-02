from agent_config.AgentState import agentState
from langgraph.types import interrupt, Command
from langchain_core.messages import AIMessage

def quotation_agent_node(state: agentState):
    print("[INVOKE][quotation_agent_node]")

    return interrupt(
        value={
            "show_quote_form": True,
            "message": AIMessage(content="Proceed to form data input"),
            "quotation_json": state.quotation_json,
        }
    )












