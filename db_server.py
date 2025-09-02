# db_server.py - Database API (Port 8001)
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import PyMongoError
from utils.Response.QuoteIdResponse import QuoteIdResponse
from utils.get_db_collection import get_db_collection
from utils.Enum.CollectionEnum import CollectionEnum
from utils.Enum.DbEnum import DbEnum


# Create FastAPI app for Database operations
app = FastAPI(title="Database API", version="0.0.0", description="MongoDB operations for finance data")

# Configure CORS - Only Agent API should call Database API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",  # Agent API (only caller)
        # No Streamlit here - it should go through Agent API
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now all DB calls can read env vars
client, quotation_collection = (
    get_db_collection(CollectionEnum.QUOTATION, DbEnum.DB_FINANCE)
)

@app.get("/health")
async def health_check():
    client = None
    try:
        client.admin.command("ping")     # Ping the server

        return {
            "service": "Database API",
            "status": "HEALTHY",
            "db": DbEnum.DB_FINANCE,
        }
    except PyMongoError as e:
        return {
            "service": "Database API",
            "status": "UNHEALTHY",
            "error": str(e)
        }
    finally:
        if client:
            client.close()  # Close the connection
        

@app.get("/api/quote/latest-id", response_model=QuoteIdResponse)
async def get_latest_quote_id_api():
    """Get the next available quote ID"""
    
    try:
        latest_quote_id = get_latest_quote_id()
        return QuoteIdResponse(
            success=True,
            latest_quote_id=latest_quote_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=QuoteIdResponse(
                success=False,
                error=str(e)
            ).dict()
        )





# @app.post("/api/quote/create", response_model=QuoteResponse)
# async def create_quote(quote_request: QuoteCreateRequest):
#     """Create a new quote using the next available quote ID as _id"""
#     try:
#         # Validate and process line items
#         processed_line_items, total_amount = validate_and_process_line_items(quote_request.line_items)
        
#         # Get the next quote ID
#         next_quote_id = get_latest_quote_id()
        
#         # Determine project name based on logic
#         project_name = determine_project_name(
#             quote_request.line_items, 
#             quote_request.project_name
#         )
        
#         client = MongoClient(MONGO_URL)
#         db = client[DB_NAME]
#         collection = db[COLLECTION_NAME]
        
#         quote_data = {
#             "_id": next_quote_id,
#             "quote_id": next_quote_id,  # Also store as quote_id field for compatibility
#             "customer": quote_request.customer,
#             "project_name": project_name,
#             "status": quote_request.status,
#             "line_items": processed_line_items,  # Use processed items with numeric fields
#             "total_amount_mop": total_amount,  # Calculated total
#             "created_at": quote_request.created_at or datetime.now()
#         }
        
#         # Insert with our custom _id
#         collection.insert_one(quote_data)
        
#         client.close()
        
#         return QuoteResponse(
#             success=True,
#             quote=quote_data
#         )
#     except ValueError as ve:
#         # Handle validation errors
#         raise HTTPException(
#             status_code=400,
#             detail=QuoteResponse(
#                 success=False,
#                 error=f"Validation error: {str(ve)}"
#             ).dict()
#         )
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=QuoteResponse(
    #             success=False,
    #             error=str(e)
    #         ).dict()
    #     )
        
if __name__ == '__main__':
    print("🗄️  Starting Database API on port 8001...")
    uvicorn.run(
        "db_server:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )