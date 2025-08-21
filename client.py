import streamlit as st
from ui.style import apply_styles, DIVIDER
import uuid
from streamlit.runtime.scriptrunner import get_script_run_ctx
from ui.update_chat_handlers import handle_chat_submit

st.set_page_config(
    page_title="AI Assistant", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Apply all styles
apply_styles()

# --- Sidebar / Navigation ---
st.sidebar.title("MENU")
st.sidebar.write("📄 創建報價單 (Create Quote Form)")
st.sidebar.write("📋 創建發票 (Create Invoice Form)")

#--------CREATE SESSION ID--------#
def create_new_session_id():
    return str(uuid.uuid4())

#--------GET SESSION ID--------#
def get_session_id():
    ctx = get_script_run_ctx()
    if ctx:
        return ctx.session_id
    else:
        return str(uuid.uuid4())

def init_session_state():
    defaults = {
        "messages": "",
        "chat_history": [],
        "session_id": create_new_session_id(),
        "show_quote_form": False,
        "quotation_data": None,
        "status": "success",
        "is_typing": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    print("Initialize session state variables\n")
    print(f"session_id: {st.session_state.session_id}\n")   

def main():
    init_session_state()

    # --- Chat Display ---
    st.subheader("PakAI – 專屬內部AI助手")
    
    # Display chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.write(f"👤 **您:** {message['content']}")
            else:
                st.write(f"🤖 **AI代理:** {message['content']}")
        st.divider()

    # --- User Input Area ---
    user_input = st.text_area(
        "在此輸入您的訊息...",
        value="create a new quotation for a new customer",
        height=50,
        help="輸入您的請求並點擊提交按鈕"
    )
    submit_button = st.button("提交", key="submit-btn", help="發送訊息給AI代理", use_container_width=True)

    # Handle submit button click
    if submit_button and user_input.strip() != "":
        handle_chat_submit(user_input)
        st.rerun()  # Refresh to show updated chat history
    
    # --- Render Quote Form Component (controlled by AI agent) ---
    if st.session_state.show_quote_form:
        st.divider()
        st.subheader("📄 報價單表單")
        st.write("I'll help you create a quotation. Please fill out the form below with the required details.")
        from ui.component.quote_form import render_quote_form
        render_quote_form()
    else:
        st.info("💬 與AI代理聊天以完成任務")
        
if __name__ == "__main__":
    main()

