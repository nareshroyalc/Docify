import React, { useState } from 'react';
import './DocumentationForm.css';

function DocumentationForm({ onSubmit, loading }) {
  const [topic, setTopic] = useState('');
  const [relatedTopics, setRelatedTopics] = useState(['', '', '']);
  const [priority, setPriority] = useState('medium');
  const [details, setDetails] = useState('');
  const [challenges, setChallenges] = useState('');

  const handleTopicChange = (e) => {
    setTopic(e.target.value);
  };

  const handleRelatedTopicChange = (index, value) => {
    const newTopics = [...relatedTopics];
    newTopics[index] = value;
    setRelatedTopics(newTopics);
  };

  const handleAddTopic = () => {
    setRelatedTopics([...relatedTopics, '']);
  };

  const handleRemoveTopic = (index) => {
    if (relatedTopics.length > 1) {
      setRelatedTopics(relatedTopics.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!topic.trim()) {
      alert('Please enter a topic');
      return;
    }

    const filteredTopics = relatedTopics.filter((t) => t.trim());

    onSubmit({
      topic: topic.trim(),
      related_topics: filteredTopics,
      priority: priority,
      details: details.trim(),
      challenges: challenges.trim(),
    });
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h2>📝 Document Your Work</h2>

      <div className="form-group">
        <label htmlFor="topic">Main Topic *</label>
        <input
          id="topic"
          type="text"
          value={topic}
          onChange={handleTopicChange}
          placeholder="e.g., LangChain Integration, FastAPI Development"
          disabled={loading}
          required
        />
        <p className="help-text">The main work topic you want to document</p>
      </div>

      <div className="form-row">
        <div className="form-group form-group-half">
          <label htmlFor="priority">Priority Level *</label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            disabled={loading}
            className="priority-select"
          >
            <option value="low">🟢 Low - Minimal Documentation</option>
            <option value="medium">🟡 Medium - Standard Documentation</option>
            <option value="high">🔴 High - Detailed Documentation</option>
          </select>
          <p className="help-text">Higher priority adds more detail</p>
        </div>

        <div className="form-group form-group-half">
          <label htmlFor="details">Additional Details (Optional)</label>
          <input
            id="details"
            type="text"
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            placeholder="e.g., Reduced latency by 40%, Fixed critical bugs"
            disabled={loading}
          />
          <p className="help-text">Specific accomplishments or context</p>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="challenges">Challenges Faced (Optional)</label>
        <textarea
          id="challenges"
          value={challenges}
          onChange={(e) => setChallenges(e.target.value)}
          placeholder="e.g., Encountered memory issues with large datasets, API rate limiting caused delays"
          disabled={loading}
          rows="3"
          className="form-textarea"
        />
        <p className="help-text">Any obstacles or issues you encountered</p>
      </div>

      <div className="form-group">
        <label>Related Topics (Optional)</label>
        <div className="related-topics">
          {relatedTopics.map((relatedTopic, index) => (
            <div key={index} className="related-topic-item">
              <input
                type="text"
                value={relatedTopic}
                onChange={(e) => handleRelatedTopicChange(index, e.target.value)}
                placeholder={`Subtopic ${index + 1} (optional)`}
                disabled={loading}
              />
              {relatedTopics.length > 1 && (
                <button
                  type="button"
                  className="btn-remove"
                  onClick={() => handleRemoveTopic(index)}
                  disabled={loading}
                >
                  ✕
                </button>
              )}
            </div>
          ))}
        </div>
        <button
          type="button"
          className="btn-add-topic"
          onClick={handleAddTopic}
          disabled={loading || relatedTopics.length >= 10}
        >
          + Add Related Topic
        </button>
      </div>

      <button
        type="submit"
        className="btn-submit"
        disabled={loading || !topic.trim()}
      >
        {loading ? '⏳ Generating...' : '🚀 Generate Documentation'}
      </button>

      <p className="form-note">
        ℹ️ Documentation will be generated and automatically written to your Google Doc
      </p>
    </form>
  );
}

export default DocumentationForm;
