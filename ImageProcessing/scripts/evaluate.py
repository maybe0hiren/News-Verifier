import os
import sys
import torch
from torchvision import transforms, datasets
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ImageProcessing.scripts.detectionModel import detectionModel

device = torch.device("cpu")

testingDataFolder = "dataset/test"
model = "ImageProcessing/models/best_model.pth"
resultsStorage = "ImageProcessing/results.txt"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

testingData = datasets.ImageFolder(root=testingDataFolder, transform=transform)
testLoader = torch.utils.data.DataLoader(testingData, batch_size=32, shuffle=False)

aiModel = detectionModel(outputs=2)
aiModel.load_state_dict(torch.load(model, map_location=device))
aiModel.to(device)
aiModel.eval()

predictionList = []
labelList = []

with torch.no_grad():
    for images, labels in testLoader:
        images = images.to(device)
        labels = labels.to(device)

        outputs = aiModel(images)
        _, predicted = torch.max(outputs, 1)

        predictionList.extend(predicted.cpu().numpy())
        labelList.extend(labels.cpu().numpy())

classNames = testingData.classes
accuracy = accuracy_score(labelList, predictionList)
precision = precision_score(labelList, predictionList)
recall = recall_score(labelList, predictionList)
f1Score = f1_score(labelList, predictionList)
report = classification_report(labelList, predictionList, target_names=classNames)

print("Evaluation Metrics:")
print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall   : {recall * 100:.2f}%")
print(f"F1 Score : {f1Score  * 100:.2f}%\n")
print("Full Classification Report:")
print(report)

with open(resultsStorage, "w") as f:
    f.write("Evaluation Report\n")
    f.write("------------------\n")
    f.write(f"Accuracy : {accuracy * 100:.2f}%\n")
    f.write(f"Precision: {precision * 100:.2f}%\n")
    f.write(f"Recall   : {recall * 100:.2f}%\n")
    f.write(f"F1 Score : {f1Score * 100:.2f}%\n\n")
    f.write(report)

print(f"\nReport saved to: {resultsStorage}")

# print("Class index mapping:", testingData.class_to_idx)
