# Dependencies & Compatibility Guide

## 📦 Complete Dependency List

### Core Dependencies (Required)

```txt
# AI & LangChain Ecosystem
langchain==0.3.14
langchain-openai==0.3.0
langchain-community==0.3.14
langgraph==0.2.64

# Vector Store
langchain-chroma==0.2.0
chromadb>=0.4.0

# API Framework
fastapi
uvicorn

# Data Models
pydantic

# Utilities
python-multipart
python-dotenv
tqdm
gdown
```

### Azure SDK Dependencies (Optional - Free Tier Compatible)

```txt
# Azure Storage (Session & Vector Store Persistence)
azure-data-tables>=12.4.0
azure-storage-blob>=12.19.0
azure-identity>=1.15.0

# Azure Monitoring (Logging & Telemetry)
azure-monitor-opentelemetry>=1.2.0
opencensus-ext-azure>=1.1.13
applicationinsights>=0.11.10
```

---

## ✅ Compatibility Matrix

| Package | Version | Python | Notes |
|---------|---------|--------|-------|
| Python | 3.11 | Required | Azure App Service supports 3.11 |
| LangChain | 0.3.14 | 3.8-3.12 | ✅ Stable |
| LangGraph | 0.2.64 | 3.8-3.12 | ✅ Stable |
| FastAPI | Latest | 3.7+ | ✅ Compatible |
| Azure SDK | Latest | 3.7+ | ✅ Free tier compatible |

---

## 🔧 Installation Options

### Option 1: Full Installation (All Features)

```powershell
# Install all dependencies including Azure integrations
cd backend
pip install -r requirements.txt
```

**Features Enabled**:
- ✅ AI Agent with LangGraph
- ✅ Azure OpenAI Integration
- ✅ Persistent Sessions (Azure Table Storage)
- ✅ Vector Store Backup (Azure Blob Storage)
- ✅ Application Insights Monitoring

### Option 2: Minimal Installation (No Azure Persistence)

```powershell
# Install only core dependencies
cd backend
pip install langchain==0.3.14 langchain-openai==0.3.0 langchain-community==0.3.14 langgraph==0.2.64 langchain-chroma==0.2.0 chromadb fastapi uvicorn pydantic python-dotenv
```

**Features Enabled**:
- ✅ AI Agent with LangGraph
- ✅ Azure OpenAI Integration
- ⚠️ In-memory sessions (lost on restart)
- ⚠️ Local ChromaDB (not backed up)
- ❌ No monitoring

### Option 3: Development Installation

```powershell
# Install with development tools
cd backend
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black mypy
```

---

## 🔍 Dependency Verification

### Check Installed Packages

```powershell
# Verify all packages are installed
pip list | Select-String -Pattern "langchain|azure|fastapi|uvicorn"
```

### Expected Output:
```
applicationinsights        0.11.10
azure-core                 1.30.0
azure-data-tables          12.4.0
azure-identity             1.15.0
azure-monitor-opentelemetry 1.2.0
azure-storage-blob         12.19.0
fastapi                    0.104.1
langchain                  0.3.14
langchain-chroma           0.2.0
langchain-community        0.3.14
langchain-openai           0.3.0
langgraph                  0.2.64
opencensus-ext-azure       1.1.13
uvicorn                    0.24.0
```

### Test Imports

```powershell
python -c "from langchain_openai import AzureChatOpenAI; print('✓ LangChain OpenAI')"
python -c "from langgraph.graph import StateGraph; print('✓ LangGraph')"
python -c "from fastapi import FastAPI; print('✓ FastAPI')"
python -c "from azure.data.tables import TableServiceClient; print('✓ Azure Tables')"
python -c "from azure.storage.blob import BlobServiceClient; print('✓ Azure Blob')"
python -c "from applicationinsights import TelemetryClient; print('✓ App Insights')"
```

---

## ⚙️ Configuration Variables

### Required Variables (Minimum)

```env
# Azure OpenAI (REQUIRED)
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
AZURE_API_VERSION=2024-02-15-preview
```

### Optional Azure Integration Variables

```env
# Azure Storage (Optional - for persistence)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_TABLE_NAME=checkpoints
AZURE_BLOB_CONTAINER_NAME=chromadb

# Feature Flags
USE_AZURE_TABLE_STORAGE=false  # Set to true when configured
USE_AZURE_BLOB_STORAGE=false   # Set to true when configured
USE_APPLICATION_INSIGHTS=false  # Set to true when configured

# Application Insights (Optional - for monitoring)
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...
```

---

## 🐛 Troubleshooting

### Issue: Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
```powershell
# Ensure you're in the correct directory
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt --upgrade
```

### Issue: Azure SDK Conflicts

**Symptom**: `ImportError: cannot import name 'TableServiceClient'`

**Solution**:
```powershell
# Uninstall and reinstall Azure packages
pip uninstall azure-data-tables azure-storage-blob -y
pip install azure-data-tables>=12.4.0 azure-storage-blob>=12.19.0
```

### Issue: LangGraph Version Mismatch

**Symptom**: `AttributeError: module 'langgraph' has no attribute 'checkpoint'`

**Solution**:
```powershell
# Ensure correct version
pip install langgraph==0.2.64 --force-reinstall
```

### Issue: ChromaDB Binary Issues

**Symptom**: `Error loading shared library` on Windows

**Solution**:
```powershell
# Install Visual C++ redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

# Or use a different ChromaDB version
pip install chromadb==0.4.22
```

---

## 🔄 Graceful Degradation

The application is designed to work with missing optional dependencies:

### Without Azure Table Storage
```
⚠ Using in-memory checkpointer (sessions will not persist across restarts)
```
**Impact**: Sessions lost on restart, but app works fine.

### Without Azure Blob Storage
```
⚠ Azure Blob Storage sync disabled
```
**Impact**: No cloud backup for ChromaDB, but local storage works.

### Without Application Insights
```
⚠ Application Insights disabled in configuration
```
**Impact**: No Azure monitoring, but local logs work.

---

## 📊 Dependency Tree

```
backend/
├── Core AI Stack
│   ├── langchain==0.3.14
│   │   ├── langchain-openai==0.3.0 (Azure OpenAI)
│   │   └── langchain-community==0.3.14
│   ├── langgraph==0.2.64 (Agent workflow)
│   └── langchain-chroma==0.2.0 (Vector store)
│       └── chromadb>=0.4.0
│
├── API Framework
│   ├── fastapi (REST API)
│   ├── uvicorn (ASGI server)
│   └── pydantic (Data validation)
│
├── Azure Integration (Optional)
│   ├── azure-data-tables>=12.4.0 (Sessions)
│   ├── azure-storage-blob>=12.19.0 (Backups)
│   └── azure-monitor-opentelemetry>=1.2.0 (Monitoring)
│       ├── opencensus-ext-azure>=1.1.13
│       └── applicationinsights>=0.11.10
│
└── Utilities
    ├── python-dotenv (Environment variables)
    ├── python-multipart (File uploads)
    ├── tqdm (Progress bars)
    └── gdown (Google Drive downloads)
```

---

## 🎯 Production Checklist

- [ ] Python 3.11 installed
- [ ] Virtual environment created
- [ ] All dependencies installed from requirements.txt
- [ ] Azure OpenAI credentials configured
- [ ] Environment variables set (.env file)
- [ ] Imports tested successfully
- [ ] Application starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Azure Table Storage configured (optional)
- [ ] Azure Blob Storage configured (optional)
- [ ] Application Insights configured (optional)

---

## 📚 Package Documentation

- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Azure Python SDK Docs](https://docs.microsoft.com/python/api/overview/azure/)
- [ChromaDB Docs](https://docs.trychroma.com/)

---

## 🔧 Quick Fix Commands

```powershell
# Reinstall everything from scratch
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Upgrade all packages
pip install -r requirements.txt --upgrade

# Check for security vulnerabilities
pip audit

# Generate current requirements
pip freeze > requirements-frozen.txt

# Install specific Azure packages only
pip install azure-data-tables azure-storage-blob applicationinsights

# Test application startup
python -c "from app import app; print('✓ App imports successfully')"
```

---

## ✅ Verification Script

Save as `verify_dependencies.py`:

```python
#!/usr/bin/env python
"""Verify all dependencies are properly installed"""

import sys

def check_import(module_name, package_name=None):
    try:
        __import__(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name}: {str(e)}")
        return False

print("Checking Core Dependencies...")
core_ok = all([
    check_import("langchain", "LangChain"),
    check_import("langchain_openai", "LangChain OpenAI"),
    check_import("langgraph", "LangGraph"),
    check_import("fastapi", "FastAPI"),
    check_import("uvicorn", "Uvicorn"),
    check_import("chromadb", "ChromaDB"),
])

print("\nChecking Azure Dependencies (Optional)...")
azure_ok = all([
    check_import("azure.data.tables", "Azure Tables"),
    check_import("azure.storage.blob", "Azure Blob"),
    check_import("applicationinsights", "Application Insights"),
])

if core_ok:
    print("\n✓ Core dependencies are properly installed")
else:
    print("\n✗ Some core dependencies are missing")
    sys.exit(1)

if not azure_ok:
    print("⚠ Azure dependencies not installed (optional features disabled)")
else:
    print("✓ Azure dependencies are properly installed")
```

Run with:
```powershell
python verify_dependencies.py
```

---

**Status**: All dependencies properly configured with graceful degradation! ✅
