# Azure Native Components - Implementation Guide

## ✅ Implemented Azure Integrations

### 1. Application Insights (Monitoring & Logging)

**Status**: ✅ Fully Integrated

**What it does**:
- Centralized logging and monitoring
- Performance metrics tracking
- Error and exception tracking
- Custom events and metrics
- Query performance analysis

**Configuration**:
```env
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx...
USE_APPLICATION_INSIGHTS=true
```

**Benefits**:
- ✅ FREE: 5GB data ingestion per month
- ✅ Real-time monitoring in Azure Portal
- ✅ Automatic error tracking
- ✅ Performance bottleneck detection
- ✅ Custom dashboards

**Usage**:
```python
# Automatically tracks:
- All HTTP requests and responses
- Errors and exceptions
- Custom events (agent_initialized, query_received, etc.)
- Metrics (query_success, query_error, health_check)
```

**View Logs**: Azure Portal > Application Insights > Logs/Live Metrics

---

### 2. Azure Table Storage (Session Persistence)

**Status**: ✅ Fully Integrated

**What it does**:
- Persistent storage for LangGraph checkpoints
- Session state survives app restarts
- Shared sessions across multiple instances
- Fast key-value lookups

**Configuration**:
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_TABLE_NAME=checkpoints
USE_AZURE_TABLE_STORAGE=true
```

**Benefits**:
- ✅ FREE: 20,000 operations included
- ✅ No data loss on restart
- ✅ Automatic scaling
- ✅ Multi-instance support
- ✅ NoSQL flexibility

**How it works**:
```python
# Replaces in-memory MemorySaver
from utils.azure_checkpointer import AzureTableCheckpointer

# Automatically:
- Saves conversation state per thread_id
- Restores sessions on app restart
- Enables conversation history
```

**Fallback**: If Azure Table Storage is not configured, automatically falls back to in-memory MemorySaver.

---

### 3. Azure Blob Storage (ChromaDB Persistence)

**Status**: ✅ Fully Integrated

**What it does**:
- Backup ChromaDB vector store to cloud
- Restore ChromaDB on app startup
- Share knowledge base across instances
- Version control for embeddings

**Configuration**:
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_BLOB_CONTAINER_NAME=chromadb
USE_AZURE_BLOB_STORAGE=true
```

**Benefits**:
- ✅ FREE: 5GB storage included
- ✅ Persistent knowledge base
- ✅ Automatic backup/restore
- ✅ Multiple backup versions
- ✅ Disaster recovery

**How it works**:
```python
from utils.azure_blob_sync import get_blob_sync

# On startup:
blob_sync = get_blob_sync()
blob_sync.download_chromadb()  # Restore from cloud

# Optional: Periodic backup
blob_sync.upload_chromadb()  # Backup to cloud
```

**Manual Operations**:
```python
# List available backups
backups = blob_sync.list_backups()

# Restore specific backup
blob_sync.download_chromadb(backup_name="backup-2025-11-10")

# Delete old backup
blob_sync.delete_backup("old-backup")
```

---

## 🎯 Benefits of Azure Native Integration

### Operational Benefits

| Feature | Before | After | Impact |
|---------|--------|-------|--------|
| Session Persistence | In-memory (lost on restart) | Azure Table Storage | 🟢 Permanent |
| Log Retention | 24 hours | 90 days | 🟢 75x longer |
| Vector Store | Local only | Cloud backup | 🟢 Disaster recovery |
| Error Tracking | Manual log review | Automatic alerts | 🟢 Proactive |
| Performance | No insights | Full metrics | 🟢 Optimizable |
| Multi-Instance | Not supported | Shared state | 🟢 Scalable |

### Cost Analysis

| Service | Free Tier | Usage | Monthly Cost |
|---------|-----------|-------|--------------|
| Application Insights | 5GB data | ~100MB | **$0** |
| Table Storage | 20K ops | ~5K ops | **$0** |
| Blob Storage | 5GB | ~500MB | **$0** |
| **Total** | | | **$0** |

**Only pay for**: Azure OpenAI token usage (~$5-20/month)

---

## 📊 Monitoring Dashboard

### Key Metrics Tracked

1. **Agent Performance**
   - `agent_initialized`: Agent startup success/failure
   - `query_received`: Total queries received
   - `query_success`: Successful responses
   - `query_error`: Failed queries
   - `health_check`: Health check pings

2. **Application Health**
   - HTTP request duration
   - Error rates
   - Exception details
   - Dependency calls (Azure OpenAI)

3. **Custom Events**
   - Agent initialization
   - Query processing
   - Session restoration
   - ChromaDB backup/restore

### Viewing Metrics

**Azure Portal**:
```
Application Insights > Logs > Run Query:

// Query success rate (last 24 hours)
customMetrics
| where name == "query_success" or name == "query_error"
| summarize count() by name
| render piechart

// Average query processing time
requests
| where url contains "support-agent"
| summarize avg(duration) by bin(timestamp, 1h)
| render timechart

// Recent errors
exceptions
| where timestamp > ago(24h)
| project timestamp, type, outerMessage
| order by timestamp desc
```

---

## 🔧 Configuration Guide

### Local Development

```env
# .env file for local development
USE_AZURE_TABLE_STORAGE=false
USE_AZURE_BLOB_STORAGE=false
USE_APPLICATION_INSIGHTS=false
```

**Recommendation**: Use in-memory storage locally for faster development.

### Production Deployment

```env
# .env file for production
USE_AZURE_TABLE_STORAGE=true
USE_AZURE_BLOB_STORAGE=true
USE_APPLICATION_INSIGHTS=true
AZURE_STORAGE_CONNECTION_STRING=...
APPLICATIONINSIGHTS_CONNECTION_STRING=...
```

**Recommendation**: Enable all Azure services in production.

---

## 🚀 Getting Started

### Step 1: Create Azure Storage Account

```powershell
# Create storage account
az storage account create `
    --name stsupportagent `
    --resource-group rg-support-agent `
    --location eastus `
    --sku Standard_LRS

# Get connection string
az storage account show-connection-string `
    --name stsupportagent `
    --resource-group rg-support-agent `
    --output tsv
```

### Step 2: Configure Environment Variables

Copy connection string to `.env`:
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
USE_AZURE_TABLE_STORAGE=true
USE_AZURE_BLOB_STORAGE=true
```

### Step 3: Test Integration

```powershell
# Start backend
cd backend
python app.py

# Check health endpoint (should show Azure services enabled)
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent_initialized": true,
  "azure_table_storage": "true",
  "azure_blob_storage": "true",
  "application_insights": true
}
```

---

## 🔍 Troubleshooting

### Issue: Table Storage Not Working

**Symptoms**: Sessions lost after restart

**Check**:
1. Verify connection string is correct
2. Check `USE_AZURE_TABLE_STORAGE=true`
3. Look for errors in logs

**Fix**:
```powershell
# Test connection
az storage account show --name stsupportagent --resource-group rg-support-agent

# Regenerate key if needed
az storage account keys renew --name stsupportagent --resource-group rg-support-agent --key primary
```

### Issue: Blob Storage Upload Fails

**Symptoms**: ChromaDB not backing up

**Check**:
1. Verify container exists
2. Check storage account permissions
3. Verify connection string

**Fix**:
```powershell
# Create container manually
az storage container create --name chromadb --account-name stsupportagent

# List containers
az storage container list --account-name stsupportagent
```

### Issue: Application Insights Not Receiving Data

**Symptoms**: No logs in Azure Portal

**Check**:
1. Verify connection string format
2. Check `USE_APPLICATION_INSIGHTS=true`
3. Wait 2-5 minutes for data ingestion

**Fix**:
```powershell
# Get correct connection string
az monitor app-insights component show `
    --app ai-support-agent `
    --resource-group rg-support-agent `
    --query connectionString
```

---

## 📈 Performance Optimization

### Reduce Application Insights Costs

```python
# In production, log at INFO level only
logging.basicConfig(level=logging.INFO)  # Not DEBUG

# Sample telemetry (track 10% of requests)
# Add to app.py:
import random
if random.random() < 0.1:  # 10% sampling
    telemetry_client.track_event(...)
```

### Optimize Table Storage Operations

```python
# Batch operations when possible
# Cache frequently accessed sessions in memory
# Set expiration policy for old sessions (manual cleanup)
```

### Minimize Blob Storage Usage

```python
# Backup on schedule, not every query
# Use delta backups (only changed files)
# Cleanup old backups regularly
```

---

## 🎓 Best Practices

### 1. **Gradual Rollout**
- Start with Application Insights only
- Add Table Storage when confident
- Enable Blob Storage last

### 2. **Monitor Free Tier Limits**
- Set up Azure Cost Alerts
- Monitor operation counts
- Review usage monthly

### 3. **Fallback Strategy**
- Code gracefully handles missing Azure services
- Falls back to in-memory when needed
- Logs warnings, not errors

### 4. **Security**
- Never commit connection strings
- Use Azure Key Vault in production
- Rotate keys regularly

### 5. **Testing**
- Test with Azure services enabled
- Test failover scenarios
- Validate backup/restore

---

## 📚 Additional Resources

- [Azure Table Storage Documentation](https://docs.microsoft.com/azure/storage/tables/)
- [Azure Blob Storage Documentation](https://docs.microsoft.com/azure/storage/blobs/)
- [Application Insights Documentation](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [LangGraph Checkpointers](https://langchain-ai.github.io/langgraph/concepts/persistence/)

---

## ✅ Integration Checklist

- [x] Application Insights integrated
- [x] Azure Table Storage checkpointer implemented
- [x] Azure Blob Storage sync implemented
- [x] Configuration variables added
- [x] Fallback mechanisms in place
- [x] Error handling implemented
- [x] Logging enhanced
- [x] Health check updated
- [x] Documentation complete

**Status**: ✅ Ready for production deployment!
