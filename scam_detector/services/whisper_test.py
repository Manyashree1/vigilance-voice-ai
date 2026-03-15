import whisper

print("Loading model...")

model = whisper.load_model("base")

print("Model loaded")

result = model.transcribe("sample2.wav")

print("Transcription:")
print(result["text"])