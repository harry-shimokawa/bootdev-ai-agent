"""
System prompt module for the bootdev-ai-agent.

This module provides the system prompt functionality.
"""


def get_system_prompt():
    """
    Get the system prompt for the AI agent.
    
    Returns:
        String containing the system prompt
    """
    return """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""