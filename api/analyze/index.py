from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import asyncio
import os
from typing import Optional
import uuid
from datetime import datetime

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import WebsiteAnalyzer
from report_generator import PDFReportGenerator
from main import get_analysis_result, save_analysis_result, run_analysis

app = FastAPI(title="Website Analyzer API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Analysis results are now stored in files via main.py functions

class AnalysisRequest(BaseModel):
    url: HttpUrl
    options: Optional[dict] = {}

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    message: str

@app.post("/", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start website analysis in background"""
    analysis_id = str(uuid.uuid4())
    
    # Initialize analysis result
    analysis_result = {
        "id": analysis_id,
        "url": str(request.url),
        "status": "started",
        "started_at": datetime.now().isoformat(),
        "progress": 0,
        "results": None,
        "error": None
    }
    
    # Save initial result
    save_analysis_result(analysis_id, analysis_result)
    
    # Start background analysis
    background_tasks.add_task(run_analysis, analysis_id, str(request.url), request.options)
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status="started",
        message="Analysis started successfully"
    )

# run_analysis function is imported from main.py

# Vercel serverless function handler
def handler(request):
    return app(request.scope, request.receive, request.send)