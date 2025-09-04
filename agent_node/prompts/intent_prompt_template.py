from pydantic import BaseModel
from typing import Literal, List, Optional

class IntentClassifierOutput(BaseModel):
    intents: List[Literal[
        'create_quotation', 'create_invoice', 'issue_quotation',
        'read_quotation', 'read_invoice', 'issue_invoice'
        'update_quotation', 'update_invoice', 
        'delete_quotation', 'delete_invoice'
    ]]
    messages: Optional[List[str]] = None

#----------------------------------------------------------------------------------------------------------#

INTENT_SYSTEM_PROMPT = """
    You are an AI assistant that analyzes user's input and identifies their underlying request intent(s).

    Your task:
    Step 1: Read the following user input:
        ```text
        {user_input}
"""

# Supported operations section
SUPPORTED_OPERATIONS = """
    Step 2: Identify what the sender is asking for. You now support the following types of requests:

    **Create Operations:**
    - **Create** quotation
    - **Issue** a new or replacement invoice due to loss

    **Read/Query Operations:**
    - **Get/Find/Search** quotations or invoices
    - **Count** quotations or invoices
    - **List** quotations or invoices
    - **Show latest/recent** quotations or invoices
    - **Get statistics** about quotations or invoices

    **Update Operations:**
    - **Update/Modify** existing quotations or invoices
    - **Approve/Reject** quotations
    - **Change status** of quotations or invoices

    **Delete Operations:**
    - **Delete/Remove** quotations or invoices
    - **Cancel** quotations or invoices
"""

# Possible intents list
POSSIBLE_INTENTS = """
    Possible intents include:
    
    **Quotation Operations:**
    - create_quotation
    - issue_quotation
    - read_quotation
    - update_quotation
    - delete_quotation
    
    **Invoice Operations:**
    - create_invoice
    - issue_invoice
    - read_invoice
    - update_invoice
    - delete_invoice
    
    **PDF Generation:**
    - create_quotation_pdf
    - create_invoice_pdf
"""

# Important notes section
IMPORTANT_NOTES = """
    **IMPORTANT NOTES:**
        - Customers may NOT use these exact words.
        - Their emails may be long, conversational, or unclear.
        - You must infer their true intent(s) from context, even if not explicitly stated.
        - Look for action words like: get, find, show, count, list, update, change, delete, remove, etc.

    ------------------------------
"""

# Examples section
EXAMPLES = """
    Examples:
    **Example 1:**
    - **Input**: "Create a new quotation for a new customer."
    - **Intents**: ["create_quotation"]
    - **messages**: Explicitly asks to generate a quotation.

    **Example 2:**
    - **Input**: "Send ACME an INV for order #123."
    - **Intents**: ["create_invoice"]
    - **messages**: Direct request to send an invoice for a specific order.

    **Example 3:**
    - **Input**: "Get the latest quotation from 2025"
    - **Intents**: ["read_quotation"]
    - **messages**: User wants to retrieve recent quotation data.

    **Example 4:**
    - **Input**: "Count all invoices above 10000 MOP"
    - **Intents**: ["read_invoice"]
    - **messages**: User wants to count invoices matching criteria.

    **Example 5:**
    - **Input**: "Update quotation status to approved for customer XYZ"
    - **Intents**: ["update_quotation"]
    - **messages**: User wants to modify quotation status.

    **Example 6:**
    - **Input**: "First prepare a QUO, then INV after approval."
    - **Intents**: ["create_quotation", "create_invoice"]
    - **messages**: User asks for both steps — first a quotation, then an invoice.

    **Example 7:**
    - **Input**: "What are your rates?"
    - **Intents**: []
    - **messages**: Inquiry about pricing, not a request for specific operations.
"""

# Output format section
OUTPUT_FORMAT = f"""
    Step 3: Output ONLY valid JSON. REMOVE extra response, explanations or formatting. The JSON **MUST** strictly follow this schema:
        ```json
        {{
            "intents": ["<all inquiry intents you identified>"],
            "messages": ["<your reasoning for the identified intents>"]
        }}
        
        **Example of the required format:**
        ```json
        {{
            "intents": ["read_quotation"],
            "messages": ["User wants to retrieve recent quotation data based on year filter."]
        }}
"""

# Complete template using concatenation
intent_prompt_template = (
    INTENT_SYSTEM_PROMPT +
    SUPPORTED_OPERATIONS +
    POSSIBLE_INTENTS +
    IMPORTANT_NOTES +
    EXAMPLES +
    OUTPUT_FORMAT
)