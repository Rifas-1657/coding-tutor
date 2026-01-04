import React, { useState } from 'react';
import './InputArea.css';

const InputArea = ({ value, onChange }) => {
  const [collapsed, setCollapsed] = useState(true);

  return (
    <div className="input-area">
      <div className="input-area-header" onClick={() => setCollapsed(!collapsed)}>
        <span className="input-area-label">
          Program Input (if your code needs scanf/input/cin)
        </span>
        <span className="input-area-toggle">{collapsed ? '▼' : '▲'}</span>
      </div>
      {!collapsed && (
        <textarea
          className="input-area-textarea"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Enter input values, one per line&#10;Example:&#10;5&#10;10&#10;15"
          rows={4}
        />
      )}
    </div>
  );
};

export default InputArea;


