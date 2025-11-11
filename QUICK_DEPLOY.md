# 🚀 Quick Deploy - Azure Cheat Sheet

## One-Command Deploy

```powershell
.\deploy-to-azure.ps1 -AzureOpenAIKey "YOUR_KEY" -AzureOpenAIEndpoint "https://YOUR_RESOURCE.openai.azure.com/" -AzureDeploymentName "YOUR_DEPLOYMENT"
```

---

## Manual Deploy (3 Minutes)

### 1. Create & Deploy Backend
```powershell
$NAME = "backend-support-$(Get-Random -Minimum 1000 -Maximum 9999)"

az group create --name rg-support-agent --location eastus
az appservice plan create --name plan-support-agent --resource-group rg-support-agent --sku F1 --is-linux
az webapp create --resource-group rg-support-agent --plan plan-support-agent --name $NAME --runtime "PYTHON:3.11"
az webapp config set --resource-group rg-support-agent --name $NAME --startup-file "startup.sh"
az webapp config appsettings set --resource-group rg-support-agent --name $NAME --settings AZURE_OPENAI_API_KEY="YOUR_KEY" AZURE_OPENAI_ENDPOINT="YOUR_ENDPOINT" AZURE_DEPLOYMENT_NAME="YOUR_DEPLOYMENT" ENVIRONMENT="production" SCM_DO_BUILD_DURING_DEPLOYMENT="true"

cd backend
az webapp up --name $NAME --resource-group rg-support-agent
```

### 2. Verify
```powershell
python verify_deployment.py https://$NAME.azurewebsites.net
```

---

## Essential Commands

```powershell
# Stream logs
az webapp log tail --name <app-name> --resource-group rg-support-agent

# Restart app
az webapp restart --name <app-name> --resource-group rg-support-agent

# Update env variable
az webapp config appsettings set --name <app-name> --resource-group rg-support-agent --settings KEY=VALUE

# Health check
curl https://<app-name>.azurewebsites.net/health

# Test query
curl -X POST https://<app-name>.azurewebsites.net/query -H "Content-Type: application/json" -d '{"message":"test","thread_id":"123"}'
```

---

## Required Environment Variables

```
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
ENVIRONMENT=production
```

---

## Troubleshooting

**App won't start?**
```powershell
az webapp log tail --name <app-name> --resource-group rg-support-agent
```

**502 Bad Gateway?**
- Wait 2-3 minutes for cold start
- Check logs for errors
- Verify environment variables

**Queries failing?**
- Check AZURE_OPENAI_API_KEY is set
- Verify deployment name matches
- Check /health endpoint

---

## Free Tier Limits

- **App Service F1**: 60 min CPU/day, 1GB RAM
- **Static Web Apps**: 100GB bandwidth/month
- **Storage**: 5GB, 20K operations/month
- **App Insights**: 5GB data/month

**Cost**: $0/month (except Azure OpenAI usage)

---

## File Changes Made

✅ `backend/app.py` - Production-ready with PORT binding  
✅ `backend/startup.sh` - Linux startup script  
✅ `backend/startup.txt` - Simple startup command  
✅ `backend/web.config` - Windows configuration  
✅ `backend/gunicorn.conf.py` - Gunicorn config  
✅ `backend/.deployment` - Build settings  
✅ `backend/requirements.txt` - Added gunicorn  
✅ `frontend/src/services/api.ts` - New /query endpoint  
✅ `verify_deployment.py` - Deployment checker  
✅ `DEPLOYMENT_CHECKLIST.md` - Complete guide  
✅ `DEPLOYMENT_READY.md` - Production summary  

---

## Endpoints

- **Root**: `GET /` - API info
- **Health**: `GET /health` - Health status
- **Query**: `POST /query` - Main endpoint (JSON body)
- **Legacy**: `POST /support-agent` - Old endpoint (query params)
- **Docs**: `GET /docs` - Interactive API docs

---

**📖 Full Guide**: See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
