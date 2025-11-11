# 🚀 Quick Start Guide - Agentic AI Support System

Get your AI support agent running in **5 minutes**!

## Prerequisites

- Python 3.11+
- Node.js 18+
- Azure OpenAI access (required)
- Azure Storage Account (optional, for persistence)

---

## Step 1: Install Dependencies

### Backend

```powershell
cd backend

# Option A: Core dependencies only (no Azure persistence)
pip install langchain==0.3.14 langchain-openai==0.3.0 langchain-community==0.3.14 langgraph==0.2.64 langchain-chroma==0.2.0 chromadb fastapi uvicorn python-dotenv python-multipart

# Option B: Full installation (with Azure services)
pip install -r requirements.txt
```

### Frontend

```powershell
cd frontend
npm install
```

---

## Step 2: Configure Environment

Create `.env` file in `backend/` directory:

### Minimum Configuration (No Persistence)

```env
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
AZURE_API_VERSION=2024-02-15-preview

# Features (Optional)
USE_AZURE_TABLE_STORAGE=false
USE_AZURE_BLOB_STORAGE=false
USE_APPLICATION_INSIGHTS=false
```

### Full Configuration (With Persistence)

```env
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
AZURE_API_VERSION=2024-02-15-preview

# Azure Storage (Optional but recommended)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
AZURE_TABLE_NAME=checkpoints
AZURE_BLOB_CONTAINER_NAME=chromadb

# Application Insights (Optional)
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...

# Feature Flags
USE_AZURE_TABLE_STORAGE=true
USE_AZURE_BLOB_STORAGE=true
USE_APPLICATION_INSIGHTS=true

# Application
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:5173
```

---

## Step 3: Verify Setup

Run the verification script to check dependencies:

```powershell
cd backend
python verify_dependencies.py
```

Expected output:
```
✓ All core dependencies are installed
✓ Required environment variables are set
🎉 Application is ready to run!
```

---

## Step 4: Start Backend

```powershell
cd backend
python app.py
```

Expected output:
```
✓ Support agent initialized successfully
✓ Server started on http://0.0.0.0:8000
```

Test the health endpoint:
```powershell
curl http://localhost:8000/health
```

---

## Step 5: Start Frontend

In a **new terminal**:

```powershell
cd frontend
npm run dev
```

Expected output:
```
VITE v5.4.11  ready in 523 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## Step 6: Test the Application

1. Open browser to `http://localhost:5173`
2. You should see the chat interface
3. Type a message: "Hello, I need help with my order"
4. Wait for the AI agent to respond

### Expected Behavior:
- ✅ Message appears in chat
- ✅ "AI is thinking..." animation shows
- ✅ AI responds with categorized support
- ✅ Sentiment analysis shown in logs

---

## 🎯 Testing Checklist

### Basic Functionality
- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Can send messages
- [ ] AI responds correctly
- [ ] Conversation history persists

### Backend Tests
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test query endpoint
curl -X POST http://localhost:8000/query `
  -H "Content-Type: application/json" `
  -d '{"message": "I need help with shipping", "thread_id": "test123"}'
```

### Frontend Tests
1. **Message Input**: Type and send message
2. **Response Display**: AI response appears
3. **Conversation Flow**: Multiple messages work
4. **Error Handling**: Backend offline shows error
5. **UI Responsiveness**: Works on different screen sizes

---

## 🔧 Troubleshooting

### Issue: Backend won't start

**Check 1**: Dependencies installed?
```powershell
python verify_dependencies.py
```

**Check 2**: Environment variables set?
```powershell
cat .env
```

**Check 3**: Port 8000 available?
```powershell
netstat -ano | findstr :8000
```

### Issue: Frontend can't connect to backend

**Check 1**: Backend running?
```powershell
curl http://localhost:8000/health
```

**Check 2**: CORS configured?
Check `backend/app.py` - ALLOWED_ORIGINS should include `http://localhost:5173`

**Check 3**: API URL correct?
Check `frontend/src/services/api.ts` - baseURL should be `http://localhost:8000`

### Issue: Azure services not working

**Check 1**: Connection strings valid?
```powershell
# Test Azure Storage
az storage account show --name <account-name>
```

**Check 2**: Feature flags enabled?
```env
USE_AZURE_TABLE_STORAGE=true
USE_AZURE_BLOB_STORAGE=true
```

**Check 3**: Packages installed?
```powershell
pip list | findstr azure
```

### Issue: ChromaDB errors

**Solution 1**: Install Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Solution 2**: Use specific ChromaDB version
```powershell
pip install chromadb==0.4.22
```

---

## 📊 Architecture Overview

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │◄───────►│   Frontend  │◄───────►│   Backend   │
│   User UI   │  HTTP   │  React App  │  REST   │  FastAPI    │
└─────────────┘         └─────────────┘         └─────────────┘
                             ▲                         │
                             │                         ▼
                             │                   ┌──────────┐
                             │                   │ LangGraph│
                             │                   │  Agent   │
                             │                   └──────────┘
                             │                         │
                             │                         ▼
                             │              ┌────────────────────┐
                             │              │  Azure OpenAI      │
                             │              │  (GPT-4)           │
                             │              └────────────────────┘
                             │                         │
                             │                         ▼
                             │              ┌────────────────────┐
                             └──────────────│  Azure Storage     │
                                           │  - Table Storage   │
                                           │  - Blob Storage    │
                                           │  - App Insights    │
                                           └────────────────────┘
```

---

## 🎯 Next Steps

### For Local Development:
1. ✅ Application running locally
2. → Add custom knowledge base documents to `backend/data/`
3. → Customize agent behavior in `backend/nodes/`
4. → Style frontend in `frontend/src/App.css`

### For Azure Deployment:
1. ✅ Application tested locally
2. → Create Azure resources (see `AZURE_DEPLOYMENT.md`)
3. → Configure GitHub secrets (see `DEPLOYMENT_GUIDE.md`)
4. → Run deployment script: `.\deploy-to-azure.ps1`
5. → Monitor with Application Insights

### For Production:
1. ✅ Application deployed to Azure
2. → Set up custom domain
3. → Configure SSL certificate
4. → Enable monitoring alerts
5. → Set up CI/CD pipeline
6. → Configure backup strategy

---

## 📚 Documentation

- **[DEPENDENCIES_GUIDE.md](DEPENDENCIES_GUIDE.md)** - Complete dependency documentation
- **[COMPATIBILITY_SUMMARY.md](COMPATIBILITY_SUMMARY.md)** - Compatibility and fixes summary
- **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** - Azure deployment guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Detailed deployment instructions
- **[AZURE_NATIVE_GUIDE.md](AZURE_NATIVE_GUIDE.md)** - Azure services integration
- **[README.md](backend/README.md)** - Backend documentation
- **[README.md](frontend/README.md)** - Frontend documentation

---

## 💡 Tips

### Development Tips:
- Use `USE_AZURE_*=false` for faster local development
- Enable Application Insights only when debugging
- Use in-memory checkpointer for testing
- Hot reload works for both frontend and backend

### Production Tips:
- Always enable Azure Table Storage for session persistence
- Set up Blob Storage backup schedule
- Monitor Application Insights for errors
- Use environment-specific .env files
- Set ENVIRONMENT=production in Azure

### Cost Optimization:
- Azure Free Tier covers most development needs
- Table Storage: 20K operations/month free
- Blob Storage: 5GB storage free
- App Insights: 5GB data/month free
- Static Web Apps: 100GB bandwidth free
- App Service F1: 60 minutes CPU/day free

---

## ❓ Need Help?

### Check Logs:
```powershell
# Backend logs
cat backend/logs/app.log

# Azure App Service logs (if deployed)
az webapp log tail --name your-backend-app --resource-group your-rg
```

### Health Check:
```powershell
curl http://localhost:8000/health | ConvertFrom-Json
```

### Common Commands:
```powershell
# Restart backend
cd backend; python app.py

# Rebuild frontend
cd frontend; npm run build

# Check dependencies
cd backend; python verify_dependencies.py

# View environment
cd backend; cat .env

# Test Azure connection
az account show
```

---

## 🎉 Success Criteria

Your application is working correctly when:

✅ Backend health endpoint returns 200 OK  
✅ Frontend loads without console errors  
✅ Chat messages send and receive responses  
✅ AI categorizes queries correctly  
✅ Sentiment analysis shows in responses  
✅ Conversation history persists (if Azure Storage enabled)  
✅ Logs show no errors  

**Congratulations! Your AI Support Agent is ready! 🚀**
