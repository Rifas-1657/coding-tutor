# Docker Sandbox Implementation

## Overview

The Coding-Tutor project has been migrated from host-based code execution to a **Docker-based sandbox system**. All code execution (Python, C, C++, Java) now happens inside isolated Docker containers.

## What Changed

### 1. Docker Sandbox Image (`Dockerfile.sandbox`)

- **Location**: Project root
- **Base**: Ubuntu 22.04
- **Includes**: gcc, g++, openjdk-17-jdk, python3
- **Security**: Non-root user (`sandboxuser`), network disabled, resource limits
- **Build**: `docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .`

### 2. Backend Services

#### `backend/services/sandbox_runner.py` (NEW)
- **Purpose**: Docker-based code execution
- **Features**:
  - Isolated container execution
  - Resource limits (128MB RAM, 50% CPU, 30s timeout)
  - Supports compile-only mode
  - Streaming output support (for WebSocket)

#### `backend/services/websocket_execution.py` (UPDATED)
- **Before**: Used subprocess with host compilers
- **After**: Uses `DockerSandboxRunner` for all execution
- **Result**: No dependency on host gcc/g++/java/python

#### `backend/services/sandbox.py` (UPDATED)
- **Before**: Host-based execution with subprocess
- **After**: Wrapper around `DockerSandboxRunner` (backward compatibility)
- **Result**: All execution goes through Docker

#### `backend/services/compiler_manager.py` (MARKED OBSOLETE)
- **Status**: No longer used
- **Reason**: All compilers are in Docker image
- **Action**: Marked with OBSOLETE comments

### 3. Dependencies

#### `requirements.txt` (UPDATED)
- **Added**: `docker==7.0.0`
- **Required**: Docker Desktop must be running

### 4. Documentation

#### `SETUP.md` (UPDATED)
- Added Docker installation instructions
- Updated troubleshooting section
- Removed references to host compiler installation

#### `compilers/README.md` (NEW)
- Explains that compilers/ folder is obsolete
- Provides migration guidance

## How It Works

### Execution Flow

1. **User submits code** → Frontend → Backend API/WebSocket
2. **Backend** → `DockerSandboxRunner.run_code()`
3. **Docker** → Creates temporary directory, mounts to `/sandbox`
4. **Container** → Executes code with resource limits
5. **Output** → Streamed back to frontend terminal
6. **Cleanup** → Container removed, temp directory deleted

### Language-Specific Commands

- **Python**: `python3 -u /sandbox/main.py`
- **C**: `gcc /sandbox/main.c -o /sandbox/a.out && /sandbox/a.out`
- **C++**: `g++ /sandbox/main.cpp -o /sandbox/a.out && /sandbox/a.out`
- **Java**: `javac /sandbox/Main.java && java -cp /sandbox Main`

### Security Features

- **Network**: Disabled (`network_disabled=True`)
- **User**: Non-root (`sandboxuser`)
- **Memory**: 128MB limit per execution
- **CPU**: 50% of one core
- **Timeout**: 30 seconds
- **Isolation**: Each execution in separate container

## Setup Instructions

### 1. Install Docker Desktop
- Download from https://www.docker.com/products/docker-desktop
- Start Docker Desktop

### 2. Build Sandbox Image
```bash
docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .
```

### 3. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Start Backend
```bash
python -m uvicorn main:app --reload
```

## Benefits

### Before (Host-Based)
- ❌ Required gcc/g++/java/python on host
- ❌ Platform-specific issues (Windows vs Linux)
- ❌ "gcc not found" errors
- ❌ "Main.class not found" errors
- ❌ Security concerns (direct host execution)

### After (Docker-Based)
- ✅ No host compiler dependencies
- ✅ Same environment on all platforms
- ✅ All compilers guaranteed available
- ✅ Isolated, secure execution
- ✅ Easy to update compilers (rebuild image)

## Troubleshooting

### Docker Image Not Found
```bash
docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .
```

### Docker Not Running
- Start Docker Desktop
- Verify: `docker ps`

### Permission Errors (Linux/Mac)
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Container Errors
```bash
docker logs <container_id>
```

## Migration Notes

- **compilers/ folder**: No longer needed, marked obsolete
- **CompilerManager**: Deprecated, use DockerSandboxRunner
- **Host compilers**: Not required
- **Backward compatibility**: `sandbox.py` still works but uses Docker

## Future Enhancements

- True interactive stdin/stdout streaming (container.attach())
- Per-language resource limits
- Execution history/logging
- Multi-container support for parallel execution

