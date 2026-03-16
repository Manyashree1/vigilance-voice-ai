import os
import logging
from transformers import pipeline

# Silence the "Tied Weights" and "Symlink" warnings
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
logging.getLogger("transformers").setLevel(logging.ERROR)

# Load model ONCE at the global level for maximum speed
print("🚀 [SYSTEM] Initializing Scam Intent Engine...")
classifier = pipeline(
    "zero-shot-classification", 
    model="valhalla/distilbart-mnli-12-3",
    device=-1 # CPU
)

def detect_scam_intent(text):
    # 1. Targeted labels for security
    candidate_labels = [
        "requesting sensitive passwords or otp", 
        "financial fraud and bank scam", 
        "kidnapping threat", 
        "safe casual conversation"
    ]
    
    # 2. Run the AI Model
    result = classifier(text, candidate_labels=candidate_labels)
    top_intent = result['labels'][0]
    score = result['scores'][0]

    # 3. THE SAFETY NET (Keyword Check)
    # Even if the AI is 1GB, simple keywords are often more reliable for security
    danger_keywords = ["password", "otp", "pin", "cvv", "credit card", "bank account", "transfer"]
    contains_danger_word = any(word in text.lower() for word in danger_keywords)

    # 4. Final Logic
    # Risk is HIGH if AI detects scam OR if danger keywords are present
    if (top_intent != "safe casual conversation" and score > 0.3) or contains_danger_word:
        risk_level = "HIGH"
    else:
        risk_level = "LOW"
    
    return {
        "intent": "Sensitive Information Request" if contains_danger_word else top_intent,
        "confidence": score,
        "risk_level": risk_level
    }
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