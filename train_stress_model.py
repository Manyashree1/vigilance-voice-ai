import librosa
import numpy as np
import os
import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_stress_features(audio_path):
    """Extracts stress-related features (pitch, energy, zero crossing rate)."""
    try:
        y, sr = librosa.load(audio_path, sr=16000)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_mean = np.mean(pitches[magnitudes > np.median(magnitudes)]) if len(pitches) > 0 else 0
        rms_mean = np.mean(librosa.feature.rms(y=y))
        zcr_mean = np.mean(librosa.feature.zero_crossing_rate(y))
        return np.array([pitch_mean, rms_mean, zcr_mean])
    except Exception as e:
        logger.error(f"Error processing {audio_path}: {e}")
        return np.zeros(3)

def generate_dummy_data(num_samples=150):
    """Generates dummy features since we don't have a stress audio dataset available."""
    logger.info("Generating dummy acoustic features for stress detection training...")
    X = np.random.rand(num_samples, 3) * [300, 0.5, 0.5] # pitch, energy, zcr ranges
    # Classes: 0: Low, 1: Medium, 2: High
    y = np.random.randint(0, 3, num_samples)
    return X, y

def train():
    logger.info("Starting stress model training...")
    
    # In a real scenario, you would extract features from a directory of audio files
    X, y = generate_dummy_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = SVC(kernel='rbf', probability=True, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    logger.info(f"Test Accuracy: {acc:.4f}")
    
    model_path = "scam_detector/models/stress_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    logger.info(f"Model saved to {model_path}")

if __name__ == "__main__":
    train()
