import React, { useState, useCallback, useEffect, useRef } from 'react';
import './App.css';
import NavBar from './components/Navigation/NavBar';
import CodeEditor from './components/Editor/CodeEditor';
import ResizableTerminal from './components/Output/ResizableTerminal';
import Dashboard from './components/Dashboard/Dashboard';
import { WebSocketExecutionService } from './services/websocketService';
import { runCode } from './services/api';

function App() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('c');
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');
  const [hints, setHints] = useState([]);
  const [isRunning, setIsRunning] = useState(false);
  const [currentView, setCurrentView] = useState('editor');
  const [executionTime, setExecutionTime] = useState(0);
  const [stats, setStats] = useState({
    totalRuns: 0,
    successCount: 0,
    errorCount: 0,
    hintsRequested: 0,
  });
  
  // New state for redesigned UI
  const [terminalVisible, setTerminalVisible] = useState(false);
  const [terminalOutput, setTerminalOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [waitingForInput, setWaitingForInput] = useState(false);
  const [inputPrompt, setInputPrompt] = useState('');
  const editorRef = useRef(null);
  const wsServiceRef = useRef(null);

  // Initialize WebSocket service
  useEffect(() => {
    const wsService = new WebSocketExecutionService();
    
    const onOutput = (output) => {
      setTerminalOutput(prev => prev + output);
      setTerminalVisible(true);
    };
    
    const onError = (error) => {
      setTerminalOutput(prev => prev + '\n[ERROR] ' + error + '\n');
      setTerminalVisible(true);
      setError(error);
    };
    
    const onInputRequired = (prompt) => {
      setWaitingForInput(true);
      setInputPrompt(prompt || '> ');
    };
    
    const onComplete = (result) => {
      setIsExecuting(false);
      setWaitingForInput(false);
      setIsRunning(false);
      if (result && result.success !== undefined) {
        setStats(prev => ({
          ...prev,
          totalRuns: prev.totalRuns + 1,
          successCount: result.success ? prev.successCount + 1 : prev.successCount,
          errorCount: result.success ? prev.errorCount : prev.errorCount + 1,
        }));
      }
      // Auto-focus input if program is waiting for input (will be handled by terminal component)
    };
    
    wsService.connect(onOutput, onError, onInputRequired, onComplete);
    wsServiceRef.current = wsService;
    
    return () => {
      if (wsServiceRef.current) {
        wsServiceRef.current.disconnect();
      }
    };
  }, []);


  const handleCodeChange = useCallback((newCode) => {
    setCode(newCode);
  }, []);

  const handleLanguageChange = useCallback((newLanguage) => {
    setLanguage(newLanguage);
    setCode('');
    setOutput('');
    setTerminalOutput('');
    setError('');
    setHints([]);
  }, []);

  // Terminal execute handler (for WebSocket input)
  const handleTerminalExecute = useCallback((type, data) => {
    if (type === 'input' && wsServiceRef.current) {
      // Echo user input to terminal
      setTerminalOutput(prev => prev + data + '\n');
      wsServiceRef.current.sendInput(data);
      // Keep waitingForInput true - program may need more input
      // Input field will stay visible as long as isExecuting is true
    }
  }, []);


  // Execution handlers
  const handleRunCode = useCallback(() => {
    if (!code.trim()) {
      setTerminalOutput('Error: Please write some code before running.\n');
      setTerminalVisible(true);
      return;
    }
    
    setTerminalOutput('');
    setOutput('');
    setError('');
    setIsExecuting(true);
    setIsRunning(true);
    setTerminalVisible(true);
    
    // Use WebSocket for interactive execution
    if (wsServiceRef.current && wsServiceRef.current.isConnected()) {
      wsServiceRef.current.executeCode(code, language, null, false);
    } else {
      // Fallback to regular API if WebSocket not available
      handleRunCodeAPI();
    }
  }, [code, language]);

  const handleRunCodeAPI = async () => {
    setIsExecuting(true);
    setIsRunning(true);
    try {
      const result = await runCode(code, language, null);
      setTerminalOutput(result.output || '');
      setError(result.error || '');
      setOutput(result.output || '');
      setExecutionTime(result.execution_time || 0);
      setTerminalVisible(true);
      
      setStats(prev => ({
        ...prev,
        totalRuns: prev.totalRuns + 1,
        successCount: result.success ? prev.successCount + 1 : prev.successCount,
        errorCount: result.error ? prev.errorCount + 1 : prev.errorCount,
      }));
    } catch (error) {
      setTerminalOutput(`Error: ${error.message}\n`);
      setError(error.message);
      setTerminalVisible(true);
    } finally {
      setIsExecuting(false);
      setIsRunning(false);
    }
  };

  const handleCompileOnly = useCallback(() => {
    if (!code.trim()) {
      setTerminalOutput('Error: Please write some code before compiling.\n');
      setTerminalVisible(true);
      return;
    }
    
    // Only compile for languages that need it
    if (language === 'python') {
      setTerminalOutput('Python is an interpreted language - no compilation needed.\n');
      setTerminalVisible(true);
      return;
    }
    
    setTerminalOutput('');
    setOutput('');
    setError('');
    setIsExecuting(true);
    setTerminalVisible(true);
    
    // Use WebSocket for compile-only
    if (wsServiceRef.current && wsServiceRef.current.isConnected()) {
      wsServiceRef.current.executeCode(code, language, null, true);
    } else {
      setTerminalOutput('Error: WebSocket not connected. Please try again.\n');
      setIsExecuting(false);
    }
  }, [code, language]);

  const handleCompileAndRun = useCallback(() => {
    handleRunCode();
  }, [handleRunCode]);

  // Terminal handlers
  const handleTerminalToggle = useCallback(() => {
    setTerminalVisible(prev => !prev);
  }, []);

  return (
    <div className="app">
      <NavBar
        language={language}
        onLanguageChange={handleLanguageChange}
        editorRef={editorRef.current}
        onTerminalToggle={handleTerminalToggle}
        terminalVisible={terminalVisible}
        onRunCode={handleRunCode}
        onCompileOnly={handleCompileOnly}
        onCompileAndRun={handleCompileAndRun}
      />

      {currentView === 'editor' && (
        <div className="app-content">
          <ResizableTerminal
            visible={terminalVisible}
            onClose={() => setTerminalVisible(false)}
            output={terminalOutput + (error ? '\n[ERROR] ' + error : '')}
            onExecute={handleTerminalExecute}
            isExecuting={isExecuting || isRunning}
            waitingForInput={waitingForInput}
            inputPrompt={inputPrompt}
          >
            <div className="editor-view">
              <div className="editor-container">
                <CodeEditor
                  code={code}
                  language={language}
                  onChange={handleCodeChange}
                  editorRef={editorRef}
                />
              </div>
            </div>
          </ResizableTerminal>
        </div>
      )}

      {currentView === 'dashboard' && (
        <Dashboard stats={stats} />
      )}
    </div>
  );
}

export default App;
