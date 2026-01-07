"""
Sandboxed Practice API
Executes code in non-interactive sandbox.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.sandbox_runner import DockerSandboxRunner
from stats import StatsManager
import json
import os

router = APIRouter()
stats_manager = StatsManager()


class RunCodeRequest(BaseModel):
    """Request model for code execution."""
    code: str
    language: str
    exercise_id: str
    user_input: str = ""


@router.post("/run")
async def run_code(request: RunCodeRequest):
    """
    Execute code in sandbox (non-interactive).
    Returns execution results.
    """
    try:
        runner = DockerSandboxRunner()
        
        # Input injection strategy for non-interactive sandbox execution:
        # 1. User-provided input (from InputArea component) takes priority
        # 2. If no user input, use exercise test case input (for automated testing)
        # 3. If no input available, provide empty stdin (programs will get EOF)
        # Note: Input is preloaded into stdin before execution - this is why
        # programs using scanf/cin/input() appear to receive values "automatically"
        stdin_data = request.user_input if request.user_input else ""
        if stdin_data and not stdin_data.endswith('\n'):
            stdin_data += '\n'
        if request.user_input and request.user_input.strip():
            # User explicitly provided input via InputArea - use it
            stdin_data = request.user_input.strip()
            if not stdin_data.endswith('\n'):
                stdin_data += '\n'
        else:
            # No user input provided - check if exercise has test case input
            # exercise = _load_exercise(request.language, request.exercise_id)
            # if exercise and exercise.get("testcases"):
            #     # Use first test case input for automated testing
            #     first_test = exercise["testcases"][0]
            #     stdin_data = first_test.get("input", "")
            #     # Ensure input ends with newline if it's not empty
            #     if stdin_data and not stdin_data.endswith('\n'):
            #         stdin_data += '\n'
            # If no input available, stdin_data remains empty (programs get EOF)
            stdin_data = ""
        result = runner.run_code(
            request.language,
            request.code,
            stdin_data
        )
        
        has_error = not result["success"] or bool(result.get("error", ""))
        error_type = None
        if has_error:
            error_msg = result.get("error", "")
            if "compile" in error_msg.lower() or "syntax" in error_msg.lower() or "error:" in error_msg.lower():
                error_type = "COMPILE_ERROR"
            elif "runtime" in error_msg.lower() or "segmentation" in error_msg.lower():
                error_type = "RUNTIME_ERROR"
            else:
                error_type = "RUNTIME_ERROR"
        
        stats_manager.record_attempt(
            language=request.language,
            success=result["success"],
            error=has_error,
            hint_used=False
        )
        
        response = {
            "success": result["success"],
            "output": result.get("output", ""),
            "error": result.get("error", ""),
            "hint_available": has_error,
            "error_type": error_type
        }
        
        return response
        
    except Exception as e:
        stats_manager.record_attempt(
            language=request.language,
            success=False,
            error=True
        )
        raise HTTPException(status_code=500, detail=str(e))


def _load_exercise(language: str, exercise_id: str) -> Optional[Dict[str, Any]]:
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

