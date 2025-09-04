from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agentic_flow import run_agent, resume_agent
from utils.Exception.InterrutpException import InterruptException
from utils.Request.UserRequest import UserRequest
from fastapi.staticfiles import StaticFiles

# Create FastAPI app
app = FastAPI(title="Quote & Invoice API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

thread_store = {}


QUOTATIONS_DIR = "/Users/keven/Desktop/product/_quotations"
app.mount("/quotations", StaticFiles(directory=QUOTATIONS_DIR), name="quotations")


@app.post("/call-agent")
def call_agent(user_request: UserRequest):
    print(f"Server received request:{user_request.session_id} {user_request.message}\n")
    try:
        final_result = run_agent(user_request)

        return {
            "status": "success",
            "result": final_result
        }

    except InterruptException as interrupt:
        return {
            "status": "interrupt",
            "session_id": user_request.session_id,
            "result": interrupt.value
        }
        
    except Exception as e:
        print(f"[ERROR][end_point][call_agent]: {str(e)}")
        return {
            "status": "fail",
            "result": str(e)
        }

@app.post("/human-in-loop/feedback")
def handle_human_feedback(user_request: UserRequest):
    print(f"Server received human feedback: {user_request.session_id} {user_request.message}")
    if user_request.quotation_json:
        print(f"Quotation JSON received: {user_request.quotation_json}")
    
    try:
        resume_result = resume_agent(user_request)
        return {
            "status": "success",
            "result": resume_result
        }
    
    except Exception as e:
        print("[ERROR][end_point][handle_human_feedback]", {str(e)})
        return {
            "status": "fail",
            "result": str(e)
        }


if __name__ == '__main__':
    uvicorn.run(
        "server:app",  # Replace 'your_module_name' with the actual name of your module.
        host="127.0.0.1",  # Optional: Specify the host, default is '127.0.0.1' (localhost).
        port=8000,  # Optional: Specify the port, default is 8000.
        reload=True  # Enable the auto-reload feature.
    )