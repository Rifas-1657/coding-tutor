from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Language(str, Enum):
    c = "c"
    cpp = "cpp"
    python = "python"
    java = "java"

class CodeRequest(BaseModel):
    code: str
    language: Language
    input_data: Optional[str] = None

class CodeResponse(BaseModel):
    output: str
    error: str
    success: bool
    execution_time: float
