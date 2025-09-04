from typing import Annotated, Dict, List, Optional, Any
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel
from entity.Quote import Quote
from entity.Invoice import Invoice

class agentState(BaseModel):
    user_input: str
    intents: Optional[set[str]] = None
    next_agents: Optional[list[str]] = None  #optimize using set
    
    # Lists of business objects
    quotations: List[Dict[str, Any]] = []
    invoices: List[Dict[str, Any]] = []
    pdf_path: Optional[str] = None
    
    messages: Annotated[list[AnyMessage], add_messages] = None
    steps_completed: Optional[list[str]] = None
    
    current_agent_index: int = 0
    human_feedback: Optional[list[str]] = None
    interrupt_flag: bool = False
    feedback_outcome: Optional[str] = None    # New fields for dynamic query approach
    
    extracted_info: Optional[Dict[str, Any]] = None
    query_result: Optional[Any] = None
    current_operation: Optional[str] = None
