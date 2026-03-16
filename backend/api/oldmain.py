import sys
import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Import AI modules
from src.deepfake_detector import detect_deepfake
from src.speech_to_text import transcribe_audio
from src.scam_phrase_detector import detect_scam_phrases
from src.scam_intent_detector import detect_scam_intent
from src.stress_detector import detect_stress

app = FastAPI(title="Vigilance Voice AI")

# Enable CORS
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

        # Save uploaded audio
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1️⃣ Deepfake Detection
        label, confidence = detect_deepfake(str(temp_path))
        is_fake = label.lower() == "fake"

        # 2️⃣ Speech to Text + Translation
        stt_result = transcribe_audio(str(temp_path))

        original_text = stt_result.get("original_text", "")
        english_text = stt_result.get("english_text", "")
        language = stt_result.get("language", "unknown")

        analysis_text = english_text.lower()

        # Detect corrupted STT output
        stt_corrupted = False
        if len(original_text) > 20 and len(set(original_text)) < 5:
            stt_corrupted = True

        # 3️⃣ Phrase Detection
        phrases, phrase_risk = detect_scam_phrases(analysis_text)

        # 4️⃣ Intent Detection
        intent_result = detect_scam_intent(analysis_text)

        intent = intent_result.get("intent", "unknown")
        intent_conf = float(intent_result.get("confidence", 0))
        intent_risk = intent_result.get("risk_level", "LOW")

        # 5️⃣ Stress Detection
        stress_result = detect_stress(str(temp_path))
        stress_level = stress_result.get("stress_level", "LOW")
        stress_score = stress_result.get("stress_score", 0)

        # ===============================
        # 🚨 URGENCY SCAM DETECTION
        # ===============================

        urgency_patterns = [
            "account will be blocked",
            "account suspended",
            "account verification",
            "bank verification",
            "within minutes",
            "limited time",
            "immediately",
            "urgent action",
            "your account will be blocked"
        ]

        urgency_detected = any(p in analysis_text for p in urgency_patterns)

        # ===============================
        # 🧠 UNIVERSAL RISK ENGINE
        # ===============================

        risk_score = 0

        # Phrase signal
        phrase_weights = {
            "LOW": 0,
            "MEDIUM": 1,
            "HIGH": 2
        }
        risk_score += phrase_weights.get(phrase_risk, 0)

        # Intent signal
        intent_weights = {
            "LOW": 0,
            "MEDIUM": 2,
            "HIGH": 3
        }
        risk_score += intent_weights.get(intent_risk, 0)

        # Intent confidence boost
        if intent_conf > 0.75:
            risk_score += 1

        # Stress manipulation
        if stress_level == "HIGH":
            risk_score += 1

        # Deepfake impersonation
        if is_fake:
            risk_score += 3

        # Urgency tactic
        if urgency_detected:
            risk_score += 2

        # STT corruption protection
        if stt_corrupted:
            risk_score += 1

        # Multi‑signal fusion
        signals = 0

        if phrase_risk != "LOW":
            signals += 1

        if intent_risk != "LOW":
            signals += 1

        if urgency_detected:
            signals += 1

        if is_fake:
            signals += 1

        if signals >= 2:
            risk_score += 1

        # ===============================
        # 🚨 FINAL CLASSIFICATION
        # ===============================

        if risk_score >= 5:
            final_risk = "HIGH"
        elif risk_score >= 2:
            final_risk = "MEDIUM"
        else:
            final_risk = "LOW"

        response = {

            "filename": file.filename,

            "language_detected": language,

            "transcript_original": original_text,
            "transcript_english": english_text,

            "deepfake_result": label,
            "deepfake_confidence": float(round(confidence, 2)),

            "detected_phrases": phrases,
            "phrase_risk": phrase_risk,

            "stress_level": stress_level,
            "stress_score": float(stress_score),

            "scam_intent": intent,
            "intent_confidence": intent_conf,

            "final_risk": final_risk,

            "analysis": "AI Scam Voice Detected" if is_fake else "Human Voice Verified",

            "recommendation": (
                "⚠ Do NOT share OTP, bank details, or personal information."
                if final_risk == "HIGH"
                else "No major scam signals detected."
            )
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path.exists():
            temp_path.unlink()