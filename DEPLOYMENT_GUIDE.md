# Complete Azure Deployment and CI/CD Setup Guide

## 📋 Prerequisites Checklist

- [ ] Azure account with active subscription
- [ ] GitHub account
- [ ] Azure CLI installed (`az --version`)
- [ ] Git installed
- [ ] Azure OpenAI resource and deployment created

---

## 🚀 Step-by-Step Deployment

### Step 1: Clone and Prepare Repository

```powershell
# If not already done, initialize git repository
cd c:\Users\rathokap\Downloads\agentic-ai
git init
git add .
git commit -m "Initial commit"

# Create GitHub repository and push
# Go to GitHub.com and create a new repository named 'agentic-ai'
git remote add origin https://github.com/YOUR_USERNAME/agentic-ai.git
git branch -M main
git push -u origin main
```

### Step 2: Create Azure Resources

```powershell
# Login to Azure
az login

# Set your subscription (list subscriptions first if you have multiple)
az account list --output table
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Set variables
$RESOURCE_GROUP = "rg-support-agent"
$LOCATION = "eastus"
$APP_SERVICE_PLAN = "plan-support-agent"
$BACKEND_APP_NAME = "backend-support-agent-$(Get-Random -Minimum 1000 -Maximum 9999)"
$STORAGE_ACCOUNT = "stsupportagent$(Get-Random -Minimum 1000 -Maximum 9999)"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service Plan (F1 Free tier)
az appservice plan create `
    --name $APP_SERVICE_PLAN `
    --resource-group $RESOURCE_GROUP `
    --sku F1 `
    --is-linux `
    --location $LOCATION

# Create Web App for Backend
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $APP_SERVICE_PLAN `
    --name $BACKEND_APP_NAME `
    --runtime "PYTHON:3.11"

# Enable logging
az webapp log config `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --application-logging filesystem `
    --detailed-error-messages true `
    --failed-request-tracing true `
    --web-server-logging filesystem

# Create Storage Account (Free tier - 5GB)
az storage account create `
    --name $STORAGE_ACCOUNT `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --sku Standard_LRS `
    --kind StorageV2

# Create Application Insights (Free tier - 5GB/month)
az monitor app-insights component create `
    --app ai-support-agent `
    --location $LOCATION `
    --resource-group $RESOURCE_GROUP `
    --application-type web

# Get Application Insights connection string
$APP_INSIGHTS_KEY = az monitor app-insights component show `
    --app ai-support-agent `
    --resource-group $RESOURCE_GROUP `
    --query connectionString `
    --output tsv

Write-Host "Backend App URL: https://$BACKEND_APP_NAME.azurewebsites.net" -ForegroundColor Green
Write-Host "Application Insights Key: $APP_INSIGHTS_KEY" -ForegroundColor Yellow
```

### Step 3: Configure Backend Environment Variables

```powershell
# Set all required environment variables
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_APP_NAME `
    --settings `
        AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_KEY" `
        AZURE_OPENAI_ENDPOINT="https://YOUR_RESOURCE.openai.azure.com/" `
        AZURE_DEPLOYMENT_NAME="YOUR_DEPLOYMENT_NAME" `
        AZURE_API_VERSION="2024-02-15-preview" `
        ENVIRONMENT="production" `
        ALLOWED_ORIGINS="https://YOUR_STATIC_WEB_APP.azurestaticapps.net" `
        CHROMA_TELEMETRY_ENABLED="False" `
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
        ENABLE_ORYX_BUILD="true" `
        APPLICATIONINSIGHTS_CONNECTION_STRING="$APP_INSIGHTS_KEY"

Write-Host "✓ Environment variables configured" -ForegroundColor Green
```

### Step 4: Get Backend Publish Profile

```powershell
# Download publish profile for GitHub Actions
az webapp deployment list-publishing-profiles `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --xml > backend-publish-profile.xml

Write-Host "✓ Publish profile saved to backend-publish-profile.xml" -ForegroundColor Green
Write-Host "Copy the contents of this file for GitHub Secrets" -ForegroundColor Yellow
```

### Step 5: Create Azure Static Web App

```powershell
# Create Static Web App (Free tier)
$STATIC_WEB_APP_NAME = "swa-support-agent"

az staticwebapp create `
    --name $STATIC_WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --sku Free

# Get deployment token for GitHub Actions
$SWA_TOKEN = az staticwebapp secrets list `
    --name $STATIC_WEB_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query properties.apiKey `
    --output tsv

Write-Host "Static Web App URL: https://$STATIC_WEB_APP_NAME.azurestaticapps.net" -ForegroundColor Green
Write-Host "Deployment Token (save for GitHub Secrets): $SWA_TOKEN" -ForegroundColor Yellow
```

### Step 6: Configure GitHub Secrets

Go to your GitHub repository: `https://github.com/YOUR_USERNAME/agentic-ai/settings/secrets/actions`

Add the following secrets:

1. **AZURE_WEBAPP_PUBLISH_PROFILE**
   - Value: Contents of `backend-publish-profile.xml`

2. **AZURE_STATIC_WEB_APPS_API_TOKEN**
   - Value: The `$SWA_TOKEN` from previous step

3. **VITE_API_URL**
   - Value: `https://$BACKEND_APP_NAME.azurewebsites.net`

```powershell
# Print reminder of what to add
Write-Host "`n=== GitHub Secrets Required ===" -ForegroundColor Cyan
Write-Host "1. AZURE_WEBAPP_PUBLISH_PROFILE" -ForegroundColor Yellow
Write-Host "   Location: backend-publish-profile.xml" -ForegroundColor White
Write-Host "`n2. AZURE_STATIC_WEB_APPS_API_TOKEN" -ForegroundColor Yellow
Write-Host "   Value: $SWA_TOKEN" -ForegroundColor White
Write-Host "`n3. VITE_API_URL" -ForegroundColor Yellow
Write-Host "   Value: https://$BACKEND_APP_NAME.azurewebsites.net" -ForegroundColor White
Write-Host "`nAdd these at: https://github.com/YOUR_USERNAME/agentic-ai/settings/secrets/actions" -ForegroundColor Cyan
```

### Step 7: Update Workflow Files

Update the backend workflow file `.github/workflows/backend-deploy.yml`:

```yaml
env:
  AZURE_WEBAPP_NAME: $BACKEND_APP_NAME  # Replace with your actual name
```

### Step 8: Deploy via GitHub Actions

```powershell
# Make a small change to trigger deployment
cd c:\Users\rathokap\Downloads\agentic-ai
git add .
git commit -m "Configure for Azure deployment"
git push origin main

Write-Host "`n✓ Code pushed to GitHub. GitHub Actions will now deploy your app!" -ForegroundColor Green
Write-Host "Monitor deployment at: https://github.com/YOUR_USERNAME/agentic-ai/actions" -ForegroundColor Cyan
```

---

## 🔍 Step 9: Verify Deployment

### Test Backend

```powershell
# Test health endpoint
$BACKEND_URL = "https://$BACKEND_APP_NAME.azurewebsites.net"
curl "$BACKEND_URL/health"

# Test support agent endpoint
curl -X POST "$BACKEND_URL/support-agent?query=Hello&uid=test123"
```

### Test Frontend

Open your browser and navigate to:
```
https://$STATIC_WEB_APP_NAME.azurestaticapps.net
```

---

## 📊 Step 10: Monitor Your Application

### View Logs

```powershell
# Stream backend logs
az webapp log tail --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --log-file logs.zip
```

### Application Insights

Go to Azure Portal:
1. Navigate to Application Insights resource
2. View live metrics, failures, performance
3. Set up alerts for errors or performance issues

---

## 🛠️ Troubleshooting

### Issue: Backend returns 503

**Solution:**
```powershell
# Check if app is running
az webapp show --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP --query state

# Restart app
az webapp restart --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP

# Check logs
az webapp log tail --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP
```

### Issue: Frontend can't connect to backend

**Solution:**
1. Check CORS configuration in backend `app.py`
2. Verify `VITE_API_URL` in frontend `.env`
3. Check backend health endpoint
4. Verify Static Web App environment variables

### Issue: GitHub Actions failing

**Solution:**
1. Check if secrets are set correctly
2. Verify publish profile is valid
3. Check workflow logs on GitHub Actions tab

---

## 📈 Scaling Beyond Free Tier

When you're ready to scale:

### Backend (B1 Tier - $13/month)
```powershell
az appservice plan update `
    --name $APP_SERVICE_PLAN `
    --resource-group $RESOURCE_GROUP `
    --sku B1
```

Benefits:
- No sleep mode
- Custom domains
- More CPU time
- Better performance

### Add Redis for Session Management
```powershell
az redis create `
    --name redis-support-agent `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --sku Basic `
    --vm-size c0
```

### Add Cosmos DB for Vector Search
```powershell
az cosmosdb create `
    --name cosmos-support-agent `
    --resource-group $RESOURCE_GROUP `
    --locations regionName=$LOCATION `
    --capabilities EnableNoSQLVectorSearch
```

---

## 🧹 Cleanup (Delete All Resources)

To delete everything and stop charges:

```powershell
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

---

## 📝 Cost Monitoring

Set up cost alerts:

```powershell
# View current costs
az consumption usage list --start-date 2025-11-01 --end-date 2025-11-30

# Set up budget (via Azure Portal)
# Go to: Cost Management + Billing > Budgets > Add
```

---

## ✅ Deployment Checklist

- [ ] Azure resources created
- [ ] Backend environment variables configured
- [ ] GitHub repository created
- [ ] GitHub secrets configured
- [ ] Workflow files updated with app names
- [ ] Code pushed to GitHub
- [ ] GitHub Actions completed successfully
- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] End-to-end test completed
- [ ] Monitoring configured
- [ ] Cost alerts set up

---

## 🎉 Success!

Your application is now deployed on Azure with CI/CD!

- **Frontend URL**: `https://$STATIC_WEB_APP_NAME.azurestaticapps.net`
- **Backend URL**: `https://$BACKEND_APP_NAME.azurewebsites.net`
- **API Docs**: `https://$BACKEND_APP_NAME.azurewebsites.net/docs`
- **GitHub Actions**: `https://github.com/YOUR_USERNAME/agentic-ai/actions`

Every push to `main` branch will automatically deploy your changes!
