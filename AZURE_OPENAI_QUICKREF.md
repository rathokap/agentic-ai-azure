# 🔑 Azure OpenAI Quick Reference Card

## 🎯 What You Need

```
✅ AZURE_OPENAI_API_KEY         → Your secret API key
✅ AZURE_OPENAI_ENDPOINT        → Your resource URL
✅ AZURE_DEPLOYMENT_NAME        → Your model deployment name
✅ AZURE_API_VERSION            → API version (use 2024-02-15-preview)
```

---

## ⚡ Quick Setup (3 Steps)

### 1️⃣ Create Azure OpenAI Resource (2 min)

```powershell
az login

az cognitiveservices account create `
    --name "openai-support-$(Get-Random)" `
    --resource-group "rg-openai" `
    --location "eastus" `
    --kind OpenAI `
    --sku S0
```

### 2️⃣ Deploy GPT Model (1 min)

```powershell
# Via CLI
az cognitiveservices account deployment create `
    --name "openai-support-1234" `
    --resource-group "rg-openai" `
    --deployment-name "gpt-4-deployment" `
    --model-name "gpt-4"

# Or use: https://oai.azure.com → Deployments → Create
```

### 3️⃣ Get Credentials (30 sec)

```powershell
# Get Endpoint
az cognitiveservices account show `
    --name "openai-support-1234" `
    --resource-group "rg-openai" `
    --query "properties.endpoint" -o tsv

# Get API Key
az cognitiveservices account keys list `
    --name "openai-support-1234" `
    --resource-group "rg-openai" `
    --query "key1" -o tsv
```

---

## 📍 Where to Find in Azure Portal

### API Key & Endpoint
```
Azure Portal 
→ Your Azure OpenAI Resource
→ Keys and Endpoint (left sidebar)
→ Copy KEY 1 and Endpoint
```

### Deployment Name
```
Azure OpenAI Studio (oai.azure.com)
→ Deployments
→ Your deployment name (e.g., "gpt-4-deployment")
```

---

## 📝 Example .env Configuration

```bash
# Copy these EXACT formats (replace values with yours)

AZURE_OPENAI_API_KEY=4a5b6c7d8e9f0g1h2i3j4k5l6m7n8o9p
AZURE_OPENAI_ENDPOINT=https://openai-support-1234.openai.azure.com/
AZURE_DEPLOYMENT_NAME=gpt-4-deployment
AZURE_API_VERSION=2024-02-15-preview
```

---

## ✅ Verification Test

```powershell
# Quick test script
@"
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2024-02-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

response = client.chat.completions.create(
    model=os.getenv('AZURE_DEPLOYMENT_NAME'),
    messages=[{'role': 'user', 'content': 'Hello!'}]
)

print('✅ Success!', response.choices[0].message.content)
"@ | python
```

---

## 🚨 Common Mistakes

| Error | Wrong | Correct |
|-------|-------|---------|
| **Missing slash** | `https://xxx.openai.azure.com` | `https://xxx.openai.azure.com/` ✅ |
| **Wrong deployment** | `gpt-4` (model name) | `gpt-4-deployment` (your deployment name) ✅ |
| **Old API version** | `2023-05-15` | `2024-02-15-preview` ✅ |
| **Missing protocol** | `openai-xxx.openai.azure.com` | `https://openai-xxx.openai.azure.com/` ✅ |

---

## 💰 Cost Estimates

| Model | Cost per 1K tokens | 100 queries/day |
|-------|-------------------|-----------------|
| GPT-3.5 Turbo | $0.002 | ~$5-10/month |
| GPT-4 | $0.03-0.06 | ~$20-40/month |
| GPT-4 Turbo | $0.01-0.03 | ~$10-20/month |

---

## 📞 Need Help?

- **Full Guide**: [AZURE_OPENAI_SETUP.md](AZURE_OPENAI_SETUP.md)
- **Request Access**: [https://aka.ms/oai/access](https://aka.ms/oai/access)
- **Azure Portal**: [https://portal.azure.com](https://portal.azure.com)
- **OpenAI Studio**: [https://oai.azure.com](https://oai.azure.com)

---

## 🎯 Checklist

- [ ] Azure account created
- [ ] Azure OpenAI access approved
- [ ] Resource created
- [ ] Model deployed
- [ ] API key copied
- [ ] Endpoint URL copied
- [ ] Deployment name noted
- [ ] `.env` file configured
- [ ] Connection tested ✅

**🎉 Ready to use Azure OpenAI!**
