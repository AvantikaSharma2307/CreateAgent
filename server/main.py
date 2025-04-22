from fastapi import FastAPI, HTTPException
from pydantic import BaseModel # type: ignore
import requests # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore


load_dotenv()

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # Frontend origin
    "http://localhost:5500"   # Optional: also allow localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows these domains to access the backend
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],            # Allow all headers
)


# Load API keys from .env or hardcode for testing
RETEll_API_KEY = os.getenv("RETELL_API_KEY", "your_retell_api_key")
VAPI_API_KEY = os.getenv("VAPI_API_KEY", "your_vapi_api_key")
llm_id=os.getenv("llm_id","your_llm_id")


# ----------- Standard Input Models --------------

class AgentRequest(BaseModel):
    provider: str  # 'retell' or 'vapi'
    voice: str
     # Only used for Retell


class VapiCallRequest(BaseModel):
    assistant_id: str
    phone_number: str
    webhook_url: str = None


# ----------- API Endpoints --------------

@app.post("/create-agent")
def create_agent(request: AgentRequest):
    if request.provider.lower() == "retell":
        return create_retell_agent(request)
    elif request.provider.lower() == "vapi":
        return create_vapi_agent(request)
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")


@app.post("/make-call")
def make_call(request: VapiCallRequest):
    return initiate_vapi_call(request)


# ----------- Provider Functions --------------

def create_retell_agent(request: AgentRequest):
    headers = {
        "Authorization": f"Bearer {RETEll_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "response_engine": {
            "type": "retell-llm",
            "llm_id": llm_id
        },
        "voice_id": request.voice,
    }

    res = requests.post("https://api.retellai.com/create-agent", json=payload, headers=headers)
    if res.status_code == 201:
        return res.json()
    else:
        raise HTTPException(status_code=res.status_code, detail=res.text)


def create_vapi_agent(request: AgentRequest):
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "voice": request.voice
    }

    res = requests.post("https://api.vapi.ai/assistant", json=payload, headers=headers)
    if res.status_code in [200, 201]:
        return res.json()
    else:
        raise HTTPException(status_code=res.status_code, detail=res.text)


def initiate_vapi_call(request: VapiCallRequest):
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "assistant_id": request.assistant_id,
        "phone_number": request.phone_number,
        "webhook_url": request.webhook_url or "https://your-default-webhook.com"
    }

    res = requests.post("https://api.vapi.ai/call", json=payload, headers=headers)

    if res.status_code in [200, 201]:
        return res.json()
    else:
        raise HTTPException(status_code=res.status_code, detail=res.text)
