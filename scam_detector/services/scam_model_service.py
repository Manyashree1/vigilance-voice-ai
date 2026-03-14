import os
import pickle
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import logging

logger = logging.getLogger(__name__)

class ScamModelService:
    def __init__(self, model_path: str = "models/scam_model.pkl"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
        
        # Determine absolute path for the model relative to the current file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.full_model_path = os.path.join(base_dir, model_path)
        
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        try:
            if os.path.exists(self.full_model_path):
                with open(self.full_model_path, "rb") as f:
                    state_dict = pickle.load(f)
                self.model.load_state_dict(state_dict)
                logger.info(f"Successfully loaded scam model from {self.full_model_path}")
                self.model_loaded = True
            else:
                logger.warning(f"Scam model not found at {self.full_model_path}. Using base BERT.")
        except Exception as e:
            logger.error(f"Error loading scam model: {e}")
            
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str) -> dict:
        if not text.strip():
            return {"scam_probability": 0.0, "label": "safe"}
            
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
        
        scam_prob = float(probs[0][1])
        label = "scam" if scam_prob > 0.5 else "safe"
        
        return {
            "scam_probability": round(scam_prob, 4),
            "label": label
        }

# Singleton instance for the service
scam_service = ScamModelService()

def predict_scam(text: str) -> dict:
    return scam_service.predict(text)
