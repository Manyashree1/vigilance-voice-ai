import torch.nn as nn
import timm

class DeepfakeDetector(nn.Module):
    def __init__(self):
        super().__init__()
        # EfficientNet-B0 pre-trained weights ke saath load kar rahe hain
        self.model = timm.create_model('efficientnet_b0', pretrained=True)
        # Final layer badal kar 2 classes (Real vs Fake) ke liye
        self.model.classifier = nn.Linear(self.model.classifier.in_features, 2)

    def forward(self, x):
        return self.model(x)