# Integration Guide - UI/UX Redesign

This guide explains how to integrate all the new components into `App.js`.

## Current Status

✅ All components have been created
✅ Backend endpoints are ready
⏳ **App.js needs to be updated to use new components**

## Step-by-Step Integration

### 1. Update App.js Imports

Replace old imports with new ones:

```jsx
// Remove these:
import RunButton from './components/Controls/RunButton';
import HintButton from './components/Controls/HintButton';
import FileControls from './components/Controls/FileControls';
import InputArea from './components/Controls/InputArea';
import OutputPanel from './components/Output/OutputPanel';
import ErrorDisplay from './components/Output/ErrorDisplay';
import HintPanel from './components/Hints/HintPanel';

// Add these:
import NavBar from './components/Navigation/NavBar';
import CodeEditor from './components/Editor/CodeEditor';
import ResizableTerminal from './components/Output/ResizableTerminal';
import AITutorPanel from './components/AITutor/AITutorPanel';
import { WebSocketExecutionService } from './services/websocketService';
import { listFilesFromStorage } from './services/fileStorage';
```

### 2. Update App State

Add new state variables:

```jsx
const [terminalVisible, setTerminalVisible] = useState(false);
const [aiTutorOpen, setAITutorOpen] = useState(false);
const [terminalOutput, setTerminalOutput] = useState('');
const [isExecuting, setIsExecuting] = useState(false);
const [editorRef, setEditorRef] = useState(null);
const [recentFiles, setRecentFiles] = useState([]);
const wsServiceRef = useRef(null);
```

### 3. Initialize WebSocket Service

```jsx
useEffect(() => {
  const wsService = new WebSocketExecutionService();
  
  wsService.connect(
    (output) => {
      setTerminalOutput(prev => prev + output);
      setTerminalVisible(true);
    },
    (error) => {
      setTerminalOutput(prev => prev + '\n[ERROR] ' + error);
      setTerminalVisible(true);
    },
    (prompt) => {
      // Handle input required
      // This will be handled by InteractiveTerminal
    },
    (result) => {
      setIsExecuting(false);
      // Execution complete
    }
  );
  
  wsServiceRef.current = wsService;
  
  return () => {
    wsService.disconnect();
  };
}, []);
```

### 4. Load Recent Files

```jsx
useEffect(() => {
  loadRecentFiles();
}, []);

const loadRecentFiles = async () => {
  try {
    const files = await listFilesFromStorage();
    setRecentFiles(files);
  } catch (error) {
    console.error('Error loading recent files:', error);
  }
};
```

### 5. Update Code Editor

```jsx
<CodeEditor
  code={code}
  language={language}
  onChange={handleCodeChange}
  editorRef={editorRef}
/>
```

### 6. Replace Navigation

Replace the old navbar with:

```jsx
<NavBar
  language={language}
  onLanguageChange={handleLanguageChange}
  onNewFile={handleNewFile}
  onOpenFile={handleOpenFile}
  onSaveFile={handleSaveFile}
  onSaveAsFile={handleSaveAsFile}
  recentFiles={recentFiles}
  onLoadRecentFile={handleLoadRecentFile}
  editorRef={editorRef}
  onTerminalToggle={() => setTerminalVisible(!terminalVisible)}
  terminalVisible={terminalVisible}
  onRunCode={handleRunCode}
  onCompileOnly={handleCompileOnly}
  onCompileAndRun={handleCompileAndRun}
  onAITutorToggle={() => setAITutorOpen(!aiTutorOpen)}
  aiTutorOpen={aiTutorOpen}
/>
```

### 7. Update Layout Structure

Replace the old layout with:

```jsx
<div className="app">
  <NavBar ... />
  
  <div className="app-content">
    <ResizableTerminal
      visible={terminalVisible}
      onClose={() => setTerminalVisible(false)}
      output={terminalOutput}
      onExecute={handleTerminalExecute}
      isExecuting={isExecuting}
    >
      <div className="editor-view">
        <CodeEditor ... />
      </div>
    </ResizableTerminal>
  </div>
  
  <AITutorPanel
    isOpen={aiTutorOpen}
    onClose={() => setAITutorOpen(false)}
    code={code}
    language={language}
  />
</div>
```

### 8. Implement Handler Functions

```jsx
const handleRunCode = () => {
  if (!code.trim()) return;
  
  setTerminalOutput('');
  setIsExecuting(true);
  setTerminalVisible(true);
  
  if (wsServiceRef.current) {
    wsServiceRef.current.executeCode(code, language);
  }
};

const handleTerminalExecute = (type, data) => {
  if (type === 'input' && wsServiceRef.current) {
    wsServiceRef.current.sendInput(data);
  }
};

const handleNewFile = () => {
  if (code.trim() && window.confirm('Unsaved changes will be lost. Continue?')) {
    setCode('');
    setTerminalOutput('');
    setError('');
  } else if (!code.trim()) {
    setCode('');
  }
};

// Similar handlers for other menu actions...
```

## Important Notes

1. **Remove InputArea**: The separate input box is no longer needed - input is handled in the terminal.

2. **Terminal Visibility**: Terminal is hidden by default. It shows automatically when code runs or user toggles it.

3. **WebSocket Connection**: Ensure backend WebSocket endpoint is accessible. In development, it should be `ws://localhost:8000/ws/execute`.

4. **Editor Ref**: The editor ref needs to be passed down so menu actions (undo, redo, find) can work.

5. **ResizableTerminal Structure**: The `ResizableTerminal` component expects its children to be the editor area. It wraps both editor and terminal.

## Testing Checklist

After integration, test:

- [ ] Navigation menus open/close correctly
- [ ] Keyboard shortcuts work
- [ ] Terminal shows/hides correctly
- [ ] Terminal resize works smoothly
- [ ] Code execution via WebSocket works
- [ ] Interactive input in terminal works
- [ ] AI Tutor panel slides in/out
- [ ] Hint Mode works
- [ ] AI Tutor chat works
- [ ] Recent files load correctly
- [ ] File operations work
- [ ] Preferences (font size, theme) apply correctly

## Troubleshooting

**WebSocket not connecting:**
- Check backend is running on port 8000
- Verify WebSocket endpoint is accessible
- Check browser console for connection errors

**Terminal not showing:**
- Check `terminalVisible` state is set to true
- Verify `ResizableTerminal` receives `visible={true}`

**Menu actions not working:**
- Ensure `editorRef` is properly set
- Check Monaco Editor is mounted before menu actions

**AI Tutor not responding:**
- Verify backend AI tutor endpoint is working
- Check network tab for API calls
- Currently uses placeholder responses (needs LLM integration)

