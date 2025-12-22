#!/bin/bash
# Start the Docify API server

echo "🚀 Starting Docify API..."
echo "📚 Documentation available at: http://localhost:8000/docs"
echo ""

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-api.txt
else
    source venv/bin/activate
fi

# Start API
python api.py
