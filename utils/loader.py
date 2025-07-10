from torchvision import datasets, transforms
from torch.utils.data import DataLoader as dl 

def processImages(datasetFolder, imgSlotSize=16, imgSize=224):
    processedTrainImages = transforms.Compose([
        transforms.Resize((imgSize, imgSize)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
    ]) 
    processedValidateImages = transforms.Compose([
        transforms.Resize((imgSize, imgSize)),
        transforms.ToTensor(),
        transforms.Normalize()
    ])
    

    trainingDataset = datasets.ImageFolder(root=f"dataset/train", transform=processedTrainImages)
    validatingDataset = datasets.ImageFolder(root=f"dataset/validate", transform=processedValidateImages)


    trainingDataLoader = dl(trainingDataset, batch_size=imgSlotSize, shuffle=True)
    validatingDataLoader = dl(validatingDataset, batch_size=imgSlotSize, shuffle=False)

    return trainingDataLoader, validatingDataLoader, trainingDataset.classes
