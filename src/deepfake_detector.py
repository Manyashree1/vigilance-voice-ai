import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

MODEL = "garystafford/wav2vec2-deepfake-voice-detector"

# Load model
feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL)
model = AutoModelForAudioClassification.from_pretrained(MODEL)

def detect_deepfake(audio_path: str) -> tuple[str, float]:
    """
    Returns:
        label: "Fake" or "Real"
        confidence: probability in %
    """
    wav, sr = librosa.load(audio_path, sr=16000)
    if len(wav.shape) > 1:
        wav = wav.mean(axis=1)  # mono
    inputs = feature_extractor(wav, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1).squeeze()
    pred = torch.argmax(probs).item()
    confidence = float(probs[pred]) * 100
    label = "Fake" if pred == 1 else "Real"
    return label, confidence

