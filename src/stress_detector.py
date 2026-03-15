import torch
import librosa
import numpy as np
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification

# Load pretrained model
MODEL_NAME = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)

labels = model.config.id2label


def detect_stress(audio_path):

    # Load audio
    speech, sr = librosa.load(audio_path, sr=16000)

    # Extract features
    inputs = feature_extractor(
        speech,
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )

    # Model prediction
    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_id = torch.argmax(logits).item()
    emotion = labels[predicted_id]

    confidence = torch.softmax(logits, dim=1)[0][predicted_id].item()

    # Map emotions to stress
    if emotion in ["angry", "fear", "disgust"]:
        level = "HIGH"
    elif emotion in ["sad"]:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "emotion_detected": emotion,
        "stress_level": level,
        "stress_score": round(confidence, 2)
    }