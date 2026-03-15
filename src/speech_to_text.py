from faster_whisper import WhisperModel

# Force CPU to avoid the "cublas64_12.dll not found" error
# int8 makes it run fast on your processor
model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_path):
    # beam_size=5 improves accuracy for different accents
    segments, info = model.transcribe(audio_path, beam_size=5)

    text = ""
    for segment in segments:
        text += segment.text + " "

    return text.strip()