import json
from datetime import datetime
from typing import Dict, List, Tuple

from pyarrow import input_stream
import pytz
import requests
import streamlit as st

def build_form() -> Dict[str, str]:
    """Build a form with the quote fields and return the input values."""
    # --- Labels and internal keys ---
    fields: List[Tuple[str, str, str]] = [
        ("serial_no", "序號", "Serial No."),
        ("content", "內容", "Content"),
        ("quantity", "數量", "Quantity"),
        ("unit", "單位", "Unit"),
        ("unit_price_mop", "單價（澳門元）", "Unit Price (MOP)"),
        ("subtotal_mop", "小計（澳門元）", "Subtotal (MOP)"),
        ("customer", "客戶", "Customer"),
        ("code_no", "編號", "Code No."),
        ("address", "地址", "Address"),
        ("date", "日期", "Date"),
    ]
    
    values: Dict[str, str] = {}
    
    # Get today's date in Beijing timezone
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today_date = datetime.now(beijing_tz).strftime("%Y-%m-%d")
    
    # Split fields into two columns (5 items each)
    col1_fields = fields[:5]
    col2_fields = fields[5:]
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # First column
    with col1:
        for key, chinese_label, english_label in col1_fields:
            # Display both Chinese and English labels
            label = f"{chinese_label} / {english_label}"
            if key == "date":
                # Show today's date as read-only
                values[key] = st.text_input(label, value=today_date, disabled=True)
            elif key == "serial_no":
                values[key] = st.text_input(label, value="001", disabled=True)
            elif key == "content":
                values[key] = st.text_input(label, value="A3連接橋D匝道箱樑木模板支撐架計算", disabled=True)
            elif key == "quantity":
                values[key] = st.text_input(label, value="1", disabled=True)
            elif key == "unit":
                values[key] = st.text_input(label, value="lot", disabled=True)
            elif key == "unit_price_mop":
                values[key] = st.text_input(label, value="5000.00", disabled=True)
            else:
                values[key] = st.text_input(label, placeholder="")
    
    # Second column
    with col2:
        for key, chinese_label, english_label in col2_fields:
            # Display both Chinese and English labels
            label = f"{chinese_label} / {english_label}"
            if key == "date":
                # Show today's date as read-only
                values[key] = st.text_input(label, value=today_date, disabled=True)
            elif key == "subtotal_mop":
                # Calculate subtotal based on quantity and unit price
                quantity = float(values.get("quantity", "0") or "0")
                unit_price = float(values.get("unit_price_mop", "0") or "0")
                subtotal = quantity * unit_price
                values[key] = st.text_input(label, value=f"{subtotal:.2f}", disabled=True)
            elif key == "customer":
                values[key] = st.text_input(label, value="ABC Company Ltd.", disabled=True)
            elif key == "code_no":
                values[key] = st.text_input(label, value="QT-2024-001", disabled=True)
            elif key == "address":
                values[key] = st.text_input(label, value="123 Business Street, Macau", disabled=True)
            else:
                values[key] = st.text_input(label, placeholder="")
    
    return values, fields

def render_quote_form():
    """Render the complete quote form component."""
    with st.form("entry_form", clear_on_submit=False):
        st.subheader("創建報價單 (Create Quote)")
        st.write("請輸入以下資訊：")  # Small instruction in Chinese as the labels are Chinese.
        inputs, fields = build_form()
        submitted = st.form_submit_button("提交給AI代理 (Submit Form to AI Agent)")
        
        if submitted:
            # Validate that required fields are filled
            required_fields = ["customer", "content", "quantity", "unit", "unit_price_mop", 
                "subtotal_mop", "code_no", "address", "date", "serial_no"]
            missing_fields = [field for field in required_fields if not inputs.get(field, "").strip()]
            
            if missing_fields:
                st.error(f"請填寫以下必填欄位: {', '.join(missing_fields)}")
                return False, inputs
            else:
                # Submit the form data to the agent
                submit_form_data_to_agent(inputs)
                return True, inputs
        
        return False, inputs

def submit_form_data_to_agent(inputs: Dict[str, str]):
    """Submit form data to the AI agent via human-in-loop/feedback endpoint"""
    print("[UI][Submitting form data to the agent system]")
    
    # Build structured JSON from form inputs
    quotation_json = {
        "customer": inputs.get("customer", ""),
        "code_no": inputs.get("code_no", ""),
        "address": inputs.get("address", ""),
        "date": inputs.get("date", ""),
        "items": [
            {
                "serial_no": inputs.get("serial_no", ""),
                "description": inputs.get("content", ""),
                "quantity": inputs.get("quantity", ""),
                "unit": inputs.get("unit", ""),
                "unit_price_mop": inputs.get("unit_price_mop", ""),
                "subtotal_mop": inputs.get("subtotal_mop", ""),
            }
        ],
        "totals": {
            "subtotal_mop": inputs.get("subtotal_mop", ""),
            "currency": "MOP",
        },
    }
    
    # Compose payload for agent system
    payload = {
        "quotation_json": quotation_json,
        "message": "I want to create a quotation with the provided form data.",
        "session_id": st.session_state.get("session_id", "default_session")
    }
    
    headers = {"Content-Type": "application/json"}
    url = "http://localhost:8000/human-in-loop/feedback"

    with st.spinner("正在提交表單數據給AI代理..."):
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), timeout=300)
            
            # Try json first, fallback to text
            try:
                response_data = resp.json()
                
                # Handle different response types
                if response_data.get("status") == "success":
                    st.success("✅ 報價單處理成功！")
                    if "result" in response_data:
                        st.write("## 查看報價單:")
                        st.write(f"報價單位置: desktop/product/_quotations/quotation_{quotation_json["code_no"]}.html")
                    # Hide the form after successful submission
                    st.session_state.show_quote_form = False
                elif response_data.get("status") == "interrupt":
                    st.warning("⏸️ AI代理需要更多信息")
                    if "result" in response_data:
                        st.write("### AI代理回應:")
                        st.write(response_data["result"])
                        
                else:
                    st.error("❌ 處理請求時發生錯誤")
                    st.json(response_data)
                    
            except Exception as json_error:
                st.error(f"解析回應時發生錯誤: {json_error}")
                st.text(resp.text)
                
        except requests.exceptions.RequestException as e:
            st.error("無法連接到AI代理服務器。")
            st.exception(e)
            st.info("請確保FastAPI服務器正在運行且可訪問。")

