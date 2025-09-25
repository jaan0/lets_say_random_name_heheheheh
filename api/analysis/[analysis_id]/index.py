from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the shared functions from main.py
from main import get_analysis_result

app = FastAPI(title="Analysis Status API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_analysis_status(analysis_id: str):
    """Get analysis status and results"""
    result = get_analysis_result(analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return result

# Vercel serverless function handler
def handler(request):
    return app(request.scope, request.receive, request.send)