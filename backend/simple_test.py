"""
Simple test to see the full response from /demo endpoint
"""
import requests
import json
import time

print("Calling POST /demo endpoint...")
start_time = time.time()

try:
    response = requests.post(
        "http://localhost:8000/demo",
        json={"interval_seconds": 0}  # Set to 0 for faster execution
    )
    
    elapsed = time.time() - start_time
    print(f"\nRequest completed in {elapsed:.2f} seconds")
    print(f"Status Code: {response.status_code}")
    print(f"\nFull Response:")
    print(json.dumps(response.json(), indent=2))
    
except Exception as e:
    print(f"Error: {str(e)}")
