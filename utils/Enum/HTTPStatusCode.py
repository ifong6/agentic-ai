from enum import Enum

class HTTPStatusCode(Enum):
    OK = (200, "OK")
    CREATED = (201, "Created")
    ACCEPTED = (202, "Accepted")
    NO_CONTENT = (204, "No Content")
    
    BAD_REQUEST = (400, "Bad Request")
    UNAUTHORIZED = (401, "Unauthorized")
    FORBIDDEN = (403, "Forbidden")
    NOT_FOUND = (404, "Not Found")
    METHOD_NOT_ALLOWED = (405, "Method Not Allowed")
    CONFLICT = (409, "Conflict")
    
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
    NOT_IMPLEMENTED = (501, "Not Implemented")
    BAD_GATEWAY = (502, "Bad Gateway")
    SERVICE_UNAVAILABLE = (503, "Service Unavailable")

    def code(self):
        return self.value[0]

    def message(self):
        return self.value[1]
