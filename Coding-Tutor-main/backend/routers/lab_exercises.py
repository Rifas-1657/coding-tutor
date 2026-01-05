"""
Lab Exercises API Router - Disabled for Interactive Practice Mode
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/evaluate")
async def evaluate_code(request):
    """Disabled - test cases not used in interactive mode."""
    raise HTTPException(status_code=404, detail="Test case evaluation disabled in interactive mode")

@router.get("/subjects")
async def get_available_subjects():
    """Get list of available subjects for RAG."""
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    INDEX_DIR = os.path.join(BASE_DIR, "indexes")
    
    subjects = []
    if os.path.exists(INDEX_DIR):
        for filename in os.listdir(INDEX_DIR):
            if filename.endswith(".index"):
                subject = filename.replace(".index", "")
                subjects.append(subject)
    
    return {"subjects": subjects}