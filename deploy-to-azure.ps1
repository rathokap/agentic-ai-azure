# Azure Deployment Automation Script
# This script automates the entire Azure deployment process

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup = "rg-support-agent",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$true)]
    [string]$AzureOpenAIKey,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureOpenAIEndpoint,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureDeploymentName
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Azure Deployment Automation" -ForegroundColor Cyan
Write-Host "Customer Support Agent" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Azure CLI not found. Please install Azure CLI first." -ForegroundColor Red
    Write-Host "Download from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Azure CLI found" -ForegroundColor Green

# Check if logged in to Azure
Write-Host "`nChecking Azure login status..." -ForegroundColor Yellow
$loginStatus = az account show 2>$null
if (-not $loginStatus) {
    Write-Host "Not logged in to Azure. Initiating login..." -ForegroundColor Yellow
    az login
} else {
    Write-Host "✓ Already logged in to Azure" -ForegroundColor Green
}

# Show current subscription
$currentSub = az account show --query name -o tsv
Write-Host "`nCurrent Subscription: $currentSub" -ForegroundColor Cyan

# Generate unique names
$randomSuffix = Get-Random -Minimum 1000 -Maximum 9999
$APP_SERVICE_PLAN = "plan-support-agent"
$BACKEND_APP_NAME = "backend-support-agent-$randomSuffix"
$STORAGE_ACCOUNT = "stsupportagent$randomSuffix"
$STATIC_WEB_APP_NAME = "swa-support-agent-$randomSuffix"
$APP_INSIGHTS_NAME = "ai-support-agent"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Resource Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host "Location: $Location" -ForegroundColor White
Write-Host "Backend App: $BACKEND_APP_NAME" -ForegroundColor White
Write-Host "Static Web App: $STATIC_WEB_APP_NAME" -ForegroundColor White
Write-Host "Storage Account: $STORAGE_ACCOUNT" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Proceed with deployment? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

try {
    # Step 1: Create Resource Group
    Write-Host "`n[1/7] Creating Resource Group..." -ForegroundColor Cyan
    az group create --name $ResourceGroup --location $Location --output none
    Write-Host "✓ Resource Group created" -ForegroundColor Green

    # Step 2: Create App Service Plan
    Write-Host "`n[2/7] Creating App Service Plan (F1 Free Tier)..." -ForegroundColor Cyan
    az appservice plan create `
        --name $APP_SERVICE_PLAN `
        --resource-group $ResourceGroup `
        --sku F1 `
        --is-linux `
        --location $Location `
        --output none
    Write-Host "✓ App Service Plan created" -ForegroundColor Green

    # Step 3: Create Web App for Backend
    Write-Host "`n[3/7] Creating Backend Web App..." -ForegroundColor Cyan
    az webapp create `
        --resource-group $ResourceGroup `
        --plan $APP_SERVICE_PLAN `
        --name $BACKEND_APP_NAME `
        --runtime "PYTHON:3.11" `
        --output none
    
    # Enable logging
    az webapp log config `
        --name $BACKEND_APP_NAME `
        --resource-group $ResourceGroup `
        --application-logging filesystem `
        --detailed-error-messages true `
        --failed-request-tracing true `
        --web-server-logging filesystem `
        --output none
    
    Write-Host "✓ Backend Web App created" -ForegroundColor Green

    # Step 4: Create Storage Account
    Write-Host "`n[4/7] Creating Storage Account..." -ForegroundColor Cyan
    az storage account create `
        --name $STORAGE_ACCOUNT `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku Standard_LRS `
        --kind StorageV2 `
        --output none
    Write-Host "✓ Storage Account created" -ForegroundColor Green

    # Step 5: Create Application Insights
    Write-Host "`n[5/7] Creating Application Insights..." -ForegroundColor Cyan
    az monitor app-insights component create `
        --app $APP_INSIGHTS_NAME `
        --location $Location `
        --resource-group $ResourceGroup `
        --application-type web `
        --output none
    
    $APP_INSIGHTS_KEY = az monitor app-insights component show `
        --app $APP_INSIGHTS_NAME `
        --resource-group $ResourceGroup `
        --query connectionString `
        --output tsv
    
    Write-Host "✓ Application Insights created" -ForegroundColor Green

    # Step 6: Create Static Web App
    Write-Host "`n[6/7] Creating Static Web App..." -ForegroundColor Cyan
    az staticwebapp create `
        --name $STATIC_WEB_APP_NAME `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku Free `
        --output none
    
    $SWA_TOKEN = az staticwebapp secrets list `
        --name $STATIC_WEB_APP_NAME `
        --resource-group $ResourceGroup `
        --query properties.apiKey `
        --output tsv
    
    Write-Host "✓ Static Web App created" -ForegroundColor Green

    # Step 7: Configure Backend Environment Variables
    Write-Host "`n[7/7] Configuring Backend Environment Variables..." -ForegroundColor Cyan
    
    $BACKEND_URL = "https://$BACKEND_APP_NAME.azurewebsites.net"
    $FRONTEND_URL = "https://$STATIC_WEB_APP_NAME.azurestaticapps.net"
    
    az webapp config appsettings set `
        --resource-group $ResourceGroup `
        --name $BACKEND_APP_NAME `
        --settings `
            AZURE_OPENAI_API_KEY="$AzureOpenAIKey" `
            AZURE_OPENAI_ENDPOINT="$AzureOpenAIEndpoint" `
            AZURE_DEPLOYMENT_NAME="$AzureDeploymentName" `
            AZURE_API_VERSION="2024-02-15-preview" `
            ENVIRONMENT="production" `
            ALLOWED_ORIGINS="$FRONTEND_URL,http://localhost:3000" `
            CHROMA_TELEMETRY_ENABLED="False" `
            SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
            ENABLE_ORYX_BUILD="true" `
            APPLICATIONINSIGHTS_CONNECTION_STRING="$APP_INSIGHTS_KEY" `
        --output none
    
    Write-Host "✓ Environment variables configured" -ForegroundColor Green

    # Download publish profile
    Write-Host "`nDownloading publish profile..." -ForegroundColor Cyan
    $publishProfilePath = "backend-publish-profile.xml"
    az webapp deployment list-publishing-profiles `
        --name $BACKEND_APP_NAME `
        --resource-group $ResourceGroup `
        --xml > $publishProfilePath
    
    Write-Host "✓ Publish profile saved" -ForegroundColor Green

    # Success Summary
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Deployment Successful! 🎉" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Resource URLs:" -ForegroundColor Cyan
    Write-Host "  Backend API:    $BACKEND_URL" -ForegroundColor White
    Write-Host "  API Docs:       $BACKEND_URL/docs" -ForegroundColor White
    Write-Host "  Health Check:   $BACKEND_URL/health" -ForegroundColor White
    Write-Host "  Frontend:       $FRONTEND_URL" -ForegroundColor White
    Write-Host ""
    Write-Host "GitHub Secrets Required:" -ForegroundColor Cyan
    Write-Host "  Repository: https://github.com/YOUR_USERNAME/agentic-ai/settings/secrets/actions" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. AZURE_WEBAPP_PUBLISH_PROFILE" -ForegroundColor White
    Write-Host "     File: $publishProfilePath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. AZURE_STATIC_WEB_APPS_API_TOKEN" -ForegroundColor White
    Write-Host "     Value: $SWA_TOKEN" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. VITE_API_URL" -ForegroundColor White
    Write-Host "     Value: $BACKEND_URL" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Add the GitHub secrets listed above" -ForegroundColor White
    Write-Host "  2. Update .github/workflows/backend-deploy.yml with:" -ForegroundColor White
    Write-Host "     AZURE_WEBAPP_NAME: $BACKEND_APP_NAME" -ForegroundColor Gray
    Write-Host "  3. Push your code to GitHub" -ForegroundColor White
    Write-Host "  4. GitHub Actions will automatically deploy" -ForegroundColor White
    Write-Host ""
    Write-Host "Monitoring:" -ForegroundColor Cyan
    Write-Host "  Azure Portal: https://portal.azure.com" -ForegroundColor White
    Write-Host "  Resource Group: $ResourceGroup" -ForegroundColor White
    Write-Host ""

    # Save configuration to file
    $configFile = "azure-deployment-config.txt"
    @"
Azure Deployment Configuration
Generated: $(Get-Date)

Resource Group: $ResourceGroup
Location: $Location

Backend App Name: $BACKEND_APP_NAME
Backend URL: $BACKEND_URL

Static Web App Name: $STATIC_WEB_APP_NAME
Frontend URL: $FRONTEND_URL

Storage Account: $STORAGE_ACCOUNT
Application Insights: $APP_INSIGHTS_NAME

GitHub Secrets:
1. AZURE_WEBAPP_PUBLISH_PROFILE (see: $publishProfilePath)
2. AZURE_STATIC_WEB_APPS_API_TOKEN: $SWA_TOKEN
3. VITE_API_URL: $BACKEND_URL
"@ | Out-File -FilePath $configFile -Encoding UTF8

    Write-Host "Configuration saved to: $configFile" -ForegroundColor Green
    Write-Host ""

} catch {
    Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "`nTo cleanup partial deployment, run:" -ForegroundColor Yellow
    Write-Host "  az group delete --name $ResourceGroup --yes" -ForegroundColor White
    exit 1
}
