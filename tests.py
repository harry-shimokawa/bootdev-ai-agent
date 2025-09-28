"""
Test module for the bootdev-ai-agent application.

This module contains tests for file operations including writing and reading.
"""

from functions.write_file import write_file


def test_write_file():
    """Test the write_file function with various inputs."""
    
    # Test 1: Write a valid file with 28 characters
    content1 = "This is a test file content."  # 28 characters
    result1 = write_file(".", "test_output.txt", content1)
    print(result1)
    
    # Test 2: Write another file with 26 characters  
    content2 = "Another test file content!"  # 26 characters
    result2 = write_file(".", "another_test.txt", content2)
    print(result2)
    
    # Test 3: Try to write outside working directory (should fail)
    result3 = write_file(".", "../outside.txt", "Should fail")
    print(result3)


if __name__ == "__main__":
    test_write_file()
