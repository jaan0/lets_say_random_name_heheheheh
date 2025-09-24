from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the shared analysis_results from the main module
try:
    from analyze.index import analysis_results
except ImportError:
    # Fallback for when running independently
    analysis_results = {}

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

# Export the app for Vercel
handler = app
