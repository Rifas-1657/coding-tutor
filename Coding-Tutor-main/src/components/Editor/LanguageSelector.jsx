import React from 'react';
import './LanguageSelector.css';

const LanguageSelector = ({ language, onLanguageChange }) => {
  const languages = [
    { value: 'c', label: 'C' },
    { value: 'cpp', label: 'C++' },
    { value: 'python', label: 'Python' },
    { value: 'java', label: 'Java' },
  ];

  const handleChange = (e) => {
    if (onLanguageChange) {
      onLanguageChange(e.target.value);
    }
  };

  return (
    <div className="language-selector">
      <label htmlFor="language-select">Language: </label>
      <select
        id="language-select"
        value={language}
        onChange={handleChange}
        className="language-dropdown"
      >
        {languages.map((lang) => (
          <option key={lang.value} value={lang.value}>
            {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;


