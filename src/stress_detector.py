import torch
import librosa
from transformers import Wav2Vec2FeatureExtractor, AutoModelForAudioClassification

MODEL_NAME = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)

labels = model.config.id2label


def detect_stress(audio_path):

    speech, sr = librosa.load(audio_path, sr=16000)

    inputs = feature_extractor(
        speech,
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=1)[0]

    predicted_id = torch.argmax(probs).item()
    emotion = labels[predicted_id]

    confidence = probs[predicted_id].item()

    # Stress mapping
    if emotion in ["angry", "fear", "disgust"]:
        stress_score = confidence
    elif emotion in ["sad"]:
        stress_score = confidence * 0.6
    else:
        stress_score = confidence * 0.3

    # Stress level thresholds
    if stress_score > 0.7:
        level = "HIGH"
    elif stress_score > 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "emotion_detected": emotion,
        "stress_level": level,
        "stress_score": round(stress_score, 2)
    }