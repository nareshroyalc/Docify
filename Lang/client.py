# Simple Python client for Docify Generator API

import requests
from typing import Optional, Dict, Any, List

class DocifyClient:
    """Client library for Docify Generator API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def generate(
        self,
        topic: str,
        related_topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate documentation and write to Google Docs
        
        Args:
            topic: Main work topic
            related_topics: List of related topics/subtopics
            
        Returns:
            Response with document URL and success status
        """
        payload = {
            "topic": topic,
            "related_topics": related_topics or []
        }
        
        response = self.session.post(
            f"{self.base_url}/generate",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if API is running"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()


# ==================== Usage Examples ====================

if __name__ == "__main__":
    client = DocifyClient()
    
    # Check if API is running
    print("🔍 Checking API health...")
    health = client.health_check()
    print(f"Status: {health['status']}")
    print(f"Agents Ready: {health['agents_ready']}\n")
    
    if not health['agents_ready']:
        print("❌ API not ready. Please start server: python api.py")
        exit(1)
    
    # Generate documentation
    print("📝 Generating documentation...")
    result = client.generate(
        topic="FastAPI Implementation",
        related_topics=[
            "REST API endpoints",
            "Async operations",
            "Error handling",
            "Google Docs integration"
        ]
    )
    
    if result['success']:
        print(f"✅ {result['message']}")
        print(f"📄 Document URL: {result['doc_url']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
        
        # Show preview
        if result.get('content_preview'):
            preview = result['content_preview']
            print(f"\n📋 Preview:")
            print(f"  Title: {preview.get('title')}")
            print(f"  Summary: {preview.get('summary')[:100]}...")
            if preview.get('key_achievements'):
                print(f"  Key Achievements:")
                for achievement in preview['key_achievements'][:3]:
                    print(f"    • {achievement}")
    else:
        print(f"❌ Error: {result['message']}")
