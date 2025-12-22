import React, { useState } from 'react';
import './App.css';
import DocumentationForm from './components/DocumentationForm';
import ResponseDisplay from './components/ResponseDisplay';

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Failed to generate documentation');
      } else {
        setResponse(data);
      }
    } catch (err) {
      setError(err.message || 'Failed to connect to API. Make sure the backend is running on http://localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>✨ Docify Generator</h1>
        <p>AI-Powered Documentation Generation</p>
      </header>

      <main className="container">
        <div className="content">
          <DocumentationForm onSubmit={handleSubmit} loading={loading} />

          {error && <div className="error-box">{error}</div>}

          {loading && (
            <div className="loading-box">
              <div className="spinner"></div>
              <p>🤖 Generating documentation...</p>
              <p className="loading-text">Please wait, this may take 10-30 seconds</p>
            </div>
          )}

          {response && <ResponseDisplay data={response} />}
        </div>
      </main>

      <footer className="footer">
        <p>Docify © 2025 | Powered by Gemini AI & FastAPI</p>
      </footer>
    </div>
  );
}

export default App;
