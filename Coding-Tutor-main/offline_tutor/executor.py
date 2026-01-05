"""
Offline Code Execution Engine
Supports C, C++, Java, Python with real interactive stdin/stdout.
"""

import subprocess
import tempfile
import shutil
import os
import threading
import queue
import time
from typing import Optional, Callable, Dict, Any


class OfflineExecutor:
    """Execute code locally with interactive stdin/stdout support."""
    
    SUPPORTED_LANGUAGES = ['c', 'cpp', 'java', 'python']
    DEFAULT_TIMEOUT = 30  # seconds
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize offline executor.
        
        Args:
            timeout: Execution timeout in seconds
        """
        self.timeout = timeout
        self.process = None
        self.temp_dir = None
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.stdout_thread = None
        self.stderr_thread = None
        self.is_running = False
    
    def _prepare_code_file(self, code: str, language: str) -> tuple:
        """
        Create temporary directory and write code file.
        
        Returns:
            (temp_dir, code_file_path)
        """
        temp_dir = tempfile.mkdtemp(prefix='offline_tutor_')
        
        if language == 'python':
            filename = 'main.py'
        elif language == 'c':
            filename = 'main.c'
        elif language == 'cpp':
            filename = 'main.cpp'
        elif language == 'java':
            filename = 'Main.java'
            # Ensure code has public class Main
            if 'public class Main' not in code and 'class Main' not in code:
                if 'public class' not in code:
                    code = f'public class Main {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}'
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        code_file = os.path.join(temp_dir, filename)
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return temp_dir, code_file
    
    def _get_execution_command(self, language: str, code_file: str) -> list:
        """
        Get command to execute code.
        
        Returns:
            List of command arguments
        """
        if language == 'python':
            return ['python', '-u', code_file]  # -u for unbuffered output
        
        elif language == 'c':
            # Compile first
            exe_file = os.path.join(os.path.dirname(code_file), 'a.out')
            compile_cmd = ['gcc', code_file, '-o', exe_file]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode != 0:
                raise RuntimeError(f"Compilation failed: {compile_result.stderr}")
            return [exe_file]
        
        elif language == 'cpp':
            # Compile first
            exe_file = os.path.join(os.path.dirname(code_file), 'a.out')
            compile_cmd = ['g++', code_file, '-o', exe_file]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode != 0:
                raise RuntimeError(f"Compilation failed: {compile_result.stderr}")
            return [exe_file]
        
        elif language == 'java':
            # Compile first
            compile_cmd = ['javac', code_file]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, cwd=os.path.dirname(code_file))
            if compile_result.returncode != 0:
                raise RuntimeError(f"Compilation failed: {compile_result.stderr}")
            # Run Java
            return ['java', '-cp', os.path.dirname(code_file), 'Main']
        
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _read_stdout(self):
        """Read stdout line by line in background thread."""
        try:
            if self.process and self.process.stdout:
                # Use readline for line-buffered reading
                for line in iter(self.process.stdout.readline, ''):
                    if not line:
                        break
                    # Remove trailing newlines but keep the line content
                    cleaned_line = line.rstrip('\n\r')
                    if cleaned_line:  # Only queue non-empty lines
                        self.stdout_queue.put(cleaned_line)
        except Exception:
            pass
        finally:
            self.stdout_queue.put(None)  # Sentinel to indicate end
    
    def _read_stderr(self):
        """Read stderr line by line in background thread."""
        try:
            if self.process and self.process.stderr:
                for line in iter(self.process.stderr.readline, ''):
                    if not line:
                        break
                    self.stderr_queue.put(line.rstrip('\n\r'))
        except Exception:
            pass
        finally:
            self.stderr_queue.put(None)  # Sentinel to indicate end
    
    def start_execution(self, code: str, language: str) -> Dict[str, Any]:
        """
        Start code execution with interactive stdin/stdout.
        
        Args:
            code: Source code to execute
            language: One of 'c', 'cpp', 'java', 'python'
        
        Returns:
            dict with keys: success, message, process_id
        """
        if self.is_running:
            return {"success": False, "message": "Execution already in progress"}
        
        if language not in self.SUPPORTED_LANGUAGES:
            return {"success": False, "message": f"Unsupported language: {language}"}
        
        try:
            # Prepare code file
            self.temp_dir, code_file = self._prepare_code_file(code, language)
            
            # Get execution command
            cmd = self._get_execution_command(language, code_file)
            
            # Start process with interactive stdin/stdout
            # Use line buffered mode for interactive I/O
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered for interactive programs
                cwd=os.path.dirname(code_file) if language != 'python' else None
            )
            
            self.is_running = True
            
            # Start background threads to read stdout/stderr
            self.stdout_queue = queue.Queue()
            self.stderr_queue = queue.Queue()
            self.stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
            self.stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
            self.stdout_thread.start()
            self.stderr_thread.start()
            
            return {
                "success": True,
                "message": "Execution started",
                "process_id": id(self.process)
            }
        
        except RuntimeError as e:
            # Compilation error
            self._cleanup()
            return {
                "success": False,
                "message": str(e),
                "error_type": "COMPILE_ERROR"
            }
        except Exception as e:
            self._cleanup()
            return {
                "success": False,
                "message": str(e),
                "error_type": "EXECUTION_ERROR"
            }
    
    def send_input(self, input_data: str) -> Dict[str, Any]:
        """
        Send input to running process.
        
        Args:
            input_data: Input string (will be sent with newline)
        
        Returns:
            dict with keys: success, message
        """
        if not self.is_running or not self.process:
            return {"success": False, "message": "No active execution"}
        
        if not self.process.stdin:
            return {"success": False, "message": "Process stdin not available"}
        
        try:
            # Check if process is still running
            if self.process.poll() is not None:
                return {"success": False, "message": "Process has terminated"}
            
            # Send input with newline and ensure it's flushed immediately
            input_str = str(input_data) + '\n'
            self.process.stdin.write(input_str)
            self.process.stdin.flush()
            
            # Small delay to ensure input is processed
            import time
            time.sleep(0.01)  # 10ms delay
            
            return {"success": True, "message": "Input sent"}
        except BrokenPipeError:
            return {"success": False, "message": "Process stdin pipe is closed"}
        except Exception as e:
            return {"success": False, "message": f"Error sending input: {str(e)}"}
    
    def read_output(self, timeout: float = 0.1) -> Dict[str, Any]:
        """
        Read available output from stdout and stderr.
        
        Args:
            timeout: Timeout for reading (seconds)
        
        Returns:
            dict with keys: stdout_lines, stderr_lines, is_complete
        """
        stdout_lines = []
        stderr_lines = []
        
        # Read from stdout queue
        while True:
            try:
                line = self.stdout_queue.get(timeout=timeout)
                if line is None:  # Sentinel
                    break
                stdout_lines.append(line)
            except queue.Empty:
                break
        
        # Read from stderr queue
        while True:
            try:
                line = self.stderr_queue.get(timeout=timeout)
                if line is None:  # Sentinel
                    break
                stderr_lines.append(line)
            except queue.Empty:
                break
        
        # Check if process is still running
        is_complete = False
        if self.process:
            if self.process.poll() is not None:
                is_complete = True
        
        return {
            "stdout_lines": stdout_lines,
            "stderr_lines": stderr_lines,
            "is_complete": is_complete
        }
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Wait for process to complete and get final result.
        
        Args:
            timeout: Maximum time to wait (None = use default timeout)
        
        Returns:
            dict with keys: success, stdout, stderr, returncode, execution_time
        """
        if not self.is_running or not self.process:
            return {"success": False, "message": "No active execution"}
        
        start_time = time.time()
        timeout = timeout or self.timeout
        
        try:
            # Wait for process with timeout
            self.process.wait(timeout=timeout)
            execution_time = time.time() - start_time
            
            # Read remaining output
            stdout_lines = []
            stderr_lines = []
            
            # Wait for threads to finish
            if self.stdout_thread:
                self.stdout_thread.join(timeout=1.0)
            if self.stderr_thread:
                self.stderr_thread.join(timeout=1.0)
            
            # Drain queues
            while True:
                try:
                    line = self.stdout_queue.get_nowait()
                    if line is not None:
                        stdout_lines.append(line)
                except queue.Empty:
                    break
            
            while True:
                try:
                    line = self.stderr_queue.get_nowait()
                    if line is not None:
                        stderr_lines.append(line)
                except queue.Empty:
                    break
            
            return {
                "success": True,
                "stdout": '\n'.join(stdout_lines),
                "stderr": '\n'.join(stderr_lines),
                "returncode": self.process.returncode,
                "execution_time": execution_time
            }
        
        except subprocess.TimeoutExpired:
            # Kill process on timeout
            self.process.kill()
            self.process.wait()
            return {
                "success": False,
                "message": "Execution timed out",
                "error_type": "TIMEOUT",
                "execution_time": time.time() - start_time
            }
        finally:
            self._cleanup()
    
    def stop_execution(self) -> Dict[str, Any]:
        """
        Stop running execution.
        
        Returns:
            dict with keys: success, message
        """
        if not self.is_running or not self.process:
            return {"success": False, "message": "No active execution"}
        
        try:
            self.process.kill()
            self.process.wait(timeout=2.0)
            self._cleanup()
            return {"success": True, "message": "Execution stopped"}
        except Exception as e:
            self._cleanup()
            return {"success": False, "message": str(e)}
    
    def _cleanup(self):
        """Clean up resources."""
        self.is_running = False
        
        # Close process streams
        if self.process:
            try:
                if self.process.stdin:
                    self.process.stdin.close()
                if self.process.stdout:
                    self.process.stdout.close()
                if self.process.stderr:
                    self.process.stderr.close()
            except Exception:
                pass
            self.process = None
        
        # Clean up temp directory
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception:
                pass
            self.temp_dir = None

