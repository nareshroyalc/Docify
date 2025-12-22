# Docify Generator - Simple One-Endpoint API

## 🎯 What It Does

Single endpoint that takes user input and generates documentation directly to Google Docs.

## 🚀 Quick Start

### 1. Install & Start
```bash
pip install -r requirements-api.txt
python api.py
```

### 2. Use the Endpoint

**Endpoint:** `POST http://localhost:8000/generate`

#### Using cURL
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LangChain Implementation",
    "related_topics": ["Pydantic integration", "Structured output", "Error handling"]
  }'
```

#### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "FastAPI Development",
        "related_topics": ["REST API", "Async endpoints", "Error handling"]
    }
)

result = response.json()
print(f"✅ Success: {result['success']}")
print(f"📄 Document: {result['doc_url']}")
print(f"⏰ Created: {result['timestamp']}")
```

#### Using JavaScript
```javascript
const response = await fetch('http://localhost:8000/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        topic: 'Machine Learning Model',
        related_topics: ['Training', 'Evaluation', 'Deployment']
    })
});

const result = await response.json();
console.log(`Document: ${result.doc_url}`);
```

## 📊 Request & Response

### Request
```json
{
  "topic": "Your main work topic",
  "related_topics": ["subtopic1", "subtopic2", "subtopic3"]
}
```

### Response (Success)
```json
{
  "success": true,
  "message": "✅ Documentation generated and written to Google Docs successfully!",
  "timestamp": "2025-12-16T10:30:00.123456",
  "doc_url": "https://docs.google.com/document/d/YOUR_DOC_ID",
  "content_preview": {
    "title": "Work Log - 2025-12-16 - Your Topic",
    "summary": "Generated summary...",
    "key_achievements": ["Achievement 1", "Achievement 2"]
  }
}
```

### Response (Error)
```json
{
  "success": false,
  "error": "Generation failed: API error details",
  "timestamp": "2025-12-16T10:30:00.123456"
}
```

## 📚 Interactive Documentation

Visit http://localhost:8000/docs to test the endpoint in the Swagger UI.

## 🎓 Examples

### Example 1: Daily Work Log
```python
requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "Backend API Development",
        "related_topics": [
            "FastAPI implementation",
            "Database schema",
            "Error handling"
        ]
    }
)
```

### Example 2: Project Documentation
```python
requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "LangChain Integration Project",
        "related_topics": [
            "Gemini API setup",
            "Structured output",
            "Google Docs integration",
            "Testing suite"
        ]
    }
)
```

### Example 3: Feature Implementation
```python
requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "Authentication Module",
        "related_topics": [
            "JWT implementation",
            "Password hashing",
            "Refresh tokens",
            "Role-based access"
        ]
    }
)
```

## 🔍 Other Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/generate` | POST | **Main endpoint** - Generate and write docs |
| `/health` | GET | Check if API is running |
| `/docs` | GET | Interactive Swagger UI documentation |
| `/` | GET | API welcome info |

## ⚙️ Configuration

The API uses environment variables from `.env`:
```
GEMINI_API_KEY=your-api-key
SERVICE_ACCOUNT_FILE=doc-bee-cec8fb727916.json
DOC_ID=your-google-docs-id
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Run: `pip install -r requirements-api.txt` |
| `Port 8000 already in use` | Run: `uvicorn api:app --port 8080` |
| `403 Forbidden error` | Share Google Doc with service account email |
| `GEMINI_API_KEY not found` | Create `.env` file with your API key |

## 📝 That's It!

Just send your topic and related topics, and it automatically generates and writes documentation to Google Docs. Simple! 🚀
