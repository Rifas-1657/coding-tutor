import React, { useState, useEffect, useRef, useCallback } from 'react';
import InteractiveTerminal from './InteractiveTerminal';
import './ResizableTerminal.css';

const ResizableTerminal = ({ 
  visible, 
  onClose,
  output,
  onExecute,
  isExecuting,
  waitingForInput = false,
  inputPrompt = '',
  children
}) => {
  const [editorHeight, setEditorHeight] = useState(60); // percentage
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef(null);
  const dragStartY = useRef(0);
  const dragStartHeight = useRef(60);

  // Load saved height preference
  useEffect(() => {
    const savedHeight = localStorage.getItem('terminalEditorHeight');
    if (savedHeight) {
      setEditorHeight(parseFloat(savedHeight));
    }
  }, []);

  // Save height preference
  useEffect(() => {
    localStorage.setItem('terminalEditorHeight', editorHeight.toString());
  }, [editorHeight]);

  const handleMouseDown = useCallback((e) => {
    if (!visible) return;
    setIsDragging(true);
    dragStartY.current = e.clientY;
    dragStartHeight.current = editorHeight;
    e.preventDefault();
  }, [visible, editorHeight]);

  const handleMouseMove = useCallback((e) => {
    if (!isDragging || !containerRef.current) return;
    
    const container = containerRef.current;
    const containerHeight = container.offsetHeight;
    const deltaY = e.clientY - dragStartY.current;
    const deltaPercent = (deltaY / containerHeight) * 100;
    
    let newHeight = dragStartHeight.current - deltaPercent;
    
    // Constrain between 20% and 80%
    newHeight = Math.max(20, Math.min(80, newHeight));
    
    setEditorHeight(newHeight);
  }, [isDragging]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'ns-resize';
      document.body.style.userSelect = 'none';
      
      return () => {
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', handleMouseUp);
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
      };
    }
  }, [isDragging, handleMouseMove, handleMouseUp]);

  const terminalHeight = 100 - editorHeight;

  return (
    <div 
      ref={containerRef}
      className={`resizable-container ${visible ? 'terminal-visible' : ''}`}
    >
      <div 
        className="editor-area"
        style={{ flexBasis: visible ? `${editorHeight}%` : '100%', minHeight: '0' }}
      >
        {/* Editor content will be rendered here by parent */}
        {children}
      </div>
      
      {visible && (
        <>
          <div
            className={`resize-divider ${isDragging ? 'dragging' : ''}`}
            onMouseDown={handleMouseDown}
          >
            <div className="resize-handle"></div>
          </div>
          
          <div 
            className="terminal-area"
            style={{ flexBasis: `${terminalHeight}%`, minHeight: '0' }}
          >
            <InteractiveTerminal
              visible={true}
              onClose={onClose}
              output={output}
              onExecute={onExecute}
              isExecuting={isExecuting}
              waitingForInput={waitingForInput}
              inputPrompt={inputPrompt}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default ResizableTerminal;

