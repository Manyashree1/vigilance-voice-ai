from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

encoder = VoiceEncoder()

def analyze_voice_authenticity(audio_path):
    try:
        wav = preprocess_wav(audio_path)
        embedding = encoder.embed_utterance(wav)

        # compute statistics
        mean_val = np.mean(embedding)
        std_val = np.std(embedding)

        score = abs(mean_val) + std_val
        confidence = round(score * 100, 2)

        print("Embedding mean:", mean_val)
        print("Embedding std:", std_val)

        # classification rule
        if std_val < 0.08:
            print("⚠️ AI Voice Detected")
            return True, confidence
        else:
            print("✅ Human Voice Verified")
            return False, confidence

    except Exception as e:
        print("Error:", e)
        return False, 0