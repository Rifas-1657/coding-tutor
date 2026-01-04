import React from 'react';
import './OutputPanel.css';

const OutputPanel = ({ output, executionTime }) => {
  return (
    <div className="output-panel">
      {output && (
        <div className="output-content">
          <pre className="output-text">{output}</pre>
        </div>
      )}
      {executionTime > 0 && (
        <div className="execution-time">
          Execution time: {executionTime.toFixed(3)}s
        </div>
      )}
      {!output && executionTime === 0 && (
        <div className="output-placeholder">
          Output will appear here after running your code...
        </div>
      )}
    </div>
  );
};

export default OutputPanel;


