import os
import subprocess
import librosa
import soundfile as sf
import uuid

def convert_to_wav(input_path: str) -> str:
    """
    Converts audio file to WAV format using ffmpeg.
    Returns the path to the converted .wav file.
    """
    if input_path.lower().endswith('.wav'):
        return input_path
    
    unique_id = uuid.uuid4().hex
    output_path = f"temp_{unique_id}.wav"
    
    try:
        # Using ffmpeg to convert any audio/video to 16kHz mono WAV
        command = [
            'ffmpeg', '-y', '-i', input_path, 
            '-ar', '16000', '-ac', '1', output_path
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        print(f"Error converting audio with ffmpeg: {e}")
        # Fallback to librosa if ffmpeg fails (though librosa might fail on m4a/mp4 without ffmpeg installed)
        try:
            y, sr = librosa.load(input_path, sr=16000, mono=True)
            sf.write(output_path, y, sr)
            return output_path
        except Exception as fallback_e:
            print(f"Fallback librosa conversion failed: {fallback_e}")
            raise RuntimeError("Could not convert audio file to WAV.")
