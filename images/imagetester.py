import torch
from PIL import Image
import torch.hub
from torchvision import transforms
from efficientnet_pytorch import EfficientNet


# Load the same model architecture (nvidia_efficientnet_b0)
efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True)
efficientnet.classifier.fc = torch.nn.Linear(in_features=efficientnet.classifier.fc.in_features, out_features=290)

# Load the trained weights (same as saved previously)
efficientnet.load_state_dict(torch.load("/uolstore/home/users/sc21cm/disswork/synoptic-project-CameronFMacKay/images/best_efficientnet.pth"))

# Set model to evaluation mode and move to device
efficientnet.eval().to('cpu')  # or 'mps' for Apple Silicon GPU, or 'cuda' for a regular GPU

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

base_dir = "/vol/scratch/SoC/misc/2024/sc21cm/train_256_places365standard/data_256/"
import os
image_paths = []
labels = []

for main_dir in os.listdir(base_dir):
    main_path = os.path.join(base_dir, main_dir)
    if os.path.isdir(main_path):
        for place in os.listdir(main_path):
            place_path = os.path.join(main_path, place)
            if os.path.isdir(place_path):
                files = [os.path.join(place_path, f) for f in os.listdir(place_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
                image_paths.extend(files)
                labels.extend([f"{main_dir}/{place}"] * len(files))

# Shuffle dataset (combined image paths and labels) before splitting
combined = list(zip(image_paths, labels))
image_paths, labels = zip(*combined)

# Create a mapping of label names to numeric indices
unique_labels = sorted(set(labels))
label_to_index = {label: idx for idx, label in enumerate(unique_labels)}
index_to_label = {idx: label for label, idx in label_to_index.items()}


print(f"Predicted: {index_to_label[predicted_label.item()]}")