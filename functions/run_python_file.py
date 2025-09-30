"""
Module for safely running Python files within a working directory.

This module provides functionality to execute Python files with security
constraints and timeout protection.
"""

import os
import subprocess
import sys


def is_within_directory(working_directory, file_path):
    """Check if file_path is within the working_directory bounds."""
    working_dir_abs = os.path.abspath(working_directory)
    target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))
    return target_file_abs.startswith(working_dir_abs)


def run_python_file(working_directory, file_path, args=None):
    """
    Execute a Python file within the working directory with safety constraints.
    
    Args:
        working_directory: Base directory where execution is permitted
        file_path: Path to Python file (relative to working_directory)  
        args: Optional list of command line arguments to pass to the script
        
    Returns:
        String containing execution results or error message
    """
    if args is None:
        args = []
        
    try:
        # Check if file_path is outside the working directory
        if not is_within_directory(working_directory, file_path):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        # Construct full file path
        full_file_path = os.path.join(working_directory, file_path)

        # Check if file exists
        if not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'

        # Check if file is a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute the Python file with subprocess
        completed_process = subprocess.run(
            [sys.executable, file_path] + args,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        result_parts = []
        
        # Add stdout if present
        if completed_process.stdout:
            result_parts.append(f"STDOUT: {completed_process.stdout.strip()}")
        
        # Add stderr if present  
        if completed_process.stderr:
            result_parts.append(f"STDERR: {completed_process.stderr.strip()}")
            
        # Add exit code if non-zero
        if completed_process.returncode != 0:
            result_parts.append(f"Process exited with code {completed_process.returncode}")

        if not result_parts:
            return "No output produced."

        return "\n".join(result_parts)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds."
    except Exception as e:
        return f"Error executing Python file: {e}"

