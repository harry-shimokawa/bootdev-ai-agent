"""
Main module for the bootdev-ai-agent application.

This module provides the core functionality for AI-powered agent operations
using Google's Generative AI services.
"""

from __future__ import annotations

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

MAX_ITERATIONS = 20
USAGE_MESSAGE = 'Usage: python main.py "Your prompt here" [--verbose]'
WORKING_DIRECTORY = "./calculator"


def print_usage_stats(usage) -> None:
    """Print usage stats from the API response."""
    if not usage:
        raise RuntimeError(
            "No usage metadata available. This likely indicates a failed API request."
        )

    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")


def build_tool_response(function_name: str, payload: dict[str, str]) -> types.Content:
    """Build a tool response for the model."""
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response=payload,
            )
        ],
    )


def call_function(function_call_part, verbose: bool = False) -> types.Content:
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

    if function_name not in available_functions:
        return build_tool_response(
            function_name,
            {"error": f"Unknown function: {function_name}"},
        )

    func = available_functions[function_name]
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIRECTORY

    try:
        function_result = func(**args)
        return build_tool_response(
            function_name,
            {"result": function_result},
        )
    except (TypeError, ValueError, OSError, IOError, KeyError) as err:
        return build_tool_response(
            function_name,
            {"error": f"Error executing {function_name}: {type(err).__name__}"},
        )


def parse_cli_args(argv: list[str]) -> tuple[str, bool]:
    """Parse CLI arguments and return the prompt and verbose flag."""
    if len(argv) <= 1:
        raise ValueError("No prompt provided.")

    verbose = "--verbose" in argv
    args_without_verbose = [arg for arg in argv[1:] if arg != "--verbose"]
    if not args_without_verbose:
        raise ValueError("No prompt provided.")

    return " ".join(args_without_verbose), verbose


def print_usage_error() -> None:
    """Print the command line usage error and usage message."""
    print(
        "Error: No prompt provided. Please provide a prompt as a command line argument.",
        file=sys.stderr,
    )
    print(USAGE_MESSAGE, file=sys.stderr)


def get_api_key() -> str:
    """Return the Gemini API key or raise a ValueError if missing."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY.")
    return api_key


def build_messages(user_prompt: str) -> list[types.Content]:
    """Build the initial messages list."""
    return [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


def build_tools() -> types.Tool:
    """Build the tool declaration for function calling."""
    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )


def append_candidate_messages(resp, messages: list[types.Content]) -> None:
    """Append candidate content to the conversation history."""
    for candidate in resp.candidates or []:
        if candidate.content:
            messages.append(candidate.content)


def get_response_parts(resp) -> list[types.Part]:
    """Return parts from the first candidate response if present."""
    if not resp.candidates:
        return []

    content = resp.candidates[0].content
    if not content or not content.parts:
        return []

    return list(content.parts)


def validate_function_response(function_call_result: types.Content) -> None:
    """Validate the structure of a function call response."""
    if not getattr(function_call_result, "parts", None):
        raise RuntimeError("Invalid function call result: missing parts")

    first_part = function_call_result.parts[0]
    if not getattr(first_part, "function_response", None):
        raise RuntimeError("Invalid function call result: missing function_response")

    if not getattr(first_part.function_response, "response", None):
        raise RuntimeError("Invalid function call result: missing response")


def log_model_text(part: types.Part, verbose: bool) -> None:
    """Log model text parts when verbose is enabled."""
    text = getattr(part, "text", None)
    if verbose and text:
        print(f"Model text: {text.strip()}")


def handle_response_parts(
    parts: list[types.Part],
    messages: list[types.Content],
    verbose: bool,
) -> bool:
    """Process response parts, handling function calls and text."""
    function_calls_made = False
    for part in parts:
        function_call_part = getattr(part, "function_call", None)
        if function_call_part:
            function_calls_made = True
            function_call_result = call_function(function_call_part, verbose)
            validate_function_response(function_call_result)

            if verbose:
                response = function_call_result.parts[0].function_response.response
                print(f"-> {response}")

            messages.append(function_call_result)
        else:
            log_model_text(part, verbose)

    return function_calls_made


def run_conversation(client, messages: list[types.Content], verbose: bool) -> None:
    """Run the agent conversation loop until completion."""
    system_prompt = get_system_prompt()
    available_functions = build_tools()
    resp = None

    for _ in range(MAX_ITERATIONS):
        resp = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        append_candidate_messages(resp, messages)
        parts = get_response_parts(resp)
        function_calls_made = handle_response_parts(parts, messages, verbose)

        if resp.text and not function_calls_made:
            usage = getattr(resp, "usage_metadata", None)
            print_usage_stats(usage)
            print("Response:")
            print(resp.text.strip())
            break

        if not function_calls_made and not resp.text:
            print("No function calls made and no final response. Ending conversation.")
            break
    else:
        print(f"Reached maximum iterations ({MAX_ITERATIONS}). Ending conversation.")


def main() -> None:
    """Entry point for the CLI."""
    load_dotenv()

    try:
        user_prompt, verbose = parse_cli_args(sys.argv)
    except ValueError:
        print_usage_error()
        sys.exit(1)

    try:
        api_key = get_api_key()
    except ValueError:
        print(
            "Error: Missing GEMINI_API_KEY. Add it to your environment or to a .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    if verbose:
        print(f"User prompt: {user_prompt}")

    client = genai.Client(api_key=api_key)
    messages = build_messages(user_prompt)

    try:
        run_conversation(client, messages, verbose)
    except (ValueError, TypeError) as err:
        print(f"Input error: {type(err).__name__}", file=sys.stderr)
        sys.exit(1)
    except (OSError, IOError) as err:
        print(f"File system error: {type(err).__name__}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as err:
        print(str(err), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
