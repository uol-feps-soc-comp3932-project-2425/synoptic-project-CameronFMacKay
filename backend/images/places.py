import torch
from PIL import Image
import torch.hub
from torchvision import transforms
import csv

def classify_image(image_path):
    efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True )
    efficientnet.classifier.fc = torch.nn.Linear(in_features=efficientnet.classifier.fc.in_features, out_features=58)
    efficientnet.load_state_dict(torch.load("../images/best_efficientnet57.pth", map_location=torch.device('cpu')))
    efficientnet.eval().to('cpu') 

    transform = transforms.Compose([
        transforms.Resize((256, 256)), 
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    input_tensor = input_tensor.to('cpu')

    with torch.no_grad():
        outputs = efficientnet(input_tensor)
        _, predicted_label = torch.max(outputs, 1)

    # Load class mapping from CSV
    class_mapping = {}
    with open('../images/classmapping.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            class_mapping[int(row[0])] = row[1] 
    predicted_class_name = class_mapping.get(predicted_label.item(), "Unknown")
    return predicted_class_name