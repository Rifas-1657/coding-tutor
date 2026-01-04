"""
Testcase Engine for Lab Exercises
Compares actual output with expected output.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class TestResult(Enum):
    """Test result types."""
    PASS = "PASS"
    COMPILE_ERROR = "COMPILE_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    LOGICAL_ERROR = "LOGICAL_ERROR"
    TIMEOUT = "TIMEOUT"


class TestCase:
    """Represents a single test case."""
    
    def __init__(self, input_data: str, expected_output: str, description: str = ""):
        """
        Initialize test case.
        
        Args:
            input_data: Input for the program
            expected_output: Expected output
            description: Optional description
        """
        self.input_data = input_data
        self.expected_output = expected_output.strip()
        self.description = description
    
    def normalize_output(self, output: str) -> str:
        """
        Normalize output for comparison (remove trailing whitespace, normalize newlines).
        
        Args:
            output: Output string to normalize
        
        Returns:
            Normalized output
        """
        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in output.strip().split('\n')]
        # Remove empty lines at end
        while lines and not lines[-1]:
            lines.pop()
        return '\n'.join(lines)


class LabExercise:
    """Represents a lab exercise with testcases."""
    
    def __init__(self, exercise_id: str, title: str, description: str, testcases: List[TestCase]):
        """
        Initialize lab exercise.
        
        Args:
            exercise_id: Unique identifier
            title: Exercise title
            description: Exercise description
            testcases: List of test cases
        """
        self.exercise_id = exercise_id
        self.title = title
        self.description = description
        self.testcases = testcases


class TestRunner:
    """Runs testcases against code execution."""
    
    def __init__(self, executor):
        """
        Initialize test runner.
        
        Args:
            executor: OfflineExecutor instance
        """
        self.executor = executor
    
    def run_testcase(
        self,
        code: str,
        language: str,
        testcase: TestCase
    ) -> Dict[str, Any]:
        """
        Run a single testcase.
        
        Args:
            code: Source code
            language: Programming language
            testcase: TestCase to run
        
        Returns:
            dict with keys: result, actual_output, expected_output, message
        """
        # Start execution
        start_result = self.executor.start_execution(code, language)
        if not start_result["success"]:
            return {
                "result": TestResult.COMPILE_ERROR,
                "actual_output": "",
                "expected_output": testcase.expected_output,
                "message": start_result.get("message", "Compilation failed")
            }
        
        # Send input
        if testcase.input_data:
            input_result = self.executor.send_input(testcase.input_data)
            if not input_result["success"]:
                self.executor.stop_execution()
                return {
                    "result": TestResult.RUNTIME_ERROR,
                    "actual_output": "",
                    "expected_output": testcase.expected_output,
                    "message": "Failed to send input"
                }
        
        # Wait for completion
        completion_result = self.executor.wait_for_completion()
        
        if not completion_result["success"]:
            error_type = completion_result.get("error_type", "RUNTIME_ERROR")
            if error_type == "TIMEOUT":
                return {
                    "result": TestResult.TIMEOUT,
                    "actual_output": completion_result.get("stdout", ""),
                    "expected_output": testcase.expected_output,
                    "message": "Execution timed out"
                }
            else:
                return {
                    "result": TestResult.RUNTIME_ERROR,
                    "actual_output": completion_result.get("stdout", ""),
                    "expected_output": testcase.expected_output,
                    "message": completion_result.get("message", "Runtime error"),
                    "stderr": completion_result.get("stderr", "")
                }
        
        # Compare outputs
        actual_output = completion_result.get("stdout", "")
        normalized_actual = testcase.normalize_output(actual_output)
        normalized_expected = testcase.normalize_output(testcase.expected_output)
        
        if normalized_actual == normalized_expected:
            return {
                "result": TestResult.PASS,
                "actual_output": actual_output,
                "expected_output": testcase.expected_output,
                "message": "Test passed"
            }
        else:
            return {
                "result": TestResult.LOGICAL_ERROR,
                "actual_output": actual_output,
                "expected_output": testcase.expected_output,
                "message": "Output mismatch"
            }
    
    def run_exercise(
        self,
        code: str,
        language: str,
        exercise: LabExercise
    ) -> Dict[str, Any]:
        """
        Run all testcases for an exercise.
        
        Args:
            code: Source code
            language: Programming language
            exercise: LabExercise to run
        
        Returns:
            dict with keys: exercise_id, total_tests, passed, failed, results
        """
        results = []
        passed = 0
        failed = 0
        
        for i, testcase in enumerate(exercise.testcases):
            test_result = self.run_testcase(code, language, testcase)
            results.append({
                "testcase_index": i,
                "description": testcase.description,
                **test_result
            })
            
            if test_result["result"] == TestResult.PASS:
                passed += 1
            else:
                failed += 1
        
        return {
            "exercise_id": exercise.exercise_id,
            "total_tests": len(exercise.testcases),
            "passed": passed,
            "failed": failed,
            "results": results
        }

