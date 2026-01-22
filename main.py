import os
import azure.cognitiveservices.speech as speechsdk
from google import genai
from google.genai import types
from dotenv import load_dotenv
from default_prompt import system_prompt
from rich.console import Console
import argparse

# --- Argument Parsing ---    
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# --- Configuration and Initialization ---
console = Console()

# --- Global Variables ---
chat_history = []
history_tokens = []
HISTORY_TOKENS_LIMIT = 3000  # Adjust based on model limits

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")
client = genai.Client(api_key=GEMINI_API_KEY)


# Configure Azure Speech Services
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
if not all([AZURE_SPEECH_KEY, AZURE_SPEECH_REGION]):
    raise ValueError("Azure Speech credentials not found in .env file.")

speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
# Set the voice for the assistant. Find more voices at https://aka.ms/speech/voices/neural
#speech_config.speech_synthesis_voice_name = "en-US-DavisNeural" / en-US-CoraMultilingualNeural ro-RO-AlinaNeural zh-CN-YunfengNeural zh-CN-YunhaoNeural
speech_config.speech_synthesis_voice_name = "zh-CN-YunzeNeural" #zh-CN-YunzeNeural #ro-RO-AlinaNeural
speech_config.speech_recognition_language = "en-US" # You can change this if needed

# --- Core Functions ---

def speech_to_text():
    """Listens for a single utterance from the microphone and returns the recognized text."""
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    console.print("Listening...", style="cyan")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        console.print("No speech could be recognized.", style="yellow")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        console.print(f"Speech Recognition canceled: {cancellation_details.reason}", style="bold red")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            console.print(f"Error details: {cancellation_details.error_details}", style="bold red")
        return None
    return None

def get_llm_response(prompt):
    """Sends a prompt to the Gemini model and returns the text response."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=chat_history,
            config=types.GenerateContentConfig(system_instruction=system_prompt,temperature=0.5,top_p=0.7),
            )
        if response.text:
            chat_history.append(
                types.Content(
                    role=response.candidates[0].content.role,
                    parts=[types.Part(text=response.text)]
                )
            )
            manage_history(response.usage_metadata.prompt_token_count, response.usage_metadata.candidates_token_count)

        return response.text
    except Exception as e:
        console.print(f"An error occurred with the LLM: {e}", style="bold red")
        return "Well shucks, I seem to have misplaced my train of thought."

def text_to_speech(text):
    """Synthesizes text into speech and plays it through the default speaker."""
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        console.print(f"Speech synthesis canceled: {cancellation_details.reason}", style="bold red")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            console.print(f"Error details: {cancellation_details.error_details}", style="bold red")


def manage_history(prompt_tokens, response_tokens):
    global history_tokens
    history_tokens.append(prompt_tokens + response_tokens)
    history_sum = sum(history_tokens)
                
    if args.verbose:
        console.print(f"History so far: {chat_history}\n")
        console.print(f"Prompt tokens so far: {history_sum}\n", style="bold cyan")

    if history_sum > HISTORY_TOKENS_LIMIT:
        if args.verbose:
            console.print("Token limit exceeded, trimming history...", style="bold yellow")
        # Remove the oldest user and AI messages
        while history_sum > HISTORY_TOKENS_LIMIT and len(chat_history) > 2:
            removed_user = chat_history.pop(1)  # Remove oldest user message
            removed_ai = chat_history.pop(1)    # Remove corresponding AI message
            removed_tokens = history_tokens.pop(0)
            history_sum -= removed_tokens
        if args.verbose:
            console.print(f"Trimmed history. New token count: {history_sum}\n", style="bold green")
    

# --- Main Conversational Loop ---

def main():
    """The main function to run the voice assistant loop."""
    console.print("AI Assistant is running. Say 'goodbye' or press Ctrl+C to exit.", style="bold magenta")


    try:

        while True:
            user_text = speech_to_text()

            if user_text:
                console.print(f"You said: {user_text}", style="blue")
                chat_history.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=user_text)]
                    )
                )
            

                # Check for exit condition via voice
                if "goodbye" in user_text.lower():
                    farewell_message = "Alright then, catch you later, partner."
                    console.print(f"AI: {farewell_message}", style="yellow")
                    text_to_speech(farewell_message)
                    break

                # Get response from the language model
                ai_response = get_llm_response(user_text)

                if ai_response:
                    console.print(f"AI said: {ai_response}", style="bold white on dark_green")

                    # Speak the AI's response
                    text_to_speech(ai_response)

                    

    except KeyboardInterrupt:
        console.print("\nCtrl+C detected. Shutting down, partner.", style="bold yellow")
    except Exception as e:
        console.print(f"An unexpected error occurred: {e}", style="bold red")

if __name__ == "__main__":
    main()
