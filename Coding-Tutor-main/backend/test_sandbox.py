"""
Comprehensive test suite for DockerSandboxRunner.
Tests all critical functionality to ensure production-grade quality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.sandbox_runner import DockerSandboxRunner


def test_c_scanf():
    """Test C program with scanf."""
    print("TEST 1: C scanf...")
    runner = DockerSandboxRunner()
    code = """#include <stdio.h>
int main() {
    int x;
    scanf("%d", &x);
    printf("%d", x * 2);
    return 0;
}"""
    result = runner.run_code("c", code, "5\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "10", f"Expected '10', got '{result['output']}'"
    print("✅ PASS")


def test_c_nested_loops():
    """Test C nested loops."""
    print("TEST 2: C nested loops...")
    runner = DockerSandboxRunner()
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
    result = runner.run_code("c", code, "3\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert "1" in result["output"] and "2" in result["output"], f"Unexpected output: {result['output']}"
    print("✅ PASS")


def test_c_array_input():
    """Test C array input."""
    print("TEST 3: C array input...")
    runner = DockerSandboxRunner()
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
    result = runner.run_code("c", code, "3\n1 2 3\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert "1" in result["output"] and "2" in result["output"] and "3" in result["output"]
    print("✅ PASS")


def test_c_multiple_inputs():
    """Test C multiple inputs."""
    print("TEST 4: C multiple inputs...")
    runner = DockerSandboxRunner()
    code = """#include <stdio.h>
int main() {
    int a, b, c;
    scanf("%d %d %d", &a, &b, &c);
    printf("%d", a + b + c);
    return 0;
}"""
    result = runner.run_code("c", code, "1 2 3\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "6", f"Expected '6', got '{result['output']}'"
    print("✅ PASS")


def test_c_no_input():
    """Test C program with no input."""
    print("TEST 5: C no input...")
    runner = DockerSandboxRunner()
    code = """#include <stdio.h>
int main() {
    printf("Hello");
    return 0;
}"""
    result = runner.run_code("c", code, "")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "Hello", f"Expected 'Hello', got '{result['output']}'"
    print("✅ PASS")


def test_c_timeout():
    """Test C infinite loop protection (timeout)."""
    print("TEST 6: C timeout protection...")
    runner = DockerSandboxRunner()
    code = """#include <stdio.h>
int main() {
    while(1) {}
    return 0;
}"""
    result = runner.run_code("c", code, "")
    assert not result["success"], "Timeout should fail"
    assert "timed out" in result["error"].lower() or "timeout" in result["error"].lower()
    print("✅ PASS")


def test_python_input():
    """Test Python input()."""
    print("TEST 7: Python input()...")
    runner = DockerSandboxRunner()
    code = """x = int(input())
print(x * 2)"""
    result = runner.run_code("python", code, "7\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "14", f"Expected '14', got '{result['output']}'"
    print("✅ PASS")


def test_python_loops():
    """Test Python loops."""
    print("TEST 8: Python loops...")
    runner = DockerSandboxRunner()
    code = """n = int(input())
for i in range(1, n + 1):
    print(i * i)"""
    result = runner.run_code("python", code, "3\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert "1" in result["output"] and "4" in result["output"] and "9" in result["output"]
    print("✅ PASS")


def test_java_scanner():
    """Test Java Scanner input."""
    print("TEST 9: Java Scanner...")
    runner = DockerSandboxRunner()
    code = """import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int x = sc.nextInt();
        System.out.println(x * 3);
    }
}"""
    result = runner.run_code("java", code, "4\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "12", f"Expected '12', got '{result['output']}'"
    print("✅ PASS")


def test_java_class_array():
    """Test Java class + array."""
    print("TEST 10: Java class + array...")
    runner = DockerSandboxRunner()
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
    result = runner.run_code("java", code, "3\n10 20 30\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "60", f"Expected '60', got '{result['output']}'"
    print("✅ PASS")


def test_java_nested_loops():
    """Test Java nested loops."""
    print("TEST 11: Java nested loops...")
    runner = DockerSandboxRunner()
    code = """import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(j + " ");
            }
            System.out.println();
        }
    }
}"""
    result = runner.run_code("java", code, "2\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert "1" in result["output"] and "2" in result["output"]
    print("✅ PASS")


def test_invalid_code():
    """Test invalid code handling."""
    print("TEST 12: Invalid code handling...")
    runner = DockerSandboxRunner()
    code = "invalid syntax here!!!"
    result = runner.run_code("c", code, "")
    assert not result["success"], "Invalid code should fail"
    assert result["error"], "Should have error message"
    print("✅ PASS")


def test_empty_input():
    """Test empty input handling."""
    print("TEST 13: Empty input handling...")
    runner = DockerSandboxRunner()
    code = """#include <stdio.h>
int main() {
    printf("OK");
    return 0;
}"""
    result = runner.run_code("c", code, "")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "OK", f"Expected 'OK', got '{result['output']}'"
    print("✅ PASS")


def test_cpp_cin():
    """Test C++ cin."""
    print("TEST 14: C++ cin...")
    runner = DockerSandboxRunner()
    code = """#include <iostream>
using namespace std;
int main() {
    int x;
    cin >> x;
    cout << x * 2;
    return 0;
}"""
    result = runner.run_code("cpp", code, "6\n")
    assert result["success"], f"Test failed: {result['error']}"
    assert result["output"] == "12", f"Expected '12', got '{result['output']}'"
    print("✅ PASS")


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("RUNNING COMPREHENSIVE SANDBOX TESTS")
    print("=" * 60)
    
    tests = [
        test_c_scanf,
        test_c_nested_loops,
        test_c_array_input,
        test_c_multiple_inputs,
        test_c_no_input,
        test_c_timeout,
        test_python_input,
        test_python_loops,
        test_java_scanner,
        test_java_class_array,
        test_java_nested_loops,
        test_invalid_code,
        test_empty_input,
        test_cpp_cin,
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
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("⚠️  SOME TESTS FAILED - FIXING ISSUES...")
        return False
    else:
        print("✅ ALL TESTS PASSED!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

