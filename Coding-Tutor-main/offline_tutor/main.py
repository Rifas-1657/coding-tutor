"""
Main entry point for Offline Tutor
Command-line interface for testing and demonstration.
"""

import sys
import argparse
from offline_tutor import OfflineExecutor, TestCase, LabExercise, TestRunner, HintEngine


def run_interactive_demo():
    """Run interactive execution demo."""
    print("=" * 60)
    print("OFFLINE TUTOR - Interactive Execution Demo")
    print("=" * 60)
    
    executor = OfflineExecutor()
    
    print("\nEnter code (end with empty line):")
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    code = '\n'.join(code_lines)
    
    print("\nEnter language (c/cpp/java/python):")
    language = input().strip().lower()
    
    if language not in ['c', 'cpp', 'java', 'python']:
        print("Invalid language")
        return
    
    result = executor.start_execution(code, language)
    if not result["success"]:
        print(f"Error: {result.get('message')}")
        return
    
    print("\nExecution started. Enter input (empty line to finish):")
    while True:
        line = input()
        if not line:
            break
        executor.send_input(line)
    
    print("\nWaiting for completion...")
    completion = executor.wait_for_completion()
    
    print("\n" + "=" * 60)
    print("OUTPUT:")
    print("=" * 60)
    print(completion.get('stdout', ''))
    
    if completion.get('stderr'):
        print("\nSTDERR:")
        print(completion.get('stderr'))
    
    print(f"\nReturn code: {completion.get('returncode', -1)}")


def run_test_demo():
    """Run testcase demo."""
    print("=" * 60)
    print("OFFLINE TUTOR - Testcase Demo")
    print("=" * 60)
    
    executor = OfflineExecutor()
    test_runner = TestRunner(executor)
    
    # Example exercise
    testcases = [
        TestCase("5", "10", "Test with 5"),
        TestCase("3", "6", "Test with 3"),
    ]
    
    exercise = LabExercise(
        exercise_id="demo1",
        title="Double Number",
        description="Read number and print double",
        testcases=testcases
    )
    
    print("\nEnter code:")
    code_lines = []
    while True:
        line = input()
        if not line:
            break
        code_lines.append(line)
    
    code = '\n'.join(code_lines)
    
    print("\nEnter language (c/cpp/java/python):")
    language = input().strip().lower()
    
    print("\nRunning testcases...")
    results = test_runner.run_exercise(code, language, exercise)
    
    print(f"\nResults: {results['passed']}/{results['total_tests']} passed")
    
    for i, test_result in enumerate(results['results']):
        print(f"\nTest {i+1}: {test_result['result'].value}")
        if test_result['result'].value != "PASS":
            print(f"  Expected: {test_result['expected_output']}")
            print(f"  Got: {test_result['actual_output']}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Offline Intelligent Lab Code Tutor')
    parser.add_argument('--mode', choices=['interactive', 'test', 'run-tests'], 
                       default='interactive', help='Execution mode')
    
    args = parser.parse_args()
    
    if args.mode == 'run-tests':
        from offline_tutor.test_executor import run_all_tests
        success = run_all_tests()
        sys.exit(0 if success else 1)
    elif args.mode == 'interactive':
        run_interactive_demo()
    elif args.mode == 'test':
        run_test_demo()


if __name__ == "__main__":
    main()

