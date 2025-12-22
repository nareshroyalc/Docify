# Configuration & secrets
import os
from dotenv import load_dotenv

load_dotenv()

# Google Docs
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "/content/doc-bee-cec8fb727916.json")
DOC_ID = os.getenv("DOC_ID", "1dQ50-UzJASiJUDcmymfpP3hoiiZptaP-SolMaIBPhMY")
SCOPES = ["https://www.googleapis.com/auth/documents"]

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

# Doc settings
FULL_NAME = "Lakshmi Naresh Chikkala"
SURNAME = "Chikkala"

# Documentation styling
STYLE_CONFIG = {
    "primary_color": {"red": 0.26, "green": 0.52, "blue": 0.96},  # Blue
    "success_color": {"red": 0.30, "green": 0.69, "blue": 0.31},  # Green
    "warning_color": {"red": 1.0, "green": 0.76, "blue": 0.03},   # Amber
    "error_color": {"red": 0.96, "green": 0.26, "blue": 0.21},    # Red
    "text_color": {"red": 0.13, "green": 0.13, "blue": 0.13},     # Dark gray
    "code_bg_color": {"red": 0.95, "green": 0.95, "blue": 0.95}  # Light gray
}

# Section emojis for visual appeal
SECTION_EMOJIS = {
    "summary": "📋",
    "achievements": "✅",
    "technical": "💻",
    "challenges": "⚠️",
    "next_steps": "🚀",
    "metrics": "📊",
    "code": "💾",
    "tags": "🏷️"
}
