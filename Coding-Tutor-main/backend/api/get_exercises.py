"""
Get Exercises API
Returns list of exercises for a given language.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
import os

router = APIRouter()

# Enable logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/exercises/{language}")
async def get_exercises(language: str) -> List[Dict[str, Any]]:
    """
    Get all exercises for a given language.
    
    Args:
        language: Programming language (c, cpp, python, java)
    
    Returns:
        List of exercises (id, title, description only - no test cases)
    """
    # Normalize language to lowercase
    language = language.lower().strip()
    
    exercises_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "exercises",
        f"{language}.json"
    )
    
    logger.info(f"Requested exercises for language: {language}")
    logger.info(f"Exercises file path: {exercises_file}")
    logger.info(f"File exists: {os.path.exists(exercises_file)}")
    
    if not os.path.exists(exercises_file):
        logger.error(f"Exercises file not found: {exercises_file}")
        # Return empty array instead of raising exception
        return []
    
    try:
        with open(exercises_file, 'r', encoding='utf-8') as f:
            exercises = json.load(f)
        
        if not isinstance(exercises, list):
            logger.error(f"Exercises file does not contain a list: {type(exercises)}")
            return []
        
        logger.info(f"Loaded {len(exercises)} exercises from {exercises_file}")
        
        # Return only metadata (no test cases)
        result = []
        for ex in exercises:
            if isinstance(ex, dict) and ex.get("id") and ex.get("title"):
                result.append({
                    "id": ex.get("id"),
                    "title": ex.get("title"),
                    "description": ex.get("description", "")
                })
        
        logger.info(f"Returning {len(result)} exercises")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading exercises: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []

