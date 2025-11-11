#!/usr/bin/env python
"""
Azure Deployment Verification Script
Checks if the deployed application is working correctly
"""

import sys
import time
import requests
from typing import Tuple

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def check_endpoint(url: str, endpoint: str, method: str = "GET", data: dict = None, timeout: int = 30) -> Tuple[bool, str]:
    """Check if an endpoint is accessible"""
    full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        if method == "GET":
            response = requests.get(full_url, timeout=timeout)
        elif method == "POST":
            response = requests.post(full_url, json=data, timeout=timeout)
        else:
            return False, f"Unsupported method: {method}"
        
        if response.status_code in [200, 201]:
            return True, f"✓ Status {response.status_code}: {response.text[:100]}"
        else:
            return False, f"✗ Status {response.status_code}: {response.text[:100]}"
    except requests.exceptions.Timeout:
        return False, f"✗ Timeout after {timeout}s"
    except requests.exceptions.ConnectionError as e:
        return False, f"✗ Connection error: {str(e)[:100]}"
    except Exception as e:
        return False, f"✗ Error: {str(e)[:100]}"

def verify_deployment(base_url: str) -> bool:
    """Verify the deployment is working"""
    print_header("Azure Deployment Verification")
    
    print(f"Target URL: {base_url}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_passed = True
    
    # Test 1: Root endpoint
    print("[1/5] Testing root endpoint...")
    success, message = check_endpoint(base_url, "/")
    print(f"  {message}")
    if not success:
        all_passed = False
    
    # Test 2: Health check
    print("\n[2/5] Testing health endpoint...")
    success, message = check_endpoint(base_url, "/health")
    print(f"  {message}")
    if not success:
        all_passed = False
    else:
        # Parse health response
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            health_data = response.json()
            print(f"  Agent Initialized: {health_data.get('agent_initialized')}")
            print(f"  Environment: {health_data.get('environment')}")
            print(f"  Azure Table Storage: {health_data.get('azure_table_storage')}")
            print(f"  Azure Blob Storage: {health_data.get('azure_blob_storage')}")
            print(f"  Application Insights: {health_data.get('application_insights')}")
        except Exception:
            pass
    
    # Test 3: API docs
    print("\n[3/5] Testing API documentation...")
    success, message = check_endpoint(base_url, "/docs")
    print(f"  {message}")
    
    # Test 4: Query endpoint (new JSON-based)
    print("\n[4/5] Testing /query endpoint (JSON)...")
    test_data = {
        "message": "Hello, I need help with my order",
        "thread_id": "deployment_test_" + str(int(time.time()))
    }
    success, message = check_endpoint(base_url, "/query", method="POST", data=test_data, timeout=60)
    print(f"  {message}")
    if not success:
        all_passed = False
    
    # Test 5: Legacy endpoint
    print("\n[5/5] Testing /support-agent endpoint (legacy)...")
    legacy_url = f"{base_url}/support-agent?query=test&uid=test123"
    try:
        response = requests.post(legacy_url, timeout=60)
        if response.status_code == 200:
            print("  ✓ Legacy endpoint working")
        else:
            print(f"  ⚠ Legacy endpoint returned {response.status_code}")
    except Exception as e:
        print(f"  ⚠ Legacy endpoint error: {str(e)[:100]}")
    
    # Summary
    print_header("Verification Summary")
    
    if all_passed:
        print("✅ All critical tests PASSED")
        print("Deployment is successful and ready for use!")
        return True
    else:
        print("❌ Some tests FAILED")
        print("Please check the Azure portal for logs and configuration")
        print("\nTroubleshooting steps:")
        print("1. Check application logs: az webapp log tail --name <app-name> --resource-group <rg-name>")
        print("2. Verify environment variables are set correctly")
        print("3. Ensure AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are configured")
        print("4. Check if the application is still starting up (wait 2-3 minutes)")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python verify_deployment.py <backend-url>")
        print("Example: python verify_deployment.py https://backend-support-agent-1234.azurewebsites.net")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    
    # Verify URL format
    if not backend_url.startswith(("http://", "https://")):
        print("❌ Error: URL must start with http:// or https://")
        sys.exit(1)
    
    # Run verification
    success = verify_deployment(backend_url)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
