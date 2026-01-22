import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Azure credentials from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

if not all([AZURE_SPEECH_KEY, AZURE_SPEECH_REGION]):
    print("Error: Azure Speech credentials (key or region) not found in .env file.")
    print("Please ensure AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are set.")
    exit()

def text_to_speech(text):
    """Performs text-to-speech using Azure Speech SDK and plays it through the default speaker."""
    print(f"Synthesizing speech for: '{text}'")

    # Create a SpeechConfig object using your Azure credentials
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)

    # To select a voice, see https://aka.ms/speech/voices/neural for a full list.
    # 'en-US-DavisNeural' has a mature, male voice.
    speech_config.speech_synthesis_voice_name = "en-US-AdamMultilingualNeural"

    # Create a SpeechSynthesizer object. When no AudioConfig is provided,
    # it defaults to using the system's default speaker.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    try:
        # Synthesize the speech and play it
        result = speech_synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesis completed successfully.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region correctly?")

    except Exception as e:
        print(f"An error occurred during speech synthesis: {e}")
        print("Please ensure Azure Speech service is accessible and your speakers are working.")

if __name__ == "__main__":
    test_sentence = "Greetings, humble student. Prepare to be enlightened by the wisdom of the Shaolin." # A Shaolin-like greeting
    text_to_speech(test_sentence)
