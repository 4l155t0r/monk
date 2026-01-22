import sounddevice as sd
import soundfile as sf
import numpy as np

# Audio recording parameters
samplerate = 44100  # samples per second (standard audio CD quality)
duration = 5      # seconds
filename = 'output.wav'

print(f"Recording {duration} seconds of audio. Please speak now...")

try:
    # Record audio from the default input device
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished

    print(f"Recording finished. Saving to {filename}...")

    # Normalize to float32 for soundfile, if not already
    recording_float = recording.astype(np.float32) / np.iinfo(recording.dtype).max

    # Save the recorded audio to a WAV file
    sf.write(filename, recording_float, samplerate)

    print(f"Audio saved successfully to {filename}.")
    print("You can now play this file to check your microphone: `aplay output.wav` (if aplay is installed) or open it with a media player.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure your microphone is connected and recognized by WSL/Ubuntu.")
    print("You might need to install `portaudio19-dev` and `python3-pyaudio` if `sounddevice` has issues:")
    print("sudo apt-get update && sudo apt-get install portaudio19-dev python3-pyaudio")
    print("Or, try listing devices: `python -c 'import sounddevice as sd; print(sd.query_devices())'`")
