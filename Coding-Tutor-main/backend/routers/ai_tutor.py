from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.ai_tutor_service import AITutorService

router = APIRouter()
ai_tutor_service = AITutorService()

class ChatRequest(BaseModel):
    message: str
    current_code: str
    language: str
    conversation_history: List[Dict] = []
    code_observations: Optional[Dict] = None

class MonitorRequest(BaseModel):
    code: str
    language: str

@router.post("/ai-tutor/chat")
async def chat_with_tutor(request: ChatRequest):
    """Process user's question with full context and return guiding response."""
    try:
        response = await ai_tutor_service.get_tutor_response(
            request.message,
            request.current_code,
            request.language,
            request.conversation_history,
            request.code_observations
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI tutor error: {str(e)}")

@router.post("/ai-tutor/monitor")
async def monitor_code(request: MonitorRequest):
    """Analyzes code periodically to build context for AI tutor."""
    try:
        observations = ai_tutor_service.analyze_code(request.code, request.language)
        return observations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code monitoring error: {str(e)}")

