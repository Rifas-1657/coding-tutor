import React, { useState } from 'react';
import './HintCard.css';

const HintCard = ({ hint, index }) => {
  const [expanded, setExpanded] = useState(false);

  const getSeverityColor = (severity) => {
    const colors = {
      syntax: '#f48771',
      logic: '#cca700',
      runtime: '#f48771',
      edge_case: '#569cd6',
    };
    return colors[severity] || '#858585';
  };

  const getSeverityLabel = (severity) => {
    return severity.charAt(0).toUpperCase() + severity.slice(1).replace('_', ' ');
  };

  return (
    <div className="hint-card">
      <div className="hint-card-header">
        <div className="hint-number">Hint {index}</div>
        <span
          className="severity-badge"
          style={{ backgroundColor: getSeverityColor(hint.severity) }}
        >
          {getSeverityLabel(hint.severity)}
        </span>
      </div>
      <div className="hint-title">{hint.title}</div>
      <div className="hint-description">{hint.description}</div>
      {hint.example && (
        <div className="hint-example">
          <div className="example-label">Example:</div>
          <pre className="example-code">{hint.example}</pre>
        </div>
      )}
      {expanded && hint.description && (
        <div className="hint-expanded">
          <p>{hint.description}</p>
        </div>
      )}
      {hint.description && hint.description.length > 150 && (
        <button
          className="expand-button"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? 'Show Less' : 'Show More'}
        </button>
      )}
    </div>
  );
};

export default HintCard;


