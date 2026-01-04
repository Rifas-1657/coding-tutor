const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // File operations using IPC
  saveFile: async (content, defaultPath) => {
    try {
      const result = await ipcRenderer.invoke('save-file', content, defaultPath);
      return result;
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  openFile: async () => {
    try {
      const result = await ipcRenderer.invoke('open-file');
      return result;
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
});

