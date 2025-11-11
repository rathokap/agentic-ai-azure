# 🚀 Azure Deployment Readiness Checklist

## Pre-Deployment Checklist

### 1. ✅ Azure Resources Prerequisites

- [ ] **Azure Subscription**: Active subscription with sufficient credits
- [ ] **Azure CLI Installed**: Run `az --version` to verify
- [ ] **Logged into Azure**: Run `az login`
- [ ] **Correct Subscription Selected**: Run `az account show`

### 2. ✅ Azure OpenAI Configuration

- [ ] **Azure OpenAI Resource Created**: In Azure Portal
- [ ] **Model Deployed**: GPT-4 or GPT-3.5-turbo deployed
- [ ] **API Key Obtained**: From Keys and Endpoint section
- [ ] **Endpoint URL Noted**: Format: `https://YOUR-RESOURCE.openai.azure.com/`
- [ ] **Deployment Name Noted**: Name of your model deployment

### 3. ✅ Local Testing Completed

- [ ] **Backend runs locally**: `cd backend && python app.py`
- [ ] **Health endpoint works**: `curl http://localhost:8000/health`
- [ ] **Query endpoint works**: Test with sample query
- [ ] **Dependencies verified**: `python verify_dependencies.py` passes
- [ ] **Frontend connects**: Frontend can communicate with backend

### 4. ✅ Code Preparation

- [ ] **Environment variables reviewed**: Check `.env.example`
- [ ] **Secrets not committed**: `.env` in `.gitignore`
- [ ] **Requirements.txt updated**: All dependencies listed with versions
- [ ] **Startup scripts present**: `startup.sh`, `startup.txt`, `web.config`
- [ ] **Gunicorn configured**: `gunicorn.conf.py` present
- [ ] **Code committed to Git**: All changes pushed to repository

### 5. ✅ Azure Storage Configuration (Optional but Recommended)

- [ ] **Storage Account Created**: For session persistence
- [ ] **Connection String Obtained**: From Access Keys
- [ ] **Table Storage Container**: Will be auto-created
- [ ] **Blob Storage Container**: Will be auto-created
- [ ] **Feature flags configured**: `USE_AZURE_TABLE_STORAGE=true`

### 6. ✅ Application Insights Configuration (Optional)

- [ ] **Application Insights Resource Created**
- [ ] **Instrumentation Key Obtained**
- [ ] **Connection String Obtained**
- [ ] **Feature flag configured**: `USE_APPLICATION_INSIGHTS=true`

---

## Deployment Checklist

### Method 1: Automated Deployment Script

```powershell
# Run the automated deployment script
.\deploy-to-azure.ps1 `
    -AzureOpenAIKey "your-key" `
    -AzureOpenAIEndpoint "https://your-resource.openai.azure.com/" `
    -AzureDeploymentName "your-deployment-name"
```

**Checklist:**
- [ ] Script completed without errors
- [ ] Resource group created: `rg-support-agent`
- [ ] App Service created: Backend app name noted
- [ ] Static Web App created: Frontend app name noted
- [ ] Storage Account created: Storage account name noted
- [ ] Application Insights created
- [ ] Environment variables configured
- [ ] Deployment configuration file saved

### Method 2: Manual Deployment

#### Backend Deployment

**Step 1: Create Resources**
```powershell
# Set variables
$RESOURCE_GROUP = "rg-support-agent"
$LOCATION = "eastus"
$APP_NAME = "backend-support-agent-$(Get-Random -Minimum 1000 -Maximum 9999)"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan (F1 Free Tier)
az appservice plan create `
    --name plan-support-agent `
    --resource-group $RESOURCE_GROUP `
    --sku F1 `
    --is-linux

# Create Web App
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan plan-support-agent `
    --name $APP_NAME `
    --runtime "PYTHON:3.11"
```

- [ ] Resource group created
- [ ] App Service Plan created (F1 tier)
- [ ] Web App created
- [ ] App name saved: `_________________`

**Step 2: Configure Environment Variables**
```powershell
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $APP_NAME `
    --settings `
        AZURE_OPENAI_API_KEY="your-key" `
        AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/" `
        AZURE_DEPLOYMENT_NAME="your-deployment" `
        AZURE_API_VERSION="2024-02-15-preview" `
        ENVIRONMENT="production" `
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
        ENABLE_ORYX_BUILD="true"
```

- [ ] All environment variables configured
- [ ] Build settings enabled
- [ ] Settings verified in portal

**Step 3: Configure Startup Command**
```powershell
az webapp config set `
    --resource-group $RESOURCE_GROUP `
    --name $APP_NAME `
    --startup-file "startup.sh"
```

- [ ] Startup command configured
- [ ] Verified in Configuration > General Settings

**Step 4: Deploy Code**
```powershell
cd backend
az webapp up --name $APP_NAME --resource-group $RESOURCE_GROUP
```

- [ ] Deployment initiated
- [ ] Build logs checked (no errors)
- [ ] Application started successfully

#### Frontend Deployment

**Step 1: Create Static Web App**
```powershell
az staticwebapp create `
    --name swa-support-agent `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION
```

- [ ] Static Web App created
- [ ] Deployment token obtained
- [ ] App URL noted: `_________________`

**Step 2: Configure Frontend Environment**
- [ ] Update `frontend/.env` with backend URL
- [ ] Build frontend: `npm run build`
- [ ] Test build locally: `npm run preview`

**Step 3: Deploy Frontend**
```powershell
cd frontend
swa deploy --app-location ./dist --env production
```

- [ ] Frontend deployed
- [ ] Accessible via Static Web App URL
- [ ] Backend connection working

---

## Post-Deployment Verification

### 1. ✅ Backend Verification

**Test Endpoints:**
```powershell
$BACKEND_URL = "https://YOUR-BACKEND-NAME.azurewebsites.net"

# Test root
curl $BACKEND_URL

# Test health
curl $BACKEND_URL/health

# Test API docs
Start-Process "$BACKEND_URL/docs"
```

- [ ] Root endpoint returns 200
- [ ] Health endpoint shows healthy status
- [ ] Agent initialized: `true`
- [ ] Azure services status shown
- [ ] API docs accessible

**Test Query Endpoint:**
```powershell
curl -X POST "$BACKEND_URL/query" `
    -H "Content-Type: application/json" `
    -d '{"message":"Hello, I need help","thread_id":"test123"}'
```

- [ ] Query returns valid response
- [ ] Response time acceptable (< 30s)
- [ ] No errors in response

### 2. ✅ Frontend Verification

- [ ] Frontend loads in browser
- [ ] Chat interface displays correctly
- [ ] Can send messages
- [ ] Receives AI responses
- [ ] No CORS errors in console
- [ ] Conversation history works

### 3. ✅ Integration Verification

- [ ] Frontend successfully calls backend
- [ ] CORS configured correctly
- [ ] Sessions persist (if using Table Storage)
- [ ] No authentication errors
- [ ] End-to-end flow works

### 4. ✅ Monitoring Verification

**Check Logs:**
```powershell
# Stream logs
az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download --name $APP_NAME --resource-group $RESOURCE_GROUP
```

- [ ] Application logs accessible
- [ ] No critical errors
- [ ] Startup successful
- [ ] Requests being logged

**Check Application Insights (if configured):**
- [ ] Telemetry data appearing
- [ ] Request tracking working
- [ ] Exception tracking enabled
- [ ] Custom events logged

### 5. ✅ Performance Verification

- [ ] Response time < 30 seconds for queries
- [ ] Health check < 5 seconds
- [ ] No memory leaks observed
- [ ] CPU usage reasonable
- [ ] Cold start time acceptable

### 6. ✅ Security Verification

- [ ] HTTPS enabled (default for Azure)
- [ ] Environment variables not exposed
- [ ] API keys secured in App Settings
- [ ] CORS restricted to frontend domain
- [ ] No sensitive data in logs

---

## CI/CD Setup (Optional)

### GitHub Actions Configuration

**Step 1: Add GitHub Secrets**

Navigate to: `https://github.com/YOUR-USERNAME/agentic-ai/settings/secrets/actions`

Add these secrets:
- [ ] `AZURE_WEBAPP_PUBLISH_PROFILE` - From Azure Portal
- [ ] `AZURE_STATIC_WEB_APPS_API_TOKEN` - From Static Web App
- [ ] `VITE_API_URL` - Your backend URL

**Step 2: Update Workflow Files**

Update `.github/workflows/backend-deploy.yml`:
- [ ] `AZURE_WEBAPP_NAME` set to your backend app name
- [ ] Workflow file committed

Update `.github/workflows/frontend-deploy.yml`:
- [ ] Static Web App name configured
- [ ] Workflow file committed

**Step 3: Test CI/CD**
- [ ] Push code to main branch
- [ ] GitHub Actions workflow triggered
- [ ] Backend deployment successful
- [ ] Frontend deployment successful
- [ ] Deployed app working correctly

---

## Troubleshooting Checklist

### If Backend Won't Start:

- [ ] Check application logs: `az webapp log tail`
- [ ] Verify environment variables in Portal
- [ ] Check startup command in Configuration
- [ ] Verify Python version (3.11)
- [ ] Check if build completed: Look for Oryx build logs
- [ ] Test startup script locally
- [ ] Verify requirements.txt has no errors

### If Queries Fail:

- [ ] Verify AZURE_OPENAI_API_KEY is correct
- [ ] Check AZURE_OPENAI_ENDPOINT format
- [ ] Verify deployment name matches
- [ ] Check API version compatibility
- [ ] Review Application Insights for errors
- [ ] Check if agent initialized (health endpoint)

### If Frontend Can't Connect:

- [ ] Verify backend URL in frontend .env
- [ ] Check CORS configuration in backend
- [ ] Verify backend is accessible
- [ ] Check browser console for errors
- [ ] Test backend URL directly
- [ ] Verify no mixed content (HTTP/HTTPS) issues

### If Sessions Don't Persist:

- [ ] Verify Storage Account connection string
- [ ] Check USE_AZURE_TABLE_STORAGE=true
- [ ] Verify Table Storage accessible
- [ ] Check for table creation errors in logs
- [ ] Test Storage Account connectivity

---

## Rollback Procedure

If deployment fails:

```powershell
# Stop the app
az webapp stop --name $APP_NAME --resource-group $RESOURCE_GROUP

# Swap deployment slots (if configured)
az webapp deployment slot swap `
    --name $APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --slot staging `
    --target-slot production

# Or redeploy previous version
az webapp deployment source config-zip `
    --name $APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --src previous-version.zip

# Restart
az webapp start --name $APP_NAME --resource-group $RESOURCE_GROUP
```

- [ ] Rollback procedure documented
- [ ] Previous version backup available
- [ ] Rollback tested and working

---

## Production Readiness Sign-off

### Backend
- [ ] ✅ All pre-deployment checks passed
- [ ] ✅ Deployment successful
- [ ] ✅ All endpoints responding correctly
- [ ] ✅ Health checks passing
- [ ] ✅ Logging configured
- [ ] ✅ Monitoring enabled

### Frontend
- [ ] ✅ Build successful
- [ ] ✅ Deployment successful
- [ ] ✅ UI loading correctly
- [ ] ✅ Backend integration working
- [ ] ✅ No console errors

### Integration
- [ ] ✅ End-to-end flow working
- [ ] ✅ Session persistence verified
- [ ] ✅ Performance acceptable
- [ ] ✅ Security measures in place

### Documentation
- [ ] ✅ Deployment documented
- [ ] ✅ URLs documented
- [ ] ✅ Configuration documented
- [ ] ✅ Troubleshooting guide available

---

## Final Sign-off

**Deployment Date**: _______________
**Deployed By**: _______________
**Backend URL**: _______________
**Frontend URL**: _______________
**Version**: _______________

**Status**: 
- [ ] ✅ **READY FOR PRODUCTION**
- [ ] ⚠️ **READY WITH MINOR ISSUES** (document below)
- [ ] ❌ **NOT READY** (document blockers below)

**Notes**:
```
[Add any deployment notes, issues, or observations here]
```

---

## Useful Commands Reference

```powershell
# View logs
az webapp log tail --name <app-name> --resource-group <rg-name>

# Restart app
az webapp restart --name <app-name> --resource-group <rg-name>

# Update environment variable
az webapp config appsettings set --name <app-name> --resource-group <rg-name> --settings KEY=VALUE

# Scale up (if needed, costs apply)
az appservice plan update --name <plan-name> --resource-group <rg-name> --sku B1

# View deployment history
az webapp deployment list --name <app-name> --resource-group <rg-name>

# SSH into container (Linux)
az webapp ssh --name <app-name> --resource-group <rg-name>

# Download logs
az webapp log download --name <app-name> --resource-group <rg-name>
```

---

**✅ Deployment Complete!** Your AI Support Agent is now running on Azure.
