import React from 'react';
import { runCode } from '../../services/api';
import './RunButton.css';

const RunButton = ({ code, language, inputData, isRunning, setIsRunning, onComplete }) => {
  const handleRun = async () => {
    if (!code.trim()) {
      onComplete({
        output: '',
        error: 'Please write some code before running.',
        success: false,
        execution_time: 0,
      });
      return;
    }

    setIsRunning(true);
    try {
      const result = await runCode(code, language, inputData || null);
      onComplete(result);
    } catch (error) {
      onComplete({
        output: '',
        error: `Error executing code: ${error.message}`,
        success: false,
        execution_time: 0,
      });
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <button
      className="run-button"
      onClick={handleRun}
      disabled={isRunning}
    >
      {isRunning ? (
        <>
          <span className="spinner"></span>
          Running...
        </>
      ) : (
        'Run Code'
      )}
    </button>
  );
};

export default RunButton;

