# Docify FastAPI - Quick Integration Guide

## 🚀 Getting Started (5 Minutes)

### Step 1: Install Dependencies
```bash
cd d:\docify\Lang
pip install -r requirements-api.txt
```

### Step 2: Start the API
```bash
python api.py
```

You should see:
```
🚀 Starting Docify API Server...
📚 API Documentation: http://localhost:8000/docs
🔄 Interactive API: http://localhost:8000/redoc
```

### Step 3: Test the API
Open your browser to: **http://localhost:8000/docs**

You'll see the interactive Swagger UI with all endpoints.

---

## 📡 API Overview

### Main Endpoints

#### 1️⃣ Generate Documentation
```bash
POST /api/v1/generate
Content-Type: application/json

{
  "topic": "Your work topic",
  "details": "Additional details"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Documentation generated and written successfully!",
  "doc_url": "https://docs.google.com/document/d/...",
  "timestamp": "2025-12-16T10:30:00"
}
```

#### 2️⃣ Generate Preview (No Google Docs Write)
```bash
POST /api/v1/generate-only

{
  "topic": "Your work topic",
  "details": "Additional details"
}
```

Returns generated content without writing to Google Docs.

#### 3️⃣ Health Check
```bash
GET /health
```

Checks if API and agents are working.

#### 4️⃣ Get Agent Status
```bash
GET /api/v1/status
```

Shows detailed information about all agents.

#### 5️⃣ Document Utilities
```bash
GET /api/v1/get-insertion-point
GET /api/v1/doc-info
```

Utility endpoints for working with Google Docs.

---

## 💻 Usage Examples

### Example 1: Using cURL
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "FastAPI Implementation",
    "details": "Built REST API wrapper for agents"
  }'
```

### Example 2: Using Python Requests
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "topic": "My Work Topic",
        "details": "What I accomplished today"
    }
)

result = response.json()
if result['success']:
    print(f"✅ Document created: {result['doc_url']}")
    print(f"⏰ Created at: {result['timestamp']}")
else:
    print(f"❌ Error: {result['message']}")
```

### Example 3: Using the Provided Client
```python
from client import DocifyClient

client = DocifyClient()

# Generate documentation
result = client.generate_documentation(
    topic="Machine Learning Model Training",
    details="Trained YOLO model with custom dataset"
)

print(f"Success: {result['success']}")
print(f"Document: {result['doc_url']}")
```

### Example 4: Check API Status
```python
from client import DocifyClient

client = DocifyClient()

# Check health
health = client.health_check()
print(f"API Status: {health['status']}")
print(f"Agents Ready: {health['agents_ready']}")

# Get full status
status = client.get_status()
print(f"Gemini Agent: {status['gemini_agent']['status']}")
print(f"Docs Agent: {status['docs_agent']['status']}")
```

---

## 🔄 Workflow

### Complete Documentation Flow

```
1. Client sends request to /api/v1/generate
   ↓
2. FastAPI validates request
   ↓
3. Gemini Agent generates structured documentation
   ↓
4. Docs Agent writes to Google Docs
   ↓
5. API returns success response with document URL
   ↓
6. Document appears in Google Docs
```

### Preview-Only Flow

```
1. Client sends request to /api/v1/generate-only
   ↓
2. FastAPI validates request
   ↓
3. Gemini Agent generates documentation
   ↓
4. API returns generated content (no Docs write)
   ↓
5. Client receives JSON response
```

---

## 🎯 Common Scenarios

### Scenario 1: Daily Documentation
```python
from client import DocifyClient
import json

client = DocifyClient()

# Log today's work
work_log = {
    "topic": "Data Pipeline Development",
    "details": """
    - Fixed data loading issues
    - Optimized preprocessing pipeline
    - Added error handling
    """
}

result = client.generate_documentation(**work_log)
if result['success']:
    print("✅ Daily documentation complete!")
```

### Scenario 2: Project Documentation
```python
# Generate documentation for entire project
result = client.generate_documentation(
    topic="LangChain Integration Project",
    details="Complete implementation of structured output generation"
)

print(f"Project documented: {result['doc_url']}")
```

### Scenario 3: Review Generated Content
```python
# Generate without writing to Docs first
preview = client.generate_preview(
    topic="New Feature",
    details="Implementation details"
)

# Review the generated content
content = preview['data']
print(f"Title: {content['title']}")
print(f"Summary: {content['summary']}")
print(f"Achievements: {content['key_achievements']}")

# If satisfied, write to Docs
if input("Approve? (y/n): ").lower() == 'y':
    result = client.generate_documentation(
        topic="New Feature",
        details="Implementation details"
    )
```

---

## 🔐 Configuration

### Environment Variables (.env)
```
GEMINI_API_KEY=your-gemini-api-key
SERVICE_ACCOUNT_FILE=doc-bee-cec8fb727916.json
DOC_ID=your-google-docs-id
```

### Custom Configuration
```python
# In your code
client = DocifyClient(base_url="http://localhost:8080")

# Or specify custom doc ID
result = client.generate_documentation(
    topic="Work",
    details="Details",
    doc_id="custom-document-id"
)
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: fastapi` | Run `pip install -r requirements-api.txt` |
| `Port 8000 already in use` | Change port: `uvicorn api:app --port 8080` |
| `Agents not initialized` | Check logs during startup for errors |
| `403 Forbidden writing to Docs` | Share Google Doc with service account email |
| `GEMINI_API_KEY not found` | Create `.env` file with API key |

---

## 📊 Response Status Codes

| Code | Meaning | When It Happens |
|------|---------|-----------------|
| 200 | ✅ Success | Documentation generated |
| 400 | ❌ Bad Request | Missing or invalid fields |
| 422 | ❌ Validation Error | Invalid request format |
| 500 | ❌ Server Error | API processing failed |
| 503 | ❌ Service Unavailable | Agents not initialized |

---

## 🎓 Learning Resources

### API Documentation (Interactive)
```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
http://localhost:8000/openapi.json  # OpenAPI spec
```

### Code References
- [api.py](api.py) - Main FastAPI application
- [client.py](client.py) - Python client library
- [agents/gemini_agent.py](agents/gemini_agent.py) - AI generation
- [agents/docs_agent.py](agents/docs_agent.py) - Google Docs integration
- [utils/page_manager.py](utils/page_manager.py) - Document utilities

---

## 📝 Next Steps

1. ✅ Start the API: `python api.py`
2. ✅ Visit: http://localhost:8000/docs
3. ✅ Try an endpoint in Swagger UI
4. ✅ Use the Python client for automation
5. ✅ Integrate into your workflow

---

## 💬 Support

For detailed information:
- See [API_README.md](API_README.md) for comprehensive documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- See [FASTAPI_SUMMARY.md](FASTAPI_SUMMARY.md) for complete overview

For examples:
- Interactive Swagger UI at http://localhost:8000/docs
- Python examples in [client.py](client.py)
- Test examples in [test_api.py](test_api.py)

---

## ✨ You're Ready!

Your Docify FastAPI is fully set up. Start generating documentation! 🚀
