from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routers import code_execution, hints, files

# Verify Docker CLI is available
try:
    import subprocess
    result = subprocess.run(
        ['docker', '--version'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"[STARTUP] Docker CLI available: {result.stdout.strip()}")
    else:
        print(f"[STARTUP] WARNING: Docker CLI check failed")
        print(f"[STARTUP] Code execution will fail until Docker Desktop is running")
except FileNotFoundError:
    print(f"[STARTUP] WARNING: Docker CLI not found")
    print(f"[STARTUP] Please ensure Docker Desktop is installed and running")
except Exception as e:
    print(f"[STARTUP] WARNING: Docker CLI check failed: {e}")
    print(f"[STARTUP] Code execution will fail until Docker Desktop is running")

app = FastAPI(title="Coding Tutor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(code_execution.router, prefix="/api", tags=["code"])
app.include_router(hints.router, prefix="/api", tags=["hints"])
app.include_router(files.router, prefix="/api", tags=["files"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Coding Tutor API"}

@app.websocket("/ws/execute")
async def websocket_execute(websocket: WebSocket):
    """WebSocket endpoint for code execution (batch mode)."""
    await websocket.accept()
    
    try:
        from services.websocket_execution import WebSocketExecutionHandler
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "execute":
                # Execute code with input provided upfront (batch mode)
                handler = WebSocketExecutionHandler(
                    websocket,
                    data.get("code", ""),
                    data.get("language", "c")
                )
                # Run in background with input provided upfront
                import asyncio
                compile_only = data.get("compile_only", False)
                stdin_data = data.get("input_data") or data.get("stdin")  # Accept input upfront
                asyncio.create_task(handler.execute(compile_only=compile_only, stdin_data=stdin_data))
                
    except WebSocketDisconnect:
        pass  # Normal disconnect, no cleanup needed for batch execution
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "content": f"WebSocket error: {str(e)}"
            })
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

