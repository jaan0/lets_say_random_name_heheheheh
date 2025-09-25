import json
import os

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the shared functions from main.py
from main import get_analysis_result

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Extract analysis_id from the request path
        # The path will be something like /api/analysis/12345
        path_parts = request.path.split('/')
        analysis_id = path_parts[-1] if path_parts else None
        
        if not analysis_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Analysis ID is required"})
            }
        
        # Get analysis result
        result = get_analysis_result(analysis_id)
        if not result:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Analysis not found"})
            }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(result)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }