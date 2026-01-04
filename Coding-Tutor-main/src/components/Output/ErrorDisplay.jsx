import React from 'react';
import './ErrorDisplay.css';

const ErrorDisplay = ({ error }) => {
  if (!error) {
    return null;
  }

  // Parse error message for line numbers and error types
  const parseError = (errorText) => {
    const lines = errorText.split('\n');
    const parsedErrors = [];
    
    lines.forEach((line, index) => {
      // GCC/C++ error format: filename:line:column: error: message
      const gccMatch = line.match(/(\w+\.\w+):(\d+):(\d+):\s*(error|warning|note):\s*(.+)/);
      if (gccMatch) {
        parsedErrors.push({
          line: parseInt(gccMatch[2]),
          type: gccMatch[4],
          message: gccMatch[5],
          raw: line,
        });
        return;
      }
      
      // Python error format: File "filename", line X
      const pythonMatch = line.match(/File\s+["'](.+?)["'],\s+line\s+(\d+)/);
      if (pythonMatch) {
        const nextLine = lines[index + 1];
        if (nextLine) {
          parsedErrors.push({
            line: parseInt(pythonMatch[2]),
            type: 'error',
            message: nextLine.trim(),
            raw: line + '\n' + nextLine,
          });
        }
        return;
      }
      
      // Java error format: filename.java:line: error: message
      const javaMatch = line.match(/(\w+\.java):(\d+):\s*error:\s*(.+)/);
      if (javaMatch) {
        parsedErrors.push({
          line: parseInt(javaMatch[2]),
          type: 'error',
          message: javaMatch[3],
          raw: line,
        });
        return;
      }
    });
    
    return parsedErrors.length > 0 ? parsedErrors : [{ type: 'error', message: errorText, raw: errorText }];
  };

  const errors = parseError(error);

  return (
    <div className="error-display">
      {errors.map((err, index) => (
        <div key={index} className="error-item">
          {err.line && (
            <div className="error-header">
              <span className="error-line">Line {err.line}</span>
              <span className={`error-badge ${err.type}`}>
                {err.type.charAt(0).toUpperCase() + err.type.slice(1)}
              </span>
            </div>
          )}
          <div className="error-message">{err.message || err.raw}</div>
        </div>
      ))}
    </div>
  );
};

export default ErrorDisplay;


