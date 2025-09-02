import json
import os
from agent_config.AgentState import agentState
from langchain_core.messages import AIMessage
from utils.invoke_llm import invoke_llm
from utils.save_quote_html import save_quotation_html

InvoiceHtmlResponse={
    "type": "object",
    "properties": {
        "filledHtml": {"type": "string"}
    },
    "required": ["filledHtml"]
}

invoice_processing_prompt_template_ = """
    Fill the invoice template with the given data. Here is the mapping between JSON fields and HTML elements:
    {{
        "json_to_html_mapping": {{
            "customer": "customerName",
            "no": "QuoteNo",
            "address": "customerAddr",
            "date": "QuoteDate",
            "items": "info_items"
        }}
    }}

    IMPORTANT REQUIREMENTS:
    - Only update the relevant fields with JSON values. Do not remove or modify other HTML structure.
    
    - Preserve all button-related code exactly as provided
   
    - Preserve the JavaScript functions for:
        * PDF generation using html2pdf.bundle.min.js
        * The savePDFToFile() function that handles automatic PDF generation
   
    - Ensure the html2pdf script is properly included for PDF generation
    - The system will automatically call savePDFToFile() to generate the PDF
    
    -Preserve all line items in:
    備註：
    1. 本發票不包括任何文件運輸及提交工作;
    2. 本發票不包括文件打印服務;
    3. 本發票在發出日起30天有效;
    4. 如對本發票有何問題請與我司聯繫。

    JSON data to use:
    {invoice_json}

    INPUT HTML TEMPLATE:
    {html_src}

    OUTPUT:
    - Return the complete HTML after filling in the values. 
    - Output ONLY valid HTML, no explanations or extra text.
"""

def invoice_pdf_agent_node(state: agentState):
    print("[INVOKE][invoice_pdf_agent_node]")

    # Ensure we have invoice JSON to process
    if not state.invoice_json:
        return {
            "messages": [AIMessage(content="No invoice JSON available for processing.")]
        }

    invoice_html_template_path = f"/Users/keven/Desktop/product_v01/invoice_html_template.html"
    # Read the HTML template using absolute path
    with open(invoice_html_template_path, 'r') as f:
        html_src = f.read()

    system_prompt = invoice_processing_prompt_template_.format(
        invoice_json=json.dumps(state.invoice_json, indent=2),
        html_src=html_src
    )

    response = invoke_llm(system_prompt, InvoiceHtmlResponse)
    filled_html = response["filledHtml"]

    # Save both HTML and PDF to root directory
    output_dir = "/Users/keven/Desktop/product_v01"
    
    # Save HTML first
    html_path = save_quotation_html(filled_html, state.invoice_json, output_dir)
    
    # Save PDF using the savePDFToFile function
    pdf_filename = f"_invoice_pdf_{state.invoice_json['code_no']}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    
    return {
        "messages": [AIMessage(content=f"Invoice generated. Files saved:\nHTML: {html_path}\nPDF: {pdf_path}")]
    }
