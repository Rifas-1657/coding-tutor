import React, { useState } from 'react';
import './Menu.css';

const EditMenu = ({ isActive, onClick, editorRef }) => {
  const [showPreferences, setShowPreferences] = useState(false);

  const handleFontSizeChange = (size) => {
    if (editorRef?.current) {
      editorRef.current.updateOptions({ fontSize: size });
      localStorage.setItem('editorFontSize', size.toString());
    }
  };

  const handleTabSizeChange = (size) => {
    if (editorRef?.current) {
      editorRef.current.updateOptions({ tabSize: size });
      localStorage.setItem('editorTabSize', size.toString());
    }
  };

  const handleThemeChange = (theme) => {
    // This would require Monaco theme change - simplified here
    localStorage.setItem('editorTheme', theme);
    if (editorRef?.current) {
      // Theme change would be handled by Monaco Editor instance
    }
  };

  return (
    <div className="menu-item">
      <button className="menu-button" onClick={onClick}>
        Edit
      </button>
      {isActive && (
        <div className="menu-dropdown">
          <div className="menu-item" onClick={() => editorRef?.current?.trigger('', 'undo')}>
            <span>Undo</span>
            <span className="menu-shortcut">Ctrl+Z</span>
          </div>
          <div className="menu-item" onClick={() => editorRef?.current?.trigger('', 'redo')}>
            <span>Redo</span>
            <span className="menu-shortcut">Ctrl+Y</span>
          </div>
          <div className="menu-divider"></div>
          <div className="menu-item" onClick={() => document.execCommand('cut')}>
            <span>Cut</span>
            <span className="menu-shortcut">Ctrl+X</span>
          </div>
          <div className="menu-item" onClick={() => document.execCommand('copy')}>
            <span>Copy</span>
            <span className="menu-shortcut">Ctrl+C</span>
          </div>
          <div className="menu-item" onClick={() => document.execCommand('paste')}>
            <span>Paste</span>
            <span className="menu-shortcut">Ctrl+V</span>
          </div>
          <div className="menu-divider"></div>
          <div className="menu-item" onClick={() => editorRef?.current?.trigger('', 'actions.find')}>
            <span>Find</span>
            <span className="menu-shortcut">Ctrl+F</span>
          </div>
          <div className="menu-item" onClick={() => editorRef?.current?.trigger('', 'actions.startFindReplace')}>
            <span>Replace</span>
            <span className="menu-shortcut">Ctrl+H</span>
          </div>
          <div className="menu-divider"></div>
          <div
            className="menu-item menu-submenu-trigger"
            onMouseEnter={() => setShowPreferences(true)}
            onMouseLeave={() => setShowPreferences(false)}
          >
            <span>Preferences</span>
            <span>▶</span>
            {showPreferences && (
              <div className="menu-submenu menu-submenu-right">
                <div className="menu-item menu-header">Font Size</div>
                <div className="menu-item menu-sub-item" onClick={() => handleFontSizeChange(12)}>Small (12px)</div>
                <div className="menu-item menu-sub-item" onClick={() => handleFontSizeChange(14)}>Medium (14px)</div>
                <div className="menu-item menu-sub-item" onClick={() => handleFontSizeChange(16)}>Large (16px)</div>
                <div className="menu-item menu-sub-item" onClick={() => handleFontSizeChange(18)}>Extra Large (18px)</div>
                <div className="menu-divider"></div>
                <div className="menu-item menu-header">Tab Size</div>
                <div className="menu-item menu-sub-item" onClick={() => handleTabSizeChange(2)}>2 spaces</div>
                <div className="menu-item menu-sub-item" onClick={() => handleTabSizeChange(4)}>4 spaces</div>
                <div className="menu-item menu-sub-item" onClick={() => handleTabSizeChange(8)}>8 spaces</div>
                <div className="menu-divider"></div>
                <div className="menu-item menu-header">Theme</div>
                <div className="menu-item menu-sub-item" onClick={() => handleThemeChange('light')}>Light</div>
                <div className="menu-item menu-sub-item" onClick={() => handleThemeChange('dark')}>Dark</div>
                <div className="menu-item menu-sub-item" onClick={() => handleThemeChange('high-contrast')}>High Contrast</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default EditMenu;

