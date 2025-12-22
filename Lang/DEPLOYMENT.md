# FastAPI Configuration Examples

## 1. Production Configuration (production.py)
```python
# Production settings
import os
from api import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=4,
        reload=False,
        log_level="info",
        access_log=True
    )
```

Run: `python production.py`

## 2. Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements-api.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-api.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  docify-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SERVICE_ACCOUNT_FILE=doc-bee-cec8fb727916.json
      - DOC_ID=${DOC_ID}
    volumes:
      - ./doc-bee-cec8fb727916.json:/app/doc-bee-cec8fb727916.json:ro
    restart: unless-stopped
```

Build & Run:
```bash
docker build -t docify-api .
docker run -p 8000:8000 --env-file .env docify-api
```

## 3. Environment Variables (.env)
```
# Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Google Docs
SERVICE_ACCOUNT_FILE=doc-bee-cec8fb727916.json
DOC_ID=your-default-google-docs-id

# API
PORT=8000
LOG_LEVEL=info
```

## 4. Nginx Reverse Proxy Configuration

```nginx
server {
    listen 80;
    server_name docify.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 5. Systemd Service (Linux)

### /etc/systemd/system/docify-api.service
```ini
[Unit]
Description=Docify API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/docify
Environment="PATH=/opt/docify/venv/bin"
ExecStart=/opt/docify/venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable & Start:
```bash
sudo systemctl enable docify-api
sudo systemctl start docify-api
sudo systemctl status docify-api
```

## 6. Rate Limiting & Middleware

Add to api.py:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# Apply to endpoints
@app.post("/api/v1/generate")
@limiter.limit("10/minute")
async def generate_documentation(request: DocumentationRequest):
    ...
```

## 7. CORS Configuration

Add to api.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 8. Gunicorn + Uvicorn Workers

```bash
pip install gunicorn

gunicorn api:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

## 9. AWS Lambda Deployment

```python
# lambda_handler.py
from fastapi import FastAPI
from mangum import Mangum
from api import app

handler = Mangum(app)
```

Deploy with SAM CLI or AWS CLI

## 10. Monitoring & Logging

Add to api.py:
```python
import logging
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

## 11. OpenTelemetry Instrumentation

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
```

## 12. CI/CD with GitHub Actions

```yaml
name: Deploy Docify API

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt -r requirements-api.txt
      - run: pytest tests/
      - run: docker build -t docify-api .
      - run: docker push myregistry/docify-api:latest
```
