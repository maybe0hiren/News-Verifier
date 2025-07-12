import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import torch 
import torch.nn as tnn
import torch.optim as topt

from ImageProcessing.utils.loader import processImages
from ImageProcessing.scripts.detectionModel import detectionModel

def evaluation(model, loader, device):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        accuracy = (correct/total)*100
        print("Accuracy: ", accuracy)
        return accuracy

def training(model, trainingLoader, validationLoader, device, num_epochs=10, learningRate=0.001):
    class_weights = torch.tensor([1.0, 2.0]).to(device)
    modelError = tnn.CrossEntropyLoss(weight=class_weights)
    optimizer = topt.Adam(model.parameters(), lr = learningRate)
    best_accuracy = 0.0

    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch+1}/{num_epochs}")
        model.train()
        runningLoss = 0.0
        correct = 0
        total = 0

        for images, labels in trainingLoader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = modelError(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            runningLoss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        trainingAccuracy = (correct/total)*100
        avgLoss = runningLoss/len(trainingLoader)
        print(f"Train Loss: {avgLoss:.4f}, Train Accuracy: {trainingAccuracy:.2f}%")

        validationAccuracy = evaluation(model, validationLoader, device)

        if validationAccuracy > best_accuracy:
            best_accuracy = validationAccuracy
            torch.save(model.state_dict(), "ImageProcessing/models/best_model.pth")
            print("Best model saved")
    print("Training Complete")

if __name__ == "__main__":
    device = torch.device("cpu")
    
    trainingLoader, validationLoader, class_names = processImages("data", imgSlotSize=32)

    model = detectionModel(outputs=2)
    model.to(device)

    training(model, trainingLoader, validationLoader, device, num_epochs=20, learningRate=0.001)

    # for images, labels in trainingLoader:
    #     print("Sample labels:", labels[:10])
    #     break