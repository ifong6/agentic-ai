from typing import Dict, Any, List
from langchain.schema import AIMessage

from agent_config.AgentState import agentState
from utils.invoke_llm import invoke_llm
from pydantic import BaseModel
from entity.Quote import Quotation
from entity.Invoice import Invoice


class InfoExtractOutput(BaseModel):
    quotations: List[Quotation] = []
    invoices: List[Invoice] = []
    messages: List[str]

SYSTEM_ROLE = """\
You are an Information Extraction Agent specialized in analyzing Chinese and English text to extract key business information.
"""

TASK = """\
Your task is to extract and categorize information for both quotations and invoices from the input text.

For each quotation or invoice, extract:
1. Customer (客戶) - Look for terms containing "有限公司", "公司", "limited", or "LLC".
2. Project Name (項目名稱) - For SINGLE sets, project_name and content are the SAME.
   For MULTIPLE sets, project_name is the MAIN project name, and content belongs to each line item.
3. Line items - A list of line items, each with a cost in MOP.
"""

PATTERN_RULES = """\
Rules for identifying multiple quotations or invoices:
- Data follows a repeating 3-item pattern: company → project → cost.
- Patterns may be separated by newlines OR spaces.

Pattern Recognition Rules:
1. Customer:
   - Contains "有限公司", "公司", "limited", "LLC", or "company".
   - Usually first in each quotation.
2. Project Description:
   - Between company name and cost.
   - Describes technical work/scope.
   - In MULTIPLE sets: this is the overarching project name.
3. Line Items:
   - Must include price in MOP.
   - Default unit: "Lot" if unspecified.
   - Sequential serial numbers (1, 2, 3...).
"""

OUTPUT_RULES = """\
Important Extraction Rules:
- Extract ALL possible quotations or invoices following the pattern.
- Use "unknown" if any field is missing.
- Always output valid JSON with keys: quotations → quote_id, status, customer, project_name, line_items.
"""

EXAMPLES = """\
------------------------------
Example 1: Newline-separated
Input:
長聯建築工程有限公司
A3連接橋D匝道箱樑木模板支撐架計算
7000MOP

Output:
{
  "quotations": [
    {
      "quote_id": "Q-JCP-25-01-1",
      "status": "active",
      "customer": "長聯建築工程有限公司",
      "project_name": "A3連接橋D匝道箱樑木模板支撐架計算",
      "line_items": [
        {
          "serial_no": "1",
          "content": "A3連接橋D匝道箱樑木模板支撐架計算",
          "quantity": "1",
          "unit": "Lot",
          "unit_price_mop": "7000",
          "subtotal_mop": "7000"
        }
      ],
      "total_amount_mop": "7000",
      "currency": "MOP"
    }
  ]
}

------------------------------
Example 2: Multiple line items
Input:
金輝A8項目模板計算
樑模板計算 5000MOP
牆體模板計算 5000MOP

Output:
{
  "quotations": [
    {
      "quote_id": "Q-JCP-25-01-1",
      "status": "active",
      "customer": "金輝",
      "project_name": "金輝A8項目模板計算",
      "line_items": [
        {
          "serial_no": "1",
          "content": "樑模板計算",
          "quantity": "1",
          "unit": "Lot",
          "unit_price_mop": "5000",
          "subtotal_mop": "5000"
        },
        {
          "serial_no": "2",
          "content": "牆體模板計算",
          "quantity": "1",
          "unit": "Lot",
          "unit_price_mop": "5000",
          "subtotal_mop": "5000"
        }
      ], 
      "total_amount_mop": "10000",
      "currency": "MOP"
    }
  ]
}
"""

# Build full prompt
info_extract_prompt_template = (
    SYSTEM_ROLE +
    TASK +
    PATTERN_RULES +
    OUTPUT_RULES +
    EXAMPLES
)


def info_extract_agent_node(state: agentState):
    print("[INVOKE][info_extract_agent_node]")
    
    system_prompt = info_extract_prompt_template.format(user_input=state.user_input)
    parsed_response = invoke_llm(system_prompt, InfoExtractOutput)
    
    try:
        # Get extracted info and messages
        quotations = parsed_response.get("quotations", [])
        invoices = parsed_response.get("invoices", [])
        llm_result_msg = parsed_response.get("messages", [])[-1]
            
        return {
            "quotations": quotations,
            "invoices": invoices,
            "messages": [AIMessage(content=llm_result_msg)]
        }
        
    except Exception as e:
        error_msg = f"[Error][info_extract_agent_node]: {str(e)}"
        print(error_msg)
        return {
            "quotations": [],
            "invoices": [],
            "messages": [AIMessage(content=error_msg)]
        }
