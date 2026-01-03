import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    """
    Get information about files and directories within the working directory boundaries.
    
    Args:
        working_directory: The permitted working directory path
        directory: The directory to list (relative to working_directory)
    
    Returns:
        String representation of directory contents or error message
    """
    try:
        # Get absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_dir_abs = os.path.abspath(os.path.join(working_directory, directory))
        
        # Check if target directory is within working directory boundaries
        try:
            within = os.path.commonpath([working_dir_abs, target_dir_abs]) == working_dir_abs
        except ValueError:
            # Raised if paths are on different drives - treat as outside
            within = False
        if not within:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if target path exists and is a directory
        if not os.path.exists(target_dir_abs):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(target_dir_abs):
            return f'Error: "{directory}" is not a directory'
        
        # List directory contents
        entries = []
        for item in os.listdir(target_dir_abs):
            item_path = os.path.join(target_dir_abs, item)
            try:
                file_size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                entries.append(f" - {item}: file_size={file_size} bytes, is_dir={is_dir}")
            except OSError as e:
                entries.append(f" - {item}: Error getting info - {str(e)}")
        
        # Sort entries for consistent output
        entries.sort()
        
        return "\n".join(entries)
        
    except Exception as e:
        return f"Error: {str(e)}"


# Schema declaration for the LLM to understand how to use this function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
