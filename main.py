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

All paths you provide should be relative to the working directory. To list files in the current working directory, simply use "." as the directory parameter. If a location is not specified, assume the code in question will be in the current working directory. Look through all relevant files in the working directory to find it. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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

    for i in range(MAX_ITERATIONS):
        # loop up to MAX_ITERATIONS times calling generate_content. It will return None until it finally has no function calls and returns response.text
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                break
        except Exception as e:
            print(f"Error during content generation: {e}")


def generate_content(client, messages, verbose: bool = False):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

    if verbose and usage.metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # After calling client's generate_content method, check the .candidates property of the response.
    # It's a list of response variations (usually just one). It contains the equivalent of "I want to call get_files_info...", 
    # so we need to add it to our conversation. Iterate over each candidate and add its .content to your messages list.
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return f"Response: {response.text}"

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    messages.append(types.Content(role="user", parts=function_call_result.parts))

if __name__ == "__main__":
    main()
