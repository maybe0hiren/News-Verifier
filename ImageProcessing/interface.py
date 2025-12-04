import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

MODEL_PATH = "/home/Hiren/Documents/Cache/News-Verifier/resnet18_ai_classifier.pth"

_device = "cuda" if torch.cuda.is_available() else "cpu"
_model = None

def _load_model():
    global _model
    if _model is None:
        print("Loading model from:", MODEL_PATH)

        model = models.resnet18(weights=None)
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, 1)

        model.load_state_dict(torch.load(MODEL_PATH, map_location=_device))
        model.to(_device)
        model.eval()
        _model = model

_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def classify_image(image_path):
    _load_model()

    if not os.path.exists(image_path):
        return "ERROR: File not found."

    img = Image.open(image_path).convert("RGB")
    img_tensor = _transform(img).unsqueeze(0).to(_device)

    with torch.no_grad():
        output = _model(img_tensor)
        sig = torch.sigmoid(output).item()

    print(sig)
    if sig < 0.5:
        return "REAL"
    else:
        return "AI Generated"