import google.generativeai as genai
from typing import Dict, List, Any
import json
import re
from datetime import datetime
from config import *

class GeminiAgent:
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini agent for work documentation
        
        Args:
            api_key: Your Google Gemini API key
            model_name: Model to use (default: gemini-1.5-flash)
        """
        genai.configure(api_key=api_key)
        
        # Configure generation settings for better JSON output
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,  # Increased from 2048 to handle longer responses
            "response_mime_type": "application/json"  # Force JSON response
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        
    def generate_work_documentation(self, task_topic: str, details: str = "") -> Dict[str, Any]:
        """
        Generate comprehensive technical documentation for your work
        
        Args:
            task_topic: Main topic/task you worked on
            details: Additional details about what you did
            
        Returns:
            Dictionary with raw_content, structured data, and timestamp
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Enhanced prompt for better documentation generation
        prompt = f"""You are a technical documentation assistant for AI/ML Engineer Lakshmi Naresh Chikkala.

Generate a DETAILED and PROFESSIONAL work log entry based on the following information:

**Task/Topic:** {task_topic}
**Additional Details:** {details if details else "Not provided"}
**Date:** {timestamp}

Create documentation that includes:
1. A clear explanation of WHAT the task was about
2. WHY this work was needed (business/technical justification)
3. HOW you approached and solved it (methodology)
4. Specific technical implementations or configurations
5. Real challenges you might have faced doing this work
6. Concrete next steps

CRITICAL: Return ONLY a valid JSON object. Do NOT include markdown formatting, code blocks, or any text outside the JSON.

JSON Structure Required:

{{
    "title": "Work Log - {timestamp.split()[0]} - [Descriptive Title]",
    "summary": "2-3 sentence executive summary",
    "task_description": "Detailed explanation of the task",
    "key_achievements": [
        "Achievement 1 with details",
        "Achievement 2 with details",
        "Achievement 3 with details"
    ],
    "technical_implementation": {{
        "approach": "Methodology used",
        "technologies": ["tech1", "tech2", "tech3"],
        "code_snippets": ["Implementation detail 1", "Configuration detail 2"],
        "architecture_decisions": "Key decisions made"
    }},
    "challenges_faced": [
        {{
            "challenge": "Specific challenge description",
            "solution": "How it was resolved",
            "learning": "Key takeaway"
        }}
    ],
    "metrics_and_results": {{
        "headers": ["Metric", "Value", "Impact"],
        "rows": [
            ["Task Status", "Completed", "Ready for deployment"],
            ["Time Invested", "4 hours", "Within estimate"],
            ["Quality", "High", "Meets standards"]
        ]
    }},
    "next_steps": [
        "Action item 1",
        "Action item 2",
        "Action item 3"
    ],
    "tags": ["ml-engineering", "deployment", "optimization"]
}}

Make it realistic, detailed, and technical. Keep achievements and challenges concise but informative."""

        try:
            print(f"🤖 Generating documentation for: {task_topic}")
            print(f"⏳ Calling Gemini API...")
            
            # Generate content from Gemini
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            print(f"✅ Received response from Gemini")
            print(f"📝 Response length: {len(raw_text)} characters")
            
            # Since response_mime_type is set to application/json, the response should be pure JSON
            # Try to parse it directly first
            try:
                structured_data = json.loads(raw_text)
                print(f"✅ Successfully parsed JSON directly")
                
                return {
                    "raw_content": raw_text,
                    "structured": structured_data,
                    "timestamp": timestamp,
                    "status": "success"
                }
            except json.JSONDecodeError as direct_error:
                print(f"⚠️ Direct JSON parse failed: {direct_error}")
                print(f"🔍 Attempting JSON extraction...")
                
                # Try to extract and fix JSON
                json_str = self._extract_and_fix_json(raw_text)
                
                if json_str:
                    try:
                        structured_data = json.loads(json_str)
                        print(f"✅ Successfully parsed extracted JSON")
                        
                        return {
                            "raw_content": raw_text,
                            "structured": structured_data,
                            "timestamp": timestamp,
                            "status": "success"
                        }
                    except json.JSONDecodeError as extract_error:
                        print(f"❌ Extracted JSON still invalid: {extract_error}")
                        print(f"📄 Extracted JSON preview: {json_str[:500]}")
                else:
                    print(f"❌ JSON extraction failed completely")
                    print(f"📄 Full response preview: {raw_text[:500]}")
            
            # If all parsing failed, use fallback
            return self._create_fallback_with_ai_content(task_topic, details, timestamp, raw_text)
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            return self._create_fallback_with_ai_content(task_topic, details, timestamp, None)
    
    def _extract_and_fix_json(self, text: str) -> str:
        """
        Extract JSON from text and attempt to fix common issues
        """
        # Remove markdown code blocks if present
        cleaned = text.strip()
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        cleaned = cleaned.strip()
        
        # Find the start of JSON
        start_idx = cleaned.find('{')
        if start_idx == -1:
            print(f"⚠️ No opening brace found")
            return None
        
        # Find the matching closing brace using brace counting
        brace_count = 0
        end_idx = -1
        in_string = False
        escape_next = False
        
        for i in range(start_idx, len(cleaned)):
            char = cleaned[i]
            
            # Handle escape sequences
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            # Track string boundaries
            if char == '"':
                in_string = not in_string
                continue
            
            # Count braces only outside strings
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i
                        break
        
        if end_idx == -1:
            print(f"⚠️ No matching closing brace found. Open braces: {brace_count}")
            
            # Try to find the last brace and use that
            last_brace = cleaned.rfind('}')
            if last_brace != -1:
                print(f"🔧 Using last brace found at position {last_brace}")
                end_idx = last_brace
            else:
                return None
        
        json_str = cleaned[start_idx:end_idx + 1]
        
        # Validate the extracted JSON
        try:
            json.loads(json_str)
            print(f"✅ Extracted valid JSON ({len(json_str)} characters)")
            return json_str
        except json.JSONDecodeError as e:
            print(f"⚠️ Extracted JSON is invalid: {e}")
            print(f"🔍 Error at position {e.pos}")
            
            # Try to fix common issues
            # 1. Truncated strings
            if e.msg.startswith("Unterminated string"):
                print(f"🔧 Attempting to fix unterminated string...")
                # Add closing quote before the error position
                fixed = json_str[:e.pos] + '"' + json_str[e.pos:]
                try:
                    json.loads(fixed)
                    return fixed
                except:
                    pass
            
            return None
    
    def _create_fallback_with_ai_content(self, task_topic: str, details: str, 
                                        timestamp: str, raw_response: str = None) -> Dict[str, Any]:
        """
        Create a structured fallback response with enhanced content
        """
        print(f"⚠️  Using enhanced fallback structure")
        
        # Try to extract useful information from raw response if available
        summary_text = f"Worked on {task_topic}"
        if details:
            summary_text += f": {details}"
        
        if raw_response:
            # Try to extract some useful content from the raw response
            summary_text = raw_response[:200] + "..." if len(raw_response) > 200 else raw_response
        
        return {
            "raw_content": raw_response if raw_response else f"Work Log: {task_topic} - {details}\nProgress made on {timestamp}",
            "structured": {
                "title": f"Work Log - {timestamp.split()[0]} - {task_topic}",
                "summary": summary_text,
                "task_description": f"Task involved: {task_topic}. {details if details else 'Implementation and configuration work completed.'}",
                "key_achievements": [
                    f"Successfully worked on {task_topic}",
                    f"Completed required configurations and implementations",
                    f"Validated and tested the solution"
                ],
                "technical_implementation": {
                    "approach": "Systematic implementation following best practices",
                    "technologies": ["Python", "ML/AI Tools", "Configuration Management"],
                    "code_snippets": [f"Implemented {task_topic} configurations", "Applied optimization techniques"],
                    "architecture_decisions": "Followed modular design principles and industry standards"
                },
                "challenges_faced": [
                    {
                        "challenge": "Technical complexity and integration issues",
                        "solution": "Broke down into manageable components and tested incrementally",
                        "learning": "Importance of systematic approach and thorough testing"
                    }
                ],
                "metrics_and_results": {
                    "headers": ["Metric", "Value", "Impact"],
                    "rows": [
                        ["Task Status", "Completed", "Ready for next phase"],
                        ["Time Invested", "As planned", "On schedule"],
                        ["Quality", "High", "Meets requirements"]
                    ]
                },
                "next_steps": [
                    "Test implementation in staging environment",
                    "Document configuration for team reference",
                    "Plan integration with downstream systems"
                ],
                "tags": ["configuration", "implementation", "ml-engineering"]
            },
            "timestamp": timestamp,
            "status": "fallback"
        }


# Example usage
if __name__ == "__main__":
    # Initialize agent
    agent = GeminiAgent(api_key=GEMINI_API_KEY)
    
    # Generate documentation
    result = agent.generate_work_documentation(
        task_topic="YOLO models to Triton engines deployment",
        details="Deployed YOLO models to NVIDIA Triton Inference Server. Fixed issues in pre-processing and post-processing pipelines."
    )
    
    # Pretty print the result
    print("\n" + "="*80)
    print("📄 GENERATED DOCUMENTATION")
    print("="*80)
    print(json.dumps(result["structured"], indent=2))
    print("\n" + "="*80)
    print(f"⏰ Generated at: {result['timestamp']}")
    print(f"✅ Status: {result['status']}")