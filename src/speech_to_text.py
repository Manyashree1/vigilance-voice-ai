from faster_whisper import WhisperModel

# Load model once
model = WhisperModel(
    "large-v3",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(audio_path):

    # Transcribe original language
    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    original_text = " ".join([seg.text for seg in segments]).strip()

    # Translate to English
    segments_en, _ = model.transcribe(
        audio_path,
        beam_size=5,
        task="translate"
    )

    english_text = " ".join([seg.text for seg in segments_en]).strip()

    return {
        "original_text": original_text,
        "english_text": english_text,
        "language": info.language
    }