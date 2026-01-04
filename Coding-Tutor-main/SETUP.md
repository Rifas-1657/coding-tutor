# Setup Guide

## Initial Setup

### Prerequisites

1. **Docker Desktop** (Required)
   - Download and install from https://www.docker.com/products/docker-desktop
   - Ensure Docker is running before starting the backend
   - Verify installation: `docker --version`

2. **Node.js** (v16+)
   - Download from https://nodejs.org/

3. **Python** (3.8+)
   - Download from https://www.python.org/

### Setup Steps

1. **Build Docker Sandbox Image:**
   ```bash
   docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .
   ```
   This creates the sandbox image with all compilers (gcc, g++, javac, python3).

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Add Application Icon:**
   - Place a PNG icon file at `public/icon.png` (recommended: 256x256px)
   - For development, you can use any placeholder PNG file

## Development Workflow

### Option 1: Run React and FastAPI separately (Recommended for development)

1. **Terminal 1 - Start FastAPI backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```
   **Note for Windows**: If you encounter Docker connection issues, try running without `--reload`:
   ```bash
   python -m uvicorn main:app
   ```
   Backend will run on `http://localhost:8000`

2. **Terminal 2 - Start React frontend:**
   ```bash
   npm start
   ```
   Frontend will run on `http://localhost:3000`

3. Open `http://localhost:3000` in your browser

### Option 2: Run with Electron (Integrated)

1. **Build React app first:**
   ```bash
   npm run build
   ```

2. **Run Electron:**
   ```bash
   npm run electron
   ```

   Or set environment variable for development mode:
   ```bash
   $env:ELECTRON_IS_DEV="1"  # Windows PowerShell
   export ELECTRON_IS_DEV=1  # Linux/Mac
   npm run electron
   ```

## Testing

### Test Code Execution

1. Select a language (C, C++, Python, or Java)
2. Write a simple program, e.g.:
   - **C**: `#include <stdio.h>\nint main() { printf("Hello, World!"); return 0; }`
   - **Python**: `print("Hello, World!")`
   - **Java**: `public class Program { public static void main(String[] args) { System.out.println("Hello, World!"); } }`
3. Click "Run Code"
4. Check the output panel for results

### Test Hint System

1. Write code with an intentional error
2. Click "Run Code" to see the error
3. Click "Get Hint" to receive guidance

### Test File Operations

1. Write some code
2. Click "Save" to save the file
3. Click "Open" to load a previously saved file

## Building for Production

### Windows
```bash
npm run build:win
```
Installer will be in the `dist` directory.

### macOS
```bash
npm run build:mac
```
DMG file will be in the `dist` directory.

### Linux
```bash
npm run build:linux
```
AppImage will be in the `dist` directory.

## Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r backend/requirements.txt`
- Verify port 8000 is not in use

### React app won't start
- Ensure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again
- Check that port 3000 is not in use

### Code execution fails
- **Docker not running**: Ensure Docker Desktop is running
- **Docker image not found**: Run `docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .`
- **Permission errors**: On Linux/Mac, ensure your user is in the `docker` group
- **Container errors**: Check Docker logs: `docker logs <container_id>`

### File operations don't work
- File operations only work in Electron (not in browser development mode)
- Ensure Electron is running: `npm run electron`

## Docker Sandbox System

All code execution now happens inside isolated Docker containers. This provides:

- **No host dependencies**: No need to install gcc/g++/java/python on your machine
- **Isolation**: Each execution runs in a clean, isolated container
- **Security**: Network disabled, resource limits (128MB RAM, 50% CPU), non-root user
- **Consistency**: Same environment across Windows, Linux, and macOS

### Sandbox Configuration

- **Image**: `coding-tutor-sandbox:latest`
- **Memory Limit**: 128MB per execution
- **CPU Limit**: 50% of one CPU core
- **Timeout**: 30 seconds per execution
- **Network**: Disabled for security

### Rebuilding the Sandbox

If you need to update the sandbox image:
```bash
docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .
```

## Notes

- **compilers/ folder is obsolete**: All compilers are now in the Docker image
- The application requires Docker to be running for code execution
- All code execution is sandboxed with timeouts and cleanup


