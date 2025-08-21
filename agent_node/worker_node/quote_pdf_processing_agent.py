import json
from agent_config.AgentState import agentState
from langchain_core.messages import AIMessage
from utils.invoke_llm import invoke_llm
from utils.save_quote_html import save_quotation_html

QuoteHtmlResponse={
    "type": "object",
    "properties": {
        "filledHtml": {"type": "string"}
    },
    "required": ["filledHtml"]
}

quote_pdf_processing_prompt_template_ = """
    Fill the invoice template with the given data. Here is the mapping between JSON fields and HTML elements:
    {{
        "json_to_html_mapping": {{
            "customer": "customerName",
            "code_no": "invoiceNo",
            "address": "customerAddr",
            "date": "invoiceDate",
            "items": "tbody"
        }}
    }}

    IMPORTANT REQUIREMENTS:
    - Only update the relevant fields with JSON values. Do not remove or modify other HTML structure.
    
    - Preserve all button-related code exactly as provided:
   
    -Preserve the JavaScript functions for row manipulation and recalculation
    
    -Preserve all line items in:
    備註：
    1. 本報價不包括任何文件運輸及提交工作；
    2. 本報價不包括文件打印服務；
    3. 本報價在發出日起60天有效；
    4. 如對本報價有何問題請與我司聯繫。

    JSON data to use:
    {quotation_json}

    INPUT HTML TEMPLATE:
    {html_src}

    OUTPUT:
    - Return the complete HTML after filling in the values. 
    - Output ONLY valid HTML, no explanations or extra text.
"""

def quote_pdf_processing_agent_node(state: agentState):
    print("[INVOKE][quote_pdf_processing_agent_node]")

    # Ensure we have quotation JSON to process
    if not state.quotation_json:
        return {
            "messages": [AIMessage(content="No quotation JSON available for processing.")]
        }

    quotation_html_template_path = f"/Users/keven/Desktop/product/quotation_modern_dynamic.html"
    # Read the HTML template using absolute path
    with open(quotation_html_template_path, 'r') as f:
        html_src = f.read()

    system_prompt = quote_pdf_processing_prompt_template_.format(
        quotation_json=json.dumps(state.quotation_json, indent=2),
        html_src=html_src
    )

    response = invoke_llm(system_prompt, QuoteHtmlResponse)
    filled_html = response["filledHtml"]

    output_dir = "/Users/keven/Desktop/product/_quotations"
    save_quotation_html(filled_html, state.quotation_json, output_dir)
   
    return {
        "messages": [AIMessage(content="quote html generated.")]
    }
    
    