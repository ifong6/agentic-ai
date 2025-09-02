from typing import Dict, Any, List
from datetime import datetime
from langchain.schema import AIMessage
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from agent_config.AgentState import agentState
from tools.invoice_tools import (
    get_latest_invoice_number,
    create_invoice,
    save_invoice,
    update_invoice,
    remove_invoice
)

class InvoiceProcessOutput(BaseModel):
    invoice_info: List[Dict[str, Any]] = []
    messages: List[str]

# Tool descriptions for the prompt
tools = [
    {
        "name": "get_latest_invoice_number",
        "description": "Returns the latest invoice number from database to generate the next invoice ID (INV-JCP-XX-1)",
        "func": get_latest_invoice_number
    },
    {
        "name": "create_invoice",
        "description": "Creates an Invoice object with proper validation",
        "func": create_invoice
    },
    {
        "name": "save_invoice",
        "description": "Saves an Invoice object to the database",
        "func": save_invoice
    },
    {
        "name": "update_invoice",
        "description": "Updates an existing Invoice in the database",
        "func": update_invoice
    },
    {
        "name": "remove_invoice",
        "description": "Removes an Invoice from the database",
        "func": remove_invoice
    }
]

# React prompt template
REACT_TEMPLATE = '''
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: Process the following information into Invoice objects:

    Invoice Info:
    {invoice_info}

    Remember:
    - Invoice IDs format: INV-JCP-XX-1 (XX is sequential number)
    - Each item needs a serial number starting from 1
    - Handle errors gracefully

    Thought:{agent_scratchpad}
'''

react_prompt = PromptTemplate.from_template(REACT_TEMPLATE)

def invoice_info_processing_agent_node(state: agentState):
    print("[INVOKE][invoice_info_processing_agent_node]")
    
    try:
        # Format the prompt with current info and tools
        system_prompt = react_prompt.format(
            tools="\n".join(f"{t['name']}: {t['description']}" for t in tools),
            tool_names=", ".join(t["name"] for t in tools),
            invoice_info=state.invoice_info,
            agent_scratchpad=""  # Initial empty scratchpad
        )
        
        # TODO: Implement React agent execution logic here
        # For now, use simple processing
        
        # Process invoices
        for idx, invoice_info in enumerate(state.invoice_info):
            invoice_number = get_latest_invoice_number() + idx + 1
            invoice_serial_no = f"INV-JCP-{str(invoice_number).zfill(2)}-1"
            line_items = [{
                "serial_no": "1",
                "customer": invoice_info["customer"],
                "project_name": invoice_info["project_name"],
                "cost_mop": invoice_info["cost_mop"]
            }]
            invoice = create_invoice(invoice_serial_no, line_items)
            if save_invoice(invoice):
                state.invoices.append(invoice)
            
        return {
            "invoice_info": state.invoice_info,
            "messages": [AIMessage(content=f"Created and saved {len(state.invoices)} invoices")]
        }
        
    except Exception as e:
        error_msg = f"[Error][invoice_info_processing_agent_node]: {str(e)}"
        print(error_msg)
        return {
            "invoice_info": [],
            "messages": [AIMessage(content=error_msg)]
        }
