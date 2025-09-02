from entity.Quote import Quote
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------- DynamoDB Mapping ----------
def quote_to_ddb_item(quote: Quote):
    """
    Convert a Quote into a DynamoDB item.
    - PK/SK derived from quote_id
    - lineItems stays a LIST (simple, preserves order)
    """
    body = {
        "status": quote.status,
        "lineItems": [li.dict() for li in quote.lineItems],  # store as list
    }

    return {
        "PK": f"QUOTE#{quote.quote_id}",
        "SK": f"QUOTE#{quote.quote_id}",
        **body,
    }
    
    
# Beijing timezone
CN_TZ = ZoneInfo("Asia/Shanghai")

def _now_cn_iso() -> str:
    """Return ISO-8601 UTC+8 timestamp with seconds precision."""
    return datetime.now(CN_TZ).replace(microsecond=0).isoformat()