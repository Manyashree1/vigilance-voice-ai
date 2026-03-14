from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid
from scam_detector.services.transcription_service import transcribe_audio
from scam_detector.services.scam_model_service import predict_scam
from scam_detector.services.deepfake_service import analyze_deepfake
from scam_detector.services.stress_service import analyze_stress
from scam_detector.services.audio_service import convert_to_wav
import traceback

app = FastAPI(title="Vigilance Voice AI")

@app.get("/")
def home():
    return {"message": "Vigilance Voice AI Backend Running"}

@app.post("/analyze_audio")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Analyzes an uploaded audio file.
    Performs transcription, scam content analysis, deepfake acoustic analysis, and stress level detection.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid audio file")

    # Save incoming file to a temporary location
    unique_id = uuid.uuid4().hex
    temp_file_path = f"temp_upload_{unique_id}_{file.filename}"
    
    try:
        # 1. Read and save file
        audio_bytes = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(audio_bytes)
            
        # 2. Convert audio to WAV format for reliable processing
        wav_path = convert_to_wav(temp_file_path)
            
        # 3. Transcribe audio
        text = transcribe_audio(wav_path)
        if not text:
            raise ValueError("Transcription failed or returned empty text")
            
        # 4. Scam Probability (Text Analysis)
        scam_result = predict_scam(text)
        
        # 5. Deepfake Score (Acoustic Analysis)
        deepfake_result = analyze_deepfake(wav_path)
        
        # 6. Stress Level (Acoustic Analysis)
        stress_result = analyze_stress(wav_path)
        
        return {
            "filename": file.filename,
            "transcription": text,
            "scam_probability": scam_result.get("scam_probability", 0.0),
            "label": scam_result.get("label", "safe"),
            "deepfake_probability": deepfake_result.get("deepfake_probability", 0.0),
            "stress_level": stress_result.get("stress_level", "unknown"),
            "metrics": stress_result.get("metrics", {})
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if 'wav_path' in locals() and os.path.exists(wav_path) and wav_path != temp_file_path:
            os.remove(wav_path)

# Keep the original endpoints for backward compatibility
@app.post("/detect_scam")
async def detect_scam(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(audio_bytes)
            
        wav_path = convert_to_wav(file_location)
        text = transcribe_audio(wav_path)
        prediction = predict_scam(text)

        # Cleanup
        if os.path.exists(file_location): os.remove(file_location)
        if os.path.exists(wav_path) and wav_path != file_location: os.remove(wav_path)
        
        return {
            "filename": file.filename,
            "transcription": text,
            "scam_prediction": prediction["scam_probability"],
            "label": prediction["label"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect_deepfake")
async def detect_deepfake(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(audio_bytes)
            
        wav_path = convert_to_wav(file_location)
        result = analyze_deepfake(wav_path)

        # Cleanup
        if os.path.exists(file_location): os.remove(file_location)
        if os.path.exists(wav_path) and wav_path != file_location: os.remove(wav_path)
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect_stress")
async def detect_stress(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(audio_bytes)
            
        wav_path = convert_to_wav(file_location)
        result = analyze_stress(wav_path)

        # Cleanup
        if os.path.exists(file_location): os.remove(file_location)
        if os.path.exists(wav_path) and wav_path != file_location: os.remove(wav_path)
            
        return {"stress_level": result.get("stress_level")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
