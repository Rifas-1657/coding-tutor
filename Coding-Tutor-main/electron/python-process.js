const { spawn } = require('child_process');
const path = require('path');

function getPythonExecutable() {
  const isDev = process.env.ELECTRON_IS_DEV === '1';
  
  if (isDev) {
    // In development, try to use system Python
    return process.platform === 'win32' ? 'python' : 'python3';
  } else {
    // In production, use bundled Python or system Python
    const resourcesPath = process.resourcesPath || __dirname;
    const pythonPath = path.join(resourcesPath, 'compilers', 'python', 'python.exe');
    
    // Fallback to system Python if bundled Python doesn't exist
    try {
      const fs = require('fs');
      if (fs.existsSync(pythonPath)) {
        return pythonPath;
      }
    } catch (error) {
      console.error('Error checking bundled Python:', error);
    }
    
    return process.platform === 'win32' ? 'python' : 'python3';
  }
}

function spawnPythonServer() {
  const pythonExe = getPythonExecutable();
  const backendPath = path.join(__dirname, '..', 'backend');
  const mainPy = path.join(backendPath, 'main.py');
  
  const args = [
    '-m', 'uvicorn',
    'main:app',
    '--host', '127.0.0.1',
    '--port', '8000',
    '--log-level', 'info'
  ];
  
  console.log(`Starting Python server: ${pythonExe} ${args.join(' ')}`);
  
  const pythonProcess = spawn(pythonExe, args, {
    cwd: backendPath,
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: false
  });
  
  pythonProcess.stdout.on('data', (data) => {
    console.log(`[Python] ${data.toString()}`);
  });
  
  pythonProcess.stderr.on('data', (data) => {
    console.error(`[Python Error] ${data.toString()}`);
  });
  
  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python server:', error);
  });
  
  pythonProcess.on('exit', (code, signal) => {
    console.log(`Python server exited with code ${code} and signal ${signal}`);
  });
  
  return pythonProcess;
}

function killPythonServer(proc) {
  if (proc && !proc.killed) {
    if (process.platform === 'win32') {
      // On Windows, use taskkill to ensure process tree is terminated
      try {
        spawn('taskkill', ['/pid', proc.pid, '/T', '/F'], { stdio: 'ignore' });
      } catch (error) {
        // Fallback to direct kill
        try {
          proc.kill('SIGTERM');
        } catch (e) {
          // Ignore errors
        }
      }
    } else {
      try {
        proc.kill('SIGTERM');
        // Force kill after timeout
        setTimeout(() => {
          if (proc && !proc.killed) {
            try {
              proc.kill('SIGKILL');
            } catch (e) {
              // Ignore errors
            }
          }
        }, 5000);
      } catch (error) {
        // Ignore errors
      }
    }
  }
}

module.exports = {
  spawnPythonServer,
  killPythonServer
};

