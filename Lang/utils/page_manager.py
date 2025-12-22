# Page break & positioning logic
from typing import Dict, Any, List

def get_safe_insertion_point(doc: Dict) -> int:
    """Get safe insertion point that avoids document structure errors"""
    body = doc.get("body", {}).get("content", [])
    
    # Empty document
    if len(body) < 2:
        return 1
    
    # Find last paragraph and insert at its start
    for element in reversed(body):
        if element.get("paragraph"):
            return element.get("startIndex", 1)
    
    # Fallback: document body end - 1
    end_index = body[-1].get("endIndex", 1)
    return max(1, end_index - 1)
