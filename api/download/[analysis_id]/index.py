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
        # The path will be something like /api/download/12345
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
        
        # For now, return a mock response
        # In a real implementation, you would generate and return the actual PDF
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "message": "PDF download endpoint working",
                "analysis_id": analysis_id,
                "note": "This is a mock response. In production, this would return the actual PDF file."
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