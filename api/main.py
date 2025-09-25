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

# File-based storage for analysis results (in production, use a database)
import json

def get_analysis_results():
    """Get analysis results from file storage"""
    import tempfile
    storage_path = os.path.join(tempfile.gettempdir(), 'analysis_results.json')
    try:
        with open(storage_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_analysis_results(results):
    """Save analysis results to file storage"""
    import tempfile
    storage_path = os.path.join(tempfile.gettempdir(), 'analysis_results.json')
    with open(storage_path, 'w') as f:
        json.dump(results, f)

def get_analysis_result(analysis_id):
    """Get a specific analysis result"""
    results = get_analysis_results()
    return results.get(analysis_id)

def save_analysis_result(analysis_id, result):
    """Save a specific analysis result"""
    results = get_analysis_results()
    results[analysis_id] = result
    save_analysis_results(results)

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

@app.get("/api/")
async def api_root():
    return {"message": "Website Analyzer API is running!"}

# Endpoints are now handled by individual serverless functions

async def run_analysis(analysis_id: str, url: str, options: dict):
    """Run the complete website analysis"""
    try:
        # Get current result and update status
        result = get_analysis_result(analysis_id)
        if result:
            result["status"] = "analyzing"
            result["progress"] = 10
            save_analysis_result(analysis_id, result)
        
        # Initialize analyzer
        analyzer = WebsiteAnalyzer()
        
        # Run analysis steps
        if result:
            result["progress"] = 20
            save_analysis_result(analysis_id, result)
        performance_data = await analyzer.analyze_performance(url)
        
        if result:
            result["progress"] = 40
            save_analysis_result(analysis_id, result)
        accessibility_data = await analyzer.analyze_accessibility(url)
        
        if result:
            result["progress"] = 60
            save_analysis_result(analysis_id, result)
        seo_data = await analyzer.analyze_seo(url)
        
        if result:
            result["progress"] = 80
            save_analysis_result(analysis_id, result)
        security_data = await analyzer.analyze_security(url)
        
        if result:
            result["progress"] = 90
            save_analysis_result(analysis_id, result)
        content_data = await analyzer.analyze_content(url)
        
        # Compile results
        analysis_results_data = {
            "url": url,
            "analyzed_at": datetime.now().isoformat(),
            "performance": performance_data,
            "accessibility": accessibility_data,
            "seo": seo_data,
            "security": security_data,
            "content": content_data,
            "overall_score": calculate_overall_score(performance_data, accessibility_data, seo_data, security_data, content_data)
        }
        
        if result:
            result["results"] = analysis_results_data
            result["progress"] = 95
            save_analysis_result(analysis_id, result)
        
        # Generate PDF report
        report_generator = PDFReportGenerator()
        pdf_path = await report_generator.generate_report(analysis_results_data, analysis_id)
        
        if result:
            result["status"] = "completed"
            result["progress"] = 100
            result["pdf_path"] = pdf_path
            save_analysis_result(analysis_id, result)
        
    except Exception as e:
        result = get_analysis_result(analysis_id)
        if result:
            result["status"] = "failed"
            result["error"] = str(e)
            save_analysis_result(analysis_id, result)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
