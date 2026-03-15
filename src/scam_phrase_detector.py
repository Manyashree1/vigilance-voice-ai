# src/scam_phrase_detector.py

SCAM_PHRASES = [
    "share your otp",
    "tell me your otp",
    "verify your bank account",
    "urgent payment required",
    "send money immediately",
    "your account will be blocked",
    "confirm your card details"
]

def detect_scam_phrases(text):
    """
    Detect scam phrases in the transcript.
    Returns:
        detected_phrases (list)
        risk_level (LOW / MEDIUM / HIGH)
    """

    text = text.lower()

    detected = []

    for phrase in SCAM_PHRASES:
        if phrase in text:
            detected.append(phrase)

    # Risk logic
    if len(detected) == 0:
        risk = "LOW"
    elif len(detected) <= 2:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return detected, risk