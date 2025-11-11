# 🚀 Complete Azure Deployment Guide (Portal Method)

**Time Required**: 30-45 minutes  
**Difficulty**: Beginner-friendly  
**Method**: Azure Portal (GUI) - No command line required!

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Get Azure OpenAI Credentials](#phase-1-get-azure-openai-credentials)
3. [Phase 2: Prepare Your Application](#phase-2-prepare-your-application)
4. [Phase 3: Deploy Backend to Azure App Service](#phase-3-deploy-backend-to-azure-app-service)
5. [Phase 4: Deploy Frontend to Azure Static Web Apps](#phase-4-deploy-frontend-to-azure-static-web-apps)
6. [Phase 5: Test Your Deployment](#phase-5-test-your-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### ✅ What You Need:

- [ ] **Azure Account** - [Sign up here](https://azure.microsoft.com/free/) (free $200 credit)
- [ ] **GitHub Account** - [Sign up here](https://github.com/signup) (free)
- [ ] **Git Installed** - [Download here](https://git-scm.com/downloads)
- [ ] **VS Code** - Already installed ✅
- [ ] **Your Application Code** - Already have it ✅

### 💰 **Cost Estimate**:
- Azure OpenAI: ~$10-40/month (depending on usage)
- App Service: ~$13/month (Basic B1 tier)
- Static Web App: **FREE** tier available
- **Total**: ~$23-53/month or use Free Trial credits

---

## Phase 1: Get Azure OpenAI Credentials

### Step 1.1: Request Azure OpenAI Access (5 minutes)

1. **Go to**: [https://aka.ms/oai/access](https://aka.ms/oai/access)
2. **Fill out the form**:
   - Business email (not personal Gmail/Yahoo)
   - Company name
   - Use case: "AI-powered customer support chatbot"
3. **Submit** and wait for approval email (usually 1-3 business days)

> ⏭️ **Skip for now?** Use OpenAI directly instead. See [Alternative: OpenAI Setup](#alternative-openai-setup)

---

### Step 1.2: Create Azure OpenAI Resource (3 minutes)

Once approved:

1. **Go to Azure Portal**: [https://portal.azure.com](https://portal.azure.com)

2. **Click**: `+ Create a resource`

3. **Search**: `Azure OpenAI`

4. **Click**: `Create` → `Azure OpenAI`

5. **Fill out the form**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Subscription** | Your subscription | Usually "Pay-As-You-Go" |
   | **Resource group** | `rg-agentic-ai` | Click "Create new" |
   | **Region** | `East US` | Best for OpenAI |
   | **Name** | `openai-support-[your-initials]` | Must be globally unique |
   | **Pricing tier** | `Standard S0` | Pay-as-you-go |

6. **Click**: `Review + create` → `Create`

7. **Wait**: ~2 minutes for deployment

8. **Click**: `Go to resource`

---

### Step 1.3: Deploy GPT Model (2 minutes)

1. **From your OpenAI resource**, click: `Go to Azure OpenAI Studio`

2. **Or go directly to**: [https://oai.azure.com](https://oai.azure.com)

3. **Click**: `Deployments` (left sidebar)

4. **Click**: `+ Create new deployment`

5. **Configure deployment**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Select a model** | `gpt-4` or `gpt-35-turbo` | GPT-4 is smarter but costlier |
   | **Deployment name** | `gpt-4-deployment` | Remember this! |
   | **Model version** | Latest available | Usually auto-selected |
   | **Deployment type** | `Standard` | Default option |
   | **Tokens per minute rate limit** | `10K` | Start small |

6. **Click**: `Create`

7. **Wait**: ~30 seconds

---

### Step 1.4: Get Your Credentials (1 minute)

1. **Go back to Azure Portal**: [https://portal.azure.com](https://portal.azure.com)

2. **Navigate to**: Your Azure OpenAI resource (`openai-support-[your-initials]`)

3. **Click**: `Keys and Endpoint` (left sidebar under "Resource Management")

4. **Copy these 2 values**:
   ```
   KEY 1: [Click "Show Keys" then copy]
   Endpoint: https://openai-support-xxx.openai.azure.com/
   ```

5. **Save in Notepad**:
   ```
   AZURE_OPENAI_API_KEY=4a5b6c7d8e9f0g1h2i3j4k5l6m7n8o9p
   AZURE_OPENAI_ENDPOINT=https://openai-support-xxx.openai.azure.com/
   AZURE_DEPLOYMENT_NAME=gpt-4-deployment
   AZURE_API_VERSION=2024-02-15-preview
   ```

✅ **Phase 1 Complete!** You now have Azure OpenAI credentials.

---

## Phase 2: Prepare Your Application

### Step 2.1: Test Locally First (5 minutes)

1. **Open PowerShell in VS Code** (Terminal → New Terminal)

2. **Navigate to backend**:
   ```powershell
   cd C:\Users\rathokap\Downloads\agentic-ai\backend
   ```

3. **Create `.env` file**:
   ```powershell
   @"
   AZURE_OPENAI_API_KEY=your-key-from-step-1.4
   AZURE_OPENAI_ENDPOINT=your-endpoint-from-step-1.4
   AZURE_DEPLOYMENT_NAME=gpt-4-deployment
   AZURE_API_VERSION=2024-02-15-preview
   "@ | Out-File -Encoding UTF8 .env
   ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

5. **Test the app**:
   ```powershell
   python app.py
   ```

6. **Open browser**: [http://localhost:8000](http://localhost:8000)

7. **Test API**: [http://localhost:8000/docs](http://localhost:8000/docs)

8. **Stop the server**: Press `Ctrl+C` in terminal

✅ **Works locally?** Proceed to deployment!  
❌ **Errors?** See [Troubleshooting](#troubleshooting)

---

### Step 2.2: Push Code to GitHub (5 minutes)

Azure needs your code in GitHub to deploy it.

1. **Create `.gitignore` file** (if not exists):
   ```powershell
   cd C:\Users\rathokap\Downloads\agentic-ai
   
   @"
   # Python
   __pycache__/
   *.py[cod]
   venv/
   .env
   *.sqlite3
   
   # Node
   node_modules/
   .next/
   dist/
   build/
   
   # IDE
   .vscode/
   .idea/
   
   # OS
   .DS_Store
   Thumbs.db
   "@ | Out-File -Encoding UTF8 .gitignore
   ```

2. **Initialize Git** (if not already):
   ```powershell
   git init
   git add .
   git commit -m "Initial commit - Ready for Azure deployment"
   ```

3. **Create GitHub Repository**:
   - Go to: [https://github.com/new](https://github.com/new)
   - Repository name: `agentic-ai-support`
   - Visibility: `Private` (recommended)
   - Click: `Create repository`

4. **Push to GitHub**:
   ```powershell
   git remote add origin https://github.com/YOUR-USERNAME/agentic-ai-support.git
   git branch -M main
   git push -u origin main
   ```

5. **Verify**: Check [https://github.com/YOUR-USERNAME/agentic-ai-support](https://github.com) - your code should be there!

✅ **Phase 2 Complete!** Code is ready for deployment.

---

## Phase 3: Deploy Backend to Azure App Service

### Step 3.1: Create App Service (5 minutes)

1. **Go to Azure Portal**: [https://portal.azure.com](https://portal.azure.com)

2. **Click**: `+ Create a resource`

3. **Search**: `Web App`

4. **Click**: `Create` → `Web App`

5. **Fill out the Basics tab**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Subscription** | Your subscription | Same as before |
   | **Resource group** | `rg-agentic-ai` | Use existing |
   | **Name** | `agentic-ai-backend-[initials]` | Must be globally unique |
   | **Publish** | `Code` | Not Docker |
   | **Runtime stack** | `Python 3.11` | Match your version |
   | **Operating System** | `Linux` | Recommended |
   | **Region** | `East US` | Same as OpenAI |

6. **Linux Plan**: Click `Create new`
   - Name: `asp-agentic-ai`
   - Click OK

7. **Pricing plan**: 
   - Click `Explore pricing plans`
   - Select `Basic B1` ($13/month) or `Free F1` (limited)
   - Click `Select`

8. **Click**: `Review + create` → `Create`

9. **Wait**: ~2 minutes for deployment

10. **Click**: `Go to resource`

---

### Step 3.2: Configure Deployment Source (3 minutes)

1. **From your App Service**, click: `Deployment Center` (left sidebar)

2. **Source**: Select `GitHub`

3. **Click**: `Authorize` → Sign in to GitHub

4. **Organization**: Select your GitHub username

5. **Repository**: Select `agentic-ai-support`

6. **Branch**: Select `main`

7. **Click**: `Save` (top of page)

8. **Azure will**:
   - Create a GitHub Actions workflow
   - Automatically build and deploy your app
   - Show deployment logs

9. **Click**: `Logs` tab to watch deployment progress (~3-5 minutes)

---

### Step 3.3: Configure Environment Variables (3 minutes)

Your app needs Azure OpenAI credentials!

1. **From your App Service**, click: `Configuration` (left sidebar under "Settings")

2. **Click**: `+ New application setting`

3. **Add these 4 settings** (one at a time):

   | Name | Value | Notes |
   |------|-------|-------|
   | `AZURE_OPENAI_API_KEY` | Your key from Step 1.4 | From notepad |
   | `AZURE_OPENAI_ENDPOINT` | Your endpoint from Step 1.4 | Include trailing / |
   | `AZURE_DEPLOYMENT_NAME` | `gpt-4-deployment` | Your deployment name |
   | `AZURE_API_VERSION` | `2024-02-15-preview` | API version |

4. **Add one more setting**:
   | Name | Value | Notes |
   |------|-------|-------|
   | `ENVIRONMENT` | `production` | Enables Gunicorn |

5. **Click**: `Save` (top of page)

6. **Click**: `Continue` when prompted

7. **Wait**: ~30 seconds for restart

---

### Step 3.4: Configure Startup Command (2 minutes)

1. **From your App Service**, click: `Configuration` (left sidebar)

2. **Click**: `General settings` tab

3. **Startup Command**: Enter:
   ```bash
   gunicorn -c backend/gunicorn.conf.py backend.app:app
   ```

4. **Click**: `Save` (top of page)

5. **Click**: `Continue` when prompted

6. **Wait**: ~30 seconds for restart

---

### Step 3.5: Verify Backend Deployment (2 minutes)

1. **From your App Service overview**, find: `Default domain`
   - Example: `https://agentic-ai-backend-xxx.azurewebsites.net`

2. **Click the URL** or copy to browser

3. **Test these endpoints**:
   ```
   ✅ Root: https://your-app.azurewebsites.net/
      → Should show: {"message": "Support Agent API is running"}
   
   ✅ Health: https://your-app.azurewebsites.net/health
      → Should show service status
   
   ✅ Docs: https://your-app.azurewebsites.net/docs
      → Should show interactive API documentation
   
   ✅ Query: Test from /docs page
      → Should respond with AI-generated answer
   ```

4. **Save your backend URL** in Notepad:
   ```
   BACKEND_URL=https://agentic-ai-backend-xxx.azurewebsites.net
   ```

✅ **Phase 3 Complete!** Backend is deployed and running.

---

## Phase 4: Deploy Frontend to Azure Static Web Apps

### Step 4.1: Update Frontend API URL (2 minutes)

1. **Open**: `frontend/src/services/api.ts` in VS Code

2. **Find the line**:
   ```typescript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```

3. **Replace with your backend URL** (from Step 3.5):
   ```typescript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://agentic-ai-backend-xxx.azurewebsites.net';
   ```

4. **Save the file**

5. **Commit and push**:
   ```powershell
   cd C:\Users\rathokap\Downloads\agentic-ai
   git add frontend/src/services/api.ts
   git commit -m "Update API URL for production"
   git push
   ```

---

### Step 4.2: Create Static Web App (5 minutes)

1. **Go to Azure Portal**: [https://portal.azure.com](https://portal.azure.com)

2. **Click**: `+ Create a resource`

3. **Search**: `Static Web App`

4. **Click**: `Create` → `Static Web App`

5. **Fill out the Basics tab**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Subscription** | Your subscription | Same as before |
   | **Resource group** | `rg-agentic-ai` | Use existing |
   | **Name** | `agentic-ai-frontend` | Your choice |
   | **Plan type** | `Free` | $0/month! |
   | **Region** | `East US 2` | Closest available |
   | **Source** | `GitHub` | Default |

6. **Click**: `Sign in with GitHub` → Authorize

7. **Deployment details**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Organization** | Your GitHub username | Auto-populated |
   | **Repository** | `agentic-ai-support` | Select from list |
   | **Branch** | `main` | Default |

8. **Build Details**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **Build Presets** | `Custom` | Not React/Vue/Angular |
   | **App location** | `/frontend` | Your frontend folder |
   | **Api location** | *(leave empty)* | Backend is separate |
   | **Output location** | `dist` | Vite build output |

9. **Click**: `Review + create` → `Create`

10. **Wait**: ~3 minutes for deployment

11. **Click**: `Go to resource`

---

### Step 4.3: Get Frontend URL (1 minute)

1. **From your Static Web App**, find: `URL` in overview
   - Example: `https://happy-grass-xxx.azurestaticapps.net`

2. **Click the URL** to open your frontend

3. **Test the chat interface**:
   - Type a question: "What are your business hours?"
   - Should get AI-generated response
   - Check network tab for API calls to your backend

✅ **Phase 4 Complete!** Frontend is deployed and connected to backend.

---

## Phase 5: Test Your Deployment

### Step 5.1: End-to-End Testing (5 minutes)

1. **Open your frontend URL**: `https://your-app.azurestaticapps.net`

2. **Test these scenarios**:

   | Test | Expected Result | Status |
   |------|-----------------|--------|
   | **Page loads** | UI appears, no errors | ⬜ |
   | **Send message** | "What are your business hours?" | ⬜ |
   | **Get response** | AI-generated answer appears | ⬜ |
   | **Check sentiment** | Sentiment indicator shows | ⬜ |
   | **Test routing** | Different query types work | ⬜ |
   | **Error handling** | Invalid input handled gracefully | ⬜ |

3. **Open browser DevTools** (F12):
   - **Console**: No errors
   - **Network**: API calls to backend succeed (200 OK)
   - **Application**: No CORS errors

---

### Step 5.2: Performance Testing (3 minutes)

1. **Test API directly**:
   ```powershell
   # Test backend health
   curl https://your-backend.azurewebsites.net/health
   
   # Test query endpoint
   curl -X POST https://your-backend.azurewebsites.net/query `
     -H "Content-Type: application/json" `
     -d '{"query":"What are your business hours?"}'
   ```

2. **Expected response times**:
   - Health check: < 1 second
   - Query endpoint: 2-5 seconds (includes AI processing)

3. **Check logs**:
   - **Backend**: Azure Portal → App Service → Log stream
   - **Frontend**: Azure Portal → Static Web App → Logs

---

### Step 5.3: Save Your Deployment Info (1 minute)

Create a deployment reference file:

```powershell
@"
# 🚀 Azure Deployment Information

## Deployed on: $(Get-Date -Format "yyyy-MM-dd HH:mm")

### 🔗 URLs
- **Frontend**: https://your-app.azurestaticapps.net
- **Backend**: https://your-backend.azurewebsites.net
- **API Docs**: https://your-backend.azurewebsites.net/docs

### 🔑 Azure Resources
- **Resource Group**: rg-agentic-ai
- **App Service**: agentic-ai-backend-xxx
- **Static Web App**: agentic-ai-frontend
- **OpenAI Resource**: openai-support-xxx

### 📊 Monitoring
- **App Service Logs**: Azure Portal → App Service → Log stream
- **Static Web App Logs**: Azure Portal → Static Web App → Logs
- **OpenAI Usage**: Azure Portal → OpenAI → Metrics

### 💰 Cost Tracking
- **View costs**: Azure Portal → Cost Management + Billing

### 🔄 Update Deployment
1. Make changes in VS Code
2. Commit: git add . && git commit -m "Update"
3. Push: git push
4. Azure auto-deploys via GitHub Actions (~3-5 min)

"@ | Out-File -Encoding UTF8 DEPLOYMENT_INFO.txt
```

✅ **Phase 5 Complete!** Your application is fully deployed and tested.

---

## 🎉 Congratulations! You're Live!

### What You've Accomplished:

✅ Created Azure OpenAI resource with GPT model  
✅ Deployed backend to Azure App Service  
✅ Deployed frontend to Azure Static Web Apps  
✅ Configured environment variables  
✅ Connected frontend to backend  
✅ Tested end-to-end functionality  

### Your Live Application:

```
🌐 Frontend: https://your-app.azurestaticapps.net
🔧 Backend: https://your-backend.azurewebsites.net
📚 API Docs: https://your-backend.azurewebsites.net/docs
```

---

## 🔄 Making Updates

### Update Backend Code:

```powershell
# 1. Make changes in backend/
# 2. Test locally
cd backend
python app.py

# 3. Commit and push
git add .
git commit -m "Update backend logic"
git push

# 4. Azure deploys automatically (~3-5 min)
```

### Update Frontend Code:

```powershell
# 1. Make changes in frontend/
# 2. Test locally
cd frontend
npm run dev

# 3. Commit and push
git add .
git commit -m "Update UI"
git push

# 4. Azure deploys automatically (~2-3 min)
```

---

## 📊 Monitoring & Maintenance

### View Logs:

1. **Backend logs**:
   - Azure Portal → App Service → Log stream
   - Or: Monitoring → Log Analytics

2. **Frontend logs**:
   - Azure Portal → Static Web App → Logs
   - Or: Browser DevTools Console

### Monitor Costs:

1. **Go to**: Azure Portal → Cost Management + Billing
2. **View**: Cost analysis by resource
3. **Set**: Budget alerts (recommended: $50/month)

### Scale Up/Down:

1. **Backend**: App Service → Scale up (change tier)
2. **OpenAI**: Adjust tokens per minute in deployments
3. **Frontend**: Free tier (no scaling needed)

---

## Troubleshooting

### ❌ Backend won't start

**Symptoms**: App Service shows "Application Error"

**Solutions**:
1. Check logs: App Service → Log stream
2. Verify environment variables: Configuration → Application settings
3. Check startup command: Configuration → General settings
4. Verify requirements.txt has all dependencies
5. Check Python version matches (3.11)

**Common errors**:
```
ModuleNotFoundError: No module named 'fastapi'
→ Add 'fastapi' to requirements.txt, push to GitHub

Cannot find module 'app'
→ Check startup command: gunicorn -c backend/gunicorn.conf.py backend.app:app
```

---

### ❌ Frontend can't connect to backend

**Symptoms**: API calls fail with CORS errors

**Solutions**:
1. Check API_BASE_URL in `frontend/src/services/api.ts`
2. Verify backend URL is correct (no trailing slash in api.ts)
3. Check CORS settings in `backend/app.py`:
   ```python
   origins = [
       "http://localhost:3000",
       "http://localhost:5173",
       "https://your-app.azurestaticapps.net"  # Add your frontend URL
   ]
   ```
4. Push changes to GitHub

---

### ❌ Azure OpenAI returns 401 Unauthorized

**Symptoms**: API calls fail with "Invalid API key"

**Solutions**:
1. Verify API key: Azure Portal → OpenAI → Keys and Endpoint
2. Check environment variable: App Service → Configuration
3. Ensure no extra spaces or quotes in the key
4. Try using KEY 2 instead of KEY 1
5. Regenerate keys if needed

---

### ❌ GitHub Actions deployment fails

**Symptoms**: Red X on GitHub commits, deployment doesn't update

**Solutions**:
1. Check GitHub Actions: Repository → Actions tab
2. View failed workflow logs
3. Common issues:
   - Wrong Python version (update `.github/workflows/` file)
   - Missing dependencies (update requirements.txt)
   - Build errors (check logs for specific error)
4. Re-run workflow after fixes

---

### ❌ High costs

**Symptoms**: Bill higher than expected

**Solutions**:
1. Check OpenAI usage: Azure Portal → OpenAI → Metrics
2. Reduce token limits: OpenAI Studio → Deployments → Edit
3. Add rate limiting in backend code
4. Switch to cheaper model (GPT-3.5 instead of GPT-4)
5. Set budget alerts: Cost Management → Budgets

---

### ❌ Slow response times

**Symptoms**: API takes >10 seconds to respond

**Solutions**:
1. Check App Service plan (upgrade from Free to Basic)
2. Enable "Always On": App Service → Configuration → General settings
3. Add caching for frequent queries
4. Optimize prompts (shorter = faster)
5. Use GPT-3.5 Turbo instead of GPT-4

---

## Alternative: OpenAI Setup

Don't have Azure OpenAI access? Use OpenAI directly:

### 1. Get OpenAI API Key:
- Go to: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Create account, add payment method
- Generate API key

### 2. Update backend code:

**In `backend/config/settings.py`**, change:
```python
# From Azure OpenAI
from openai import AzureOpenAI
client = AzureOpenAI(...)

# To OpenAI
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

### 3. Update environment variables:
```bash
# Remove Azure-specific vars
OPENAI_API_KEY=sk-proj-xxx...

# Use in App Service Configuration
```

### 4. Update model calls:
```python
# From:
model=os.getenv("AZURE_DEPLOYMENT_NAME")

# To:
model="gpt-4"  # or "gpt-3.5-turbo"
```

**Cost**: ~$20-60/month (similar to Azure OpenAI)

---

## 📚 Additional Resources

### Documentation:
- [Azure App Service Docs](https://docs.microsoft.com/azure/app-service/)
- [Azure Static Web Apps Docs](https://docs.microsoft.com/azure/static-web-apps/)
- [Azure OpenAI Docs](https://docs.microsoft.com/azure/cognitive-services/openai/)

### Support:
- [Azure Support Portal](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade)
- [GitHub Actions Docs](https://docs.github.com/actions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/azure)

### Your Local Guides:
- `AZURE_OPENAI_SETUP.md` - Detailed OpenAI setup
- `AZURE_OPENAI_QUICKREF.md` - Quick reference card
- `DEPLOYMENT_CHECKLIST.md` - Comprehensive checklist
- `README.md` - Project overview

---

## 🎯 Quick Reference

| Task | Command/Action |
|------|----------------|
| **View backend logs** | Azure Portal → App Service → Log stream |
| **View frontend logs** | Azure Portal → Static Web App → Logs |
| **Update backend** | `git add . && git commit -m "msg" && git push` |
| **Update frontend** | `git add . && git commit -m "msg" && git push` |
| **View costs** | Azure Portal → Cost Management |
| **Scale backend** | Azure Portal → App Service → Scale up |
| **Check OpenAI usage** | Azure Portal → OpenAI → Metrics |
| **View API docs** | https://your-backend.azurewebsites.net/docs |

---

## 🆘 Need Help?

If you're stuck:

1. **Check logs first** (App Service → Log stream)
2. **Review error messages** (usually very descriptive)
3. **Search Azure Docs** (most issues are documented)
4. **Check GitHub Actions logs** (for deployment issues)
5. **Review this guide's Troubleshooting section**

**Remember**: Most deployment issues are:
- Wrong environment variables (typos, missing values)
- Incorrect URLs (trailing slashes, wrong domains)
- Missing dependencies (update requirements.txt)

---

**🎉 Happy Deploying!**

Your AI-powered support agent is now live on Azure! 🚀
