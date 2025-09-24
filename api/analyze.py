from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
import asyncio
import os
from typing import Optional
import uuid
from datetime import datetime

from analyzer import WebsiteAnalyzer
from report_generator import PDFReportGenerator

app = FastAPI(title="Website Analyzer API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for analysis results (in production, use a database)
analysis_results = {}

class AnalysisRequest(BaseModel):
    url: HttpUrl
    options: Optional[dict] = {}

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    message: str

@app.get("/")
async def root():
    return {"message": "Website Analyzer API is running!"}

@app.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start website analysis in background"""
    analysis_id = str(uuid.uuid4())
    
    # Initialize analysis result
    analysis_results[analysis_id] = {
        "id": analysis_id,
        "url": str(request.url),
        "status": "started",
        "started_at": datetime.now().isoformat(),
        "progress": 0,
        "results": None,
        "error": None
    }
    
    # Start background analysis
    background_tasks.add_task(run_analysis, analysis_id, str(request.url), request.options)
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status="started",
        message="Analysis started successfully"
    )

@app.get("/analysis/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get analysis status and results"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis_results[analysis_id]

@app.get("/download/{analysis_id}")
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

async def run_analysis(analysis_id: str, url: str, options: dict):
    """Run the complete website analysis"""
    try:
        # Update status
        analysis_results[analysis_id]["status"] = "analyzing"
        analysis_results[analysis_id]["progress"] = 10
        
        # Initialize analyzer
        analyzer = WebsiteAnalyzer()
        
        # Run analysis steps
        analysis_results[analysis_id]["progress"] = 20
        performance_data = await analyzer.analyze_performance(url)
        
        analysis_results[analysis_id]["progress"] = 40
        accessibility_data = await analyzer.analyze_accessibility(url)
        
        analysis_results[analysis_id]["progress"] = 60
        seo_data = await analyzer.analyze_seo(url)
        
        analysis_results[analysis_id]["progress"] = 80
        security_data = await analyzer.analyze_security(url)
        
        analysis_results[analysis_id]["progress"] = 90
        content_data = await analyzer.analyze_content(url)
        
        # Compile results
        results = {
            "url": url,
            "analyzed_at": datetime.now().isoformat(),
            "performance": performance_data,
            "accessibility": accessibility_data,
            "seo": seo_data,
            "security": security_data,
            "content": content_data,
            "overall_score": calculate_overall_score(performance_data, accessibility_data, seo_data, security_data, content_data)
        }
        
        analysis_results[analysis_id]["results"] = results
        analysis_results[analysis_id]["progress"] = 95
        
        # Generate PDF report
        report_generator = PDFReportGenerator()
        pdf_path = await report_generator.generate_report(results, analysis_id)
        
        analysis_results[analysis_id]["status"] = "completed"
        analysis_results[analysis_id]["progress"] = 100
        analysis_results[analysis_id]["pdf_path"] = pdf_path
        
    except Exception as e:
        analysis_results[analysis_id]["status"] = "failed"
        analysis_results[analysis_id]["error"] = str(e)
        print(f"Analysis failed for {analysis_id}: {e}")

def calculate_overall_score(performance, accessibility, seo, security, content):
    """Calculate overall website score"""
    scores = []
    if performance and "score" in performance:
        scores.append(performance["score"])
    if accessibility and "score" in accessibility:
        scores.append(accessibility["score"])
    if seo and "score" in seo:
        scores.append(seo["score"])
    if security and "score" in security:
        scores.append(security["score"])
    if content and "score" in content:
        scores.append(content["score"])
    
    return round(sum(scores) / len(scores)) if scores else 0

# Vercel serverless function handler
def handler(request):
    return app(request.scope, request.receive, request.send)
