@echo off
REM Start the Docify API server (Windows)

echo.
echo 🚀 Starting Docify API...
echo 📚 Documentation available at: http://localhost:8000/docs
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

REM Install dependencies if needed
if not exist "chain\Scripts\activate.bat" (
    echo 📦 Creating virtual environment...
    python -m venv chain
    call chain\Scripts\activate.bat
    pip install -r requirements.txt
    pip install -r requirements-api.txt
) else (
    call chain\Scripts\activate.bat
)

REM Start API
python api.py
pause
