"""
Safely write file content within a working directory boundary.

Exposes a single function `write_file` that writes text content to a file
located under the provided `working_directory`. It creates parent directories
as needed, prevents path traversal outside the working directory, and returns
clear success or error messages.
"""

import os
from google.genai import types


def write_file(working_directory, file_path, content):
    """
    Write text content to a file within the working directory boundaries.

    Args:
        working_directory: Base directory where writes are permitted
        file_path: Target file path (relative to working_directory)
        content: String content to write

    Returns:
        A status string. On success:
            'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        On failure, a string starting with 'Error: ...'
    """
    try:
        # Resolve absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure target is within the working directory
        try:
            within = os.path.commonpath([working_dir_abs, target_abs]) == working_dir_abs
        except ValueError:
            # Raised if paths are on different drives (unlikely here) – treat as outside
            within = False
        if not within:
            return (
                f'Error: Cannot write "{file_path}" as it is outside '
                f'the permitted working directory'
            )

        # Ensure parent directories exist
        parent_dir = os.path.dirname(target_abs)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Disallow writing to a directory path
        if os.path.isdir(target_abs):
            return f'Error: Target path is a directory, not a file: "{file_path}"'

        # Write content (overwrite)
        with open(target_abs, 'w', encoding='utf-8') as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f'({len(content)} characters written)'
        )

    except PermissionError:
        return f'Error: Permission denied writing file "{file_path}"'
    except (OSError, IOError) as e:
        return f"Error writing file: {str(e)}"


# Schema declaration for function calling
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            )
        },
        required=["file_path", "content"]
    )
)
