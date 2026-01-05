"""
WebSocket-based code execution using Docker sandbox.
All code execution happens in isolated Docker containers with non-interactive stdin.
"""

from services.sandbox_runner import DockerSandboxRunner


class WebSocketExecutionHandler:
    """Handle code execution via WebSocket using Docker sandbox (non-interactive mode)."""
    
    def __init__(self, websocket, code, language):
        self.websocket = websocket
        self.code = code
        self.language = language.lower()
        self.sandbox_runner = DockerSandboxRunner()
        
    async def execute(self, compile_only=False, stdin_data=None):
        """
        Execute code in sandbox (non-interactive).
        Stdin is closed immediately to prevent hanging.
        """
        try:
            # Compile-only mode not supported
            if compile_only:
                await self.websocket.send_json({
                    "type": "error",
                    "content": "Compile-only mode not supported"
                })
                await self.websocket.send_json({
                    "type": "complete",
                    "success": False
                })
                return
            
            # Execute code in Docker (non-interactive mode)
            input_str = stdin_data if stdin_data else ""
            
            result = self.sandbox_runner.run_code(
                self.language,
                self.code,
                stdin_data=input_str
            )
            
            # Send output
            if result['output']:
                await self.websocket.send_json({
                    "type": "output",
                    "content": result['output']
                })
            
            # Send errors
            if result['error']:
                await self.websocket.send_json({
                    "type": "error",
                    "content": result['error']
                })
            
            # Send completion
            await self.websocket.send_json({
                "type": "complete",
                "success": result['success']
            })
            
        except Exception as e:
            await self.websocket.send_json({
                "type": "error",
                "content": f"Execution error: {str(e)}"
            })
            await self.websocket.send_json({
                "type": "complete",
                "success": False
            })
    
    def _cleanup(self):
        """Clean up resources."""
        pass