"""
Sandboxed Practice System - Main Backend
Non-interactive Docker sandbox execution.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import run_code, get_exercises, get_hint

app = FastAPI(title="Lab Practice System API")

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API routers
app.include_router(run_code.router, prefix="/api", tags=["execution"])
app.include_router(get_exercises.router, prefix="/api", tags=["exercises"])
app.include_router(get_hint.router, prefix="/api", tags=["hints"])


@app.get("/")
async def root():
    return {"message": "Lab Practice System API", "status": "online"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.get("/api/health")
async def api_health_check():
    return {"status": "ok", "message": "API is running"}


@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)


@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API is working."""
    return {"status": "ok", "message": "API is working"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
