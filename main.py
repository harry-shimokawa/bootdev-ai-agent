import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


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
        # Call the model with the messages list
        resp = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
        )

        # Print response text to stdout
        print("\n--- AI Response ---")
        if resp.text:
            print(resp.text.strip())
        else:
            print("No response text received")
        
        # Consolidated usage stats printing
        usage = getattr(resp, "usage_metadata", None)
        print_usage_stats(usage, verbose)
            
    except Exception as e:
        print(f"Error generating response: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
