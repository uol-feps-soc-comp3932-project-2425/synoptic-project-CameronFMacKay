import os
import torch
from PIL import Image
import torch.hub
from torchvision import transforms
import csv

# Always point to backend/images/ regardless of where it's called from
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))

def classify_image(image_path):
    efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True )
    efficientnet.classifier.fc = torch.nn.Linear(in_features=efficientnet.classifier.fc.in_features, out_features=58)

    model_path = os.path.join(BASE_DIR, "best_efficientnet57.pth")
    efficientnet.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    efficientnet.eval().to('cpu') 

    transform = transforms.Compose([
        transforms.Resize((256, 256)), 
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to('cpu')

    with torch.no_grad():
        outputs = efficientnet(input_tensor)
        _, predicted_label = torch.max(outputs, 1)

    class_mapping_path = os.path.join(BASE_DIR, "classmapping.csv")
    class_mapping = {}
    with open(class_mapping_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            class_mapping[int(row[0])] = row[1] 

    predicted_class_name = class_mapping.get(predicted_label.item(), "Unknown")
    return predicted_class_name
