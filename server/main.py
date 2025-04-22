from fastapi import FastAPI, HTTPException
from pydantic import BaseModel # type: ignore
import requests # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore


load_dotenv()

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],        
)


# Load API keys from .env 
RETEll_API_KEY = os.getenv("RETELL_API_KEY", "your_retell_api_key")
VAPI_API_KEY = os.getenv("VAPI_API_KEY", "your_vapi_api_key")
llm_id=os.getenv("llm_id","your_llm_id")




class AgentRequest(BaseModel):
    provider: str  # 'retell' or 'vapi'
    voice: str


# API Endpoints

@app.post("/create-agent")
def create_agent(request: AgentRequest):
    if request.provider.lower() == "retell":
        return create_retell_agent(request)
    elif request.provider.lower() == "vapi":
        return create_vapi_agent(request)
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")





#  Provider Functions 

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


