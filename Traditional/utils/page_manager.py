# Page break & positioning logic
from typing import Dict, Any, List

def get_next_page_start(doc: Dict) -> int:
    """Find start of next available page"""
    body_content = doc.get("body", {}).get("content", [])
    if not body_content:
        return 1
    
    # Find last page break or end
    last_index = body_content[-1].get("endIndex", 1)
    return last_index

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

def create_page_break(index: int) -> Dict:
    """Create a page break at the specified index"""
    return {
        "insertPageBreak": {
            "location": {"index": index}
        }
    }

def create_section_break(index: int) -> List[Dict]:
    """Create a section break with spacing"""
    return [
        {
            "insertText": {
                "location": {"index": index},
                "text": "\n\n"
            }
        },
        {
            "insertPageBreak": {
                "location": {"index": index + 2}
            }
        }
    ]

def calculate_content_length(content: str) -> int:
    """Calculate the length of content for index calculations"""
    return len(content)

def adjust_index_for_insertion(base_index: int, inserted_length: int) -> int:
    """Adjust index after a previous insertion"""
    return base_index + inserted_length
