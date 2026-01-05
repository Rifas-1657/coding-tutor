import React, { useState, useCallback, useRef } from 'react';
import './App.css';
import NavBar from './components/Navigation/NavBar';
import CodeEditor from './components/Editor/CodeEditor';
import ExerciseSelector from './components/Editor/ExerciseSelector';
import ResizableTerminal from './components/Output/ResizableTerminal';
import Dashboard from './components/Dashboard/Dashboard';
import HintButton from './components/Controls/HintButton';
import InputArea from './components/Controls/InputArea';
import { runCode, getHint } from './services/api';

function App() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('c');
  const [exerciseId, setExerciseId] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [currentView, setCurrentView] = useState('editor');
  const [stats, setStats] = useState({
    totalRuns: 0,
    successCount: 0,
    errorCount: 0,
    hintsRequested: 0,
  });
  
  // Lab practice mode state
  const [terminalVisible, setTerminalVisible] = useState(true);
  const [terminalOutput, setTerminalOutput] = useState('');
  const [hintAvailable, setHintAvailable] = useState(false);
  const [hintContent, setHintContent] = useState('');
  const [isLoadingHint, setIsLoadingHint] = useState(false);
  const [lastEvaluation, setLastEvaluation] = useState(null);
  const [userInput, setUserInput] = useState('');
  const editorRef = useRef(null);


  const handleCodeChange = useCallback((newCode) => {
    setCode(newCode);
  }, []);

  const handleLanguageChange = useCallback((newLanguage) => {
    setLanguage(newLanguage);
    setExerciseId('');
    setCode('');
    setOutput('');
    setTerminalOutput('');
    setError('');
    setHintAvailable(false);
    setLastEvaluation(null);
    setUserInput('');
  }, []);

  const handleExerciseChange = useCallback((newExerciseId) => {
    setExerciseId(newExerciseId);
    setHintAvailable(false);
    setLastEvaluation(null);
  }, []);


  const handleRunCode = useCallback(async () => {
    if (!code.trim()) {
      setTerminalOutput('Error: Please write some code before running.\n');
      setTerminalVisible(true);
      return;
    }
    
    if (!exerciseId) {
      setTerminalOutput('Error: Please select an exercise first.\n\nAvailable exercises should appear in the dropdown when you select a language.\nIf no exercises appear, check:\n1. Backend server is running on http://localhost:8000\n2. Browser console for errors\n3. Network tab for API requests\n');
      setTerminalVisible(true);
      return;
    }
    
    setTerminalOutput('Running code...\n');
    setOutput('');
    setError('');
    setIsRunning(true);
    setTerminalVisible(true);
    setHintAvailable(false);
    setLastEvaluation(null);
    
    try {
      const result = await runCode(code, language, exerciseId, userInput);
      setLastEvaluation(result);
      
      let outputText = '';
      if (result.success) {
        outputText = result.output || '';
        if (result.output) {
          outputText += '\n';
        }
      } else {
        outputText = `Error: ${result.error || 'Execution failed'}\n`;
        if (result.output) {
          outputText += `Output:\n${result.output}\n`;
        }
      }
      
      setTerminalOutput(outputText);
      setOutput(outputText);
      
      // Show hint button if there's an error
      if (!result.success || result.error) {
        setHintAvailable(true);
      } else {
        setHintAvailable(false);
        setHintContent('');
      }
      
      setStats(prev => ({
        ...prev,
        totalRuns: prev.totalRuns + 1,
        successCount: result.success ? prev.successCount + 1 : prev.successCount,
        errorCount: !result.success ? prev.errorCount + 1 : prev.errorCount,
      }));
    } catch (error) {
      setTerminalOutput(`Error: ${error.message}\n`);
      setError(error.message);
      setHintAvailable(false);
    } finally {
      setIsRunning(false);
    }
  }, [code, language, exerciseId]);

  const handleCompileOnly = useCallback(() => {
    setTerminalOutput('Compile-only mode not available. Use Run to execute code.\n');
    setTerminalVisible(true);
  }, []);

  const handleCompileAndRun = useCallback(() => {
    handleRunCode();
  }, [handleRunCode]);

  const handleHintRequest = useCallback(async () => {
    if (!lastEvaluation || !exerciseId) {
      return;
    }
    
    setIsLoadingHint(true);
    try {
      const errorMessage = lastEvaluation.error_type 
        ? `${lastEvaluation.error_type}: ${lastEvaluation.error || 'Execution failed'}`
        : `Error: ${lastEvaluation.error || 'Execution failed'}`;
      
      const result = await getHint(language, exerciseId, errorMessage, '');
      setHintContent(result.hint);
      setStats(prev => ({
        ...prev,
        hintsRequested: prev.hintsRequested + 1,
      }));
    } catch (error) {
      setHintContent(`Error getting hint: ${error.message}`);
    } finally {
      setIsLoadingHint(false);
    }
  }, [lastEvaluation, language, exerciseId]);

  // Terminal handlers
  const handleTerminalToggle = useCallback(() => {
    setTerminalVisible(prev => !prev);
  }, []);

  return (
    <div className="app">
      <NavBar
        language={language}
        onLanguageChange={handleLanguageChange}
        exerciseId={exerciseId}
        onExerciseChange={handleExerciseChange}
        editorRef={editorRef.current}
        onTerminalToggle={handleTerminalToggle}
        terminalVisible={terminalVisible}
        onRunCode={handleRunCode}
        onCompileOnly={handleCompileOnly}
        onCompileAndRun={handleCompileAndRun}
      />

      {currentView === 'editor' && (
        <div className="app-content">
          <div className="lab-controls" style={{ padding: '10px', display: 'flex', gap: '10px', alignItems: 'center', justifyContent: 'flex-end' }}>
            {hintAvailable && (
              <HintButton
                onHintClick={handleHintRequest}
                isLoading={isLoadingHint}
              />
            )}
          </div>
          <ResizableTerminal
            visible={terminalVisible}
            onClose={() => setTerminalVisible(false)}
            output={terminalOutput + (error ? '\n[ERROR] ' + error : '') + (hintContent ? '\n\n--- HINT ---\n' + hintContent : '')}
            onExecute={() => {}}
            isExecuting={isRunning}
            waitingForInput={false}
            inputPrompt=""
          >
            <div className="editor-view">
              <div className="editor-container">
                <CodeEditor
                  code={code}
                  language={language}
                  onChange={handleCodeChange}
                  editorRef={editorRef}
                />
                <InputArea
                  value={userInput}
                  onChange={setUserInput}
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
