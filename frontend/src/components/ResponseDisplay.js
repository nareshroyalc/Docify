import React from 'react';
import './ResponseDisplay.css';

function ResponseDisplay({ data }) {
  if (!data) return null;

  const renderAchievements = (achievements) => {
    if (!achievements || achievements.length === 0) return null;
    return (
      <div className="content-section">
        <h4>✅ Achievements</h4>
        <ul className="list">
          {achievements.map((achievement, idx) => (
            <li key={idx}>{achievement}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderTechnical = (technical) => {
    if (!technical) return null;
    const { approach, technologies, key_points } = technical;
    if (!approach && (!technologies || technologies.length === 0) && (!key_points || key_points.length === 0)) {
      return null;
    }
    return (
      <div className="content-section">
        <h4>🔧 Technical Implementation</h4>
        {approach && <p><strong>Approach:</strong> {approach}</p>}
        {technologies && technologies.length > 0 && (
          <div>
            <strong>Technologies:</strong>
            <div className="tech-tags">
              {technologies.map((tech, idx) => (
                <span key={idx} className="tech-tag">{tech}</span>
              ))}
            </div>
          </div>
        )}
        {key_points && key_points.length > 0 && (
          <div>
            <strong>Key Points:</strong>
            <ul className="list">
              {key_points.map((point, idx) => (
                <li key={idx}>{point}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderChallenges = (challenges) => {
    if (!challenges || challenges.length === 0) return null;
    return (
      <div className="content-section">
        <h4>⚠️ Challenges</h4>
        {challenges.map((challenge, idx) => (
          <div key={idx} className="challenge-item">
            <p><strong>Issue:</strong> {challenge.issue}</p>
            {challenge.resolution && (
              <p><strong>Resolution:</strong> {challenge.resolution}</p>
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderNextSteps = (nextSteps) => {
    if (!nextSteps || nextSteps.length === 0) return null;
    return (
      <div className="content-section">
        <h4>➡️ Next Steps</h4>
        <ul className="list">
          {nextSteps.map((step, idx) => (
            <li key={idx}>{step}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderTags = (tags) => {
    if (!tags || tags.length === 0) return null;
    return (
      <div className="content-section">
        <h4>🏷️ Tags</h4>
        <div className="tags">
          {tags.map((tag, idx) => (
            <span key={idx} className="tag">{tag}</span>
          ))}
        </div>
      </div>
    );
  };

  const renderMetrics = (metrics) => {
    if (!metrics) return null;

    return (
      <div className="metrics-section">
        <h4>📊 Generation Metrics</h4>
        <div className="metrics-grid">
          <div className="metric-card">
            <span className="metric-label">Correctness</span>
            <span className="metric-value">{(metrics.confidence_score * 100).toFixed(0)}%</span>
          </div>
          <div className="metric-card">
            <span className="metric-label">Generation Time</span>
            <span className="metric-value">{metrics.generation_time}s</span>
          </div>
        </div>
      </div>
    );
  };

  const structured = data.structured || {};
  const priority = structured.priority || 'unknown';
  const priorityEmoji = { low: '🟢', medium: '🟡', high: '🔴' }[priority] || '⚪';

  return (
    <div className="response-container">
      <div className={`response-box ${data.success ? 'success' : 'error'}`}>
        <div className="response-header">
          <h3>{data.success ? '✅ Success!' : '⚠️ Error'}</h3>
          <p className="response-message">{data.message}</p>
        </div>

        {data.success && (
          <div className="response-content">
            <div className="info-section">
              <div className="priority-badge">
                {priorityEmoji} {priority.toUpperCase()}
              </div>
              {data.doc_url && (
                <a href={data.doc_url} target="_blank" rel="noopener noreferrer" className="doc-link">
                  📄 Open in Google Docs →
                </a>
              )}
              {data.timestamp && (
                <span className="timestamp">⏰ {data.timestamp}</span>
              )}
            </div>

            {structured && Object.keys(structured).length > 0 && (
              <div className="preview-section">
                {structured.title && (
                  <h2 className="doc-title">{structured.title}</h2>
                )}

                {structured.summary && (
                  <div className="content-section summary-section">
                    <h4>📝 Summary</h4>
                    <p>{structured.summary}</p>
                  </div>
                )}

                {structured.task_description && (
                  <div className="content-section">
                    <h4>📋 Task Description</h4>
                    <p>{structured.task_description}</p>
                  </div>
                )}

                {renderAchievements(structured.achievements)}
                {renderTechnical(structured.technical_implementation)}
                {renderChallenges(structured.challenges)}
                {renderNextSteps(structured.next_steps)}
                {renderTags(structured.tags)}

                {data.metrics && renderMetrics(data.metrics)}
              </div>
            )}
          </div>
        )}

        {!data.success && (
          <div className="error-details">
            <p>{data.error || 'An error occurred'}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResponseDisplay;
