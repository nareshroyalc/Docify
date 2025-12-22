# Docify - AI-Powered Documentation Generator

An intelligent documentation generation tool powered by LangChain and Google Generative AI. Docify leverages advanced AI models to automatically generate comprehensive, well-structured documentation from your source code.

## Features

- **AI-Powered Generation**: Uses Google Generative AI via LangChain for intelligent documentation creation
- **FastAPI Backend**: High-performance REST API for documentation requests
- **React Frontend**: Modern, user-friendly interface for interactive documentation generation
- **Multiple Implementation Approaches**: Both LangChain and Traditional implementations available
- **Flexible Architecture**: Support for different documentation generation strategies
- **RESTful API**: Easy integration with external tools and workflows

## Project Structure

```
docify/
├── Lang/                      # Main LangChain-based implementation
│   ├── api.py                # FastAPI application
│   ├── main.py               # Entry point
│   ├── config.py             # Configuration management
│   ├── client.py             # API client
│   ├── test_api.py           # API tests
│   ├── agents/               # AI agents
│   │   ├── docs_agent.py     # Documentation generation agent
│   │   └── gemini_agent.py   # Google Gemini integration
│   ├── utils/                # Utility functions
│   │   └── page_manager.py   # Page management
│   ├── requirements.txt       # Python dependencies
│   └── requirements-api.txt   # API-specific dependencies
│
├── Traditional/              # Alternative implementation
│   ├── main.py
│   ├── config.py
│   ├── agents/
│   └── utils/
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── App.js            # Main application component
│   │   ├── components/       # React components
│   │   │   ├── DocumentationForm.js
│   │   │   └── ResponseDisplay.js
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── README.md
│
├── notebooks/                # Jupyter notebooks
│   ├── 01_Setup_and_Dependencies.ipynb
│   └── 02_API_Testing.ipynb
│
└── requirements.txt          # Root-level dependencies
```

## Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend)
- Google Generative AI API key
- pip and npm package managers

## Installation

### Backend Setup

1. **Clone the repository**:
```bash
git clone https://github.com/nareshroyalc/Docify.git
cd Docify
```

2. **Create virtual environment** (optional but recommended):
```bash
# Using Python venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
cd Lang
pip install -r requirements.txt
pip install -r requirements-api.txt
```

4. **Set up environment variables**:
Create a `.env` file in the `Lang/` directory:
```
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Frontend Setup

1. **Install Node dependencies**:
```bash
cd frontend
npm install
```

## Usage

### Running the Backend API

```bash
cd Lang
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

### Running the Frontend

```bash
cd frontend
npm start
```

The frontend will open at `http://localhost:3000`

### API Endpoints

#### Generate Documentation
- **POST** `/api/generate`
- **Description**: Generate documentation for provided code
- **Request Body**:
```json
{
  "code": "your_source_code_here",
  "language": "python",
  "style": "detailed"
}
```
- **Response**: Generated documentation in markdown format

#### Health Check
- **GET** `/health`
- **Description**: Check API health status

#### API Info
- **GET** `/api/info`
- **Description**: Get API version and available models

### Example Usage

**Using cURL**:
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"code":"def hello():\n    print(\"Hello, World!\")", "language":"python"}'
```

**Using Python Client**:
```python
from Lang.client import DocumentationClient

client = DocumentationClient(base_url="http://localhost:8000")
response = client.generate_documentation(
    code="def hello():\n    print('Hello, World!')",
    language="python"
)
print(response)
```

## Configuration

### API Configuration (`Lang/config.py`)

Key settings:
- `GOOGLE_API_KEY`: Your Google Generative AI API key
- `MODEL_NAME`: Default LLM model to use
- `MAX_TOKENS`: Maximum tokens for generation
- `TEMPERATURE`: Creativity level (0.0 - 1.0)

## Development

### Running Tests

```bash
cd Lang
python -m pytest test_api.py -v
```

### Using Jupyter Notebooks

1. **Setup and Dependencies**:
```bash
jupyter notebook 01_Setup_and_Dependencies.ipynb
```

2. **API Testing**:
```bash
jupyter notebook 02_API_Testing.ipynb
```

## Architecture

### Backend Flow
1. **Request** → FastAPI endpoint receives code/input
2. **Processing** → LangChain agents analyze the code
3. **Generation** → Google Generative AI generates documentation
4. **Response** → Formatted documentation returned to client

### Frontend Flow
1. **User Input** → User enters code in DocumentationForm
2. **API Call** → Form submits to backend
3. **Display** → ResponseDisplay shows generated documentation
4. **Export** → User can copy or download documentation

## Deployment

### Docker (Optional)

Build Docker image:
```bash
docker build -t docify .
```

Run container:
```bash
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key docify
```

### Production Deployment

See [DEPLOYMENT.md](Lang/DEPLOYMENT.md) for detailed deployment instructions.

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'uvicorn'`
- **Solution**: Install dependencies: `pip install -r requirements-api.txt`

**Issue**: `GOOGLE_API_KEY not set`
- **Solution**: Create `.env` file with your API key

**Issue**: CORS errors in frontend
- **Solution**: Ensure backend is running and configured for CORS

**Issue**: Port already in use
- **Solution**: 
  ```bash
  # Use different port
  uvicorn api:app --port 8001
  ```

## Documentation

- [API Documentation](Lang/API_README.md)
- [FastAPI Summary](Lang/FASTAPI_SUMMARY.md)
- [Quick Start Guide](Lang/QUICK_START.md)
- [Usage Guide](Lang/USAGE.md)
- [Deployment Guide](Lang/DEPLOYMENT.md)

## Technologies Used

- **Backend**: FastAPI, LangChain, Google Generative AI
- **Frontend**: React, JavaScript, CSS
- **APIs**: RESTful architecture, Swagger/OpenAPI
- **Database**: Configuration-based (extensible)
- **Authentication**: API Key-based (configurable)

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions:
- Create an issue on [GitHub](https://github.com/nareshroyalc/Docify/issues)
- Check existing documentation in the `Lang/` directory
- Review Jupyter notebooks for examples

## Future Enhancements

- [ ] Database integration for documentation storage
- [ ] User authentication and account management
- [ ] Multiple language support beyond Python
- [ ] Documentation versioning and history
- [ ] Team collaboration features
- [ ] Custom templates for documentation styling
- [ ] Integration with popular IDEs
- [ ] Batch documentation processing

## Contributors

- nareshroyalc

## Acknowledgments

- Google Generative AI for the language models
- LangChain for the orchestration framework
- FastAPI for the modern Python web framework
- React community for the frontend framework

---

**Last Updated**: December 2025
