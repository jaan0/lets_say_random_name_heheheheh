import requests
import json

# Test the API endpoints
base_url = "http://localhost:8000"

print("Testing API endpoints...")

# Test 1: Root endpoint
try:
    response = requests.get(f"{base_url}/")
    print(f"GET / - Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error testing GET /: {e}")

# Test 2: API root endpoint
try:
    response = requests.get(f"{base_url}/api/")
    print(f"GET /api/ - Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error testing GET /api/: {e}")

# Test 3: Analyze endpoint
try:
    test_data = {"url": "https://google.com"}
    response = requests.post(f"{base_url}/api/analyze", json=test_data)
    print(f"POST /api/analyze - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error response: {response.text}")
except Exception as e:
    print(f"Error testing POST /api/analyze: {e}")

print("\nTest completed!")
