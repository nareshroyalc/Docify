# Docify API Documentation

## Overview
Fast API server for generating and managing AI-powered documentation with Google Docs integration.

## Features
- ✅ AI-powered documentation generation using LangChain + Gemini
- 📝 Automatic writing to Google Docs
- 🔍 Document utilities (insertion points, document info)
- 🏥 Health checks and agent status monitoring
- 📚 Interactive API documentation (Swagger UI)

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-api.txt
```

Or install FastAPI directly:
```bash
pip install fastapi uvicorn[standard] pydantic
```

## Running the API

### Development Mode (with auto-reload)
```bash
python api.py
```

### Production Mode
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Custom Port
```bash
uvicorn api:app --host 0.0.0.0 --port 8080
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Endpoints

### Health & Status
```
GET /health
- Check API and agents health status

GET /
- Welcome endpoint with available endpoints

GET /api/v1/status
- Detailed status of all agents
```

### Documentation Generation
```
POST /api/v1/generate
- Generate documentation and write to Google Docs
- Request: { "topic": "string", "details": "string", "doc_id": "string (optional)" }
- Response: Generated documentation with success status

POST /api/v1/generate-only
- Generate documentation preview WITHOUT writing to Docs
- Request: { "topic": "string", "details": "string" }
- Response: Generated structured content
```

### Google Docs Utilities
```
GET /api/v1/get-insertion-point?doc_id=optional
- Get safe insertion point for adding content to a document
- Returns: { "safe_index": int, "doc_length": int }

GET /api/v1/doc-info?doc_id=optional
- Get document metadata (title, length, timestamps, etc.)
- Returns: Document information object
```

## Usage Examples

### 1. Generate and Write Documentation
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "LangChain Integration",
    "details": "Implemented structured output generation using Pydantic models"
  }'
```

### 2. Generate Preview Only
```bash
curl -X POST "http://localhost:8000/api/v1/generate-only" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "API Development",
    "details": "Created FastAPI wrapper for agents"
  }'
```

### 3. Get Insertion Point
```bash
curl -X GET "http://localhost:8000/api/v1/get-insertion-point"
```

### 4. Get Document Info
```bash
curl -X GET "http://localhost:8000/api/v1/doc-info"
```

### 5. Check Health
```bash
curl -X GET "http://localhost:8000/health"
```

## Python Client Example

```python
import requests

API_URL = "http://localhost:8000"

# Generate documentation
response = requests.post(
    f"{API_URL}/api/v1/generate",
    json={
        "topic": "FastAPI Implementation",
        "details": "Built async API wrapper for ML agents",
        "doc_id": "your-doc-id-here"  # optional
    }
)

result = response.json()
print(f"Success: {result['success']}")
print(f"Doc URL: {result['doc_url']}")
print(f"Generated: {result['timestamp']}")
```

## Environment Variables

Create a `.env` file in the Lang directory:
```
GEMINI_API_KEY=your-api-key
SERVICE_ACCOUNT_FILE=your-service-account.json
DOC_ID=your-google-docs-id
```

## Architecture

### Components
- **Gemini Agent** (`agents/gemini_agent.py`): LangChain-based AI documentation generator
- **Docs Agent** (`agents/docs_agent.py`): Google Docs API wrapper
- **Page Manager** (`utils/page_manager.py`): Document structure utilities
- **FastAPI** (`api.py`): REST API server

### Request Flow
```
Client Request
    ↓
FastAPI Endpoint
    ↓
Gemini Agent (Generate Content)
    ↓
Docs Agent (Write to Google Docs)
    ↓
Response with Status & URL
```

## Error Handling

All endpoints include proper error handling:
- **503**: Agents not initialized (check startup logs)
- **500**: Generation or write failures
- **4xx**: Invalid requests

Example error response:
```json
{
  "success": false,
  "error": "Generation failed: API key invalid",
  "timestamp": "2025-12-16T10:30:00"
}
```

## Performance Notes

- Initial startup takes 5-10 seconds to initialize agents
- Documentation generation typically takes 10-30 seconds depending on complexity
- Google Docs write operations are optimized with batch requests
- Async endpoints ensure non-blocking operation

## Troubleshooting

### Agent Initialization Fails
1. Check `.env` file has valid credentials
2. Verify service account JSON file exists
3. Check Google Docs API is enabled in GCP project
4. Ensure service account has access to target documents

### Write to Docs Fails
1. Verify service account email has document sharing permissions
2. Check document ID is correct
3. Ensure document is accessible and not read-only

### API Not Responding
1. Check if port 8000 is available
2. Review console output for startup errors
3. Verify all dependencies are installed: `pip install -r requirements.txt`

## Contributing

To add new endpoints:
1. Define request/response Pydantic models
2. Create endpoint function with proper decorators
3. Add tags for organization in Swagger UI
4. Document with docstrings

## License

Same as parent project

## Support

For issues or questions, check the interactive Swagger documentation at `/docs`
