// Dual-mode file operations - works in both Electron and browser

export const saveFile = async (content, defaultPath = null) => {
  // Check if running in Electron
  if (window.electronAPI && window.electronAPI.saveFile) {
    try {
      const result = await window.electronAPI.saveFile(content, defaultPath);
      return result;
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  // Browser fallback using File System Access API
  if ('showSaveFilePicker' in window) {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: defaultPath || 'untitled.c',
        types: [{
          description: 'Code Files',
          accept: {
            'text/plain': ['.c', '.cpp', '.py', '.java']
          }
        }]
      });
      
      const writable = await handle.createWritable();
      await writable.write(content);
      await writable.close();
      
      return { success: true, path: handle.name };
    } catch (err) {
      if (err.name === 'AbortError') {
        return { success: false, canceled: true };
      }
      return { success: false, error: err.message };
    }
  }
  
  // Fallback for browsers without File System Access API
  // Use download link approach
  try {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = defaultPath || 'untitled.c';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    return { success: true, path: defaultPath || 'untitled.c', note: 'File saved via download' };
  } catch (error) {
    return { success: false, error: 'File save not supported. Please use the installed Electron app for full file operations.' };
  }
};

export const openFile = async () => {
  // Check if running in Electron
  if (window.electronAPI && window.electronAPI.openFile) {
    try {
      const result = await window.electronAPI.openFile();
      return result;
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  // Browser fallback using File System Access API
  if ('showOpenFilePicker' in window) {
    try {
      const [handle] = await window.showOpenFilePicker({
        types: [{
          description: 'Code Files',
          accept: {
            'text/plain': ['.c', '.cpp', '.py', '.java']
          }
        }],
        multiple: false
      });
      
      const file = await handle.getFile();
      const content = await file.text();
      const extension = file.name.split('.').pop().toLowerCase();
      
      return {
        success: true,
        content,
        path: file.name,
        extension
      };
    } catch (err) {
      if (err.name === 'AbortError') {
        return { success: false, canceled: true };
      }
      return { success: false, error: err.message };
    }
  }
  
  // Fallback for browsers without File System Access API
  // Use traditional file input
  return new Promise((resolve) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.c,.cpp,.py,.java';
    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (file) {
        try {
          const content = await file.text();
          const extension = file.name.split('.').pop().toLowerCase();
          resolve({
            success: true,
            content,
            path: file.name,
            extension
          });
        } catch (error) {
          resolve({ success: false, error: error.message });
        }
      } else {
        resolve({ success: false, canceled: true });
      }
    };
    input.oncancel = () => {
      resolve({ success: false, canceled: true });
    };
    input.click();
  });
};


