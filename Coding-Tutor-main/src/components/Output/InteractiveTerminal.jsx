import React, { useState, useEffect, useRef } from 'react';
import './InteractiveTerminal.css';

const InteractiveTerminal = ({ 
  visible, 
  onClose,
  onExecute,
  output = '',
  isExecuting = false,
  waitingForInput = false,
  inputPrompt = ''
}) => {
  const outputRef = useRef(null);

  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  if (!visible) return null;

  return (
    <div className="interactive-terminal-container">
      <div className="terminal-header">
        <span className="terminal-title">Terminal</span>
        <button className="terminal-close" onClick={onClose} title="Hide Terminal (Ctrl+`)">
          ×
        </button>
      </div>
      <div className="terminal-content">
        <div className="terminal-output" ref={outputRef}>
          {output || <span className="terminal-placeholder">Terminal output will appear here...</span>}
        </div>
      </div>
    </div>
  );
};

export default InteractiveTerminal;

