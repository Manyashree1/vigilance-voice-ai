import sounddevice as sd
import numpy as np
import soundfile as sf
from deepfake_detector import detect_deepfake

samplerate = 16000
duration = 3   # seconds

print("Listening...")

while True:

    audio = sd.rec(int(duration * samplerate),
                   samplerate=samplerate,
                   channels=1)

    sd.wait()

    audio_file = "temp.wav"
    sf.write(audio_file, audio, samplerate)

    score = detect_deepfake(audio_file)

    print("Deepfake score:", score)