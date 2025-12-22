# Test suite for Docify API

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import the app - will need to modify for testing
from api import app

client = TestClient(app)

# ==================== Health & Status Tests ====================

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "agents_ready" in data
    assert "timestamp" in data

def test_root_endpoint():
    """Test welcome endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "Docify API"
    assert "endpoints" in data

def test_agent_status():
    """Test agent status endpoint"""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert "gemini_agent" in data
    assert "docs_agent" in data
    assert "timestamp" in data

# ==================== Documentation Generation Tests ====================

@patch('api.gemini_agent')
def test_generate_documentation(mock_gemini):
    """Test documentation generation endpoint"""
    # Mock the agent response
    mock_gemini.generate_work_documentation.return_value = {
        "structured": {
            "title": "Test Documentation",
            "summary": "Test summary",
            "task_description": "Test task",
            "key_achievements": ["Achievement 1"],
            "technical_implementation": {},
            "challenges_faced": [],
            "metrics_and_results": {"headers": [], "rows": []},
            "next_steps": [],
            "tags": []
        },
        "timestamp": datetime.now().isoformat()
    }
    
    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "Test Topic",
            "details": "Test Details"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "timestamp" in data
    assert "data" in data

@patch('api.gemini_agent')
def test_generate_only(mock_gemini):
    """Test documentation generation preview"""
    mock_gemini.generate_work_documentation.return_value = {
        "structured": {"title": "Test"},
        "timestamp": datetime.now().isoformat()
    }
    
    response = client.post(
        "/api/v1/generate-only",
        json={
            "topic": "Test Topic",
            "details": "Test Details"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

# ==================== Documentation Utilities Tests ====================

@patch('api.docs_agent')
def test_get_insertion_point(mock_docs):
    """Test getting safe insertion point"""
    mock_service = MagicMock()
    mock_docs.service = mock_service
    
    # Mock document
    mock_docs.service.documents().get().execute.return_value = {
        "body": {
            "content": [
                {"startIndex": 1},
                {"startIndex": 100, "endIndex": 200}
            ]
        }
    }
    
    response = client.get("/api/v1/get-insertion-point")
    assert response.status_code == 200
    data = response.json()
    assert "safe_index" in data
    assert "doc_length" in data
    assert isinstance(data["safe_index"], int)

@patch('api.docs_agent')
def test_get_document_info(mock_docs):
    """Test getting document metadata"""
    mock_service = MagicMock()
    mock_docs.service = mock_service
    
    mock_docs.service.documents().get().execute.return_value = {
        "title": "Test Document",
        "body": {
            "content": [
                {"startIndex": 1, "endIndex": 100}
            ]
        },
        "mimeType": "application/vnd.google-apps.document",
        "createdTime": "2025-12-01T00:00:00Z",
        "modifiedTime": "2025-12-16T00:00:00Z"
    }
    
    response = client.get("/api/v1/doc-info")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Document"
    assert "length" in data
    assert data["success"] == True

# ==================== Error Handling Tests ====================

def test_missing_required_field():
    """Test validation of required fields"""
    response = client.post(
        "/api/v1/generate",
        json={"details": "Missing topic"}
    )
    assert response.status_code == 422  # Validation error

def test_invalid_doc_id_format():
    """Test handling of invalid document ID"""
    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "Test",
            "details": "",
            "doc_id": ""  # Empty doc ID
        }
    )
    # Should still work with default doc ID or handle gracefully
    assert response.status_code in [200, 400, 500]

@patch('api.gemini_agent', None)
def test_agent_not_initialized():
    """Test error handling when agent not initialized"""
    response = client.post(
        "/api/v1/generate",
        json={"topic": "Test", "details": ""}
    )
    assert response.status_code == 503

# ==================== Request/Response Model Tests ====================

def test_documentation_request_validation():
    """Test DocumentationRequest validation"""
    from api import DocumentationRequest
    
    # Valid request
    req = DocumentationRequest(
        topic="Test Topic",
        details="Test Details"
    )
    assert req.topic == "Test Topic"
    assert req.details == "Test Details"
    
    # Test with optional fields
    req2 = DocumentationRequest(topic="Test")
    assert req2.details == ""

def test_documentation_response_model():
    """Test DocumentationResponse model"""
    from api import DocumentationResponse
    
    resp = DocumentationResponse(
        success=True,
        message="Test message",
        timestamp="2025-12-16T00:00:00",
        doc_url="https://docs.google.com/document/d/test"
    )
    assert resp.success == True
    assert "Test message" in resp.message

# ==================== Integration Tests ====================

@patch('api.gemini_agent')
@patch('api.docs_agent')
def test_end_to_end_documentation_generation(mock_docs, mock_gemini):
    """Test complete documentation generation flow"""
    # Setup mocks
    mock_gemini.generate_work_documentation.return_value = {
        "structured": {
            "title": "End-to-End Test",
            "summary": "Test summary"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    mock_docs.write_daily_entry.return_value = True
    
    response = client.post(
        "/api/v1/generate",
        json={
            "topic": "Integration Test",
            "details": "Testing full flow"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    mock_gemini.generate_work_documentation.assert_called_once()
    mock_docs.write_daily_entry.assert_called_once()

# ==================== Performance Tests ====================

def test_concurrent_requests():
    """Test handling of concurrent requests"""
    import concurrent.futures
    
    def make_request():
        return client.get("/health")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    assert all(r.status_code == 200 for r in results)
    assert len(results) == 10

# ==================== Test Fixtures ====================

@pytest.fixture
def sample_documentation():
    """Fixture providing sample documentation"""
    return {
        "topic": "Sample Work Topic",
        "details": "Sample additional details",
        "timestamp": datetime.now().isoformat()
    }

@pytest.fixture
def sample_doc_id():
    """Fixture providing a sample document ID"""
    return "1dQ50-UzJASiJUDcmymfpP3hoiiZptaP-SolMaIBPhMY"

# ==================== Run Tests ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
