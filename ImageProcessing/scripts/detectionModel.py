import torch
import torch.nn as tnn 
from torchvision import models
import torch.optim as opt 

def detectionModel(outputs=2):
    classifierModel = models.resnet18(pretrained=True)

    for x in classifierModel.parameters():
        x.requires_grad = True
    
    finalLayerInputSize = classifierModel.fc.in_features
    classifierModel.fc = tnn.Linear(finalLayerInputSize, outputs)

    return classifierModel