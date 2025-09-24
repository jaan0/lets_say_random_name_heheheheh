from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main import analysis_results

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/{analysis_id}")
async def download_report(analysis_id: str):
    """Download PDF report"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    result = analysis_results[analysis_id]
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
