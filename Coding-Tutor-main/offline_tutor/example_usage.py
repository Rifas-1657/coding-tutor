"""
Example usage of Offline Tutor
Demonstrates how to use the executor, tester, and hint engine.
"""

from offline_tutor import OfflineExecutor, TestCase, LabExercise, TestRunner, TestResult, HintEngine


def example_interactive_execution():
    """Example: Interactive code execution."""
    print("=" * 60)
    print("EXAMPLE 1: Interactive Execution")
    print("=" * 60)
    
    executor = OfflineExecutor()
    
    # Python code that reads input
    code = """n = int(input())
for i in range(1, n + 1):
    print(i * i)"""
    
    # Start execution
    result = executor.start_execution(code, 'python')
    print(f"Execution started: {result['success']}")
    
    # Send input
    executor.send_input("5")
    
    # Wait for completion
    completion = executor.wait_for_completion()
    print(f"Output: {completion['stdout']}")
    print(f"Return code: {completion['returncode']}")


def example_testcase_execution():
    """Example: Running testcases."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Testcase Execution")
    print("=" * 60)
    
    executor = OfflineExecutor()
    test_runner = TestRunner(executor)
    
    # Create testcases
    testcases = [
        TestCase("5", "1\n4\n9\n16\n25", "Test with n=5"),
        TestCase("3", "1\n4\n9", "Test with n=3"),
        TestCase("1", "1", "Test with n=1"),
    ]
    
    # Create exercise
    exercise = LabExercise(
        exercise_id="ex1",
        title="Square Numbers",
        description="Print squares of numbers from 1 to n",
        testcases=testcases
    )
    
    # Student code (correct)
    student_code = """n = int(input())
for i in range(1, n + 1):
    print(i * i)"""
    
    # Run tests
    results = test_runner.run_exercise(student_code, 'python', exercise)
    
    print(f"Exercise: {results['exercise_id']}")
    print(f"Total tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    
    for i, test_result in enumerate(results['results']):
        print(f"\nTest {i+1}: {test_result['result'].value}")
        if test_result['result'] != TestResult.PASS:
            print(f"  Expected: {test_result['expected_output']}")
            print(f"  Got: {test_result['actual_output']}")


def example_hint_generation():
    """Example: Generating hints."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Hint Generation")
    print("=" * 60)
    
    hint_engine = HintEngine()
    
    # Student code with error
    student_code = """n = int(input())
for i in range(1, n):
    print(i * i)"""
    
    # Failed testcase
    failed_testcases = [{
        "result": TestResult.LOGICAL_ERROR,
        "expected_output": "1\n4\n9",
        "actual_output": "1\n4"
    }]
    
    # Generate hint
    hint = hint_engine.generate_hint(
        student_code,
        'python',
        failed_testcases,
        "Print squares from 1 to n"
    )
    
    print(f"Hint (English): {hint['hint_english']}")
    print(f"Hint (Tanglish): {hint['hint_tanglish']}")
    print(f"Hint (Hindi): {hint['hint_hindi']}")


if __name__ == "__main__":
    try:
        example_interactive_execution()
        example_testcase_execution()
        example_hint_generation()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

