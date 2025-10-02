"""
Main module for the bootdev-ai-agent application.

This module provides the core functionality for AI-powered agent operations
using Google's Generative AI services.
"""

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.system_prompt import get_system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file


def print_usage_stats(usage, verbose: bool) -> None:
    if verbose:
        # In verbose mode, print to stdout
        if usage:
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        else:
            print("Prompt tokens: N/A")
            print("Response tokens: N/A")
    else:
        # In non-verbose mode, don't print anything
        pass


def main() -> None:
    # Load env vars from .env
    load_dotenv()

    # Get API key from environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Missing GEMINI_API_KEY. Add it to your environment or to a .env file.", file=sys.stderr)
        sys.exit(1)

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Check for command line arguments for custom prompt and verbose flag
    if len(sys.argv) > 1:
        # Check if --verbose flag is present
        verbose = "--verbose" in sys.argv
        
        # Remove --verbose from arguments to get the prompt
        args_without_verbose = [arg for arg in sys.argv[1:] if arg != "--verbose"]
        
        if args_without_verbose:
            user_prompt = " ".join(args_without_verbose)
            if verbose:
                print(f"User prompt: {user_prompt}")
        else:
            print("Error: No prompt provided. Please provide a prompt as a command line argument.", file=sys.stderr)
            print("Usage: python main.py \"Your prompt here\" [--verbose]", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: No prompt provided. Please provide a prompt as a command line argument.", file=sys.stderr)
        print("Usage: python main.py \"Your prompt here\" [--verbose]", file=sys.stderr)
        sys.exit(1)

    # Create a list of types.Content with the user's prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        # Get the system prompt
        system_prompt = get_system_prompt()
        
        # Create available functions tool
        available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file,
            ]
        )
        
        # Call the model with the messages list, system prompt, and tools
        resp = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt
            ),
        )

        # Handle response - check for function calls first
        print("\n--- AI Response ---")
        
        # Check if there are function calls in the response
        if resp.candidates and resp.candidates[0].content.parts:
            for part in resp.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call_part = part.function_call
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                    
                    # Actually execute the function call
                    if function_call_part.name == "get_files_info":
                        directory = function_call_part.args.get("directory", ".")
                        result = get_files_info(".", directory)
                        print(f"Function result:\n{result}")
                    elif function_call_part.name == "get_file_content":
                        file_path = function_call_part.args.get("file_path")
                        result = get_file_content(".", file_path)
                        print(f"Function result:\n{result}")
                    elif function_call_part.name == "write_file":
                        file_path = function_call_part.args.get("file_path")
                        content = function_call_part.args.get("content")
                        result = write_file(".", file_path, content)
                        print(f"Function result:\n{result}")
                    elif function_call_part.name == "run_python_file":
                        file_path = function_call_part.args.get("file_path")
                        args = function_call_part.args.get("args", [])
                        result = run_python_file(".", file_path, args)
                        print(f"Function result:\n{result}")
                elif hasattr(part, 'text') and part.text:
                    print(part.text.strip())
        elif resp.text:
            print(resp.text.strip())
        else:
            print("No response received")
        
        # Consolidated usage stats printing
        usage = getattr(resp, "usage_metadata", None)
        print_usage_stats(usage, verbose)
            
    except Exception as e:
        print(f"Error generating response: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
