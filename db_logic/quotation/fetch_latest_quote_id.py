from utils.Enum.HTTPStatusCode import HTTPStatusCode


def fetch_latest_quote_id():
    """
    Fetch the next available quote ID from the database.
    Returns a dict with success flag, quote ID info, and HTTP status details.
    """
    try:
        latest_quote_id = get_latest_quote_id()
        status = HTTPStatusCode.OK
        return {
            "success": True,
            "latest_quote_id": latest_quote_id,
            "http_code": status.code(),
            "http_status": f"{status.code()} {status.message()}"
        }
    except Exception as e:
        status = HTTPStatusCode.INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error": str(e),
            "http_code": status.code(),
            "http_status": f"{status.code()} {status.message()}"
        }
