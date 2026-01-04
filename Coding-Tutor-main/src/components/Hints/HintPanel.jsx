import React from 'react';
import HintCard from './HintCard';
import './HintPanel.css';

const HintPanel = ({ hints }) => {
  if (!hints || hints.length === 0) {
    return (
      <div className="hint-panel">
        <div className="hint-placeholder">
          Click "Get Hint" to receive guidance on your code...
        </div>
      </div>
    );
  }

  return (
    <div className="hint-panel">
      <div className="hint-header">
        <h3>Hints ({hints.length})</h3>
      </div>
      <div className="hint-list">
        {hints.map((hint, index) => (
          <HintCard key={index} hint={hint} index={index + 1} />
        ))}
      </div>
    </div>
  );
};

export default HintPanel;


