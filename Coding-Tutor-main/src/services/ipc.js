// IPC service for Electron file operations
export const saveFile = async (content, defaultPath = null) => {
  if (window.electronAPI && window.electronAPI.saveFile) {
    try {
      const result = await window.electronAPI.saveFile(content, defaultPath);
      return result;
    } catch (error) {
      console.error('Error saving file:', error);
      return { success: false, error: error.message };
    }
  } else {
    // Fallback for browser environment (development)
    return { success: false, error: 'File operations only available in Electron' };
  }
};

export const openFile = async () => {
  if (window.electronAPI && window.electronAPI.openFile) {
    try {
      const result = await window.electronAPI.openFile();
      return result;
    } catch (error) {
      console.error('Error opening file:', error);
      return { success: false, error: error.message };
    }
  } else {
    // Fallback for browser environment (development)
    return { success: false, error: 'File operations only available in Electron' };
  }
};


