from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from entity.LineItem import LineItem

# Quote class to contain quote data
class Quote(BaseModel):
    quote_id: str = Field(pattern=r'^Q-JCP-\d{2}-\d{2}-[1-9]$')
    lineItems: List[LineItem]
    status: Literal["active", "closed"] = "active"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    
