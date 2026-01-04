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
  const [inputValue, setInputValue] = useState('');
  const outputRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-focus input when terminal becomes visible and program is waiting for input
  useEffect(() => {
    if (visible && (waitingForInput || isExecuting) && inputRef.current) {
      // Use setTimeout to ensure DOM is ready
      const timer = setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [visible, waitingForInput, isExecuting]);

  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  const handleInputSubmit = (e) => {
    e.preventDefault();
    // Only send input when user explicitly presses Enter
    if (isExecuting && onExecute && inputValue !== '') {
      // Send the input value
      onExecute('input', inputValue);
      setInputValue('');
      // Re-focus input after sending for next input
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 50);
    }
  };

  const handleKeyDown = (e) => {
    // Only submit on Enter key press
    if (e.key === 'Enter' && isExecuting && inputValue !== '') {
      handleInputSubmit(e);
    }
  };

  const clearTerminal = () => {
    setInputValue('');
    if (onExecute) {
      onExecute('clear', '');
    }
  };

  // Listen for clear terminal event
  useEffect(() => {
    const handleClear = () => clearTerminal();
    window.addEventListener('clearTerminal', handleClear);
    return () => window.removeEventListener('clearTerminal', handleClear);
  }, []);


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
        {(waitingForInput || isExecuting) && (
          <div className="terminal-input-container">
            <span className="terminal-prompt">{inputPrompt || '> '}</span>
            <form onSubmit={handleInputSubmit} className="terminal-input-form">
              <input
                ref={inputRef}
                type="text"
                className="terminal-input"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Enter input (press Enter to send)..."
                disabled={!isExecuting}
              />
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default InteractiveTerminal;

