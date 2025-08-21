from typing import Any, List
from langchain_core.messages import BaseMessage

def to_text_list(messages: List[Any]) -> List[str]:
    out: List[str] = []
    for m in messages:
        if isinstance(m, str):
            out.append(m)
        elif isinstance(m, BaseMessage):  # HumanMessage, AIMessage, SystemMessage, ToolMessage
            out.append(m.content or "")
        elif isinstance(m, dict):
            out.append(str(m.get("content", "")))
        else:
            # last resort: try content attr or fallback to str
            out.append(getattr(m, "content", str(m)))
    return out