from asyncio import subprocess
import webbrowser
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import re
import os
import queue
import time
from selenium import webdriver
import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# =========================
# SETTINGS
# =========================


MICROPHONE = 4

SAMPLE_RATE = 16000
CHUNK_SECONDS = 3

MODEL_SIZE = "base.en"

WORDS = {
    "fuck",
    "shit",
    "crap",
    "crud",
    "bitch",
    "whore",
    "slut",
    "faggot",
    "fag",
    "kill",
    "retard",
    "god",
    "gosh",
    "damn",
    "dang",
    "darn",
    "dick",
    "ass",
    "hell",
    "heck",
    "frick",
    "wanker",
    "twink",
    "chud",
    "jesus",
    "hate",
    "flip",
    "stupid",
    "midget",
    "fatass",
    "shut",
    "dumb",
    "dumbest",
    "idiot",
    "shittings",
    "tranny"
}

# =========================
# LOAD WHISPER
# =========================

print("Loading Whisper...")

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

print("Whisper loaded.")
print("Listening...")

# =========================
# AUDIO QUEUE
# =========================

audio_queue = queue.Queue()


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)

    audio_queue.put(indata.copy())


# =========================
# START MICROPHONE
# =========================

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=MICROPHONE,
    blocksize=int(SAMPLE_RATE * CHUNK_SECONDS),
    callback=audio_callback
):

    while True:

        try:
            audio = audio_queue.get()

            # Convert stereo/2D array to mono
            audio = audio.flatten()

            # Ignore extremely quiet chunks
            volume = np.sqrt(np.mean(audio ** 2))

            if volume < 0.005:
                continue

            # =========================
            # TRANSCRIBE
            # =========================

            segments, info = model.transcribe(
                audio,
                language="en",
                beam_size=5,
                vad_filter=True,
                vad_parameters={
                    "min_silence_duration_ms": 300
                }
            )

            text = " ".join(
                segment.text for segment in segments
            ).lower().strip()

            if not text:
                continue

            print("Heard:", text)

            # =========================
            # EXIT
            # =========================

            if re.search(r"\bexit\b", text):
                print("Exiting...")
                break

            # =========================
            # WORD DETECTION
            # =========================

            spoken_words = set(
                re.findall(r"\b[a-zA-Z]+\b", text)
            )

            detected = spoken_words.intersection(WORDS)

            if detected:

                print()
                print("==============================")
                print("       WORD DETECTED")
                print("==============================")
                print("Detected:", detected)
                print("==============================")
                print()
                url = "https://www.youtube.com/watch?v=adtuUeRb4Ts&autoplay=1"

                options = Options()
                options.add_argument("--autoplay-policy=no-user-gesture-required")

                driver = webdriver.Chrome(options=options)

                # Open the first tab
                driver.get(url)
                time.sleep(3)

                # Open the remaining tabs
                for i in range(9):
                    driver.execute_script(f"window.open('{url}', '_blank');")
                    time.sleep(3)

                print("Opened all videos.")
        except KeyboardInterrupt:
            print("\nStopped.")
            break

        except Exception as e:
            print("Error:", e)
