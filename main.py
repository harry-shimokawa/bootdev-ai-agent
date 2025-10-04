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


def call_function(function_call_part, verbose=False):
    """
    Handle the abstract task of calling one of our four functions.
    
    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: Whether to print detailed function call information
        
    Returns:
        types.Content with function response or error message
    """
    function_name = function_call_part.name
    
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Dictionary mapping function names to actual functions
    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    
    # Check if function name is valid
    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Get the function and add working_directory to args
    func = available_functions[function_name]
    args = dict(function_call_part.args)  # Make a copy
    args["working_directory"] = "./calculator"
    
    try:
        # Call the function with keyword arguments
        function_result = func(**args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing {function_name}: {str(e)}"},
                )
            ],
        )


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
        
        # Agent conversation loop - maximum 20 iterations
        max_iterations = 20
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call the model with the current messages list, system prompt, and tools
            resp = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                ),
            )
            
            # Add the response candidate(s) content to our messages
            if resp.candidates:
                for candidate in resp.candidates:
                    if candidate.content:
                        messages.append(candidate.content)
            
            # Handle function calls in the response first
            function_calls_made = False
            if resp.candidates and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        function_call_part = part.function_call
                        function_calls_made = True
                        
                        # Use the new call_function to handle the function call
                        function_call_result = call_function(function_call_part, verbose)
                        
                        # Validate the response structure
                        if not hasattr(function_call_result, 'parts') or not function_call_result.parts:
                            raise Exception("Invalid function call result: missing parts")
                        
                        if not hasattr(function_call_result.parts[0], 'function_response'):
                            raise Exception("Invalid function call result: missing function_response")
                            
                        if not hasattr(function_call_result.parts[0].function_response, 'response'):
                            raise Exception("Invalid function call result: missing response")
                        
                        # Print the result if in verbose mode
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                        
                        # Add function response to messages as a 'user' message
                        messages.append(function_call_result)
                        
                    elif hasattr(part, 'text') and part.text:
                        # If there's text content, print it but don't break yet
                        # The model might still be thinking
                        if verbose:
                            print(f"Model text: {part.text.strip()}")
            
            # Check if we got a final text response and no function calls (conversation is done)
            if resp.text and not function_calls_made:
                print("Final response:")
                print(resp.text.strip())
                break
            
            # If no function calls were made and no final text, something went wrong
            if not function_calls_made and not resp.text:
                print("No function calls made and no final response. Ending conversation.")
                break
                
        if iteration >= max_iterations:
            print(f"Reached maximum iterations ({max_iterations}). Ending conversation.")
        
        # Consolidated usage stats printing
        usage = getattr(resp, "usage_metadata", None)
        print_usage_stats(usage, verbose)
            
    except Exception as e:
        print(f"Error generating response: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
