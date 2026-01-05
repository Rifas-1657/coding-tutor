"""
Sandbox execution handler for WebSocket.
Uses Docker sandbox with non-interactive stdin.
"""

import asyncio
from services.sandbox_runner import DockerSandboxRunner


class LabExecutionHandler:
    """Handle sandbox code execution via WebSocket using Docker sandbox."""
    
    def __init__(self, websocket, code, language):
        self.websocket = websocket
        self.code = code
        self.language = language.lower()
        
    async def execute(self, exercise_data=None, subject=None):
        """
        Execute code in sandbox (non-interactive).
        
        Args:
            exercise_data: dict with exercise_id (optional, not used for execution)
            subject: Subject name for RAG (optional)
        """
        try:
            await self._execute_simple()
        except Exception as e:
            await self.websocket.send_json({
                "type": "error",
                "content": f"Execution error: {str(e)}"
            })
            await self.websocket.send_json({
                "type": "complete",
                "success": False
            })
    
    async def _execute_simple(self):
        """Execute code in sandbox."""
        runner = DockerSandboxRunner()
        
        result = await asyncio.to_thread(
            runner.run_code,
            self.language,
            self.code,
            ""
        )
        
        if result.get("output"):
            await self.websocket.send_json({
                "type": "output",
                "content": result["output"]
            })
        
        if result.get("error"):
            await self.websocket.send_json({
                "type": "error",
                "content": result["error"]
            })
        
        await self.websocket.send_json({
            "type": "complete",
            "success": result.get("success", False)
        })

