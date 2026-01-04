from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Severity(str, Enum):
    syntax = "syntax"
    logic = "logic"
    runtime = "runtime"
    edge_case = "edge_case"

class Hint(BaseModel):
    severity: Severity
    title: str
    description: str
    example: Optional[str] = None

class HintRequest(BaseModel):
    code: str
    language: str
    error_message: Optional[str] = None

class HintResponse(BaseModel):
    hints: List[Hint]


