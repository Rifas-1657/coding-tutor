import React from 'react';
import './Menu.css';

const RunMenu = ({ isActive, onClick, onCompile, onRun, onCompileAndRun }) => {
  return (
    <div className="menu-item">
      <button className="menu-button" onClick={onClick}>
        Run
      </button>
      {isActive && (
        <div className="menu-dropdown">
          <div className="menu-item" onClick={onCompile}>
            <span>Compile</span>
            <span className="menu-shortcut">F7</span>
          </div>
          <div className="menu-item" onClick={onRun}>
            <span>Run</span>
            <span className="menu-shortcut">F5</span>
          </div>
          <div className="menu-item" onClick={onCompileAndRun}>
            <span>Compile and Run</span>
            <span className="menu-shortcut">Ctrl+F5</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default RunMenu;

