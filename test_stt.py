import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Azure credentials from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
AZURE_SPEECH_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT")

if not all([AZURE_SPEECH_KEY, AZURE_SPEECH_REGION, AZURE_SPEECH_ENDPOINT]):
    print("Error: Azure Speech credentials (key, region, or endpoint) not found in .env file.")
    print("Please ensure AZURE_SPEECH_KEY, AZURE_SPEECH_REGION, and AZURE_SPEECH_ENDPOINT are set.")
    exit()

def speech_to_text_from_mic():
    """Performs speech-to-text from the default microphone using Azure Speech SDK."""
    print("Initializing Azure Speech Recognizer...")

    # Create a SpeechConfig object using your Azure credentials
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    speech_config.speech_recognition_language = "en-EN" # You can change this if needed

    # If using a custom endpoint, specify it
    # speech_config.endpoint_id = AZURE_SPEECH_ENDPOINT # Only if you have a custom endpoint ID, not the full URL

    # Create an AudioConfig object for microphone input
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a SpeechRecognizer object
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone. Say 'stop' or pause to end recognition.")
    print("Listening...")

    try:
        # Start continuous recognition. The events will handle the results.
        # This is for scenarios where you want to process longer audio or multiple phrases.
        # For simple 'listen once then stop', use recognize_once_async().

        # For this test, we'll use recognize_once_async for simplicity, which listens for a single utterance.
        # The service determines the end of an utterance by detecting silence.
        result = speech_recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"Recognized: {result.text}")
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region?")

    except Exception as e:
        print(f"An error occurred during speech recognition: {e}")
        print("Please ensure Azure Speech service is accessible and your microphone is working.")

if __name__ == "__main__":
    speech_to_text_from_mic()
