from datetime import datetime
from typing import List
import pytz
import re
from pydantic import BaseModel, Field
from entity.LineItem import LineItem

# Invoice class to contain invoice data
class Invoice(BaseModel):
    serial_no: str = Field(pattern=r'^INV-JCP-\d{2}-[1-9]$')
    line_items: List[LineItem]
    created_at: datetime
    updated_at: datetime
