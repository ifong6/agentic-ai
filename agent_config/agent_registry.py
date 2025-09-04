from agent_node.info_processing_agents.quotation_query_agent import quotation_query_agent_node
from agent_node.info_processing_agents.invoice_query_agent import invoice_query_agent_node
from agent_node.info_extract_agent import info_extract_agent_node
from agent_node.intent_agent import intent_agent_node
from agent_node.final_response_agent import final_response_agent_node
from agent_node.planning_agent import planning_agent_node
from agent_node.pdf_agents.quote_pdf_agent import quote_pdf_agent_node
from agent_node.pdf_agents.invoice_pdf_agent import invoice_pdf_agent_node

AGENT_NODES = {
    "intent_agent": intent_agent_node,
    "info_extract_agent": info_extract_agent_node,
    "planning_agent": planning_agent_node,
    "quotation_query_agent": quotation_query_agent_node,
    "invoice_query_agent": invoice_query_agent_node,
    "quote_pdf_agent": quote_pdf_agent_node,
    "invoice_pdf_agent": invoice_pdf_agent_node,
    "final_response_agent": final_response_agent_node
}

# ------------ agentic_flow_config for static edges ------------
STATIC_EDGES = [
    ("intent_agent", "info_extract_agent"),
    ("info_extract_agent", "planning_agent"),
    ("quotation_query_agent", "planning_agent"),
    ("invoice_query_agent", "planning_agent"),
]

CONDITIONAL_EDGES = [
    {
        "source": "planning_agent",
        "path": lambda state: state.next_agents[state.current_agent_index],
        "path_map": {
            "quotation_query_agent": "quotation_query_agent",
            "invoice_query_agent": "invoice_query_agent",
            "quote_pdf_agent": "quote_pdf_agent",
            "invoice_pdf_agent": "invoice_pdf_agent",
            "final_response_agent": "final_response_agent",
        }
    }
]