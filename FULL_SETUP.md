# Quick Start Guide - Docify Frontend & Backend

## 🚀 Full Setup (Frontend + Backend)

### Terminal 1: Start Backend FastAPI
```bash
cd d:\docify\Lang
python api.py
```

Output:
```
🚀 Starting Docify Generator...
📚 API Documentation: http://localhost:8000/docs
📝 Main Endpoint: POST http://localhost:8000/generate
```

### Terminal 2: Start Frontend React
```bash
cd d:\docify\frontend
npm install  # First time only
npm start
```

Output:
```
Compiled successfully!
You can now view docify-frontend in the browser.
  Local:            http://localhost:3000
```

## 📱 Access the App

Open your browser to: **http://localhost:3000**

## 🎯 Using the App

1. Enter your main topic (e.g., "FastAPI Implementation")
2. Add related topics (optional - click "+ Add Related Topic")
3. Click "🚀 Generate Documentation"
4. Wait for generation (10-30 seconds)
5. Click "Open in Google Docs" to view result

## ⚙️ What's Happening

```
Frontend (React)           Backend (FastAPI)         AI (Gemini)
     ↓                            ↓                        ↓
User enters topic      →  API receives request  →  Generates docs
     ↓
User sees response    ←  Returns doc URL      ←  Writes to Docs
```

## 🛠️ Folder Structure

```
d:\docify\
├── Lang/
│   ├── api.py                    # FastAPI server
│   ├── config.py
│   ├── agents/
│   │   ├── gemini_agent.py
│   │   └── docs_agent.py
│   └── utils/
│       └── page_manager.py
│
└── frontend/
    ├── src/
    │   ├── App.js                # Main React component
    │   ├── components/
    │   │   ├── DocumentationForm.js
    │   │   └── ResponseDisplay.js
    │   └── index.js
    ├── package.json
    └── README.md
```

## 📝 Environment Variables

Make sure `.env` file exists in `Lang/` folder:
```
GEMINI_API_KEY=your-key-here
SERVICE_ACCOUNT_FILE=doc-bee-cec8fb727916.json
DOC_ID=your-google-doc-id
```

## 🔍 Testing the API Directly

### With cURL
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Test Topic",
    "related_topics": ["Subtopic 1", "Subtopic 2"]
  }'
```

### With Python
```python
import requests

response = requests.post(
    "http://localhost:8000/generate",
    json={
        "topic": "Test Topic",
        "related_topics": ["Subtopic 1", "Subtopic 2"]
    }
)

print(response.json())
```

### Interactive Swagger UI
Visit: **http://localhost:8000/docs**

## 🐛 Troubleshooting

### Frontend won't start
```
npm ERR! code ENOENT
npm ERR! syscall open
```
**Solution:**
```bash
cd frontend
npm install
npm start
```

### Can't connect to backend
```
Failed to connect to API. Make sure the backend is running on http://localhost:8000
```
**Solution:** Make sure backend is running in Terminal 1

### Port already in use
```
Port 3000 is already in use
```
**Solution:**
```bash
# Use different port
PORT=3001 npm start
```

### API returns 503 error
```
The model is overloaded. Please try again later.
```
**Solution:** Wait a few seconds and try again. The API will use fallback if Gemini is overloaded.

## 📚 Documentation

- [API_README.md](./Lang/API_README.md) - API details
- [USAGE.md](./Lang/USAGE.md) - API usage examples
- [frontend/README.md](./frontend/README.md) - Frontend details

## ✅ Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can access http://localhost:8000/docs (Swagger)
- [ ] Google Doc is shared with service account email
- [ ] .env file has correct API key and Doc ID
- [ ] Can submit form without errors
- [ ] Generated documentation appears in Google Docs

## 🚀 Next Steps

1. **Customize Styling** - Edit `frontend/src/App.css`
2. **Add More Features** - Extend form with more inputs
3. **Deploy Frontend** - Vercel, Netlify, or GitHub Pages
4. **Deploy Backend** - AWS, Google Cloud, Heroku

## 💡 Tips

- Generate documentation regularly for better records
- Check Google Docs in real-time while app is running
- Use Swagger UI (localhost:8000/docs) to test API directly
- Browser DevTools (F12) to debug frontend issues

## ❓ Need Help?

1. Check terminal error messages
2. Look at browser console (F12)
3. Check network requests (DevTools → Network tab)
4. Review API response in Swagger UI

---

**Happy documenting! 📝✨**
