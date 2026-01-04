from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, List
from services.file_manager import FileManager

router = APIRouter()
file_manager = FileManager()

class FileSaveRequest(BaseModel):
    filename: str
    content: str

class FileResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    filename: Optional[str] = None
    path: Optional[str] = None
    error: Optional[str] = None

class FileListResponse(BaseModel):
    files: List[dict]

@router.post("/save", response_model=FileResponse)
async def save_code_file(request: FileSaveRequest):
    """Save file to persistent storage (NOT sandbox temp)."""
    try:
        path = file_manager.save_file(request.filename, request.content)
        return FileResponse(
            success=True,
            filename=request.filename,
            path=path
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {str(e)}")

@router.get("/load/{filename}", response_model=FileResponse)
async def load_code_file(filename: str):
    """Load file from persistent storage."""
    try:
        content = file_manager.load_file(filename)
        return FileResponse(
            success=True,
            content=content,
            filename=filename
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File load failed: {str(e)}")

@router.get("/list", response_model=FileListResponse)
async def list_saved_files():
    """Get list of all saved files."""
    try:
        files = file_manager.list_files()
        return FileListResponse(files=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File list failed: {str(e)}")

@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    """Delete a file from persistent storage."""
    try:
        file_manager.delete_file(filename)
        return {"success": True}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File delete failed: {str(e)}")

