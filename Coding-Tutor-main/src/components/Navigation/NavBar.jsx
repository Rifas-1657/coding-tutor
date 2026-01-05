import React, { useState, useEffect } from 'react';
import EditMenu from './EditMenu';
import TerminalMenu from './TerminalMenu';
import RunMenu from './RunMenu';
import HelpMenu from './HelpMenu';
import LanguageSelector from '../Editor/LanguageSelector';
import ExerciseSelector from '../Editor/ExerciseSelector';
import './NavBar.css';

const NavBar = ({ 
  language, 
  onLanguageChange,
  exerciseId,
  onExerciseChange,
  editorRef,
  onTerminalToggle,
  terminalVisible,
  onRunCode,
  onCompileOnly,
  onCompileAndRun
}) => {
  const [activeMenu, setActiveMenu] = useState(null);

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Check for Ctrl/Cmd key
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const ctrlKey = isMac ? e.metaKey : e.ctrlKey;

      if (ctrlKey && !e.shiftKey && e.key === 'z') {
        e.preventDefault();
        if (editorRef?.current) {
          editorRef.current.trigger('', 'undo');
        }
      } else if (ctrlKey && e.key === 'y' || (ctrlKey && e.shiftKey && e.key === 'z')) {
        e.preventDefault();
        if (editorRef?.current) {
          editorRef.current.trigger('', 'redo');
        }
      } else if (ctrlKey && e.key === 'x') {
        e.preventDefault();
        document.execCommand('cut');
      } else if (ctrlKey && e.key === 'c') {
        e.preventDefault();
        document.execCommand('copy');
      } else if (ctrlKey && e.key === 'v') {
        e.preventDefault();
        document.execCommand('paste');
      } else if (ctrlKey && e.key === 'f') {
        e.preventDefault();
        if (editorRef?.current) {
          editorRef.current.trigger('', 'actions.find');
        }
      } else if (ctrlKey && e.key === 'h') {
        e.preventDefault();
        if (editorRef?.current) {
          editorRef.current.trigger('', 'actions.startFindReplace');
        }
      } else if (ctrlKey && e.key === '`') {
        e.preventDefault();
        onTerminalToggle();
      } else if (e.key === 'F5') {
        e.preventDefault();
        onRunCode();
      } else if (e.key === 'F7') {
        e.preventDefault();
        onCompileOnly();
      } else if (ctrlKey && e.key === 'F5') {
        e.preventDefault();
        onCompileAndRun();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [editorRef, onTerminalToggle, onRunCode, onCompileOnly, onCompileAndRun]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      setActiveMenu(null);
    };
    if (activeMenu) {
      setTimeout(() => window.addEventListener('click', handleClickOutside), 0);
      return () => window.removeEventListener('click', handleClickOutside);
    }
  }, [activeMenu]);

  const handleMenuClick = (menuName) => {
    setActiveMenu(activeMenu === menuName ? null : menuName);
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <EditMenu
          isActive={activeMenu === 'edit'}
          onClick={() => handleMenuClick('edit')}
          editorRef={editorRef}
        />
        <TerminalMenu
          isActive={activeMenu === 'terminal'}
          onClick={() => handleMenuClick('terminal')}
          terminalVisible={terminalVisible}
          onToggle={onTerminalToggle}
        />
        <RunMenu
          isActive={activeMenu === 'run'}
          onClick={() => handleMenuClick('run')}
          onCompile={onCompileOnly}
          onRun={onRunCode}
          onCompileAndRun={onCompileAndRun}
        />
        <HelpMenu
          isActive={activeMenu === 'help'}
          onClick={() => handleMenuClick('help')}
        />
      </div>
      <div className="navbar-right">
        <LanguageSelector
          language={language}
          onLanguageChange={onLanguageChange}
        />
        <ExerciseSelector
          language={language}
          exerciseId={exerciseId}
          onExerciseChange={onExerciseChange}
        />
      </div>
    </nav>
  );
};

export default NavBar;

