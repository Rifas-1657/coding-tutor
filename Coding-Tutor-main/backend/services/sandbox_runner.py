"""
Docker-based sandbox runner for secure code execution.
All code execution happens inside isolated Docker containers using Docker CLI.
Non-interactive execution model (like CodeChef/HackerRank).
"""

import subprocess
import tempfile
import shutil
import os


class DockerSandboxRunner:
    """Execute code in isolated Docker containers using Docker CLI."""
    
    SANDBOX_IMAGE = "coding-tutor-sandbox:latest"
    TIMEOUT = 30

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
        Non-interactive execution: input provided upfront, output returned.
        
        Args:
            language: One of 'python', 'c', 'cpp', 'java'
            code: Source code to execute
            stdin_data: Input data for program (provided upfront, can be empty string)
        
        Returns:
            dict with keys: success, output, error
        """
        temp_dir = tempfile.mkdtemp(prefix="coding_tutor_")
        try:
            if language == "python":
                filename = "main.py"
                run_cmd = "python3 -u /sandbox/main.py"

            elif language == "c":
                filename = "main.c"
                run_cmd = "gcc /sandbox/main.c -o /sandbox/a.out && /sandbox/a.out"

            elif language == "cpp":
                filename = "main.cpp"
                run_cmd = "g++ /sandbox/main.cpp -o /sandbox/a.out && /sandbox/a.out"

            elif language == "java":
                filename = "Main.java"
                run_cmd = "javac /sandbox/Main.java && java -cp /sandbox Main"
                # Ensure code has public class Main
                if 'public class Main' not in code and 'class Main' not in code:
                    if 'public class' not in code:
                        code = f'public class Main {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}'

            else:
                return {"success": False, "error": "Unsupported language"}

            with open(os.path.join(temp_dir, filename), "w", encoding="utf-8") as f:
                f.write(code)

            docker_cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "-i",
                "-v", f"{temp_dir}:/sandbox",
                self.SANDBOX_IMAGE,
                "sh", "-c", run_cmd
            ]

            result = subprocess.run(
                docker_cmd,
                input=stdin_data,
                text=True,
                capture_output=True,
                timeout=self.TIMEOUT
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Execution timed out"}

        except Exception as e:
            return {"success": False, "error": str(e)}

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
