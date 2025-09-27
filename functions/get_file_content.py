import os
from config import MAX_FILE_SIZE_CHARS


def get_file_content(working_directory, file_path):
    """
    Read the content of a file within the working directory boundaries.
    
    Args:
        working_directory: The permitted working directory path
        file_path: The file path to read (relative to working_directory)
    
    Returns:
        String content of the file or error message
    """
    try:
        # Get absolute paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Check if target file is within working directory boundaries
        if not target_file_abs.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if target path exists and is a regular file
        if not os.path.exists(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        if not os.path.isfile(target_file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file content
        with open(target_file_abs, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Truncate if too long
        if len(content) > MAX_FILE_SIZE_CHARS:
            content = content[:MAX_FILE_SIZE_CHARS]
            content += f'[...File "{file_path}" truncated at {MAX_FILE_SIZE_CHARS} characters]'
        
        return content
        
    except UnicodeDecodeError:
        return f'Error: Cannot decode file "{file_path}" as UTF-8 text'
    except PermissionError:
        return f'Error: Permission denied reading file "{file_path}"'
    except Exception as e:
        return f"Error: {str(e)}"
