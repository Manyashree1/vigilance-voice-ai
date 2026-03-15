import librosa
import numpy as np

def analyze_stress(audio_path: str) -> dict:
    """
    Extracts acoustic features from audio to detect stress levels.
    Analyzes pitch, energy, and MFCCs and returns stress level.
    """
    try:
        y, sr = librosa.load(audio_path, sr=16000)
        
        # 1. Pitch analysis (Fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_mean = np.mean(pitches[magnitudes > np.median(magnitudes)]) if len(pitches) > 0 else 0
        
        # 2. Energy analysis (RMS)
        rms = librosa.feature.rms(y=y)
        energy_mean = np.mean(rms)
        
        # 3. Speech rate proxy via zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = np.mean(zcr)

        # Basic heuristic mapping to stress levels
        # Elevated pitch, high energy, and fast speech rates correlate with stress.
        stress_score = (pitch_mean / 200.0) + (energy_mean / 0.1) + (zcr_mean / 0.1)
        
        level = "low"
        if stress_score > 3.0:
            level = "high"
        elif stress_score > 1.5:
            level = "medium"

        return {
            "stress_level": level,
            "metrics": {
                "pitch": round(float(pitch_mean), 2),
                "energy": round(float(energy_mean), 4),
                "zcr": round(float(zcr_mean), 4)
            }
        }
    except Exception as e:
        print(f"Error in stress analysis: {e}")
        return {
            "stress_level": "unknown"
        }
