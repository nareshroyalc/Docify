import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any
from datetime import datetime

class DocsAgent:
    """Writes validated, minimal documentation to Google Docs"""
    
    def __init__(self, service_account_file: str, scopes: List[str]):
        self.service_account_file = service_account_file
        self.scopes = scopes
        self.service, self.sa_email = self._init_service()
    
    def _init_service(self):
        creds = Credentials.from_service_account_file(
            self.service_account_file, 
            scopes=self.scopes
        )
        service = build("docs", "v1", credentials=creds)
        
        with open(self.service_account_file, "r") as f:
            sa = json.load(f)
        return service, sa.get("client_email")
    
    def write_entry(self, doc_id: str, doc_data: Dict) -> bool:
        """Write validated documentation with metrics"""
        try:
            # Get safe insertion point
            doc = self.service.documents().get(documentId=doc_id).execute()
            safe_index = self._get_safe_index(doc)
            
            # Check validation metrics
            metrics = doc_data.get("metrics", {})
            if metrics:
                self._log_validation(metrics)
            
            # Build content based on priority
            requests = self._build_minimal_content(safe_index, doc_data)
            
            # Write to docs
            self.service.documents().batchUpdate(
                documentId=doc_id, 
                body={"requests": requests}
            ).execute()
            
            print("✅ Documentation written successfully")
            return True
            
        except HttpError as e:
            print(f"❌ Docs API Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _get_safe_index(self, doc: Dict) -> int:
        """Find safe insertion point in document"""
        content = doc.get("body", {}).get("content", [])
        if not content:
            return 1
        
        # Find last element's end index
        last_element = content[-1]
        return last_element.get("endIndex", 1) - 1
    
    def _log_validation(self, metrics: Dict):
        """Log validation metrics"""
        risk = metrics.get("hallucination_risk", "unknown")
        confidence = metrics.get("confidence_score", 0)
        ratio = metrics.get("expansion_ratio", 0)
        
        emoji = "✅" if risk == "low" else "⚠️" if risk == "medium" else "🚨"
        print(f"{emoji} Validation: {risk.upper()} risk, {confidence:.0%} confidence, {ratio}x expansion")
    
    def _build_minimal_content(self, start_index: int, doc_data: Dict) -> List[Dict]:
        """Build formatted content with selective Google Docs styling"""
        data = doc_data["structured"]
        priority = data.get("priority", "medium")
        timestamp = doc_data["timestamp"]
        
        # Build requests with selective formatting
        requests = []
        current_index = start_index
        
        # Add title with bold formatting
        title = data.get("title", "Work Log")
        title_text = "📊 " + title + "\n"
        requests.append({
            "insertText": {
                "location": {"index": current_index},
                "text": title_text
            }
        })
        # Bold just the title text (exclude newline)
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": current_index,
                    "endIndex": current_index + len(title_text) - 1
                },
                "textStyle": {
                    "bold": True,
                    "fontSize": {"magnitude": 18, "unit": "pt"}
                },
                "fields": "bold,fontSize"
            }
        })
        current_index += len(title_text)
        
        # Add metadata line (not bold) with spacing
        meta_text = "📅 " + timestamp + " | Priority: " + priority.upper() + "\n\n"
        requests.append({
            "insertText": {
                "location": {"index": current_index},
                "text": meta_text
            }
        })
        current_index += len(meta_text)
        
        # Build content based on priority and track positions
        if priority == "low":
            content_result = self._build_low_content_with_headers(data)
        elif priority == "high":
            content_result = self._build_high_content_with_headers(data)
        else:
            content_result = self._build_medium_content_with_headers(data)
        
        content_text = content_result['text']
        
        # Insert main content
        requests.append({
            "insertText": {
                "location": {"index": current_index},
                "text": content_text
            }
        })
        
        # Apply bold formatting to headers only
        for header_info in content_result['headers']:
            start = current_index + header_info['start']
            end = current_index + header_info['end']
            requests.append({
                "updateTextStyle": {
                    "range": {
                        "startIndex": start,
                        "endIndex": end
                    },
                    "textStyle": {
                        "bold": True,
                        "fontSize": {"magnitude": 12, "unit": "pt"}
                    },
                    "fields": "bold,fontSize"
                }
            })
        
        current_index += len(content_text)
        
        # Add metrics if available
        if "metrics" in doc_data:
            metrics_text = self._format_metrics_footer(doc_data["metrics"])
            requests.append({
                "insertText": {
                    "location": {"index": current_index},
                    "text": metrics_text
                }
            })
            
            # Bold the metrics header
            metrics_header_start = metrics_text.find("GENERATION METRICS")
            if metrics_header_start >= 0:
                requests.append({
                    "updateTextStyle": {
                        "range": {
                            "startIndex": current_index + metrics_header_start,
                            "endIndex": current_index + metrics_header_start + len("GENERATION METRICS")
                        },
                        "textStyle": {
                            "bold": True,
                            "fontSize": {"magnitude": 12, "unit": "pt"}
                        },
                        "fields": "bold,fontSize"
                    }
                })
        
        return requests
    
    def _build_low_content_with_headers(self, data: Dict) -> Dict:
        """Build low priority content with accurate header tracking"""
        text = ""
        headers = []
        
        # Summary section
        text_before = text
        text += "\nSUMMARY\n"
        summary_pos = len(text_before) + 1
        headers.append({
            "start": summary_pos,
            "end": summary_pos + len("SUMMARY")
        })
        text += data.get('summary', 'No summary') + "\n"
        
        if data.get('task_description'):
            text_before = text
            text += "\n✓ COMPLETED TASK\n"
            task_pos = len(text_before) + 2  # Skip newline and emoji
            headers.append({
                "start": task_pos,
                "end": task_pos + len("COMPLETED TASK")
            })
            text += data.get('task_description') + "\n"
        
        if data.get('achievements'):
            text_before = text
            text += "\nACHIEVEMENTS\n"
            ach_pos = len(text_before) + 1
            headers.append({
                "start": ach_pos,
                "end": ach_pos + len("ACHIEVEMENTS")
            })
            
            for ach in data['achievements'][:2]:
                text += "  ✓ " + ach + "\n"
        
        if data.get('tags'):
            text_before = text
            text += "\n🏷️ TAGS\n"
            tags_pos = len(text_before) + 2  # Skip newline and emoji
            headers.append({
                "start": tags_pos,
                "end": tags_pos + len("TAGS")
            })
            text += ", ".join(data['tags']) + "\n"
        
        text += "\n"
        return {"text": text, "headers": headers}
    
    def _build_medium_content_with_headers(self, data: Dict) -> Dict:
        """Build medium priority content with accurate header tracking"""
        text = ""
        headers = []
        
        # Summary
        text += "\nSUMMARY\n"
        headers.append({"start": 1, "end": 1 + len("SUMMARY")})
        text += data.get('summary', 'No summary provided') + "\n"
        
        # Task Description
        text_len = len(text)
        text += "\nTASK DESCRIPTION\n"
        headers.append({"start": text_len + 1, "end": text_len + 1 + len("TASK DESCRIPTION")})
        text += data.get('task_description', 'No description') + "\n"
        
        # Achievements
        text_len = len(text)
        text += "\nACHIEVEMENTS\n"
        headers.append({"start": text_len + 1, "end": text_len + 1 + len("ACHIEVEMENTS")})
        for ach in data.get('achievements', [])[:3]:
            text += "  ✓ " + ach + "\n"
        
        # Technical
        tech = data.get('technical_implementation')
        if tech and (tech.get('technologies') or tech.get('key_points')):
            text_len = len(text)
            text += "\nTECHNICAL IMPLEMENTATION\n"
            headers.append({"start": text_len + 1, "end": text_len + 1 + len("TECHNICAL IMPLEMENTATION")})
            
            if tech.get('approach'):
                text += "Approach: " + tech['approach'] + "\n"
            if tech.get('technologies'):
                text += "Technologies: " + ", ".join(tech['technologies']) + "\n"
            for point in tech.get('key_points', []):
                text += "  • " + point + "\n"
        
        # Challenges
        challenges = data.get('challenges', [])
        if challenges:
            text_len = len(text)
            text += "\nCHALLENGES\n"
            headers.append({"start": text_len + 1, "end": text_len + 1 + len("CHALLENGES")})
            
            for ch in challenges[:2]:
                if isinstance(ch, dict):
                    text += "Issue: " + ch.get('issue', 'N/A') + "\n"
                    if ch.get('resolution'):
                        text += "  ✓ Resolution: " + ch['resolution'] + "\n"
        
        # Next Steps
        next_steps = data.get('next_steps', [])
        if next_steps:
            text_len = len(text)
            text += "\nNEXT STEPS\n"
            headers.append({"start": text_len + 1, "end": text_len + 1 + len("NEXT STEPS")})
            
            for step in next_steps[:2]:
                text += "  • " + step + "\n"
        
        # Tags
        if data.get('tags'):
            text_len = len(text)
            text += "\n🏷️ TAGS\n"
            headers.append({"start": text_len + 2, "end": text_len + 2 + len("TAGS")})
            text += ", ".join(data['tags']) + "\n"
        
        text += "\n"
        return {"text": text, "headers": headers}
    
    def _build_high_content_with_headers(self, data: Dict) -> Dict:
        """Build high priority content with accurate header tracking"""
        text = ""
        headers = []
        
        # Executive Summary
        text += "\nEXECUTIVE SUMMARY\n"
        headers.append({"start": 1, "end": 1 + len("EXECUTIVE SUMMARY")})
        text += data.get('summary', 'No summary provided') + "\n"
        
        # Detailed Task Description
        text_len = len(text)
        text += "\nDETAILED TASK DESCRIPTION\n"
        headers.append({"start": text_len + 1, "end": text_len + 1 + len("DETAILED TASK DESCRIPTION")})
        text += data.get('task_description', 'No description') + "\n"
        
        # Key Achievements
        text_len = len(text)
        text += "\nKEY ACHIEVEMENTS\n"
        headers.append({"start": text_len + 1, "end": text_len + 1 + len("KEY ACHIEVEMENTS")})
        for ach in data.get('achievements', []):
            text += "  ✓ " + ach + "\n"
        
        # Technical Implementation
        tech = data.get('technical_implementation')
        if tech:
            text_len = len(text)
            text += "\nTECHNICAL IMPLEMENTATION\n"
            headers.append({"start": text_len + 1, "end": text_len + 1 + len("TECHNICAL IMPLEMENTATION")})
            
            if tech.get('approach'):
                text += "Approach:\n  " + tech['approach'] + "\n"
            if tech.get('technologies'):
                text += "Technologies: " + ", ".join(tech['technologies']) + "\n"
            if tech.get('key_points'):
                text += "Key Points:\n"
                for point in tech.get('key_points', []):
                    text += "  • " + point + "\n"
        
        # Challenges & Solutions
        challenges = data.get('challenges', [])
        if challenges:
            text_len = len(text)
            text += "\nCHALLENGES & SOLUTIONS\n"
            headers.append({"start": text_len + 1, "end": text_len + 1 + len("CHALLENGES & SOLUTIONS")})
            
            for ch in challenges:
                if isinstance(ch, dict):
                    text += "Challenge:\n  " + ch.get('issue', 'N/A') + "\n"
                    if ch.get('resolution'):
                        text += "Solution:\n  " + ch['resolution'] + "\n"
        
        # Next Steps
        next_steps = data.get('next_steps', [])
        if next_steps:
            text_len = len(text)
            text += "\nNEXT STEPS & RECOMMENDATIONS\n"
            headers.append({"start": text_len + 1, "end": text_len + 1 + len("NEXT STEPS & RECOMMENDATIONS")})
            
            for step in next_steps:
                text += "  • " + step + "\n"
        
        # Tags
        if data.get('tags'):
            text_len = len(text)
            text += "\n🏷️ TAGS\n"
            headers.append({"start": text_len + 2, "end": text_len + 2 + len("TAGS")})
            text += ", ".join(data['tags']) + "\n"
        
        text += "\n"
        return {"text": text, "headers": headers}
    
    def _format_metrics_footer(self, metrics: Dict) -> str:
        """Add validation metrics footer with clean formatting"""
        lines = []
        lines.append("\nGENERATION METRICS\n")
        lines.append("Correctness: " + f"{metrics.get('confidence_score', 0):.0%}\n")
        lines.append("Generation Time: " + f"{metrics.get('generation_time', 0):.2f}s\n")
        lines.append("\nGenerated by Validated AI Documentation Assistant\n\n")
        return "".join(lines)

# Integration example
if __name__ == "__main__":
    from config import SERVICE_ACCOUNT_FILE, SCOPES, GOOGLE_DOC_ID
    from config import GEMINI_API_KEY, FULL_NAME
    from validated_doc_agent import ValidatedDocAgent, TaskPriority
    
    # Generate documentation
    agent = ValidatedDocAgent(api_key=GEMINI_API_KEY, full_name=FULL_NAME)
    doc_data = agent.generate_documentation(
        task_topic="API optimization",
        details="Reduced latency by 40% through caching",
        priority=TaskPriority.MEDIUM
    )
    
    # Write to Google Docs
    writer = ValidatedDocsWriter(SERVICE_ACCOUNT_FILE, SCOPES)
    writer.write_entry(GOOGLE_DOC_ID, doc_data)