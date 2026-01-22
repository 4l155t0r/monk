# Project Plan: Your First Voice AI Assistant !!!(NOT UPDATED)!!!

**Project Goal:** To build a simple, voice-controlled AI assistant that listens to your microphone, gets a response from Gemini, and speaks the answer back to you, all running in a continuous loop.

**Learning Focus:** This plan prioritizes clarity and learning. Each step is a self-contained building block. We will build each component separately and test it before combining them into the final application.

---

### Phase 1: Foundation & Prerequisities (The Setup)

This is the most critical phase. We need to ensure your environment is set up correctly and that your hardware (microphone) works inside WSL.

**Step 1: Setting Up Your Python Environment**

*   **Why:** We need a clean, isolated space for this project's specific libraries so they don't conflict with other Python projects on your system. This is what a "virtual environment" is for.
*   **Action:**
    1.  Open your Ubuntu terminal.
    2.  Create a project folder: `mkdir voice-assistant && cd voice-assistant`
    3.  Create a virtual environment: `python3 -m venv venv`
    4.  Activate it: `source venv/bin/activate` (You'll need to do this every time you work on the project).
    5.  Install initial libraries: `pip install sounddevice numpy google-generativeai azure-cognitiveservices-speech TTS`

**Step 2: The WSL Microphone Check (Crucial!)**

*   **Why:** Windows Subsystem for Linux (WSL) doesn't always have straightforward access to hardware like microphones. We MUST verify this works before anything else. We will do this by recording a short audio clip.
*   **Action:**
    1.  Create a Python file named `check_mic.py`.
    2.  Inside it, write a simple script using the `sounddevice` library to record 5 seconds of audio from your default microphone and save it as a `.wav` file.
    3.  Run the script: `python check_mic.py`.
    4.  Check if `output.wav` was created and play it to confirm your voice was recorded. If this fails, we will need to troubleshoot WSL audio configuration before proceeding.

**Step 3: Getting Your API Keys**

*   **Why:** The STT (Azure) and LLM (Gemini) services are protected. API keys are like passwords that let your script use them. We will use environment variables to keep them safe and out of your source code.
*   **Action:**
    1.  **Gemini API Key:** Get one from Google AI Studio.
    2.  **Azure Speech Service API Key:** Create a "Speech" resource in the Azure portal. You will get an API key and a "region" (e.g., `eastus`).
    3.  **Store them:** In your terminal (while the venv is active), run:
        ```bash
        export GOOGLE_API_KEY="your_gemini_key_here"
        export AZURE_SPEECH_KEY="your_azure_key_here"
        export AZURE_SPEECH_REGION="your_azure_region_here"
        ```

---

### Phase 2: Building the Core Components (In Isolation)

Now we'll write separate, small scripts to test each major part of the assistant.

**Step 4: Speech-to-Text (STT) - Hearing**

*   **Goal:** Create a script that listens to the microphone and prints what you said as text.
*   **Action:**
    1.  Create a file `test_stt.py`.
    2.  Using the `azure-cognitiveservices-speech` library, write a script that connects to the Azure service using your key/region.
    3.  The script should listen to the default microphone and print the transcribed text to the console when you stop speaking.

**Step 5: AI Response (LLM) - Thinking**

*   **Goal:** Create a script that sends a pre-written question to Gemini and prints the answer.
*   **Action:**
    1.  Create `test_llm.py`.
    2.  Using the `google-generativeai` library, write a script that authenticates with your API key.
    3.  Send a hard-coded prompt (e.g., "What is the biggest star in the universe?") to the `gemini-1.5-flash-latest` model.
    4.  Print the text response you get back.

**Step 6: Text-to-Speech (TTS) - Speaking**

*   **Goal:** Create a script that takes pre-written text and speaks it out loud. We are using `xtts_v2`, a high-quality local model.
*   **Action:**
    1.  Create `test_tts.py`.
    2.  Using the `TTS` library, write a script that loads the `tts_models/en/ljspeech/vits` model (a good starting point). The first time you run this, it will download the model, which may take some time.
    3.  Give it a hard-coded sentence (e.g., "Hello, this is a test.") and have it speak the audio through your speakers.

---

### Phase 3: Integration (The Grand Loop)

Now we assemble the pieces.

**Step 7: Tying It All Together**

*   **Goal:** Combine the logic from steps 4, 5, and 6 into a single script that runs in a loop.
*   **Action:**
    1.  Create a main file, `main.py`.
    2.  Structure the code inside a `while True:` loop.
    3.  **Inside the loop:**
        a.  Call your STT logic to listen and get the transcribed text from the user.
        b.  Print the user's text to the screen so you can see what the AI "heard".
        c.  Send that text to Gemini to get a response.
        d.  Print the AI's text response.
        e.  Call your TTS logic to speak the AI's response out loud.

---

### Phase 4: Making it Usable (Future Enhancements)

Once the core loop works, you can make it more sophisticated.

**Step 8: Adding a Graceful Exit**

*   **Why:** A `while True:` loop runs forever. You need a way to stop it cleanly.
*   **Action:** Add a simple check. If the text transcribed from the user is "goodbye" or "exit", use the `break` command to exit the loop.

**Step 9 (Advanced): Conversation History**

*   **Why:** Right now, the AI has no memory of past turns. To have a real conversation, it needs context.
*   **Action:** Create a list to store the conversation. Before you call the Gemini API, add the user's new message to the list. Send the whole list to the API. This lets the model "remember" what you've talked about.

**Step 10 (Advanced): Wake Word Detection**

*   **Why:** The assistant is always listening. A "wake word" (like "Hey Google") makes it wait for a command before it starts processing speech.
*   **Action:** This is more complex. You would use a library like `pvporcupine` to listen for a specific phrase before "waking up" and starting the main STT->LLM->TTS loop.

---

This plan will guide you from the ground up. I am ready to help you with the first step whenever you are. Let's start with **Step 1 and 2: Environment Setup and the critical Mic Check.**
