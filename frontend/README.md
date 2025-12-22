# Docify React Frontend

Beautiful React frontend for Docify FastAPI backend.

## Features

✨ **Clean UI** - Modern, responsive design  
⚡ **Real-time Updates** - Instant feedback on documentation generation  
📝 **Dynamic Form** - Add/remove related topics on the fly  
🎯 **Error Handling** - Clear error messages and validation  
📱 **Mobile Responsive** - Works on all devices  
🔗 **Direct Links** - Open generated Google Docs with one click  

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── DocumentationForm.js       # Form component
│   │   ├── DocumentationForm.css
│   │   ├── ResponseDisplay.js         # Response display component
│   │   └── ResponseDisplay.css
│   ├── App.js                         # Main app component
│   ├── App.css
│   ├── index.js                       # Entry point
│   └── index.css                      # Global styles
├── package.json
└── README.md
```

## Installation

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start the Development Server
```bash
npm start
```

The app will open at **http://localhost:3000**

## Usage

### Prerequisites
- Backend FastAPI running on http://localhost:8000
- Python server started: `python api.py` in the Lang folder

### How to Use

1. **Enter Main Topic** - What you worked on today
2. **Add Related Topics** (optional) - Click "Add Related Topic" to add more details
3. **Click Generate** - Wait for the documentation to be generated
4. **Open Document** - Click the Google Docs link to view the generated documentation

## Build for Production

```bash
npm run build
```

Creates optimized production build in `build/` folder.

## Configuration

### API Base URL

Change the API endpoint in `src/App.js`:

```javascript
const res = await fetch('http://localhost:8000/generate', {  // Change this URL
  method: 'POST',
  // ...
});
```

### Styling

Global styles are in `src/index.css`  
Component styles are in respective `.css` files

## Features Explained

### DocumentationForm Component
- Dynamic form for topic and related topics
- Add/remove topics with buttons
- Validation and error handling
- Loading state during submission

### ResponseDisplay Component
- Shows success/error messages
- Displays document URL with direct link
- Shows content preview (title, summary, achievements)
- Timestamp of generation

### App Component
- Manages form and response state
- Handles API calls
- Error handling and display
- Loading state management

## API Integration

The frontend sends POST requests to the backend:

**Endpoint:** `POST /generate`

**Request Payload:**
```json
{
  "topic": "Your main topic",
  "related_topics": ["topic1", "topic2", "topic3"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Documentation generated and written to Google Docs successfully!",
  "timestamp": "2025-12-16T10:30:00.123456",
  "doc_url": "https://docs.google.com/document/d/...",
  "content_preview": {
    "title": "...",
    "summary": "...",
    "key_achievements": [...]
  }
}
```

## Troubleshooting

### API Connection Error
```
Failed to connect to API. Make sure the backend is running on http://localhost:8000
```
**Solution:** Start the backend with `python api.py` in the Lang folder

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution:** Update backend to enable CORS (already done in api.py)

### Blank Screen
**Solution:** Check browser console for errors (F12 → Console)

### Slow Generation
- First request takes 10-30 seconds (AI processing)
- Subsequent requests are faster
- This is normal!

## Development

### Available Scripts

```bash
npm start       # Start development server
npm test        # Run tests
npm run build   # Build for production
npm run eject   # Eject (one-way operation!)
```

### Browser DevTools

- F12 to open DevTools
- Network tab to see API calls
- Console for error messages

## Deployment

### Option 1: Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm run build
# Deploy the 'build' folder to Netlify
```

### Option 3: GitHub Pages
```bash
npm run build
# Deploy 'build' folder as gh-pages
```

### Note on Backend URL
When deploying, update the backend URL in `src/App.js` to your production backend URL.

## Technologies Used

- **React 18** - UI library
- **CSS3** - Styling with animations
- **Fetch API** - HTTP requests
- **Responsive Design** - Mobile-first approach

## Performance

- ✅ Optimized bundle size (~50KB gzipped)
- ✅ Smooth animations and transitions
- ✅ Lazy loading and code splitting
- ✅ CSS animations (no heavy libraries)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Same as parent project

## Support

For issues:
1. Check browser console (F12)
2. Verify backend is running
3. Check network requests in DevTools
4. Review error messages on the UI

---

**Happy documenting! 🚀**
