from fastapi import APIRouter, HTTPException
from models.code_request import CodeRequest, CodeResponse
from services.sandbox import CodeSandbox

router = APIRouter()

@router.post("/run-code", response_model=CodeResponse)
async def run_code(request: CodeRequest):
    """Execute code and return results."""
    try:
        sandbox = CodeSandbox()
        result = sandbox.execute(request.code, request.language.value, request.input_data)
        
        return CodeResponse(
            output=result.get('output', ''),
            error=result.get('error', ''),
            success=result.get('success', False),
            execution_time=result.get('execution_time', 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

