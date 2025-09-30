"""
Test module for the bootdev-ai-agent application.

This module contains tests for running Python files.
"""

from functions.run_python_file import run_python_file


def test_run_python_file():
    """Test the run_python_file function with various inputs."""
    
    # Test 1: Run main.py without arguments (should print usage instructions)
    print("Test 1: run_python_file('calculator', 'main.py')")
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    print()
    
    # Test 2: Run main.py with calculator expression
    print("Test 2: run_python_file('calculator', 'main.py', ['3 + 5'])")
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result2)
    print()
    
    # Test 3: Run calculator tests.py
    print("Test 3: run_python_file('calculator', 'tests.py')")
    result3 = run_python_file("calculator", "tests.py")
    print(result3)
    print()
    
    # Test 4: Try to run file outside working directory (should fail)
    print("Test 4: run_python_file('calculator', '../main.py')")
    result4 = run_python_file("calculator", "../main.py")
    print(result4)
    print()
    
    # Test 5: Try to run non-existent file (should fail)
    print("Test 5: run_python_file('calculator', 'nonexistent.py')")
    result5 = run_python_file("calculator", "nonexistent.py")
    print(result5)


if __name__ == "__main__":
    test_run_python_file()
