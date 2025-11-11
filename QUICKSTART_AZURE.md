# Azure Deployment - Quick Reference

## 🚀 Quick Deploy

```powershell
# Run the automated deployment script
.\deploy-to-azure.ps1 `
    -AzureOpenAIKey "your-key" `
    -AzureOpenAIEndpoint "https://your-resource.openai.azure.com/" `
    -AzureDeploymentName "your-deployment-name"
```

## 📋 GitHub Secrets Setup

After running deployment script, add these secrets to GitHub:
`https://github.com/YOUR_USERNAME/agentic-ai/settings/secrets/actions`

1. **AZURE_WEBAPP_PUBLISH_PROFILE**
   - Copy contents from `backend-publish-profile.xml`

2. **AZURE_STATIC_WEB_APPS_API_TOKEN**
   - From deployment script output

3. **VITE_API_URL**
   - Your backend URL from deployment script output

## 🔄 Manual Deployment Commands

### Deploy Backend Manually
```powershell
cd backend
az webapp up --name YOUR_BACKEND_NAME --resource-group rg-support-agent --runtime PYTHON:3.11
```

### Deploy Frontend Manually
```powershell
cd frontend
npm run build
swa deploy --app-location ./dist --env production
```

## 📊 Monitoring Commands

### View Backend Logs
```powershell
az webapp log tail --name YOUR_BACKEND_NAME --resource-group rg-support-agent
```

### Test Health Endpoint
```powershell
curl https://YOUR_BACKEND_NAME.azurewebsites.net/health
```

### View Application Insights
```powershell
# Go to Azure Portal > Application Insights > ai-support-agent
```

## 🛠️ Common Operations

### Restart Backend
```powershell
az webapp restart --name YOUR_BACKEND_NAME --resource-group rg-support-agent
```

### Update Environment Variables
```powershell
az webapp config appsettings set `
    --name YOUR_BACKEND_NAME `
    --resource-group rg-support-agent `
    --settings KEY="VALUE"
```

### Scale Up (Leave Free Tier)
```powershell
# Upgrade to B1 tier ($13/month)
az appservice plan update `
    --name plan-support-agent `
    --resource-group rg-support-agent `
    --sku B1
```

## 🧹 Cleanup

### Delete All Resources
```powershell
.\cleanup-azure.ps1
# or
az group delete --name rg-support-agent --yes
```

## 📈 Cost Management

### View Current Costs
```powershell
az consumption usage list --start-date 2025-11-01 --end-date 2025-11-30
```

### Set Budget Alert
- Go to Azure Portal > Cost Management + Billing > Budgets

## 🔐 Security Checklist

- [ ] API keys stored in Azure App Settings (not in code)
- [ ] CORS configured for production domains only
- [ ] HTTPS enforced (default in Azure)
- [ ] Application Insights enabled for monitoring
- [ ] GitHub secrets configured (not committed to repo)
- [ ] Resource access restricted to necessary IPs (optional)

## 📱 URLs Reference

| Service | URL Format | Example |
|---------|------------|---------|
| Backend API | `https://{app-name}.azurewebsites.net` | Health check at `/health` |
| Frontend | `https://{app-name}.azurestaticapps.net` | Main application |
| API Docs | `https://{app-name}.azurewebsites.net/docs` | Swagger UI |
| Azure Portal | `https://portal.azure.com` | Resource management |

## 🆘 Troubleshooting

### Backend Not Responding
```powershell
# Check status
az webapp show --name YOUR_BACKEND_NAME --resource-group rg-support-agent --query state

# View logs
az webapp log tail --name YOUR_BACKEND_NAME --resource-group rg-support-agent

# Restart
az webapp restart --name YOUR_BACKEND_NAME --resource-group rg-support-agent
```

### Frontend Build Failed
```powershell
# Check GitHub Actions
# Go to: https://github.com/YOUR_USERNAME/agentic-ai/actions

# Verify secrets are set correctly
# Check: Repository Settings > Secrets and variables > Actions
```

### CORS Errors
- Update `ALLOWED_ORIGINS` in backend app settings
- Restart backend after changing settings

## 📚 Additional Resources

- [Azure App Service Docs](https://docs.microsoft.com/azure/app-service/)
- [Azure Static Web Apps Docs](https://docs.microsoft.com/azure/static-web-apps/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)
- [Application Insights Docs](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
