# FastAPI application for invoking agents and utilities
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn
from contextlib import asynccontextmanager

from config import (
    GEMINI_API_KEY, 
    MODEL_NAME, 
    SERVICE_ACCOUNT_FILE, 
    SCOPES, 
    DOC_ID,
    FULL_NAME
)
from agents.gemini_agent import ValidatedDocAgent
from agents.docs_agent import DocsAgent
from utils.page_manager import get_safe_insertion_point

# ==================== Request/Response Models ====================

class DocumentationRequest(BaseModel):
    """Request model for generating and writing documentation"""
    topic: str = Field(..., description="Main work topic to document")
    related_topics: List[str] = Field(default_factory=list, description="Related topics or subtopics")
    priority: str = Field(default="medium", description="Priority level: low, medium, or high")
    details: str = Field(default="", description="Additional details or accomplishments")
    challenges: str = Field(default="", description="Challenges encountered (optional)")

class DocumentationResponse(BaseModel):
    """Response model for documentation generation and writing"""
    success: bool = Field(..., description="Whether the operation succeeded")
    message: str = Field(..., description="Status message")
    timestamp: str = Field(..., description="When the documentation was created")
    doc_url: str = Field(..., description="URL to the generated document")
    structured: Optional[Dict[str, Any]] = Field(None, description="Complete structured documentation data")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Generation metrics for validation")
    content_preview: Optional[Dict[str, Any]] = Field(None, description="Preview of generated content")

# ==================== Global Agent Instances ====================

gemini_agent = None
docs_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup"""
    global gemini_agent, docs_agent
    
    try:
        print("🚀 Initializing agents...")
        gemini_agent = ValidatedDocAgent(GEMINI_API_KEY, FULL_NAME)
        docs_agent = DocsAgent(SERVICE_ACCOUNT_FILE, SCOPES)
        print("✅ Agents initialized successfully!")
        print(f"📧 Service Account: {docs_agent.sa_email}")
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        raise
    
    yield
    
    print("🛑 Shutting down agents...")

# ==================== FastAPI App ====================

app = FastAPI(
    title="Docify Generator",
    description="Single endpoint to generate and write documentation to Google Docs",
    version="1.0.0",
    lifespan=lifespan
)

# ==================== CORS Configuration ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:3001",      # Alternative port
        "http://127.0.0.1:3001",
        "*"                            # Allow all origins (for development)
    ],
    allow_credentials=True,
    allow_methods=["*"],              # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # Allow all headers
)

# ==================== Main Endpoint ====================

@app.post("/generate", response_model=DocumentationResponse, tags=["Documentation"])
async def generate_and_write_documentation(request: DocumentationRequest):
    """
    Generate documentation from topic and related topics, then write directly to Google Docs
    
    This is the main endpoint that:
    1. Takes user input (topic + related topics)
    2. Generates structured documentation using Gemini AI
    3. Writes the documentation to Google Docs
    4. Returns the document URL and confirmation
    
    Args:
        request: DocumentationRequest with topic and related_topics
        
    Returns:
        DocumentationResponse with document URL and success status
    """
    if not gemini_agent or not docs_agent:
        raise HTTPException(
            status_code=503,
            detail="Agents not initialized. Check server startup logs."
        )
    
    try:
        # Combine topic, details, and related topics for better documentation
        combined_details = request.details if request.details else ""
        if request.related_topics:
            if combined_details:
                combined_details += f" | Related topics: {', '.join(request.related_topics)}"
            else:
                combined_details = f"Related topics: {', '.join(request.related_topics)}"
        
        print(f"📝 Generating documentation for: {request.topic}")
        print(f"📊 Priority: {request.priority.upper()}")
        if request.related_topics:
            print(f"📌 Related topics: {', '.join(request.related_topics)}")
        if request.details:
            print(f"📋 Details: {request.details}")
        if request.challenges:
            print(f"⚠️  Challenges: {request.challenges}")
        
        # Step 1: Generate content using Gemini with priority
        from agents.gemini_agent import TaskPriority
        priority_map = {
            "low": TaskPriority.LOW,
            "medium": TaskPriority.MEDIUM,
            "high": TaskPriority.HIGH
        }
        
        doc_data = gemini_agent.generate_documentation(
            request.topic, 
            combined_details,
            challenges=request.challenges,
            priority=priority_map.get(request.priority.lower(), TaskPriority.MEDIUM)
        )
        
        print("✍️  Writing to Google Docs...")
        
        # Step 2: Write to Google Docs
        success = docs_agent.write_entry(DOC_ID, doc_data)
        
        if success:
            return DocumentationResponse(
                success=True,
                message="✅ Documentation generated and written to Google Docs successfully!",
                timestamp=doc_data.get("timestamp", datetime.now().isoformat()),
                doc_url=f"https://docs.google.com/document/d/{DOC_ID}",
                structured=doc_data.get("structured", {}),
                metrics=doc_data.get("metrics"),
                content_preview={
                    "title": doc_data.get("structured", {}).get("title"),
                    "summary": doc_data.get("structured", {}).get("summary"),
                    "key_achievements": doc_data.get("structured", {}).get("achievements", [])
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to write documentation to Google Docs. Check permissions."
            )
            
    except Exception as e:
        print(f"❌ Error generating documentation: {e}")
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")

# ==================== Info Endpoints ====================

@app.get("/", tags=["Info"])
async def root():
    """Welcome endpoint"""
    return {
        "name": "Docify Generator",
        "version": "1.0.0",
        "description": "Generate documentation with one endpoint",
        "usage": {
            "endpoint": "POST /generate",
            "example": {
                "topic": "Your work topic",
                "related_topics": ["subtopic1", "subtopic2"]
            }
        },
        "documentation": "http://localhost:8000/docs"
    }

@app.get("/health", tags=["Info"])
async def health_check():
    """Check API and agents health"""
    return {
        "status": "healthy" if gemini_agent and docs_agent else "degraded",
        "agents_ready": bool(gemini_agent and docs_agent),
        "timestamp": datetime.now().isoformat()
    }

# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions"""
    print(f"❌ Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

# ==================== Startup ====================

if __name__ == "__main__":
    print("🚀 Starting Docify Generator...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📝 Main Endpoint: POST http://localhost:8000/generate")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
