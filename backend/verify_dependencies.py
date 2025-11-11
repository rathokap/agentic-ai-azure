#!/usr/bin/env python
"""
Dependency Verification Script
Verifies all required and optional dependencies are properly installed
"""

import sys
import os

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_import(module_name, package_name=None, optional=False):
    """Check if a module can be imported"""
    display_name = package_name or module_name
    try:
        __import__(module_name)
        print(f"  ✓ {display_name:<40} [OK]")
        return True
    except ImportError as e:
        status = "OPTIONAL" if optional else "MISSING"
        print(f"  ✗ {display_name:<40} [{status}]")
        if not optional:
            print(f"     Error: {str(e)}")
        return False

def check_version(module_name, min_version=None):
    """Check module version"""
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"     Version: {version}")
        return True
    except Exception:
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    print_header("Environment Variables")
    
    required_vars = [
        ("AZURE_OPENAI_API_KEY", "Azure OpenAI API Key"),
        ("AZURE_OPENAI_ENDPOINT", "Azure OpenAI Endpoint"),
        ("AZURE_DEPLOYMENT_NAME", "Azure Deployment Name"),
    ]
    
    optional_vars = [
        ("AZURE_STORAGE_CONNECTION_STRING", "Azure Storage Connection"),
        ("APPLICATIONINSIGHTS_CONNECTION_STRING", "Application Insights"),
    ]
    
    all_ok = True
    
    for var_name, description in required_vars:
        if os.getenv(var_name):
            print(f"  ✓ {description:<40} [SET]")
        else:
            print(f"  ✗ {description:<40} [MISSING]")
            all_ok = False
    
    print("\n  Optional Variables:")
    for var_name, description in optional_vars:
        if os.getenv(var_name):
            print(f"  ✓ {description:<40} [SET]")
        else:
            print(f"  - {description:<40} [NOT SET]")
    
    return all_ok

def main():
    print_header("Agentic AI - Dependency Verification")
    print("Checking all required and optional dependencies...\n")
    
    # Check Core Dependencies
    print_header("Core Dependencies (Required)")
    core_deps = [
        ("langchain", "LangChain", False),
        ("langchain_openai", "LangChain OpenAI", False),
        ("langchain_community", "LangChain Community", False),
        ("langgraph", "LangGraph", False),
        ("langchain_chroma", "LangChain Chroma", False),
        ("chromadb", "ChromaDB", False),
        ("fastapi", "FastAPI", False),
        ("uvicorn", "Uvicorn", False),
        ("pydantic", "Pydantic", False),
        ("dotenv", "Python Dotenv", False),
    ]
    
    core_ok = True
    for module, name, optional in core_deps:
        if not check_import(module, name, optional):
            core_ok = False
    
    # Check Azure Dependencies
    print_header("Azure SDK Dependencies (Optional)")
    azure_deps = [
        ("azure.data.tables", "Azure Data Tables", True),
        ("azure.storage.blob", "Azure Storage Blob", True),
        ("azure.identity", "Azure Identity", True),
        ("opencensus.ext.azure.log_exporter", "OpenCensus Azure", True),
        ("applicationinsights", "Application Insights", True),
    ]
    
    azure_ok = True
    for module, name, optional in azure_deps:
        if not check_import(module, name, optional):
            azure_ok = False
    
    # Check Environment Variables
    env_ok = check_environment_variables()
    
    # Summary
    print_header("Verification Summary")
    
    if core_ok:
        print("  ✓ All core dependencies are installed")
    else:
        print("  ✗ Some core dependencies are missing")
        print("     Run: pip install -r requirements.txt")
    
    if azure_ok:
        print("  ✓ All Azure dependencies are installed")
    else:
        print("  ⚠ Some Azure dependencies are missing (optional features disabled)")
        print("     Run: pip install azure-data-tables azure-storage-blob applicationinsights")
    
    if env_ok:
        print("  ✓ Required environment variables are set")
    else:
        print("  ✗ Some required environment variables are missing")
        print("     Copy .env.example to .env and configure your credentials")
    
    print()
    
    # Exit code
    if core_ok and env_ok:
        print("🎉 Application is ready to run!")
        return 0
    else:
        print("⚠ Please fix the issues above before running the application")
        return 1

if __name__ == "__main__":
    # Load .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
    
    sys.exit(main())
