import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function, available_functions


MODEL_NAME = "gemini-2.0-flash-001"
MAX_ITERATIONS = 20

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    load_dotenv()
    # Connect to client -- in this case, Google AI
    api_key = os.getenv("GEMINI_API_KEY")   
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv if not arg.startswith("--")] 

    try:
        user_prompt = " ".join(args[1:]) # main.py is args[0]
    except IndexError:
        print("Please provide a prompt to the AI Agent as a command-line argument.")
        print('Example: python main.py "Please fix the bug in the calculator"')
        sys.exit(1)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose: bool = False):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

    if response.function_calls is not None:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
        if hasattr(function_call_result.parts[0].function_response, 'response') and verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(f"Response: {response.text}")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
