# Text/table formatting for Docs API
from typing import List, Dict, Any

def create_heading_style(text: str, heading_level: int, index: int) -> List[Dict]:
    """Create a styled heading with proper formatting"""
    return [
        {
            "insertText": {
                "location": {"index": index},
                "text": text + "\n"
            }
        },
        {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": index,
                    "endIndex": index + len(text) + 1
                },
                "paragraphStyle": {
                    "namedStyleType": f"HEADING_{heading_level}",
                    "spaceAbove": {"magnitude": 12, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"}
                },
                "fields": "namedStyleType,spaceAbove,spaceBelow"
            }
        }
    ]

def create_styled_text(text: str, index: int, bold: bool = False, 
                       italic: bool = False, color: Dict = None) -> List[Dict]:
    """Create styled text with formatting options"""
    requests = [
        {
            "insertText": {
                "location": {"index": index},
                "text": text
            }
        }
    ]
    
    text_style = {}
    if bold:
        text_style["bold"] = True
    if italic:
        text_style["italic"] = True
    if color:
        text_style["foregroundColor"] = {"color": {"rgbColor": color}}
    
    if text_style:
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": index,
                    "endIndex": index + len(text)
                },
                "textStyle": text_style,
                "fields": ",".join(text_style.keys())
            }
        })
    
    return requests

def create_bullet_list(items: List[str], index: int, bullet_preset: str = "BULLET_DISC_CIRCLE_SQUARE") -> List[Dict]:
    """Create a formatted bullet list"""
    requests = []
    current_index = index
    
    for item in items:
        # Insert text
        requests.append({
            "insertText": {
                "location": {"index": current_index},
                "text": item + "\n"
            }
        })
        
        # Apply bullet formatting
        requests.append({
            "createParagraphBullets": {
                "range": {
                    "startIndex": current_index,
                    "endIndex": current_index + len(item) + 1
                },
                "bulletPreset": bullet_preset
            }
        })
        
        current_index += len(item) + 1
    
    return requests

def create_table(headers: List[str], rows: List[List[str]], index: int) -> List[Dict]:
    """Create a formatted table in Google Docs"""
    num_rows = len(rows) + 1  # +1 for header
    num_cols = len(headers)
    
    requests = [
        {
            "insertTable": {
                "rows": num_rows,
                "columns": num_cols,
                "location": {"index": index}
            }
        }
    ]
    
    return requests

def create_divider(index: int) -> List[Dict]:
    """Create a visual divider line"""
    return [
        {
            "insertText": {
                "location": {"index": index},
                "text": "―" * 50 + "\n\n"
            }
        },
        {
            "updateTextStyle": {
                "range": {
                    "startIndex": index,
                    "endIndex": index + 51
                },
                "textStyle": {
                    "foregroundColor": {
                        "color": {
                            "rgbColor": {"red": 0.7, "green": 0.7, "blue": 0.7}
                        }
                    }
                },
                "fields": "foregroundColor"
            }
        }
    ]

def create_code_block(code: str, index: int) -> List[Dict]:
    """Create a formatted code block"""
    return [
        {
            "insertText": {
                "location": {"index": index},
                "text": code + "\n"
            }
        },
        {
            "updateTextStyle": {
                "range": {
                    "startIndex": index,
                    "endIndex": index + len(code) + 1
                },
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Courier New"},
                    "fontSize": {"magnitude": 10, "unit": "PT"},
                    "backgroundColor": {
                        "color": {
                            "rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}
                        }
                    }
                },
                "fields": "weightedFontFamily,fontSize,backgroundColor"
            }
        }
    ]
