"""
Get Hint API
Generates hints using RAG-first, LLM-fallback strategy.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from rag import get_hint
from stats import StatsManager
import os
import json

router = APIRouter()
stats_manager = StatsManager()


class GetHintRequest(BaseModel):
    """Request model for hint generation."""
    language: str
    exercise_id: str
    error_message: str
    failed_tests: str = ""


@router.post("/hint")
async def get_hint_api(request: GetHintRequest):
    """
    Generate hint using RAG (lab manual) first, then LLM fallback.
    Returns conceptual hint only (no code, no solution).
    """
    try:
        # Load exercise to get subject
        exercise = _load_exercise(request.language, request.exercise_id)
        subject = request.language + "_lab_manual"
        
        if exercise:
            subject = exercise.get("subject", subject)
        
        # Generate hint
        try:
            hint_data = get_hint(
                subject=subject,
                error_message=request.error_message,
                failed_tests=request.failed_tests
            )
        except Exception as hint_error:
            # Fallback if hint generation fails
            hint_data = {
                "hint": f"Error: {request.error_message}. Review your code syntax and logic.",
                "source": "Basic",
                "rag_used": False
            }
        
        # Record hint usage
        stats_manager.record_attempt(
            language=request.language,
            success=False,
            error=True,
            hint_used=True
        )
        
        return {
            "hint": hint_data.get("hint", "Review your code and check for errors."),
            "source": hint_data.get("source", "Basic"),
            "rag_used": hint_data.get("rag_used", False)
        }
        
    except Exception as e:
        # Return basic hint even if everything fails
        return {
            "hint": f"Error occurred: {request.error_message}. Please review your code carefully.",
            "source": "Basic",
            "rag_used": False
        }


def _load_exercise(language: str, exercise_id: str) -> Optional[dict]:
    """Load exercise from JSON file."""
    exercises_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "exercises",
        f"{language}.json"
    )
    
    if not os.path.exists(exercises_file):
        return None
    
    try:
        with open(exercises_file, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
            for ex in exercises:
                if ex.get("id") == exercise_id:
                    return ex
    except Exception:
        pass
    
    return None

