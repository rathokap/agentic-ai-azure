# 🔑 How to Get Azure OpenAI Credentials

This guide walks you through creating an Azure OpenAI resource and obtaining the required credentials for your application.

---

## 📋 Prerequisites

- **Azure Account**: Sign up at [https://azure.microsoft.com/free/](https://azure.microsoft.com/free/)
- **Azure OpenAI Access**: Request access at [https://aka.ms/oai/access](https://aka.ms/oai/access)
  - ⚠️ **Important**: Azure OpenAI requires approval (usually takes 1-2 business days)
  - You need an active Azure subscription
  - Access is granted per subscription

---

## 🚀 Step-by-Step Setup

### Step 1: Request Azure OpenAI Access

1. **Visit**: [https://aka.ms/oai/access](https://aka.ms/oai/access)
2. **Fill out the form** with:
   - Your Azure subscription ID
   - Business use case
   - Expected usage
3. **Wait for approval** (1-2 business days)
4. **Check email** for approval notification

---

### Step 2: Create Azure OpenAI Resource

#### Option A: Using Azure Portal (GUI)

1. **Login to Azure Portal**
   - Go to [https://portal.azure.com](https://portal.azure.com)
   - Sign in with your Azure account

2. **Create Resource**
   - Click **"Create a resource"** (top-left)
   - Search for **"Azure OpenAI"**
   - Click **"Azure OpenAI"** → **"Create"**

3. **Configure Basics**
   ```
   Subscription: [Your subscription]
   Resource Group: [Create new or select existing]
       Name: rg-openai-support-agent
   Region: East US (recommended) or your preferred region
   Name: openai-support-agent-[random] (must be globally unique)
   Pricing Tier: Standard S0
   ```

4. **Review + Create**
   - Click **"Review + create"**
   - Click **"Create"**
   - Wait 2-3 minutes for deployment

5. **Go to Resource**
   - Click **"Go to resource"** when deployment completes

#### Option B: Using Azure CLI (Faster)

```powershell
# Login to Azure
az login

# Set variables
$RESOURCE_GROUP = "rg-openai-support-agent"
$LOCATION = "eastus"
$OPENAI_NAME = "openai-support-agent-$(Get-Random -Minimum 1000 -Maximum 9999)"

# Create resource group
az group create `
    --name $RESOURCE_GROUP `
    --location $LOCATION

# Create Azure OpenAI resource
az cognitiveservices account create `
    --name $OPENAI_NAME `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --kind OpenAI `
    --sku S0 `
    --yes

# Save the name for later
Write-Host "Azure OpenAI Resource Name: $OPENAI_NAME" -ForegroundColor Green
```

---

### Step 3: Deploy GPT Model

#### Option A: Using Azure Portal

1. **Navigate to Azure OpenAI Studio**
   - In your Azure OpenAI resource, click **"Go to Azure OpenAI Studio"**
   - Or visit [https://oai.azure.com](https://oai.azure.com)

2. **Create Deployment**
   - Click **"Deployments"** (left sidebar)
   - Click **"+ Create new deployment"**

3. **Configure Deployment**
   ```
   Select a model: gpt-4 (recommended) or gpt-35-turbo
   Model version: [Latest stable version]
   Deployment name: gpt-4-deployment (remember this!)
   Content filter: Default
   Tokens per minute rate limit: 10K (adjust based on needs)
   ```
   
   **Recommended Models:**
   - **gpt-4** (best quality, higher cost)
   - **gpt-4-turbo** (fast + high quality)
   - **gpt-35-turbo** (fast, lower cost, good quality)

4. **Create Deployment**
   - Click **"Create"**
   - Wait 1-2 minutes for deployment

5. **Note the Deployment Name**
   - This is your `AZURE_DEPLOYMENT_NAME`
   - Example: `gpt-4-deployment`

#### Option B: Using Azure CLI

```powershell
# Deploy GPT-4 model
az cognitiveservices account deployment create `
    --name $OPENAI_NAME `
    --resource-group $RESOURCE_GROUP `
    --deployment-name "gpt-4-deployment" `
    --model-name "gpt-4" `
    --model-version "0613" `
    --model-format "OpenAI" `
    --sku-capacity 10 `
    --sku-name "Standard"

Write-Host "Deployment Name: gpt-4-deployment" -ForegroundColor Green
```

---

### Step 4: Get API Key and Endpoint

#### Option A: Using Azure Portal

1. **In Azure OpenAI Resource**
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to your Azure OpenAI resource

2. **Get Keys and Endpoint**
   - Click **"Keys and Endpoint"** (left sidebar under Resource Management)
   
3. **Copy Values**
   - **KEY 1** → This is your `AZURE_OPENAI_API_KEY`
   - **Endpoint** → This is your `AZURE_OPENAI_ENDPOINT`
     - Format: `https://YOUR-RESOURCE-NAME.openai.azure.com/`

4. **Example**
   ```
   KEY 1: abc123def456ghi789jkl012mno345pqr678
   Endpoint: https://openai-support-agent-1234.openai.azure.com/
   ```

#### Option B: Using Azure CLI

```powershell
# Get endpoint
$ENDPOINT = az cognitiveservices account show `
    --name $OPENAI_NAME `
    --resource-group $RESOURCE_GROUP `
    --query "properties.endpoint" `
    --output tsv

# Get API key
$API_KEY = az cognitiveservices account keys list `
    --name $OPENAI_NAME `
    --resource-group $RESOURCE_GROUP `
    --query "key1" `
    --output tsv

# Display credentials
Write-Host "`nYour Azure OpenAI Credentials:" -ForegroundColor Cyan
Write-Host "AZURE_OPENAI_ENDPOINT=$ENDPOINT" -ForegroundColor Green
Write-Host "AZURE_OPENAI_API_KEY=$API_KEY" -ForegroundColor Green
```

---

### Step 5: Configure Your Application

1. **Copy `.env.example` to `.env`**
   ```powershell
   cd backend
   Copy-Item .env.example .env
   ```

2. **Edit `.env` file** with your credentials:
   ```bash
   # Replace with YOUR actual values
   AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678
   AZURE_OPENAI_ENDPOINT=https://openai-support-agent-1234.openai.azure.com/
   AZURE_DEPLOYMENT_NAME=gpt-4-deployment
   AZURE_API_VERSION=2024-02-15-preview
   ```

3. **Verify Configuration**
   ```powershell
   python verify_dependencies.py
   ```

---

## 📝 Complete Configuration Reference

### Required Environment Variables

```bash
# === REQUIRED: Azure OpenAI Configuration ===

# Your API Key (from "Keys and Endpoint" in Azure Portal)
AZURE_OPENAI_API_KEY=your-key-here

# Your OpenAI Endpoint URL (from "Keys and Endpoint" in Azure Portal)
# Format: https://YOUR-RESOURCE-NAME.openai.azure.com/
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Your model deployment name (from Azure OpenAI Studio > Deployments)
# This is the name YOU chose when deploying the model
AZURE_DEPLOYMENT_NAME=gpt-4-deployment

# API Version (use recommended version)
AZURE_API_VERSION=2024-02-15-preview
```

### Example Values

```bash
# Real-world example (values are fake but format is correct)
AZURE_OPENAI_API_KEY=4a5b6c7d8e9f0g1h2i3j4k5l6m7n8o9p0q1r2s3t4u5v6w7x8y9z
AZURE_OPENAI_ENDPOINT=https://openai-support-agent-1234.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-4-deployment
AZURE_API_VERSION=2024-02-15-preview
```

---

## 🔍 How to Find Each Value

| Variable | Where to Find | Example |
|----------|---------------|---------|
| **AZURE_OPENAI_API_KEY** | Azure Portal → Your OpenAI Resource → Keys and Endpoint → KEY 1 | `4a5b6c7d8e9f0g1h2i3j...` |
| **AZURE_OPENAI_ENDPOINT** | Azure Portal → Your OpenAI Resource → Keys and Endpoint → Endpoint | `https://openai-xxx.openai.azure.com/` |
| **AZURE_DEPLOYMENT_NAME** | Azure OpenAI Studio → Deployments → Your deployment name | `gpt-4-deployment` |
| **AZURE_API_VERSION** | Use recommended version | `2024-02-15-preview` |

---

## ✅ Verification Steps

### Test 1: Verify Credentials

```powershell
cd backend

# Create a test script
@"
import os
from dotenv import load_dotenv

load_dotenv()

print("Checking Azure OpenAI Configuration...")
print(f"API Key: {'✓ Set' if os.getenv('AZURE_OPENAI_API_KEY') else '✗ Missing'}")
print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT', '✗ Missing')}")
print(f"Deployment: {os.getenv('AZURE_DEPLOYMENT_NAME', '✗ Missing')}")
print(f"API Version: {os.getenv('AZURE_API_VERSION', '✗ Missing')}")
"@ | Out-File -FilePath test_config.py -Encoding UTF8

python test_config.py
```

### Test 2: Test API Connection

```powershell
# Create a test script
@"
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

try:
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv('AZURE_DEPLOYMENT_NAME'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_API_VERSION')
    )
    
    response = llm.invoke('Hello, this is a test!')
    print('✅ Success! Azure OpenAI is working!')
    print(f'Response: {response.content}')
    
except Exception as e:
    print(f'❌ Error: {str(e)}')
    print('\nTroubleshooting:')
    print('1. Check if AZURE_OPENAI_API_KEY is correct')
    print('2. Check if AZURE_OPENAI_ENDPOINT format is correct')
    print('3. Check if AZURE_DEPLOYMENT_NAME matches your deployment')
    print('4. Verify your Azure OpenAI resource is active')
"@ | Out-File -FilePath test_connection.py -Encoding UTF8

python test_connection.py
```

### Test 3: Run Application

```powershell
python app.py
```

Expected output:
```
✓ Support agent initialized successfully
✓ Server started on http://0.0.0.0:8000
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "Access Denied" or "401 Unauthorized"

**Cause**: Invalid or expired API key

**Solution**:
1. Go to Azure Portal → Your OpenAI Resource
2. Go to "Keys and Endpoint"
3. Click "Regenerate Key 1"
4. Copy the NEW key to your `.env` file
5. Restart your application

### Issue 2: "Deployment Not Found"

**Cause**: Wrong deployment name

**Solution**:
1. Go to [Azure OpenAI Studio](https://oai.azure.com)
2. Click "Deployments"
3. Find your deployment name (exact spelling matters!)
4. Update `AZURE_DEPLOYMENT_NAME` in `.env`
5. Restart your application

### Issue 3: "Resource Not Found" or "404"

**Cause**: Wrong endpoint URL

**Solution**:
1. Verify endpoint format: `https://YOUR-RESOURCE-NAME.openai.azure.com/`
2. Must end with `/`
3. Must include `https://`
4. Resource name must match your Azure OpenAI resource name

### Issue 4: "Rate Limit Exceeded"

**Cause**: Too many requests

**Solution**:
1. Go to Azure OpenAI Studio → Deployments
2. Click on your deployment
3. Increase "Tokens per Minute Rate Limit"
4. Or wait and retry (rate limits reset per minute)

### Issue 5: "Subscription Not Approved"

**Cause**: Azure OpenAI access not approved yet

**Solution**:
1. Wait for approval email (1-2 business days)
2. Check [https://aka.ms/oai/access](https://aka.ms/oai/access) for status
3. Consider using alternative: OpenAI directly (not Azure)

---

## 💰 Cost Information

### Azure OpenAI Pricing (as of 2024)

| Model | Input (per 1K tokens) | Output (per 1K tokens) | Best For |
|-------|----------------------|------------------------|----------|
| **GPT-4** | $0.03 | $0.06 | Highest quality, complex tasks |
| **GPT-4 Turbo** | $0.01 | $0.03 | Fast + high quality |
| **GPT-3.5 Turbo** | $0.0015 | $0.002 | Fast, cost-effective |

### Example Monthly Costs

| Usage | Model | Estimated Cost |
|-------|-------|----------------|
| 100 queries/day | GPT-3.5 Turbo | ~$5-10/month |
| 100 queries/day | GPT-4 | ~$20-40/month |
| 1000 queries/day | GPT-3.5 Turbo | ~$50-100/month |
| 1000 queries/day | GPT-4 | ~$200-400/month |

**Note**: Costs vary based on query length and response length

### Free Tier

- ⚠️ **No free tier for Azure OpenAI**
- You pay only for what you use (pay-as-you-go)
- First $200 Azure credit for new accounts (can be used for OpenAI)

---

## 🎯 Recommended Setup

### For Development/Testing
```bash
Model: gpt-35-turbo
Rate Limit: 10K tokens/minute
Estimated Cost: $5-20/month
```

### For Production
```bash
Model: gpt-4-turbo or gpt-4
Rate Limit: 50K+ tokens/minute
Estimated Cost: $50-500/month (varies by usage)
```

---

## 📚 Additional Resources

- **Azure OpenAI Documentation**: [https://learn.microsoft.com/azure/ai-services/openai/](https://learn.microsoft.com/azure/ai-services/openai/)
- **Request Access**: [https://aka.ms/oai/access](https://aka.ms/oai/access)
- **Azure OpenAI Studio**: [https://oai.azure.com](https://oai.azure.com)
- **Pricing**: [https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- **Quickstart**: [https://learn.microsoft.com/azure/ai-services/openai/quickstart](https://learn.microsoft.com/azure/ai-services/openai/quickstart)

---

## 🔄 Alternative: Using OpenAI Directly (Non-Azure)

If you don't have Azure OpenAI access, you can use OpenAI directly:

### Setup OpenAI Account
1. Go to [https://platform.openai.com](https://platform.openai.com)
2. Sign up / Login
3. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key

### Configure Application
```bash
# In .env file, comment out Azure OpenAI and use:
# AZURE_OPENAI_API_KEY=...
# AZURE_OPENAI_ENDPOINT=...
# AZURE_DEPLOYMENT_NAME=...

# Instead, use standard OpenAI:
OPENAI_API_KEY=sk-proj-your-key-here
```

### Modify Code
You'll need to update `backend/models/llm.py` to use `ChatOpenAI` instead of `AzureChatOpenAI`.

---

## ✅ Quick Checklist

- [ ] Azure account created
- [ ] Azure OpenAI access requested and approved
- [ ] Azure OpenAI resource created
- [ ] GPT model deployed
- [ ] API key obtained
- [ ] Endpoint URL copied
- [ ] Deployment name noted
- [ ] `.env` file configured
- [ ] Connection tested successfully
- [ ] Application starts without errors

---

**🎉 Once all steps are complete, your Azure OpenAI credentials are ready to use!**

For deployment to Azure, see **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)**
