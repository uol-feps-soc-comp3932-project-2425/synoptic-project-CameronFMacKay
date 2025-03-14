import torch
from PIL import Image
import torch.hub
from torchvision import transforms
from efficientnet_pytorch import EfficientNet
import csv

# Load the same model architecture (nvidia_efficientnet_b0)
efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True)
efficientnet.classifier.fc = torch.nn.Linear(in_features=efficientnet.classifier.fc.in_features, out_features=290)

# Load the trained weights (same as saved previously)
efficientnet.load_state_dict(torch.load("/uolstore/home/users/sc21cm/disswork/synoptic-project-CameronFMacKay/images/best_efficientnet.pth"))

# Set model to evaluation mode and move to device
efficientnet.eval().to('cpu') 

# Define transformation for image preprocessing (same as during training)
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize to the model's expected input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Example for testing with a new image:
image_path = "/vol/scratch/SoC/misc/2024/sc21cm/train_256_places365standard/data_256/c/coffee_shop/00000001.jpg"
image = Image.open(image_path).convert("RGB")

# Apply transformation
input_tensor = transform(image).unsqueeze(0)  # Add batch dimension

# Move the image to the correct device (if needed)
input_tensor = input_tensor.to('cpu')  # Change to 'mps' or 'cuda' if using those devices

# Run inference
with torch.no_grad():
    outputs = efficientnet(input_tensor)
    _, predicted_label = torch.max(outputs, 1)

# Print the predicted label
print(f"Predicted label: {predicted_label.item()}")

# Load class mapping from CSV
class_mapping = {}
with open('classmapping.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        class_mapping[int(row[0])] = row[1]  # Assuming the first column is index and second is class name

# Get the predicted label class name from the CSV mapping
predicted_class_name = class_mapping.get(predicted_label.item(), "Unknown")

# Print the predicted class name
print(f"Predicted label: {predicted_class_name}")