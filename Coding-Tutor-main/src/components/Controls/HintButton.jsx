import React from 'react';
import './HintButton.css';

const HintButton = ({ onHintClick, isLoading }) => {
  const handleGetHint = () => {
    if (onHintClick) {
      onHintClick();
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
          Getting Hint...
        </>
      ) : (
        'Get Hint'
      )}
    </button>
  );
};

export default HintButton;


