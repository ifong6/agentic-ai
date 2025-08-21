from agent_node.display_quote_file_agent import display_quote_file_agent_node
from agent_node.human_feedback_handling_agent import human_feedback_handling_agent_node
from agent_node.intent_agent import intent_agent_node
from agent_node.worker_node.quotation_agent import quotation_agent_node
from agent_node.worker_node.invoice_agent import invoice_agent_node
from agent_node.final_response_agent import final_response_agent_node
from agent_node.planning_agent import planning_agent_node
from agent_node.result_summary_agent import result_summary_agent_node
from agent_node.worker_node.quote_pdf_processing_agent import quote_pdf_processing_agent_node

AGENT_NODES = {
    "intent_agent": intent_agent_node,
    "planning_agent": planning_agent_node,
    "quotation_agent": quotation_agent_node,
    "human_feedback_handling_agent": human_feedback_handling_agent_node,
    "quote_pdf_processing_agent": quote_pdf_processing_agent_node,
    "display_quote_file_agent": display_quote_file_agent_node,
    "invoice_agent": invoice_agent_node,
    "result_summary_agent": result_summary_agent_node,
    "final_response_agent": final_response_agent_node
}

# ------------ agentic_flow_config for static edges ------------
STATIC_EDGES = [
    ("intent_agent", "planning_agent"),
    ("quotation_agent", "human_feedback_handling_agent"),
    ("quote_pdf_processing_agent", "display_quote_file_agent"),
    ("invoice_agent", "final_response_agent"),
]

CONDITIONAL_EDGES = [
    {
        "source": "planning_agent",
        "path": lambda state: state.next_agents[state.current_agent_index],
        "path_map": {
            "quotation_agent": "quotation_agent",
            "invoice_agent": "invoice_agent",
        }
    }
]