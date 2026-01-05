"""
Docker Sandbox Runner
Executes code in isolated Docker containers with non-interactive stdin.
"""

import subprocess
import tempfile
import shutil
import os


class SandboxRunner:
    """Execute code in isolated Docker containers with non-interactive stdin."""
    
    SANDBOX_IMAGE = "coding-tutor-sandbox:latest"
    TIMEOUT = 30
    
    def __init__(self):
        """Initialize sandbox runner."""
        self._verify_docker()
    
    def _verify_docker(self):
        """Verify Docker CLI is available."""
        try:
            result = subprocess.run(
                ['docker', '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode != 0:
                raise RuntimeError("Docker CLI not available. Please ensure Docker Desktop is running.")
        except FileNotFoundError:
            raise RuntimeError("Docker CLI not found. Please ensure Docker Desktop is installed and running.")
        except Exception as e:
            raise RuntimeError(f"Docker CLI check failed: {str(e)}")
    
    def run_code(self, language: str, code: str, stdin_data: str = "") -> dict:
        """
        Execute code in Docker container with non-interactive stdin.
        Stdin is closed immediately to prevent hanging.
        
        Args:
            language: One of 'python', 'c', 'cpp', 'java' (case-insensitive)
            code: Source code to execute
            stdin_data: Input data (optional, defaults to empty)
        
        Returns:
            dict with keys: success, output, error
        """
        # Normalize language to lowercase
        language = language.lower().strip()
        
        temp_dir = tempfile.mkdtemp(prefix="coding_tutor_")
        try:
            # Determine filename and compile/run command
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
                return {"success": False, "error": f"Unsupported language: {language}"}
            
            # Write code to temp file
            code_file = os.path.join(temp_dir, filename)
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)
            
            # Execute in Docker (non-interactive, stdin closed)
            docker_cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "-v", f"{temp_dir}:/sandbox",
                self.SANDBOX_IMAGE,
                "sh", "-c", run_cmd
            ]
            
            result = subprocess.run(
                docker_cmd,
                text=True,
                input=stdin_data if stdin_data else "",
                capture_output=True,
                timeout=self.TIMEOUT,
                encoding='utf-8',
                errors='replace'
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip() if result.stdout else "",
                "error": result.stderr.strip() if result.stderr else ""
            }
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Execution timed out (program may be waiting for input)"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

