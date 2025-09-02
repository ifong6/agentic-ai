from typing import Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    serial_no: str = Field(pattern=r'^[1-9][0-9]?$')
    content: str
    quantity: str
    unit: str
    unit_price_mop: str
    subtotal_mop: Optional[str] = None

