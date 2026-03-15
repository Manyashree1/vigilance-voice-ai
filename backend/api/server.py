import os
import sys
import logging
from pathlib import Path

# Silence all technical noise
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("faster_whisper").setLevel(logging.ERROR)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Pathing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# These imports now happen once and keep models in RAM
from src.deepfake_detector import detect_deepfake
from src.speech_to_text import transcribe_audio
from src.scam_phrase_detector import detect_scam_phrases
from src.scam_intent_detector import detect_scam_intent
from src.stress_detector import detect_stress

app = FastAPI(title="Vigilance Voice AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "data"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/verify-call")
async def verify_call(file: UploadFile = File(...)):
    temp_path = UPLOAD_DIR / f"app_temp_{file.filename}"
    
    try:
        # Fast binary save
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        # Execution Pipeline
        label, confidence = detect_deepfake(str(temp_path))
        text = transcribe_audio(str(temp_path)) or ""
        phrases, phrase_risk = detect_scam_phrases(text)
        intent_res = detect_scam_intent(text)
        stress_res = detect_stress(str(temp_path))

        # Risk Calculation
        is_fake = str(label).lower() == "fake"
        intent_risk = intent_res.get("risk_level")
        stress_lvl = stress_res.get("stress_level", "LOW")

        # Aggregate Verdict
        final_risk = "LOW"
        if is_fake or intent_risk == "HIGH" or phrase_risk == "HIGH" or stress_lvl == "HIGH":
            final_risk = "HIGH"

        # Clean Terminal Output
        print(f"\n--- [SCAN: {file.filename}] ---")
        print(f"VERDICT: {final_risk}")
        print(f"REASON:  Deepfake={label}, Intent={intent_res.get('intent')}, Stress={stress_lvl}")
        print(f"-----------------------------------\n")

        # Response payload for the App
        return {
            "status": "success",
            "verdict": final_risk,
            "data": {
                "is_ai_voice": is_fake,
                "ai_confidence": round(confidence, 2),
                "transcript": text,
                "detected_intent": intent_res.get("intent"),
                "stress_detected": stress_lvl
            }
        }

    except Exception as e:
        print(f"Critical System Error: {e}")
        raise HTTPException(status_code=500, detail="Internal analysis error")
    finally:
        if temp_path.exists():
            temp_path.unlink()

if __name__ == "__main__":
    import uvicorn
    # Host 0.0.0.0 makes it accessible to your phone on the same WiFi
    uvicorn.run(app, host="0.0.0.0", port=8000)