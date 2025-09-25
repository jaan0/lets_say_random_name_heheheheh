from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the shared functions from main.py
from main import get_analysis_result

app = FastAPI(title="Download API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def download_report(analysis_id: str):
    """Download PDF report"""
    result = get_analysis_result(analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail="Analysis not completed yet")
    
    pdf_path = f"reports/{analysis_id}.pdf"
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        path=pdf_path,
        filename=f"website_analysis_{analysis_id[:8]}.pdf",
        media_type="application/pdf"
    )

# Vercel serverless function handler
def handler(request):
    return app(request.scope, request.receive, request.send)