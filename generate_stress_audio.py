import numpy as np
import soundfile as sf

sr = 22050
duration = 3

t = np.linspace(0, duration, sr*duration)

audio = 0.5 * np.sin(2 * np.pi * 220 * t)

sf.write("test_audio.wav", audio, sr)

print("Audio file created: test_audio.wav")