from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from langchain_core.tools import tool
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from enum import Enum

# Priority levels affect generation detail
class TaskPriority(str, Enum):
    LOW = "low"       # Minimal documentation
    MEDIUM = "medium" # Standard documentation
    HIGH = "high"     # Detailed documentation

# Validation metrics for AI generation quality
class GenerationMetrics(BaseModel):
    input_tokens: int = Field(description="Tokens in user input")
    output_tokens: int = Field(description="Tokens in AI output")
    expansion_ratio: float = Field(description="Output/Input ratio")
    hallucination_risk: str = Field(description="low/medium/high based on expansion")
    generation_time: float = Field(description="Time taken in seconds")
    confidence_score: float = Field(description="0-1 confidence in generation")

# Minimal output structures based on priority
class TechnicalImplementation(BaseModel):
    approach: Optional[str] = Field(default=None, description="Only if explicitly mentioned")
    technologies: List[str] = Field(default_factory=list, description="Only from user input")
    key_points: List[str] = Field(default_factory=list, description="Max 3 points")

class Challenge(BaseModel):
    issue: str = Field(description="Actual issue mentioned")
    resolution: Optional[str] = Field(default=None, description="Only if resolved")

class WorkLogEntry(BaseModel):
    title: str
    summary: str = Field(description="Up to 4 lines, comprehensive overview")
    task_description: str = Field(description="From user input only")
    achievements: List[str] = Field(description="Max 3, only factual")
    technical_implementation: Optional[TechnicalImplementation] = None
    challenges: List[Challenge] = Field(default_factory=list, description="User-provided or inferred challenges")
    next_steps: List[str] = Field(default_factory=list, description="Max 2")
    tags: List[str] = Field(default_factory=list)
    priority: TaskPriority
    
    @validator('achievements')
    def limit_achievements(cls, v):
        return v[:3]  # Hard limit
    
    @validator('next_steps')
    def limit_next_steps(cls, v):
        return v[:2]  # Hard limit

@tool
def calculate_input_metrics(task_topic: str, details: str) -> Dict[str, Any]:
    """Calculate input metrics for validation"""
    combined = f"{task_topic} {details}"
    word_count = len(combined.split())
    char_count = len(combined)
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "estimated_tokens": word_count * 1.3  # Rough estimate
    }

@tool
def validate_generation(input_metrics: Dict, output_data: Dict, generation_time: float) -> GenerationMetrics:
    """Validate AI generation quality"""
    input_tokens = input_metrics["estimated_tokens"]
    output_text = str(output_data)
    output_tokens = len(output_text.split()) * 1.3
    
    expansion_ratio = output_tokens / max(input_tokens, 1)
    
    # Hallucination risk assessment
    if expansion_ratio > 5:
        hallucination_risk = "high"
        confidence = 0.6
    elif expansion_ratio > 3:
        hallucination_risk = "medium"
        confidence = 0.75
    else:
        hallucination_risk = "low"
        confidence = 0.9
    
    return GenerationMetrics(
        input_tokens=int(input_tokens),
        output_tokens=int(output_tokens),
        expansion_ratio=round(expansion_ratio, 2),
        hallucination_risk=hallucination_risk,
        generation_time=round(generation_time, 2),
        confidence_score=confidence
    )

@tool
def extract_minimal_tags(task_topic: str, details: str, priority: str) -> List[str]:
    """Extract only relevant tags, max 3"""
    tags = []
    text = f"{task_topic} {details}".lower()
    
    # Core tag
    tags.append("ml-engineering")
    
    # Priority-based tag selection (max 2 additional)
    tag_mapping = {
        "model": "machine-learning",
        "api": "api-development",
        "deploy": "deployment",
        "data": "data-engineering",
        "triton": "inference",
        "yolo": "object-detection"
    }
    
    for keyword, tag in tag_mapping.items():
        if keyword in text and len(tags) < 3:
            tags.append(tag)
    
    return tags

class ValidatedDocAgent:
    def __init__(self, api_key: str, full_name: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3,  # Lower temperature = less hallucination
            max_output_tokens=2048,  # Reduced max length
            convert_system_message_to_human=True
        )
        self.full_name = full_name
        self.parser = PydanticOutputParser(pydantic_object=WorkLogEntry)
        self._build_priority_prompts()
    
    def _build_priority_prompts(self):
        """Build different prompts based on priority"""
        self.prompts = {
            TaskPriority.LOW: ChatPromptTemplate.from_messages([
                ("system", """You are a minimal documentation assistant for {full_name}.
Generate BRIEF work logs. Use ONLY information from user input.
- Summary: Up to 4 lines
- Achievements: 1-2 items max
- Challenges: Only if explicitly mentioned or user-provided
- NO technical details unless provided
{format_instructions}"""),
                ("human", "Task: {task_topic}\nDetails: {details}\nChallenges: {challenges}\nPriority: LOW")
            ]),
            
            TaskPriority.MEDIUM: ChatPromptTemplate.from_messages([
                ("system", """You are a documentation assistant for {full_name}.
Generate standard work logs. Stay close to user input.
- Summary: Up to 4 lines describing work and progress
- Achievements: 2-3 items from actual work
- Challenges: Include user-provided challenges or those mentioned
- Technical details: Only what user provided
{format_instructions}"""),
                ("human", "Task: {task_topic}\nDetails: {details}\nChallenges: {challenges}\nPriority: MEDIUM")
            ]),
            
            TaskPriority.HIGH: ChatPromptTemplate.from_messages([
                ("system", """You are a detailed documentation assistant for {full_name}.
Generate comprehensive logs but stay factual.
- Summary: Up to 4 lines with detailed overview
- Achievements: Up to 3 items
- Include technical details if provided
- Challenges: Expand on user-provided challenges with context
{format_instructions}"""),
                ("human", "Task: {task_topic}\nDetails: {details}\nChallenges: {challenges}\nPriority: HIGH")
            ])
        }
    
    def generate_documentation(
        self, 
        task_topic: str, 
        details: str = "",
        challenges: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        validate: bool = True
    ) -> Dict[str, Any]:
        """Generate minimal, validated documentation"""
        
        start_time = datetime.now()
        
        # Calculate input metrics
        input_metrics = calculate_input_metrics.invoke({
            "task_topic": task_topic,
            "details": details
        })
        
        print(f"📊 Input: {input_metrics['word_count']} words, Priority: {priority.value}")
        
        # Select prompt based on priority
        prompt = self.prompts[priority]
        
        # Build chain
        chain = (
            prompt 
            | self.llm 
            | self.parser
        )
        
        # Generate
        result = chain.invoke({
            "full_name": self.full_name,
            "task_topic": task_topic,
            "details": details if details else "Not provided",
            "challenges": challenges if challenges else "No challenges mentioned",
            "format_instructions": self.parser.get_format_instructions()
        })
        
        # Add metadata
        result.priority = priority
        result.tags = extract_minimal_tags.invoke({
            "task_topic": task_topic,
            "details": details,
            "priority": priority.value
        })
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        output = {
            "structured": result.model_dump(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "success"
        }
        
        # Validation metrics
        if validate:
            metrics = validate_generation.invoke({
                "input_metrics": input_metrics,
                "output_data": output["structured"],
                "generation_time": generation_time
            })
            # Only return confidence and generation time for display
            output["metrics"] = {
                "confidence_score": metrics.confidence_score,
                "generation_time": metrics.generation_time
            }
            
            # Warning if confidence is low
            if metrics.confidence_score < 0.7:
                print(f"⚠️  LOW CONFIDENCE: {metrics.confidence_score:.0%}")
            else:
                print(f"✅ Correctness: {metrics.confidence_score:.0%}, Time: {metrics.generation_time:.2f}s")
        
        return output

# Example usage
if __name__ == "__main__":
    from config import GEMINI_API_KEY, FULL_NAME
    
    agent = ValidatedDocAgent(api_key=GEMINI_API_KEY, full_name=FULL_NAME)
    
    # Test different priorities
    test_cases = [
        {
            "task": "Fixed bug in API",
            "details": "Corrected null pointer in /predict endpoint",
            "priority": TaskPriority.LOW
        },
        {
            "task": "YOLO to Triton deployment",
            "details": "Deployed YOLO models. Fixed preprocessing pipeline.",
            "priority": TaskPriority.MEDIUM
        },
        {
            "task": "Complete ML pipeline overhaul",
            "details": "Redesigned entire training pipeline with new data augmentation, implemented custom loss function, integrated with MLflow for tracking, deployed to production with A/B testing framework",
            "priority": TaskPriority.HIGH
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['priority'].value.upper()} Priority")
        print(f"{'='*80}")
        
        result = agent.generate_documentation(
            task_topic=test["task"],
            details=test["details"],
            priority=test["priority"]
        )
        
        print(f"\n📄 Generated {len(result['structured']['achievements'])} achievements")
        print(f"🏷️  Tags: {result['structured']['tags']}")
        
        if "metrics" in result:
            m = result["metrics"]
            print(f"\n📊 VALIDATION METRICS:")
            print(f"   Input:  {m['input_tokens']} tokens")
            print(f"   Output: {m['output_tokens']} tokens")
            print(f"   Ratio:  {m['expansion_ratio']}x")
            print(f"   Risk:   {m['hallucination_risk']}")
            print(f"   Time:   {m['generation_time']}s")