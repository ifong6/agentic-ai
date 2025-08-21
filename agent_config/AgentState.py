from typing import Annotated, Optional, Any
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel

class agentState(BaseModel):
    user_input: str
    intents: Optional[list[str]] = None
    next_agents: Optional[list[str]] = None
    
    quotation_json: Optional[Any] = None
    pdf_path: Optional[str] = None
    show_quote_form: bool = False
    
    messages: Annotated[list[AnyMessage], add_messages] = None
    steps_completed: Optional[list[str]] = None
    
    current_agent_index: int = 0
    human_feedback: Optional[list[str]] = None
    interrupt_flag: bool = False
