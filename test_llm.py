import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from default_prompt import system_prompt
import argparse
from rich import print

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("[red]Error: GEMINI_API_KEY not found in .env file.")
    print("Please ensure GEMINI_API_KEY is set.")
    exit()

def get_gemini_response():
    """Sends a prompt to the Gemini 1.5 Flash model and returns the text response."""
    print("Initializing Gemini API...")
    client = genai.Client(api_key=GEMINI_API_KEY)    
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    # Now we can access `args.user_prompt` and `args.verbose`

    # Prepare the user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    try:
        # Generate content using the Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt,),
            )

        if not response.usage_metadata:
            raise RuntimeError("No usage metadata found in response")

        if args.verbose:        
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") 
        
        print(f"[green]{response.text}")
    except Exception as e:
        print(f"[red]An error occurred while generating content: {e}")
    return 0

if __name__ == "__main__":
    response_text = get_gemini_response()
    print(f"Program exited with code: {response_text}")
