# ✨ Docify - Single Endpoint API

Your FastAPI is now simplified to ONE powerful endpoint!

## 📌 The Endpoint

**`POST /generate`** - Takes topic + related topics → Generates & writes documentation to Google Docs

## 🚀 Start Using It

### Step 1: Start the Server
```bash
python api.py
```

### Step 2: Send a Request
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "My Work Today",
    "related_topics": ["Task 1", "Task 2", "Task 3"]
  }'
```

### Step 3: Get Result
```json
{
  "success": true,
  "message": "✅ Documentation generated and written to Google Docs successfully!",
  "timestamp": "2025-12-16T10:30:00.123456",
  "doc_url": "https://docs.google.com/document/d/YOUR_DOC_ID",
  "content_preview": {
    "title": "Work Log - 2025-12-16 - My Work Today",
    "summary": "Comprehensive summary...",
    "key_achievements": ["Achievement 1", "Achievement 2"]
  }
}
```

## 🐍 Using Python

```python
from client import DocifyClient

client = DocifyClient()

# One simple call!
result = client.generate(
    topic="LangChain Implementation",
    related_topics=["Pydantic", "Structured Output", "Error Handling"]
)

print(f"✅ {result['message']}")
print(f"📄 {result['doc_url']}")
```

## 📚 See All Available Endpoints

Visit **http://localhost:8000/docs** for interactive API documentation

## 📄 Available Resources

- **USAGE.md** - Simple usage guide with examples
- **API_README.md** - Original detailed documentation (still valid for config info)
- **DEPLOYMENT.md** - Deployment configurations
- **client.py** - Simple Python client

## ✅ That's It!

Your API is ready. Just:
1. Start: `python api.py`
2. Send topic + related topics to `/generate`
3. Get documentation in Google Docs automatically

🎉 Done!
