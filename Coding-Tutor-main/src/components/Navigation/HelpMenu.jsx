import React, { useState } from 'react';
import './Menu.css';

const HelpMenu = ({ isActive, onClick }) => {
  const [showModal, setShowModal] = useState(null);

  return (
    <>
      <div className="menu-item">
        <button className="menu-button" onClick={onClick}>
          Help
        </button>
        {isActive && (
          <div className="menu-dropdown">
            <div className="menu-item" onClick={() => setShowModal('documentation')}>
              <span>Documentation</span>
            </div>
            <div className="menu-item" onClick={() => setShowModal('shortcuts')}>
              <span>Keyboard Shortcuts</span>
            </div>
            <div className="menu-divider"></div>
            <div className="menu-item" onClick={() => setShowModal('report')}>
              <span>Report Issue</span>
            </div>
            <div className="menu-item" onClick={() => setShowModal('about')}>
              <span>About</span>
            </div>
          </div>
        )}
      </div>
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>
                {showModal === 'documentation' && 'Documentation'}
                {showModal === 'shortcuts' && 'Keyboard Shortcuts'}
                {showModal === 'report' && 'Report Issue'}
                {showModal === 'about' && 'About'}
              </h2>
              <button className="modal-close" onClick={() => setShowModal(null)}>×</button>
            </div>
            <div className="modal-body">
              {showModal === 'documentation' && (
                <div>
                  <h3>Getting Started</h3>
                  <p>Welcome to Coding Tutor! This application helps you learn programming by providing a safe environment to write and run code.</p>
                  <h3>Basic Usage</h3>
                  <ul>
                    <li>Select a language from the dropdown</li>
                    <li>Write your code in the editor</li>
                    <li>Click Run or press F5 to execute your code</li>
                    <li>View output in the terminal panel</li>
                  </ul>
                  <h3>Features</h3>
                  <ul>
                    <li><strong>Interactive Terminal:</strong> Type input directly when your program needs it</li>
                    <li><strong>AI Tutor:</strong> Get guidance without spoilers (Click AI Tutor button)</li>
                    <li><strong>Hints:</strong> Receive contextual hints for errors</li>
                  </ul>
                </div>
              )}
              {showModal === 'shortcuts' && (
                <div>
                  <h3>File Operations</h3>
                  <ul>
                    <li><kbd>Ctrl+N</kbd> New File</li>
                    <li><kbd>Ctrl+O</kbd> Open File</li>
                    <li><kbd>Ctrl+S</kbd> Save File</li>
                    <li><kbd>Ctrl+Shift+S</kbd> Save As</li>
                  </ul>
                  <h3>Editing</h3>
                  <ul>
                    <li><kbd>Ctrl+Z</kbd> Undo</li>
                    <li><kbd>Ctrl+Y</kbd> Redo</li>
                    <li><kbd>Ctrl+X</kbd> Cut</li>
                    <li><kbd>Ctrl+C</kbd> Copy</li>
                    <li><kbd>Ctrl+V</kbd> Paste</li>
                    <li><kbd>Ctrl+F</kbd> Find</li>
                    <li><kbd>Ctrl+H</kbd> Replace</li>
                  </ul>
                  <h3>Terminal & Execution</h3>
                  <ul>
                    <li><kbd>Ctrl+`</kbd> Toggle Terminal</li>
                    <li><kbd>Ctrl+K</kbd> Clear Terminal</li>
                    <li><kbd>F5</kbd> Run</li>
                    <li><kbd>F7</kbd> Compile</li>
                    <li><kbd>Ctrl+F5</kbd> Compile and Run</li>
                  </ul>
                  <h3>AI Tutor</h3>
                  <ul>
                    <li><kbd>Ctrl+/</kbd> Toggle AI Tutor Panel</li>
                  </ul>
                </div>
              )}
              {showModal === 'report' && (
                <div>
                  <p>To report an issue:</p>
                  <ul>
                    <li>Describe the problem you encountered</li>
                    <li>Include steps to reproduce</li>
                    <li>Mention your operating system and language</li>
                  </ul>
                  <p>Contact: support@codingtutor.app</p>
                </div>
              )}
              {showModal === 'about' && (
                <div>
                  <h3>Coding Tutor</h3>
                  <p>Version 1.0.0</p>
                  <p>A desktop application for learning programming with AI-assisted guidance.</p>
                  <p>Built with Electron, React, and FastAPI.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default HelpMenu;

