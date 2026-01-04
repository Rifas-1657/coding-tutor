# Offline Intelligent Lab Code Tutor

An offline code execution and testing system for lab exercises with intelligent hint generation.

## Features

- **Offline Execution**: No internet, Docker, or cloud required
- **Interactive I/O**: Real stdin/stdout support (input(), scanf, cin, Scanner)
- **Multi-language**: Supports C, C++, Java, Python
- **Testcase Engine**: Automatic testcase execution and comparison
- **Hint System**: Intelligent hint generation (RAG + LLM integration ready)
- **Clean Architecture**: Well-separated modules

## Architecture

```
offline_tutor/
├── executor.py      # Core execution engine (interactive stdin/stdout)
├── tester.py        # Testcase engine (compares actual vs expected)
├── hint_engine.py   # Hint generation (placeholder for RAG/LLM)
├── rag_engine.py    # RAG engine (placeholder for local embeddings)
└── test_executor.py # Comprehensive test suite
```

## Quick Start

### Basic Execution

```python
from offline_tutor import OfflineExecutor

executor = OfflineExecutor()

# Start execution
code = """n = int(input())
print(n * 2)"""

result = executor.start_execution(code, 'python')
executor.send_input("5")
completion = executor.wait_for_completion()

print(completion['stdout'])  # Output: 10
```

### Testcase Execution

```python
from offline_tutor import TestCase, LabExercise, TestRunner, OfflineExecutor

executor = OfflineExecutor()
test_runner = TestRunner(executor)

# Create testcases
testcases = [
    TestCase("5", "10", "Test with 5"),
    TestCase("3", "6", "Test with 3"),
]

# Create exercise
exercise = LabExercise(
    exercise_id="ex1",
    title="Double the Number",
    description="Read a number and print its double",
    testcases=testcases
)

# Run tests
results = test_runner.run_exercise(student_code, 'python', exercise)
print(f"Passed: {results['passed']}/{results['total_tests']}")
```

### Hint Generation

```python
from offline_tutor import HintEngine, TestResult

hint_engine = HintEngine()

failed_testcases = [{
    "result": TestResult.LOGICAL_ERROR,
    "expected_output": "10",
    "actual_output": "5"
}]

hint = hint_engine.generate_hint(
    student_code,
    'python',
    failed_testcases,
    "Double the number"
)

print(hint['hint_english'])
```

## Running Tests

```bash
cd offline_tutor
python test_executor.py
```

## Requirements

- Python 3.7+
- gcc (for C)
- g++ (for C++)
- javac (for Java)
- python (for Python)

All compilers must be installed locally and available in PATH.

## Language Support

- **C**: Uses `gcc` for compilation
- **C++**: Uses `g++` for compilation
- **Java**: Uses `javac` and `java`
- **Python**: Uses `python` interpreter

## Execution Model

- **Interactive**: Process stays alive, waits for input
- **Real stdin/stdout**: Uses subprocess.Popen with pipes
- **Line-by-line output**: Captures stdout/stderr in real-time
- **Timeout protection**: Kills infinite loops after timeout

## Future Enhancements

- **RAG Integration**: Local embeddings + semantic search
- **Local LLM**: Generate hints using local language model
- **Multi-language hints**: Tanglish, English, Hindi
- **Code analysis**: Advanced code structure analysis

