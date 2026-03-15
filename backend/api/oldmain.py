import sys
import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Import detectors
from src.deepfake_detector import detect_deepfake
from src.speech_to_text import transcribe_audio
from src.scam_phrase_detector import detect_scam_phrases
from src.scam_intent_detector import detect_scam_intent
from src.stress_detector import detect_stress

app = FastAPI(title="Vigilance Voice AI")

# Enable CORS for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "data"
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Vigilance Voice AI is running",
        "status": "Server Active"
    }

@app.post("/verify-call")
async def verify_call(file: UploadFile = File(...)):

    temp_path = UPLOAD_DIR / f"temp_{file.filename}"

    try:

        # Save uploaded audio file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1️⃣ Deepfake detection (returns 2 values)
        label, confidence = detect_deepfake(str(temp_path))

        # 2️⃣ Speech to text
        text = transcribe_audio(str(temp_path))

        # 3️⃣ Scam phrase detection
        phrases, phrase_risk = detect_scam_phrases(text)

        # 4️⃣ Scam intent detection
        intent_result = detect_scam_intent(text)

        # 5️⃣ Stress detection (returns dictionary)
        stress_result = detect_stress(str(temp_path))
        stress_level = stress_result["stress_level"]
        stress_score = stress_result["stress_score"]

        is_fake = label.lower() == "fake"

        # Final risk logic
        final_risk = phrase_risk

        if intent_result["risk_level"] == "HIGH":
            final_risk = "HIGH"

        if stress_level == "HIGH":
            final_risk = "HIGH"

        if is_fake:
            final_risk = "HIGH"

        response = {
            "filename": file.filename,

            "deepfake_result": label,
            "deepfake_confidence": float(round(confidence, 2)),

            "transcript": text,

            "detected_phrases": phrases,
            "phrase_risk": phrase_risk,

            "stress_level": stress_level,
            "stress_score": float(stress_score),

            "scam_intent": intent_result["intent"],
            "intent_confidence": float(intent_result["confidence"]),

            "final_risk": final_risk,

            "analysis": "AI Voice Detected" if is_fake else "Human Voice Verified"
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path.exists():
            temp_path.unlink()