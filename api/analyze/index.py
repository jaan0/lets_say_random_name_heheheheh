import json
import uuid
from datetime import datetime

def handler(request):
    """Minimal Vercel serverless function handler"""
    try:
        # Handle CORS preflight
        if request.method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": ""
            }
        
        # Only allow POST requests
        if request.method != "POST":
            return {
                "statusCode": 405,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Method not allowed"})
            }
        
        # Parse request body
        try:
            body = json.loads(request.body) if request.body else {}
        except:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Invalid JSON"})
            }
        
        if "url" not in body:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "URL is required"})
            }
        
        url = body["url"]
        options = body.get("options", {})
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # For now, just return a simple response
        # In a real implementation, you would save this to a database
        # and trigger the analysis asynchronously
        
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
                "message": "Analysis started successfully",
                "url": url
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }