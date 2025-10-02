#!/usr/bin/env python3
"""
Test script to verify all function calling capabilities work correctly.
"""

import sys
import os

# Add the current directory to the path so we can import our functions
sys.path.insert(0, '.')

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content  
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test_get_files_info():
    """Test the get_files_info function."""
    print("=== Testing get_files_info ===")
    result = get_files_info(".", ".")
    print(f"Result: {result}")
    print()

def test_write_and_read_file():
    """Test writing and then reading a file."""
    print("=== Testing write_file and get_file_content ===")
    
    # Write a test file
    test_content = "Hello, World!\nThis is a test file.\nLine 3."
    write_result = write_file(".", "test_temp.txt", test_content)
    print(f"Write result: {write_result}")
    
    # Read the file back
    read_result = get_file_content(".", "test_temp.txt")
    print(f"Read result: {read_result}")
    
    # Clean up
    try:
        os.remove("test_temp.txt")
        print("Cleaned up test_temp.txt")
    except OSError:
        pass
    print()

def test_run_python_file():
    """Test running a Python file."""
    print("=== Testing run_python_file ===")
    
    # Create a simple Python script
    script_content = '''#!/usr/bin/env python3
print("Hello from test script!")
print("Args received:", end=" ")
import sys
print(sys.argv[1:])
'''
    
    # Write the script
    write_result = write_file(".", "test_script.py", script_content)
    print(f"Script write result: {write_result}")
    
    # Run the script with some arguments
    run_result = run_python_file(".", "test_script.py", ["arg1", "arg2"])
    print(f"Script execution result:\n{run_result}")
    
    # Clean up
    try:
        os.remove("test_script.py")
        print("Cleaned up test_script.py")
    except OSError:
        pass
    print()

if __name__ == "__main__":
    print("Testing all function calling capabilities...\n")
    
    test_get_files_info()
    test_write_and_read_file()
    test_run_python_file()
    
    print("All tests completed!")