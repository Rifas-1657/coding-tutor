# Compilers Directory - OBSOLETE

**This directory is no longer used.**

All code execution now happens inside Docker containers. The compilers/ folder and host-based compiler installation are not needed.

## Migration to Docker

The project now uses a Docker-based sandbox system:

1. **Docker Image**: Build the sandbox image using `Dockerfile.sandbox`
2. **Execution**: All code runs in isolated Docker containers
3. **Compilers**: gcc, g++, javac, python3 are all available inside the Docker image

## Setup

1. Build the Docker image:
   ```bash
   docker build -f Dockerfile.sandbox -t coding-tutor-sandbox:latest .
   ```

2. Ensure Docker is running before starting the backend.

## Benefits

- **No host dependencies**: No need to install gcc/g++/java/python on the host
- **Isolation**: Each execution runs in a clean, isolated container
- **Security**: Network disabled, resource limits, non-root user
- **Consistency**: Same environment across all platforms (Windows, Linux, macOS)

See `SETUP.md` for detailed setup instructions.

