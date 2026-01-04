from fastapi import APIRouter, HTTPException
from models.hint_response import HintRequest, HintResponse
from services.hint_engine import HintEngine

router = APIRouter()

@router.post("/get-hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    """Generate hints based on code and error message."""
    try:
        hint_engine = HintEngine()
        hints = hint_engine.analyze_code(
            request.code,
            request.language,
            request.error_message
        )
        
        return HintResponse(hints=hints)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hint generation failed: {str(e)}")

