import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    # Connect to client -- in this case, Google AI
    api_key = os.getenv("GEMINI_API_KEY")   
    client = genai.Client(api_key=api_key)

    try:
        question = sys.argv[1]
    except IndexError:
        print("Please provide a question as a command-line argument.")
        sys.exit(1)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=question
        )

    print(f"Question: {question}")
    print(f"Response: {response.text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
