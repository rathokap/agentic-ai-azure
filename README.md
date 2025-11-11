# 🤖 Agentic AI - Customer Support Agent

**An intelligent customer support system powered by Azure OpenAI and LangGraph** with persistent session management, sentiment analysis, and multi-node agent architecture.

[![Azure](https://img.shields.io/badge/Azure-OpenAI-blue)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.64-green)](https://github.com/langchain-ai/langgraph)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB)](https://react.dev/)
[![Production](https://img.shields.io/badge/Production-Ready-brightgreen)](DEPLOYMENT_READY.md)

> 🚀 **DEPLOYMENT READY FOR AZURE** - Complete production configuration with Gunicorn, health checks, monitoring  
> ⚡ **Quick Deploy** - See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for one-command deployment  
> 🎯 **START HERE** - New to deployment? See [START_HERE.md](START_HERE.md) for complete beginner's guide  
> ☁️ **Azure Free Tier** - Deploy for $0/month (only pay for Azure OpenAI usage)

A production-ready full-stack AI support agent with:
- ✅ Multi-node LangGraph agent workflow
- ✅ Azure OpenAI GPT-4 integration
- ✅ Persistent session management (Azure Table Storage)
- ✅ Vector database RAG with ChromaDB
- ✅ Modern React TypeScript UI
- ✅ **Production-grade server (Gunicorn + Uvicorn)**
- ✅ **Azure-optimized startup scripts**
- ✅ **Automated deployment verification**
- ✅ Azure native components (optional)
- ✅ CI/CD with GitHub Actions

## 🏗️ Architecture

```
agentic-ai/
├── backend/          # FastAPI backend with LangGraph agent
│   ├── app.py                    # Main FastAPI application
│   ├── graph/                    # LangGraph workflow
│   ├── nodes/                    # Agent nodes (categorize, sentiment, response)
│   ├── models/                   # LLM and schema definitions
│   ├── vectorstore/              # ChromaDB integration
│   └── knowledge_base/           # Document storage
│
└── frontend/         # React + TypeScript UI
    ├── src/
    │   ├── components/           # React components
    │   ├── services/             # API integration
    │   └── App.tsx               # Main application
    └── package.json
```

## ✨ Features

### Backend
- **LangGraph Workflow**: State-based agent with routing and decision-making
- **Sentiment Analysis**: Automatic sentiment detection (Positive, Negative, Neutral)
- **Query Categorization**: Classifies queries (Technical, Billing, General)
- **Vector Store Integration**: ChromaDB for knowledge base search
- **Session Management**: Thread-based conversation history
- **FastAPI**: High-performance async API
- **CORS Support**: Configured for frontend integration

### Frontend
- **Modern React UI**: Built with TypeScript and Vite
- **Conversational Interface**: Chat-like experience with message bubbles
- **Real-time Updates**: Loading indicators and smooth animations
- **Responsive Design**: Mobile-friendly layout
- **Dark Mode Support**: System preference detection
- **Error Handling**: Graceful error messages and retry logic

## 🌟 Key Features

### 🎯 Intelligent Agent System
- **Multi-Node Architecture**: Categorization → Sentiment Analysis → Response Generation
- **Context-Aware**: Maintains conversation history across sessions
- **Escalation Support**: Automatically escalates complex queries
- **Knowledge Base**: RAG (Retrieval-Augmented Generation) with ChromaDB

### 💬 Conversational Interface
- **Modern Chat UI**: React-based responsive design
- **Real-time Updates**: Instant message streaming
- **Conversation History**: Persistent session management
- **Typing Indicators**: Visual feedback during processing

### ☁️ Azure Native Integration (Optional)
- **Azure OpenAI**: GPT-4 powered responses
- **Azure Table Storage**: Persistent session checkpoints (20K ops/month free)
- **Azure Blob Storage**: ChromaDB backup and restore (5GB free)
- **Application Insights**: Production monitoring (5GB data/month free)
- **Static Web Apps**: Frontend hosting (100GB bandwidth free)
- **App Service F1**: Backend hosting (60 min CPU/day free)

### � Developer Friendly
- **TypeScript Frontend**: Type-safe React components
- **FastAPI Backend**: Modern async Python with OpenAPI docs
- **Environment-Based Config**: Easy deployment across environments
- **Graceful Degradation**: Works with or without Azure services

---

## �🚀 Quick Start

### Prerequisites

- **Python 3.11+** for backend
- **Node.js 18+** for frontend
- **Azure OpenAI access** (required)
- **Azure Storage Account** (optional, for persistence)

### 1. Install Dependencies

```powershell
# Backend (core dependencies only)
cd backend
pip install langchain==0.3.14 langchain-openai==0.3.0 langgraph==0.2.64 fastapi uvicorn python-dotenv

# OR: Full installation with Azure services
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Configure Environment

Create `backend/.env`:

```env
# Required
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your-deployment-name
AZURE_API_VERSION=2024-02-15-preview

# Optional (for persistence)
USE_AZURE_TABLE_STORAGE=false
USE_AZURE_BLOB_STORAGE=false
USE_APPLICATION_INSIGHTS=false
```

### 3. Verify Setup

```powershell
cd backend
python verify_dependencies.py
```

Expected: `✓ All core dependencies are installed`

### 4. Run Application

```powershell
# Terminal 1: Backend
cd backend
python app.py
# Starts on http://localhost:8000

# Terminal 2: Frontend
cd frontend
npm run dev
# Starts on http://localhost:5173
```

### 5. Access Application

Open browser to `http://localhost:5173` and start chatting!

**📖 Detailed 5-minute guide**: See [QUICK_START.md](QUICK_START.md)

---

## 📖 Documentation

| Document | Description | Status |
|----------|-------------|--------|
| **[START_HERE.md](START_HERE.md)** | **👉 Start here for deployment** | ⭐ NEW |
| **[DEPLOYMENT_ROADMAP.md](DEPLOYMENT_ROADMAP.md)** | Visual deployment roadmap | ⭐ NEW |
| **[AZURE_PORTAL_DEPLOYMENT.md](AZURE_PORTAL_DEPLOYMENT.md)** | Complete Azure Portal deployment guide | ⭐ NEW |
| **[AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)** | Get Azure OpenAI credentials | ⚡ NEW |
| **[AZURE_OPENAI_QUICKREF.md](AZURE_OPENAI_QUICKREF.md)** | Quick reference for credentials | ⚡ NEW |
| **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** | One-command deployment cheat sheet | ⚡ NEW |
| **[DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)** | Production transformation summary | ⚡ NEW |
| **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** | 60+ point deployment checklist | ⚡ NEW |
| **[DEPLOYMENT_COMPLETE.md](DEPLOYMENT_COMPLETE.md)** | Complete change summary | ⚡ NEW |
| **[QUICK_START.md](QUICK_START.md)** | Get running in 5 minutes | ✅ |
| **[DEPENDENCIES_GUIDE.md](DEPENDENCIES_GUIDE.md)** | Complete dependency documentation | ✅ |
| **[COMPATIBILITY_SUMMARY.md](COMPATIBILITY_SUMMARY.md)** | Code compatibility status | ✅ |
| **[AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)** | Azure free-tier deployment guide | ✅ |
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | Detailed deployment instructions | ✅ |
| **[AZURE_NATIVE_GUIDE.md](AZURE_NATIVE_GUIDE.md)** | Azure services integration | ✅ |

---

## 📖 Detailed Setup

### Backend Configuration

#### API Endpoints

**POST /query**
- **Request Body**:
  ```json
  {
    "message": "I need help with shipping",
    "thread_id": "user-123"
  }
  ```
- **Response**:
  ```json
  {
    "response": "I'll help you with shipping...",
    "sentiment": "neutral",
    "category": "shipping"
  }
  ```

**GET /health**
- **Response**:
  ```json
  {
    "status": "healthy",
    "agent_initialized": true,
    "azure_table_storage": "true",
    "application_insights": true
  }
  ```

**GET /docs**
- Interactive OpenAPI documentation

#### Testing the Backend

```powershell
# Health check
curl http://localhost:8000/health

# Test query
curl -X POST http://localhost:8000/query `
  -H "Content-Type: application/json" `
  -d '{"message": "Help with shipping", "thread_id": "test123"}'

# OpenAPI docs
Start http://localhost:8000/docs
```

### Frontend Configuration

#### Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

#### Building for Production

```powershell
cd frontend
npm run build
```

Output will be in `frontend/dist/`

## 🔧 Development

### Backend Development

**Project Structure:**
```
backend/
├── app.py                 # FastAPI application with CORS
├── main.py                # CLI interface
├── graph/
│   └── build_graph.py     # LangGraph workflow builder
├── nodes/
│   ├── categorize.py      # Query categorization
│   ├── sentiment.py       # Sentiment analysis
│   ├── router.py          # Query routing
│   ├── responses.py       # Response generation
│   └── escalate.py        # Escalation handling
├── models/
│   ├── llm.py            # LLM configuration
│   └── schema.py         # Pydantic models
└── vectorstore/
    └── chroma_store.py   # Vector DB setup
```

**Key Technologies:**
- LangChain 0.3.14
- LangGraph 0.2.64
- FastAPI
- ChromaDB
- Pydantic

### Frontend Development

**Project Structure:**
```
frontend/src/
├── components/
│   ├── ChatMessage.tsx    # Message display component
│   ├── ChatInput.tsx      # User input component
│   └── *.css             # Component styles
├── services/
│   └── api.ts            # Backend API client
├── App.tsx               # Main application
└── main.tsx              # Entry point
```

**Key Technologies:**
- React 18
- TypeScript
- Vite
- Axios

## 🎨 Customization

### Styling

The frontend uses a gradient theme. Modify colors in `frontend/src/App.css`:

```css
.app {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Agent Behavior

Modify the LangGraph nodes in `backend/nodes/` to customize:
- Query categorization logic
- Sentiment analysis
- Response generation
- Escalation criteria

### Knowledge Base

Add documents to the knowledge base:

```python
# In backend/data/load_documents.py
docs = load_documents("path/to/your/documents.json")
retriever = create_vector_db(docs)
```

## 🐳 Docker Deployment

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

---

## ☁️ Azure Deployment

### One-Command Deployment ⚡ (Recommended)

```powershell
# Deploy entire stack to Azure Free Tier in 5 minutes
.\deploy-to-azure.ps1 `
    -AzureOpenAIKey "your-key" `
    -AzureOpenAIEndpoint "https://your-resource.openai.azure.com/" `
    -AzureDeploymentName "your-deployment-name"
```

**What it creates**:
- ✅ Backend App Service (F1 Free) with Gunicorn + Uvicorn workers
- ✅ Frontend Static Web App (Free) 
- ✅ Storage Account (Free 5GB) for sessions + backups
- ✅ Application Insights (Free 5GB/month) for monitoring
- ✅ GitHub Actions CI/CD pipelines
- ✅ Complete environment configuration

**Cost**: $0/month with Azure Free Tier limits

**📖 Quick Reference**: See [QUICK_DEPLOY.md](QUICK_DEPLOY.md)

### Manual Deployment

**Backend (Azure App Service)**:
```powershell
az login
az group create --name support-agent-rg --location eastus
az appservice plan create --name support-agent-plan --resource-group support-agent-rg --sku F1 --is-linux
az webapp create --resource-group support-agent-rg --plan support-agent-plan --name support-agent-backend --runtime "PYTHON:3.11"
az webapp config appsettings set --resource-group support-agent-rg --name support-agent-backend --settings @appsettings.json
az webapp up --resource-group support-agent-rg --name support-agent-backend
```

**Frontend (Static Web Apps)**:
```powershell
cd frontend
npm run build
az staticwebapp create --name support-agent-frontend --resource-group support-agent-rg --location eastus
```

**📖 Complete guide**: See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)

## 🧪 Testing

### Backend Tests

```powershell
cd backend
python -m pytest tests/
```

### Frontend Tests

```powershell
cd frontend
npm test
```

## 📊 Monitoring

### Backend Logs

```powershell
# View backend logs
cd backend
python app.py
```

### Frontend Logs

Check browser console for frontend errors and API calls.

## 🔒 Security Best Practices

1. **API Keys**: Never commit API keys to version control
2. **CORS**: Configure specific origins in production
3. **Environment Variables**: Use Azure Key Vault for secrets
4. **HTTPS**: Always use HTTPS in production
5. **Rate Limiting**: Implement rate limiting for API endpoints

---

## � Troubleshooting

### Common Issues

**Issue**: Backend won't start  
**Solution**: Run `python verify_dependencies.py`

**Issue**: Frontend can't connect  
**Solution**: 
- Check CORS in `backend/app.py` includes `http://localhost:5173`
- Verify API URL in `frontend/src/services/api.ts`

**Issue**: ChromaDB errors on Windows  
**Solution**: Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

**Issue**: Azure services not working  
**Solution**: 
- Verify `.env` has correct connection strings
- Check feature flags: `USE_AZURE_TABLE_STORAGE=true`
- Ensure Azure packages installed: `pip install -r requirements.txt`

**Issue**: LangGraph compatibility errors  
**Solution**: This is fixed! We use LangGraph 0.2.64 compatible interface

**📖 Full troubleshooting**: See [QUICK_START.md](QUICK_START.md#-troubleshooting)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- LangChain and LangGraph teams for the amazing framework
- FastAPI for the high-performance API framework
- React and Vite teams for the modern frontend tooling

---

## 🎉 What's Ready

✅ **All Code Compatible**: Works with specified library versions, graceful degradation  
✅ **Production Server**: Gunicorn + Uvicorn multi-worker setup  
✅ **Azure Optimized**: Startup scripts for Linux and Windows App Service  
✅ **Health Monitoring**: Enhanced health checks with service status  
✅ **JSON API**: RESTful /query endpoint with Pydantic validation  
✅ **Automated Verification**: Deployment testing script included  
✅ **Complete Documentation**: 13 comprehensive guides (4 new deployment guides)  
✅ **CI/CD Ready**: GitHub Actions workflows configured  
✅ **Production Ready**: Logging, monitoring, error handling, graceful shutdown  

**Ready for**:
- ✅ Local development
- ✅ Azure Free Tier deployment  
- ✅ Production scaling

**🚀 See [DEPLOYMENT_COMPLETE.md](DEPLOYMENT_COMPLETE.md) for full transformation details**

---

## 🎯 Next Steps

**For Local Development**:
1. ✅ Follow [QUICK_START.md](QUICK_START.md)
2. → Add custom documents to `backend/data/`
3. → Customize agent nodes in `backend/nodes/`
4. → Style frontend in `frontend/src/App.css`

**For Azure Deployment**:
1. ✅ Test locally first
2. → Follow [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
3. → Run `.\deploy-to-azure.ps1`
4. → Configure GitHub secrets
5. → Monitor with Application Insights

---

## 📞 Support

- **Quick Start**: [QUICK_START.md](QUICK_START.md) - 5-minute setup
- **Dependencies**: [DEPENDENCIES_GUIDE.md](DEPENDENCIES_GUIDE.md) - Complete dependency info
- **Deployment**: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) - Azure free tier guide
- **Troubleshooting**: Check health endpoint and logs
- **Issues**: Create a GitHub issue

---

<div align="center">

**Built with ❤️ using Azure OpenAI, LangGraph, FastAPI, and React**

[Get Started](QUICK_START.md) • [Documentation](DEPENDENCIES_GUIDE.md) • [Deploy](AZURE_DEPLOYMENT.md)

🚀 **Your AI Support Agent is ready to deploy!**

</div>
