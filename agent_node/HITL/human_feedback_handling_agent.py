from agent_config.AgentState import agentState
from langgraph.types import Command, interrupt, Interrupt

def human_feedback_handling_agent_node(state: agentState):
    print("enter human_feedback_node")
    human_feedback = state.human_feedback[-1]
    quotation_json = state.quotation_json

    if quotation_json:
        return Command(
            update={"quotation_json": quotation_json},
            goto="quote_pdf_agent"
        )
    else:
        return Command(
            update={"human_feedback": human_feedback},
            goto="planning_agent"
        )


    

