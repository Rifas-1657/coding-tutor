# Backend Setup Instructions

## Quick Start

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server:**
   
   **Windows:**
   ```bash
   start_backend.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x start_backend.sh
   ./start_backend.sh
   ```
   
   **Or manually:**
   ```bash
   python main.py
   ```

4. **Verify the server is running:**
   - Open http://localhost:8000 in your browser
   - You should see: `{"message":"Lab Practice System API","status":"online"}`
   - Or check http://localhost:8000/health

## Important Notes

### Required Dependencies
- **Python 3.8+** - Required
- **Docker Desktop** - Required for code execution (must be running)
- **FastAPI & Uvicorn** - Required (installed via requirements.txt)

### Optional Dependencies (for AI hints)
- **faiss-cpu** - For RAG-based hints (optional)
- **sentence-transformers** - For RAG-based hints (optional)
- **Ollama** - For LLM-based hints (optional)

The backend will work without these optional dependencies, but hint generation will be limited to rule-based hints only.

### Troubleshooting

**Issue: "Cannot connect to backend server"**
- Make sure the backend is running (check terminal for "Application startup complete")
- Verify the server is on http://localhost:8000
- Check Windows Firewall isn't blocking port 8000

**Issue: "Docker CLI not found"**
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Make sure Docker Desktop is running before starting the backend

**Issue: Exercises not loading**
- Check that exercise files exist in `backend/exercises/`:
  - `c.json`
  - `cpp.json`
  - `python.json`
  - `java.json`
- Check backend logs for file path errors

**Issue: Code execution fails**
- Ensure Docker Desktop is running
- Check that the Docker image `coding-tutor-sandbox:latest` exists
- If the image doesn't exist, you may need to build it (see Docker setup)

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `GET /api/exercises/{language}` - Get exercises for a language (c, cpp, python, java)
- `POST /api/run` - Execute code
- `POST /api/hint` - Get hint for an error

## Development

The backend runs on `0.0.0.0:8000` to accept connections from any interface.
In production, you may want to restrict this to `127.0.0.1` for security.
