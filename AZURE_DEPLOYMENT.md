# Azure Deployment Guide - Free Tier

## 📊 Architecture Analysis

### Current Application Stack

**Backend:**
- FastAPI with async support
- LangGraph for agent workflow
- Azure OpenAI (already integrated)
- ChromaDB vector store
- Session memory (in-memory)

**Frontend:**
- React 18 + TypeScript
- Vite build system
- Static assets

---

## 🎯 Azure Native Components Mapping (Free Tier)

### 1. **Backend Hosting**

**Option A: Azure App Service (Recommended)**
- **Free Tier**: F1 (60 CPU minutes/day, 1GB RAM)
- **Benefits**: 
  - Native Python support
  - Easy deployment with Git integration
  - Environment variables management
  - Custom domains (paid tier)
- **Limitations**: 
  - Cold start after 20 mins inactivity
  - Limited compute time
  - No auto-scaling

**Option B: Azure Container Instances**
- **Free Tier**: 1 vCPU, 1.5 GB RAM (pay-as-you-go, very low cost)
- **Benefits**: 
  - Container-based deployment
  - More control over environment
- **Limitations**: 
  - Not truly "free" but very low cost (~$1-2/month)

**🏆 Recommendation: Azure App Service F1**

### 2. **Frontend Hosting**

**Azure Static Web Apps (Free Tier)**
- **Free Tier**: 100GB bandwidth/month, 0.5GB storage
- **Benefits**: 
  - Built-in CI/CD with GitHub Actions
  - Global CDN
  - Custom domains with free SSL
  - Perfect for React apps
  - Staging environments
- **No Limitations** for your use case

**🏆 Recommendation: Azure Static Web Apps**

### 3. **Database & Storage**

**Current: ChromaDB (Local File System)**

**Azure Alternatives:**

**Option A: Azure Blob Storage (Free Tier)**
- **Free Tier**: 5GB LRS hot storage, 20,000 read operations
- **Use Case**: Store ChromaDB files
- **Implementation**: Mount as volume or use Azure SDK

**Option B: Azure Cosmos DB (Free Tier)**
- **Free Tier**: 1000 RU/s, 25GB storage (one per subscription)
- **Use Case**: Replace ChromaDB with Cosmos DB vector search
- **Benefits**: Managed, scalable, global distribution
- **Limitations**: Vector search in preview

**Option C: Azure Database for PostgreSQL (Free Tier)**
- **Free Tier**: Flexible Server - Burstable tier (limited availability)
- **Use Case**: Store embeddings with pgvector extension
- **Benefits**: Mature vector search support

**🏆 Recommendation: Keep ChromaDB + Azure Blob Storage for persistence**

### 4. **AI Services**

**Azure OpenAI Service** (Already Integrated ✅)
- You're already using Azure OpenAI
- Keep using your existing deployment
- Ensure configuration uses environment variables

### 5. **Memory & Session Management**

**Current: In-Memory (MemorySaver)**

**Azure Alternatives:**

**Option A: Azure Cache for Redis (Free Tier)**
- **Free Tier**: C0 (250MB cache)
- **Use Case**: Distributed session storage
- **Benefits**: Persistent sessions across instances
- **Implementation**: LangGraph checkpoint with Redis

**Option B: Azure Table Storage**
- **Free Tier**: Part of Storage Account
- **Use Case**: Simple key-value storage for sessions
- **Benefits**: Very cheap, serverless

**🏆 Recommendation: Azure Cache for Redis C0 for production, keep in-memory for free tier**

### 6. **Monitoring & Logging**

**Azure Application Insights (Free Tier)**
- **Free Tier**: 5GB data ingestion/month
- **Benefits**:
  - Request tracking
  - Error monitoring
  - Performance metrics
  - Custom events
- **Integration**: Add Python SDK to backend

**Azure Monitor**
- **Free Tier**: Basic metrics included
- **Benefits**: Health checks, alerts

**🏆 Recommendation: Application Insights**

### 7. **CI/CD Pipeline**

**GitHub Actions (Free for public repos)**
- **Free Tier**: 2000 minutes/month for private repos
- **Benefits**:
  - Native Azure integration
  - Multi-stage deployments
  - Environment secrets management

**Azure DevOps (Alternative)**
- **Free Tier**: 1800 minutes/month, 5 users
- **Benefits**: Integrated with Azure services

**🏆 Recommendation: GitHub Actions**

### 8. **Security & Configuration**

**Azure Key Vault (Free for basic usage)**
- **Use Case**: Store API keys, connection strings
- **Benefits**: Centralized secret management
- **Limitations**: Minimal transaction cost (pennies)

**Azure App Configuration (Free Tier)**
- **Free Tier**: 10,000 requests/day
- **Use Case**: Feature flags, configuration management

**🏆 Recommendation: Environment variables (free) or Key Vault for production**

---

## 🏗️ Complete Free-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
│                   (Source Control)                       │
└────────────┬──────────────────────────┬─────────────────┘
             │                          │
             │ GitHub Actions           │ GitHub Actions
             │ (CI/CD)                  │ (CI/CD)
             ▼                          ▼
┌────────────────────────┐   ┌──────────────────────────┐
│ Azure Static Web Apps  │   │  Azure App Service (F1)  │
│    (Frontend)          │   │      (Backend)           │
│  - React Build         │   │  - FastAPI               │
│  - Global CDN          │◄──┤  - LangGraph             │
│  - Free SSL            │   │  - Python 3.11           │
└────────────────────────┘   └──────────┬───────────────┘
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │  Azure OpenAI        │
                             │  (Your Deployment)   │
                             └──────────────────────┘
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │  Azure Blob Storage  │
                             │  (ChromaDB Files)    │
                             │  - Optional          │
                             └──────────────────────┘
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │ Application Insights │
                             │    (Monitoring)      │
                             └──────────────────────┘
```

---

## 💰 Cost Breakdown (Free Tier)

| Service | Free Tier Allowance | Monthly Cost |
|---------|-------------------|--------------|
| Azure Static Web Apps | 100GB bandwidth | **$0** |
| Azure App Service F1 | 60 CPU min/day, 1GB RAM | **$0** |
| Azure OpenAI | Pay-per-token | ~$5-20 (usage-based) |
| Azure Blob Storage | 5GB storage | **$0** |
| Application Insights | 5GB data/month | **$0** |
| GitHub Actions | 2000 min/month | **$0** |
| **Total** | | **$5-20/month** |

**Note:** Only Azure OpenAI has actual costs (token usage). All other services are free tier.

---

## 🚀 Deployment Steps

### Prerequisites

1. **Azure Account** (Free tier)
2. **GitHub Account**
3. **Azure CLI** installed
4. **Git** installed

### Step 1: Prepare Azure Resources

```powershell
# Login to Azure
az login

# Set subscription (if you have multiple)
az account set --subscription "Your-Subscription-Name"

# Create resource group
az group create --name rg-support-agent --location eastus

# Create App Service Plan (Free tier)
az appservice plan create `
    --name plan-support-agent `
    --resource-group rg-support-agent `
    --sku F1 `
    --is-linux

# Create Web App for Backend
az webapp create `
    --resource-group rg-support-agent `
    --plan plan-support-agent `
    --name backend-support-agent-unique123 `
    --runtime "PYTHON:3.11"

# Create Storage Account (for ChromaDB persistence)
az storage account create `
    --name stsupportagent `
    --resource-group rg-support-agent `
    --location eastus `
    --sku Standard_LRS `
    --kind StorageV2

# Create Application Insights
az monitor app-insights component create `
    --app ai-support-agent `
    --location eastus `
    --resource-group rg-support-agent `
    --application-type web
```

### Step 2: Configure Backend Environment Variables

```powershell
# Set environment variables for App Service
az webapp config appsettings set `
    --resource-group rg-support-agent `
    --name backend-support-agent-unique123 `
    --settings `
        AZURE_OPENAI_API_KEY="your-key" `
        AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/" `
        AZURE_DEPLOYMENT_NAME="your-deployment-name" `
        AZURE_API_VERSION="2024-02-15-preview" `
        SCM_DO_BUILD_DURING_DEPLOYMENT=true `
        ENABLE_ORYX_BUILD=true
```

### Step 3: Deploy Static Web App (Frontend)

This is done via GitHub Actions (see CI/CD section below).

For manual deployment:

```powershell
# Install Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Build frontend
cd frontend
npm run build

# Deploy
swa deploy --app-location ./dist --env production
```

---

## 🔄 CI/CD Implementation

### GitHub Actions Workflows

I'll create two separate workflows:
1. **Backend deployment** to Azure App Service
2. **Frontend deployment** to Azure Static Web Apps

---

## 📝 Enhanced Configuration

### Backend Changes Needed

1. **Add Application Insights**
2. **Add health check endpoint**
3. **Add Blob Storage for ChromaDB persistence**
4. **Production-ready settings**

### Frontend Changes Needed

1. **Environment-based API URLs**
2. **Production build optimization**
3. **Error tracking integration**

---

## 🎓 Summary of Azure Services (Free Tier)

✅ **Must Use:**
- Azure Static Web Apps (Frontend) - FREE
- Azure App Service F1 (Backend) - FREE
- Azure OpenAI - PAID (~$5-20/month)
- GitHub Actions - FREE

✅ **Optional but Recommended:**
- Application Insights (Monitoring) - FREE (5GB/month)
- Azure Blob Storage (ChromaDB persistence) - FREE (5GB)

❌ **Skip for Free Tier:**
- Azure Cache for Redis (Use in-memory)
- Azure Cosmos DB (Use ChromaDB)
- Azure Key Vault (Use environment variables)

---

## ⚠️ Free Tier Limitations & Workarounds

1. **App Service F1 Sleep Mode**
   - **Issue**: Sleeps after 20 mins inactivity
   - **Workaround**: Use Azure Logic Apps (free) to ping every 15 mins

2. **CPU Time Limit (60 min/day)**
   - **Issue**: Limited compute time
   - **Workaround**: Optimize LangGraph nodes, cache responses

3. **No Custom Domains on App Service F1**
   - **Issue**: Uses azurewebsites.net domain
   - **Workaround**: Upgrade to B1 tier ($13/month) or use Static Web Apps proxy

4. **Cold Start**
   - **Issue**: First request slow after sleep
   - **Workaround**: Health check endpoint, warming requests

---

## 📋 Next Steps

1. ✅ Create Azure resources
2. ✅ Set up GitHub repository
3. ✅ Configure GitHub secrets
4. ✅ Create CI/CD workflows
5. ✅ Deploy and test

Would you like me to:
1. Create the GitHub Actions workflows?
2. Add Application Insights integration?
3. Add health check endpoints?
4. Create Azure Blob Storage integration for ChromaDB?
5. Create deployment scripts?

Let me know what you'd like to implement first! 🚀
