"""
Code execution sandbox - NOW USES DOCKER.
This module is maintained for backward compatibility but now delegates to DockerSandboxRunner.
The old host-based execution logic has been removed.
"""

from services.sandbox_runner import DockerSandboxRunner


class CodeSandbox:
    """
    Code execution sandbox using Docker containers.
    This replaces the old host-based execution completely.
    """
    
    def __init__(self):
        self.sandbox_runner = DockerSandboxRunner()
        self.timeout = 30  # Timeout is now handled by Docker
    
    def execute(self, code: str, language: str, input_data: str = None) -> dict:
        """
        Execute code based on language using Docker sandbox.
        Non-interactive execution: input provided upfront.
        
        Args:
            code: Source code to execute
            language: One of 'c', 'cpp', 'python', 'java'
            input_data: Optional input data for program (provided upfront)
        
        Returns:
            dict with keys: output, error, success
        """
        result = self.sandbox_runner.run_code(
            language.lower(),
            code,
            stdin_data=input_data if input_data else ""
        )
        # Add execution_time for backward compatibility
        result['execution_time'] = 0.0
        return result
    
    # Legacy methods maintained for backward compatibility
    def execute_c(self, code: str, input_data: str = None) -> dict:
        """Execute C code in Docker sandbox."""
        return self.execute(code, 'c', input_data)
    
    def execute_cpp(self, code: str, input_data: str = None) -> dict:
        """Execute C++ code in Docker sandbox."""
        return self.execute(code, 'cpp', input_data)
    
    def execute_python(self, code: str, input_data: str = None) -> dict:
        """Execute Python code in Docker sandbox."""
        return self.execute(code, 'python', input_data)
    
    def execute_java(self, code: str, input_data: str = None) -> dict:
        """Execute Java code in Docker sandbox."""
        return self.execute(code, 'java', input_data)