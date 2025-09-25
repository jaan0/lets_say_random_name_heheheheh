import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import get_analysis_result, save_analysis_result, run_analysis

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Parse the request
        if request.method == "POST":
            return handle_analyze_request(request)
        else:
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Method not allowed"})
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }

def handle_analyze_request(request):
    """Handle the analyze request"""
    try:
        # Parse request body
        body = json.loads(request.body) if request.body else {}
        
        if "url" not in body:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "URL is required"})
            }
        
        url = body["url"]
        options = body.get("options", {})
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Initialize analysis result
        analysis_result = {
            "id": analysis_id,
            "url": url,
            "status": "started",
            "started_at": datetime.now().isoformat(),
            "progress": 0,
            "results": None,
            "error": None
        }
        
        # Save initial result
        save_analysis_result(analysis_id, analysis_result)
        
        # Start analysis (simplified - no background tasks in serverless)
        # In a real implementation, you might want to use a queue system
        try:
            import asyncio
            asyncio.run(run_analysis(analysis_id, url, options))
        except Exception as e:
            # Update result with error
            result = get_analysis_result(analysis_id)
            if result:
                result["status"] = "failed"
                result["error"] = str(e)
                save_analysis_result(analysis_id, result)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "analysis_id": analysis_id,
                "status": "started",
                "message": "Analysis started successfully"
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }