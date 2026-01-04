import React, { useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import './CodeEditor.css';

const CodeEditor = ({ code, language, onChange, editorRef: externalRef }) => {
  const internalEditorRef = useRef(null);
  const editorRef = externalRef || internalEditorRef;

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
    
    // Configure editor options
    editor.updateOptions({
      fontSize: 14,
      minimap: { enabled: false },
      automaticLayout: true,
      bracketPairColorization: { enabled: true },
      formatOnPaste: true,
      formatOnType: true,
    });

    // Language-specific settings
    if (language === 'python') {
      monaco.languages.setLanguageConfiguration('python', {
        indentationRules: {
          increaseIndentPattern: /^\s*(def|class|if|elif|else|for|while|try|except|finally|with)\s.*:$/,
        },
      });
    }
  };

  const handleEditorChange = (value) => {
    if (onChange) {
      onChange(value || '');
    }
  };

  const getLanguageForMonaco = (lang) => {
    const langMap = {
      'c': 'c',
      'cpp': 'cpp',
      'python': 'python',
      'java': 'java',
    };
    return langMap[lang] || 'c';
  };

  return (
    <div className="code-editor-container">
      <Editor
        height="100%"
        theme="vs-dark"
        language={getLanguageForMonaco(language)}
        value={code}
        onChange={handleEditorChange}
        onMount={handleEditorDidMount}
        options={{
          selectOnLineNumbers: true,
          roundedSelection: false,
          readOnly: false,
          cursorStyle: 'line',
          automaticLayout: true,
          fontSize: 14,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          wordWrap: 'on',
        }}
      />
    </div>
  );
};

export default CodeEditor;


