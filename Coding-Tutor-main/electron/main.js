const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs').promises;
const { spawnPythonServer, killPythonServer } = require('./python-process');

let mainWindow;
let pythonProcess = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: path.join(__dirname, '../public/icon.png'),
  });

  // Start Python server before loading React app
  pythonProcess = spawnPythonServer();

  // Wait 2 seconds for backend to initialize, then load React app
  setTimeout(() => {
    const isDev = process.env.ELECTRON_IS_DEV === '1';
    
    if (isDev) {
      // In development, load from React dev server
      mainWindow.loadURL('http://localhost:3000');
      mainWindow.webContents.openDevTools();
    } else {
      // In production, load from built React app
      mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
    }
  }, 2000);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Health check function to ping backend
async function checkBackendHealth() {
  try {
    const response = await fetch('http://127.0.0.1:8000/health');
    return response.ok;
  } catch (error) {
    return false;
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Kill Python process when app quits
  if (pythonProcess) {
    killPythonServer(pythonProcess);
  }
});

app.on('will-quit', () => {
  // Ensure Python process is terminated
  if (pythonProcess) {
    killPythonServer(pythonProcess);
  }
});

// IPC handlers for file operations
ipcMain.handle('save-file', async (event, content, defaultPath) => {
  try {
    if (!mainWindow) {
      return { success: false, error: 'Main window not available' };
    }

    const result = await dialog.showSaveDialog(mainWindow, {
      title: 'Save Code File',
      defaultPath: defaultPath || 'untitled.c',
      filters: [
        { name: 'Code Files', extensions: ['c', 'cpp', 'py', 'java'] },
        { name: 'All Files', extensions: ['*'] }
      ]
    });

    if (!result.canceled && result.filePath) {
      await fs.writeFile(result.filePath, content, 'utf-8');
      return { success: true, path: result.filePath };
    }
    
    return { success: false, canceled: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('open-file', async (event) => {
  try {
    if (!mainWindow) {
      return { success: false, error: 'Main window not available' };
    }

    const result = await dialog.showOpenDialog(mainWindow, {
      title: 'Open Code File',
      filters: [
        { name: 'Code Files', extensions: ['c', 'cpp', 'py', 'java'] },
        { name: 'All Files', extensions: ['*'] }
      ],
      properties: ['openFile']
    });

    if (!result.canceled && result.filePaths.length > 0) {
      const filePath = result.filePaths[0];
      const content = await fs.readFile(filePath, 'utf-8');
      const extension = path.extname(filePath).slice(1).toLowerCase();
      return { 
        success: true, 
        content, 
        path: filePath,
        extension
      };
    }
    
    return { success: false, canceled: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

