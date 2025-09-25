import json

def handler(request):
    """Minimal Vercel serverless function handler"""
    try:
        # Handle CORS preflight
        if request.method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": ""
            }
        
        # Only allow GET requests
        if request.method != "GET":
            return {
                "statusCode": 405,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Method not allowed"})
            }
        
        # Extract analysis_id from the request path
        # The path will be something like /api/analysis/12345
        path_parts = request.path.split('/')
        analysis_id = path_parts[-1] if path_parts else None
        
        if not analysis_id:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Analysis ID is required"})
            }
        
        # For now, return a mock result
        # In a real implementation, you would retrieve this from a database
        mock_result = {
            "id": analysis_id,
            "url": "https://example.com",
            "status": "completed",
            "started_at": "2024-01-01T00:00:00",
            "progress": 100,
            "results": {
                "overall_score": 85,
                "performance": {"score": 80},
                "accessibility": {"score": 90},
                "seo": {"score": 85}
            },
            "error": None
        }
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(mock_result)
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