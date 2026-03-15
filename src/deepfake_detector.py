import torch
import librosa
import numpy as np
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

# HuggingFace model
MODEL = "garystafford/wav2vec2-deepfake-voice-detector"

print("Loading deepfake detection model...")

# Load model once at server startup
feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL)
model = AutoModelForAudioClassification.from_pretrained(MODEL)

model.eval()

print("Model loaded successfully")


def detect_deepfake(audio_path: str):
    """
    Detect if voice is AI or Human

    Returns:
        label: "Fake" or "Real"
        confidence: percentage
    """

    try:

        print("Loading audio:", audio_path)

        # Load audio (supports wav, mp3, m4a)
        wav, sr = librosa.load(audio_path, sr=16000, mono=True)

        if wav is None or len(wav) == 0:
            raise ValueError("Audio file empty")

        print("Audio length:", len(wav) / 16000, "seconds")

        # Normalize audio safely
        max_val = np.max(np.abs(wav))
        if max_val > 0:
            wav = wav / max_val

        # Minimum 3 seconds required
        if len(wav) < 16000 * 3:
            print("Audio too short for detection")
            return "Audio Too Short", 0

        # Extract features
        inputs = feature_extractor(
            wav,
            sampling_rate=16000,
            return_tensors="pt",
            padding=True
        )

        # Run model
        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits

        probs = torch.softmax(logits, dim=-1).squeeze()

        print("Model probabilities:", probs)

        pred = torch.argmax(probs).item()

        confidence = round(float(probs[pred]) * 100, 2)

        label = "Fake" if pred == 1 else "Real"

        print("Prediction:", label)
        print("Confidence:", confidence)

        return label, confidence

    except Exception as e:

        print("DETECTION ERROR:", e)

        return "Error", 0