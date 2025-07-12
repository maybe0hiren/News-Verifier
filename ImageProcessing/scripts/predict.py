import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import torch
from torchvision import transforms
from PIL import Image

from ImageProcessing.scripts.detectionModel import detectionModel

device = torch.device("cpu")

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
])

model = detectionModel(outputs=2)
model.load_state_dict(torch.load("ImageProcessing/models/best_model.pth", map_location=device))
model.to(device)
model.eval()

def prediction(imgLocation, class_names):
    img = Image.open(imgLocation).convert("RGB")
    img = transform(img).unsqueeze(0)
    img = img.to(device)

    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs.data, 1)
        predictedClass = class_names[predicted.item()]
        print(f"Prediction: {predictedClass}")

class_names = ["Fake", "Real"]

if __name__ == "__main__":
    testImgLocation = "dataset/test/fake/0416.jpg"
    prediction(testImgLocation, class_names)