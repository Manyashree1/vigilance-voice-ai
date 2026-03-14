import librosa
import numpy as np

def extract_features(audio_path):

    audio, sr = librosa.load(audio_path, sr=None)

    # Pitch estimate
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    pitch = np.mean(pitches[pitches > 0])

    # Energy (loudness)
    energy = np.mean(librosa.feature.rms(y=audio))

    # Speech tempo
    tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)

    return pitch, energy, tempo
def detect_stress(audio_path):

    pitch, energy, tempo = extract_features(audio_path)

    stress_score = 0

    if pitch > 180:
        stress_score += 0.3

    if energy > 0.02:
        stress_score += 0.3

    if tempo > 120:
        stress_score += 0.4

    if stress_score < 0.3:
        level = "LOW"
    elif stress_score < 0.6:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "pitch": float(pitch),
        "energy": float(energy),
        "tempo": float(tempo),
        "stress_score": stress_score,
        "stress_level": level
    }