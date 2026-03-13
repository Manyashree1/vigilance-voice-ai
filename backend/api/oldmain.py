import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


from fastapi import FastAPI,UploadFile,File
import shutil
import os
from pathlib import Path

# Import new deepfake detector
from src.deepfake_detector import detect_deepfake

app = FastAPI(title="Vigilance Voice AI")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "data"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {"message": "Vigilance Voice AI is running", "status": "Server Active"}


@app.post("/verify-call")
async def verify_call(file: UploadFile = File(...)):
    try:
        # Save uploaded audio
        temp_path = UPLOAD_DIR / f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Run Deepfake detection
        label, confidence = detect_deepfake(str(temp_path))

        # Delete temp file
        if temp_path.exists():
            temp_path.unlink()

        # Prepare result
        is_fake = True if label == "Fake" else False
        return {
            "filename": file.filename,
            "is_fraud": is_fake,
            "confidence": f"{confidence:.2f}%",
            "analysis": "AI Voice Detected" if is_fake else "Human Voice Verified",
            "risk_level": "HIGH" if is_fake else "LOW"
        }

    except Exception as e:
        return {"error": str(e)}