from typing import Dict, List
from datetime import datetime
import pytz
from langchain.tools import tool
from entity.Quote import Quote
from entity.LineItem import LineItem


quotation_tools = [
    {
        "name": "save_quote", 
        "description": "Save a Quote object to the database",
        "func": get_latest_quote_id_agent_node
    },
   
]