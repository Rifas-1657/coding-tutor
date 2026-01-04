# Coding Tutor Desktop Application

A desktop application built with Electron, React, and FastAPI that helps college students learn programming in lab environments. The app runs completely offline on basic lab PCs with minimal resources.

## Features

- **Multi-language Support**: C, C++, Python, and Java
- **Code Editor**: Monaco Editor with syntax highlighting (same engine as VS Code)
- **Code Execution**: Docker-based sandboxed execution with timeout protection and resource limits
- **Intelligent Hints**: AI-powered hint generation based on error analysis
- **File Operations**: Save and load code files
- **Dashboard**: Track progress and statistics
- **Offline First**: Works completely offline, no internet required

## Architecture

The application uses a three-layer architecture:

1. **Electron Main Process**: Manages the desktop window and starts the FastAPI backend
2. **React Frontend**: Provides the user interface with Monaco Editor
3. **FastAPI Backend**: Handles code execution, hint generation, and file operations

## Prerequisites

- **Docker Desktop** (Required for code execution)
- Node.js 16+ and npm
- Python 3.8+

**Note**: All compilers (gcc, g++, javac, python3) are now provided via Docker. No need to install them on your host machine.

## Installation

1. Clone the repository
2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Development

### Running the React Frontend (Development)

```bash
npm start
```

This starts the React development server on `http://localhost:3000`

### Running the FastAPI Backend (Development)

```bash
cd backend
python -m uvicorn main:app --reload
```

This starts the FastAPI server on `http://localhost:8000`

### Running the Electron App (Development)

```bash
npm run electron-dev
```

Or first build the React app, then run Electron:

```bash
npm run build
npm run electron
```

## Building for Production

### Windows

```bash
npm run build:win
```

This creates an NSIS installer in the `dist` directory.

### macOS

```bash
npm run build:mac
```

This creates a DMG disk image.

### Linux

```bash
npm run build:linux
```

This creates an AppImage.

## Project Structure

```
coding-tutor/
├── electron/          # Electron main process files
│   ├── main.js       # Entry point, window management
│   ├── preload.js    # Security bridge for IPC
│   └── python-process.js  # Python subprocess management
├── public/            # Static assets
│   ├── index.html
│   └── icon.png
├── src/               # React application
│   ├── components/    # React components
│   │   ├── Editor/   # Code editor components
│   │   ├── Controls/ # Control buttons
│   │   ├── Output/   # Output display
│   │   ├── Hints/    # Hint components
│   │   └── Dashboard/ # Dashboard components
│   ├── services/      # API and IPC services
│   ├── App.js        # Main React component
│   └── index.js      # React entry point
├── backend/           # FastAPI backend
│   ├── routers/      # API endpoints
│   ├── services/     # Business logic (sandbox, hints)
│   ├── models/       # Pydantic models
│   └── main.py       # FastAPI app
├── compilers/         # Bundled compilers (for production)
│   ├── mingw/        # MinGW for C/C++
│   ├── python/       # Python runtime
│   └── jdk/          # OpenJDK for Java
└── package.json      # Node.js dependencies and scripts
```

## Security

The sandbox implementation includes multiple safety layers:

- **Timeout Protection**: All code executions timeout after 5 seconds
- **Directory Isolation**: Each execution runs in a temporary directory
- **Resource Limits**: Memory and CPU limits (Linux)
- **No Network Access**: Subprocess doesn't grant socket permissions
- **Automatic Cleanup**: Temporary directories are always cleaned up

## Supported Languages

- **C**: GCC compiler
- **C++**: G++ compiler
- **Python**: Python 3 interpreter
- **Java**: JDK (javac + java)

## License

This project is for educational purposes.

## Contributing

This is an educational project. Contributions and improvements are welcome!


