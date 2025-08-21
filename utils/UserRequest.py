from pydantic import BaseModel
from typing import Optional, Dict, Any


class UserRequest(BaseModel):
    message: str
    session_id: str
    quotation_json: Optional[Any] = None