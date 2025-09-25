import json
import os
import base64

# Import from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the shared functions from main.py
from main import get_analysis_result

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Extract analysis_id from the request path
        # The path will be something like /api/download/12345
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
        
        if result["status"] != "completed":
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Analysis not completed yet"})
            }
        
        pdf_path = f"reports/{analysis_id}.pdf"
        if not os.path.exists(pdf_path):
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Report file not found"})
            }
        
        # Read and encode the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/pdf",
                "Content-Disposition": f"attachment; filename=website_analysis_{analysis_id[:8]}.pdf",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": pdf_base64,
            "isBase64Encoded": True
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }