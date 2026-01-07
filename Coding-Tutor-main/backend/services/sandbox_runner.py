"""
Docker-based sandbox runner for secure code execution.
All code execution happens inside isolated Docker containers using Docker CLI.
Non-interactive execution model: stdin is closed immediately to prevent hanging.
"""

import subprocess
import tempfile
import shutil
import os


class DockerSandboxRunner:
    """Execute code in isolated Docker containers using Docker CLI."""
    
    SANDBOX_IMAGE = "coding-tutor-sandbox:latest"
    TIMEOUT = 120  # Increased for advanced programs

    def __init__(self):
        """Initialize DockerSandboxRunner."""
        # Verify Docker CLI is available
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise RuntimeError("Docker CLI not available. Please ensure Docker Desktop is running.")
        except FileNotFoundError:
            raise RuntimeError("Docker CLI not found. Please ensure Docker Desktop is installed and running.")
        except Exception as e:
            raise RuntimeError(f"Docker CLI check failed: {str(e)}")

    def run_code(self, language, code, stdin_data=""):
        """
        Execute code in Docker container using Docker CLI.
        Non-interactive execution model: stdin is preloaded before execution starts.
        
        Execution Environment:
        - Runs in isolated Docker container with no TTY (non-interactive)
        - Stdin is preloaded with stdin_data before program execution
        - Programs using scanf/cin/input() read from preloaded stdin buffer
        - No interactive terminal - input appears "automatic" because it's injected upfront
        
        Args:
            language: One of 'python', 'c', 'cpp', 'java'
            code: Source code to execute
            stdin_data: Input data to preload into stdin (optional, defaults to empty)
                       If provided, this data is available immediately when program reads
        
        Returns:
            dict with keys: success, output, error
        """
        temp_dir = tempfile.mkdtemp(prefix="coding_tutor_")
        try:
            if language == "python":
                filename = "main.py"
                if stdin_data:
                    run_cmd = f"python3 -u /sandbox/main.py << 'EOF'\n{stdin_data}\nEOF"
                else:
                    run_cmd = "python3 -u /sandbox/main.py < /dev/null"

            elif language == "c":
                filename = "main.c"
                if stdin_data:
                    run_cmd = f"gcc /sandbox/main.c -o /sandbox/a.out && /sandbox/a.out << 'EOF'\n{stdin_data}\nEOF"
                else:
                    run_cmd = "gcc /sandbox/main.c -o /sandbox/a.out && /sandbox/a.out < /dev/null"

            elif language == "cpp":
                filename = "main.cpp"
                if stdin_data:
                    run_cmd = f"g++ /sandbox/main.cpp -o /sandbox/a.out && /sandbox/a.out << 'EOF'\n{stdin_data}\nEOF"
                else:
                    run_cmd = "g++ /sandbox/main.cpp -o /sandbox/a.out && /sandbox/a.out < /dev/null"

            elif language == "java":
                filename = "Main.java"
                if 'public class Main' not in code and 'class Main' not in code:
                    if 'public class' not in code:
                        code = f'public class Main {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}'
                if stdin_data:
                    run_cmd = f"javac /sandbox/Main.java && java -cp /sandbox Main << 'EOF'\n{stdin_data}\nEOF"
                else:
                    run_cmd = "javac /sandbox/Main.java && java -cp /sandbox Main < /dev/null"

            else:
                return {"success": False, "error": "Unsupported language"}

            with open(os.path.join(temp_dir, filename), "w", encoding="utf-8") as f:
                f.write(code)

            # Docker execution configuration
            # Use -i (interactive) only when stdin_data is provided
            # This ensures non-interactive execution when no input is needed
            docker_base_cmd = ["docker", "run", "--rm"]
            if stdin_data:
                docker_base_cmd.append("-i")  # Interactive mode for stdin injection
            docker_base_cmd.extend([
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "-v", f"{temp_dir}:/sandbox",
                self.SANDBOX_IMAGE,
                "sh", "-c", run_cmd
            ])

            # Execute in non-interactive Docker container
            # stdin_data is injected via subprocess input parameter (not TTY)
            result = subprocess.run(
                docker_base_cmd,
                input=stdin_data if stdin_data else "",  # Preload stdin data before execution
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT,
                encoding='utf-8',
                errors='replace'
            )

            # Combine stdout and stderr for error messages
            output = result.stdout.strip() if result.stdout else ""
            error = result.stderr.strip() if result.stderr else ""
            
            # Check for input-related issues in non-interactive environment
            # Programs that wait for input will timeout or get EOF
            input_related_errors = [
                "EOFError",
                "EOF",
                "end of file",
                "unexpected end of input",
                "no input available"
            ]
            
            # If return code is non-zero, include stderr in error
            if result.returncode != 0:
                if error:
                    # Check if it's a compilation error
                    if "error:" in error.lower() or "undefined" in error.lower() or "expected" in error.lower():
                        error = f"Compilation Error: {error}"
                    # Check if it's an input-related error in non-interactive mode
                    elif any(err in error for err in input_related_errors):
                        if not stdin_data:
                            error = f"Input Error: Program expects input but none was provided. Use the 'Program Input' field to provide input values."
                        else:
                            error = f"Input Error: {error}"
                    else:
                        error = f"Runtime Error (Exit code {result.returncode}): {error}"
                else:
                    # Check output for input-related messages
                    if not stdin_data and any(indicator in output.lower() for indicator in ["input", "enter", "scanf", "cin", "read"]):
                        error = f"Program expects input but none was provided. Use the 'Program Input' field to provide input values."
                    else:
                        error = f"Program exited with error code {result.returncode}"

            return {
                "success": result.returncode == 0,
                "output": output,
                "error": error
            }

        except subprocess.TimeoutExpired:
            # Check if program might be waiting for input
            if not stdin_data:
                return {"success": False, "error": "Execution timed out. Your program may be waiting for input. Use the 'Program Input' field to provide input values, or check for infinite loops."}
            return {"success": False, "error": "Execution timed out after 120 seconds. Your program may be running too long or stuck in an infinite loop."}

        except Exception as e:
            return {"success": False, "error": str(e)}

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)