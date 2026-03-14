from transformers import pipeline

classifier = None

labels = [
    "financial scam",
    "otp request",
    "bank verification scam",
    "normal conversation"
]

def detect_scam_intent(text):

    global classifier

    if classifier is None:
        print("Loading scam intent model...")
        classifier = pipeline(
            "zero-shot-classification",
            model="valhalla/distilbart-mnli-12-3"
        )
        print("Scam intent model loaded")

    result = classifier(text, labels)

    label = result["labels"][0]
    score = result["scores"][0]

    if label == "normal conversation":
        risk = "LOW"
    elif score > 0.7:
        risk = "HIGH"
    else:
        risk = "MEDIUM"

    return {
        "intent": label,
        "confidence": float(score),
        "risk_level": risk
    }