import React from 'react';
import { getHint } from '../../services/api';
import './HintButton.css';

const HintButton = ({ code, language, errorMessage, isLoading, setIsLoading, onHintReceived }) => {
  const handleGetHint = async () => {
    if (!code.trim()) {
      onHintReceived({ hints: [] });
      return;
    }

    setIsLoading(true);
    try {
      const result = await getHint(code, language, errorMessage);
      onHintReceived(result);
    } catch (error) {
      onHintReceived({
        hints: [{
          severity: 'logic',
          title: 'Error',
          description: `Failed to get hint: ${error.message}`,
          example: null,
        }],
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      className="hint-button"
      onClick={handleGetHint}
      disabled={isLoading}
    >
      {isLoading ? (
        <>
          <span className="spinner"></span>
          Analyzing...
        </>
      ) : (
        'Get Hint'
      )}
    </button>
  );
};

export default HintButton;


