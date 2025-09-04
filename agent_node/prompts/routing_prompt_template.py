from pydantic import BaseModel
from typing import Optional, Literal, Set

class PlanningResultOutput(BaseModel):
    next_agents: list[str]
    messages: str

#----------------------------------------------------------------------------------------------------------#

# Intent buckets (lowercase)
QUOTATION_CRUD: Set[str] = {"read quotation", "update quotation", "delete quotation", "lookup quotation"}
QUOTATION_PDF:  Set[str] = {"create quotation", "issue quotation", "create quotation pdf"}
INVOICE_CRUD:   Set[str] = {"read invoice", "update invoice", "delete invoice", "lookup invoice"}
INVOICE_PDF:    Set[str] = {"create invoice", "issue invoice", "create invoice pdf"}

def get_detected_intents(intents: Optional[set[str]]) -> Literal["both", "quotation", "invoice", "none"]:
    s = {i.lower() for i in intents} if intents else set()
    has_quotation = bool(s & (QUOTATION_CRUD | QUOTATION_PDF))
    has_invoice   = bool(s & (INVOICE_CRUD | INVOICE_PDF))
    if has_quotation and has_invoice:
        return "both"
    elif has_quotation:
        return "quotation"
    elif has_invoice:
        return "invoice"
    else:
        return "none"

def build_routing_prompt(intents: Optional[set[str]]) -> str:
    intents = str(intents or set())
    scope = get_detected_intents(intents)

    if scope == "both":
        return f"""You are a planning agent that selects the next agent(s) to run based on detected intents.
            Detected Intents:
            
            ```text
            {intents}
            
            ---

            ## Agent Capabilities:
            - "quotation_query_agent": Generates MongoDB queries from intent and extracted quotation info.
            - "invoice_query_agent": Generates MongoDB queries from intent and extracted invoice info.
            - "quote_pdf_agent": Creates one or more quotation PDFs.
            - "invoice_pdf_agent": Creates/issues one or more invoice PDFs.
            - "final_response_agent": Formats final response and closes the conversation.

            ## Routing Logic:
            - If intent mentions quotation CRUD - "quotation_query_agent"
            - If intent mentions invoice CRUD - "invoice_query_agent"
            - If intent mentions issuing a quotation - "quote_pdf_agent"
            - If intent mentions issuing an invoice - "invoice_pdf_agent"
            - If unclear - "final_response_agent"

            ## Priority Rules:
            - Do all CRUD before any PDF generation.
            - Sequential processing; finish one operation type before the next.
            - Quotation before Invoice when both appear.
            - Read - Update - Create - Delete within CRUD.

            ## Output (JSON only):
            ```json
            {{
                "next_agents": ["<ordered list of agents>"],
                "messages": "<brief rationale, max 40 words>"
            }}
        """
        
    elif scope == "quotation":
        return f"""
            You are a planning agent that selects the next agent(s) to run based on detected intents.
            Detected Intents:
            
            ```text
            {intents}
            
            ---

            ## Agent Capabilities:
            - "quotation_query_agent": Generates MongoDB queries from intent + extracted quotation info.
            - "quote_pdf_agent": Creates one or more quotation PDFs.
            - "final_response_agent": Formats final response and closes the conversation.

            ## Routing Logic:
            - If intent mentions quotation CRUD - "quotation_query_agent"
            - If intent mentions issuing a quotation - "quote_pdf_agent"
            - If unclear - "final_response_agent"

            ## Priority Rules:
            - Complete CRUD before any PDF generation.
            - Sequential processing.
            - Read - Update - Create - Delete within CRUD.

            ## Output (JSON only):
            ```json
                {{
                    "next_agents": ["<ordered list of agents>"],
                    "messages": "<brief rationale, max 15 words>"
                }}
        """

    elif scope == "invoice":
        return f"""
            You are a planning agent that selects the next agent(s) to run based on detected intents.
            
            Detected Intents:
            
            ```text
            {intents}
        
            ---

            ## Agent Capabilities:
            - "invoice_query_agent": Generates MongoDB queries from intent + extracted invoice info.
            - "invoice_pdf_agent": Creates/issues one or more invoice PDFs.
            - "final_response_agent": Formats final response and closes the conversation.

            ## Routing Logic:
            - If intent mentions invoice CRUD - "invoice_query_agent"
            - If intent mentions issuing an invoice - "invoice_pdf_agent"
            - If unclear - "final_response_agent"

            ## Priority Rules:
            - Complete CRUD before any PDF generation.
            - Sequential processing.
            - Read - Update - Create - Delete within CRUD.

            ## Output (JSON only):
            ```json
            {{
                "next_agents": ["<ordered list of agents>"],
                "messages": "<brief rationale, max words>"
            }}
        """
        
    else:  # "none" (unrelated intents)
        return f"""You are a planning agent that selects the next agent(s) to run based on detected intents.
            Detected Intents:
            
            ```text
            {intents}
            
            ---

            ## Agent Capabilities:
            - "final_response_agent": Formats final response and closes the conversation.

            ## Routing Logic:
            - If unclear or unrelated - "final_response_agent"      

            ## Priority Rules:
            - Keep response concise.

            ## Output (JSON only):
            ```json
            {{
                "next_agents": ["<ordered list of agents>"],
                "messages": "<brief rationale, max 40 words>"
            }}
        """


