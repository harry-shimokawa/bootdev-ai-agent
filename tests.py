"""
Test module for the bootdev-ai-agent application.

This module contains manual tests for the get_file_content function
to validate file reading and truncation functionality.
"""

from functions.get_file_content import get_file_content


def test_get_file_content_manual():
    """Test the get_file_content function with various inputs."""
    # Test 1: Test truncation with lorem.txt (over 20,000 chars)
    print('get_file_content("calculator", "lorem.txt"):')
    result1 = get_file_content("calculator", "lorem.txt")
    print(f"Length of content: {len(result1)} characters")
    print("First 200 characters:")
    print(result1[:200])
    print("Last 200 characters:")
    print(result1[-200:])
    print()

    # Test 2: Read calculator main.py
    print('get_file_content("calculator", "main.py"):')
    result2 = get_file_content("calculator", "main.py")
    print("Result:")
    print(result2)
    print()

    # Test 3: Read calculator.py from pkg directory
    print('get_file_content("calculator", "pkg/calculator.py"):')
    result3 = get_file_content("calculator", "pkg/calculator.py")
    print("Result:")
    print(result3)
    print()

    # Test 4: Try to access /bin/cat (should fail - outside working directory)
    print('get_file_content("calculator", "/bin/cat"):')
    result4 = get_file_content("calculator", "/bin/cat")
    print("Result:")
    print(f"    {result4}")
    print()

    # Test 5: Try to access non-existent file (should fail)
    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    result5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result:")
    print(f"    {result5}")
    print()


if __name__ == "__main__":
    test_get_file_content_manual()
