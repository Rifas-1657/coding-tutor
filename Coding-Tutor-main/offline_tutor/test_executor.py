"""
Comprehensive tests for OfflineExecutor
Tests all languages and edge cases.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from offline_tutor.executor import OfflineExecutor
import time


def test_python_input():
    """Test Python input()."""
    print("TEST 1: Python input()...")
    executor = OfflineExecutor()
    
    code = """x = int(input())
print(x * 2)"""
    
    result = executor.start_execution(code, 'python')
    assert result["success"], f"Start failed: {result.get('message')}"
    
    executor.send_input("5")
    
    output = executor.read_output(timeout=0.5)
    time.sleep(0.2)  # Give process time to process
    
    completion = executor.wait_for_completion()
    assert completion["success"], f"Execution failed: {completion.get('message')}"
    assert "10" in completion["stdout"], f"Expected '10', got '{completion['stdout']}'"
    print("✅ PASS")


def test_python_loops():
    """Test Python loops."""
    print("TEST 2: Python loops...")
    executor = OfflineExecutor()
    
    code = """n = int(input())
for i in range(1, n + 1):
    print(i * i)"""
    
    result = executor.start_execution(code, 'python')
    assert result["success"]
    
    executor.send_input("3")
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "1" in completion["stdout"] and "4" in completion["stdout"] and "9" in completion["stdout"]
    print("✅ PASS")


def test_c_scanf():
    """Test C scanf."""
    print("TEST 3: C scanf...")
    executor = OfflineExecutor()
    
    code = """#include <stdio.h>
int main() {
    int x;
    scanf("%d", &x);
    printf("%d", x * 2);
    return 0;
}"""
    
    result = executor.start_execution(code, 'c')
    assert result["success"], f"Start failed: {result.get('message')}"
    
    executor.send_input("7")
    
    completion = executor.wait_for_completion()
    assert completion["success"], f"Execution failed: {completion.get('message')}"
    assert "14" in completion["stdout"], f"Expected '14', got '{completion['stdout']}'"
    print("✅ PASS")


def test_c_nested_loops():
    """Test C nested loops."""
    print("TEST 4: C nested loops...")
    executor = OfflineExecutor()
    
    code = """#include <stdio.h>
int main() {
    int n;
    scanf("%d", &n);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            printf("%d ", j);
        }
        printf("\\n");
    }
    return 0;
}"""
    
    result = executor.start_execution(code, 'c')
    assert result["success"]
    
    executor.send_input("3")
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "1" in completion["stdout"] and "2" in completion["stdout"]
    print("✅ PASS")


def test_c_array_input():
    """Test C array input."""
    print("TEST 5: C array input...")
    executor = OfflineExecutor()
    
    code = """#include <stdio.h>
int main() {
    int n, arr[10];
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    return 0;
}"""
    
    result = executor.start_execution(code, 'c')
    assert result["success"]
    
    executor.send_input("3")
    executor.send_input("10")
    executor.send_input("20")
    executor.send_input("30")
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "10" in completion["stdout"] and "20" in completion["stdout"] and "30" in completion["stdout"]
    print("✅ PASS")


def test_cpp_cin():
    """Test C++ cin."""
    print("TEST 6: C++ cin...")
    executor = OfflineExecutor()
    
    code = """#include <iostream>
using namespace std;
int main() {
    int x;
    cin >> x;
    cout << x * 2;
    return 0;
}"""
    
    result = executor.start_execution(code, 'cpp')
    assert result["success"]
    
    executor.send_input("6")
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "12" in completion["stdout"]
    print("✅ PASS")


def test_java_scanner():
    """Test Java Scanner."""
    print("TEST 7: Java Scanner...")
    executor = OfflineExecutor()
    
    code = """import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int x = sc.nextInt();
        System.out.println(x * 3);
    }
}"""
    
    result = executor.start_execution(code, 'java')
    assert result["success"]
    
    executor.send_input("4")
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "12" in completion["stdout"]
    print("✅ PASS")


def test_java_array():
    """Test Java array."""
    print("TEST 8: Java array...")
    executor = OfflineExecutor()
    
    code = """import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }
        int sum = 0;
        for (int x : arr) {
            sum += x;
        }
        System.out.println(sum);
    }
}"""
    
    result = executor.start_execution(code, 'java')
    assert result["success"]
    
    executor.send_input("3")
    executor.send_input("10")
    executor.send_input("20")
    executor.send_input("30")
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "60" in completion["stdout"]
    print("✅ PASS")


def test_timeout():
    """Test timeout protection."""
    print("TEST 9: Timeout protection...")
    executor = OfflineExecutor(timeout=2)
    
    code = """#include <stdio.h>
int main() {
    while(1) {}
    return 0;
}"""
    
    result = executor.start_execution(code, 'c')
    assert result["success"]
    
    completion = executor.wait_for_completion()
    assert not completion["success"]
    assert "timeout" in completion.get("message", "").lower() or completion.get("error_type") == "TIMEOUT"
    print("✅ PASS")


def test_compile_error():
    """Test compile error handling."""
    print("TEST 10: Compile error handling...")
    executor = OfflineExecutor()
    
    code = "invalid syntax!!!"
    
    result = executor.start_execution(code, 'c')
    assert not result["success"]
    assert "compile" in result.get("message", "").lower() or result.get("error_type") == "COMPILE_ERROR"
    print("✅ PASS")


def test_no_input():
    """Test program with no input."""
    print("TEST 11: No input program...")
    executor = OfflineExecutor()
    
    code = """#include <stdio.h>
int main() {
    printf("Hello");
    return 0;
}"""
    
    result = executor.start_execution(code, 'c')
    assert result["success"]
    
    completion = executor.wait_for_completion()
    assert completion["success"]
    assert "Hello" in completion["stdout"]
    print("✅ PASS")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING OFFLINE EXECUTOR TESTS")
    print("=" * 60)
    
    tests = [
        test_python_input,
        test_python_loops,
        test_c_scanf,
        test_c_nested_loops,
        test_c_array_input,
        test_cpp_cin,
        test_java_scanner,
        test_java_array,
        test_timeout,
        test_compile_error,
        test_no_input,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

