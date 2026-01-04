import React from 'react';
import './Menu.css';

const TerminalMenu = ({ isActive, onClick, terminalVisible, onToggle }) => {
  return (
    <div className="menu-item">
      <button className="menu-button" onClick={onClick}>
        Terminal
      </button>
      {isActive && (
        <div className="menu-dropdown">
          <div className="menu-item" onClick={onToggle}>
            <span>{terminalVisible ? 'Hide Terminal' : 'Show Terminal'}</span>
            <span className="menu-shortcut">Ctrl+`</span>
          </div>
          <div className="menu-divider"></div>
          <div className="menu-item" onClick={() => {
            // Clear terminal - this will be wired up later
            const event = new CustomEvent('clearTerminal');
            window.dispatchEvent(event);
          }}>
            <span>Clear Terminal</span>
            <span className="menu-shortcut">Ctrl+K</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TerminalMenu;

