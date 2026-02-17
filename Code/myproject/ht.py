import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# DR class labels
DR_CLASSES = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR"
}

# Load pretrained ResNet50
model = models.resnet50(pretrained=True)

# Replace last fully connected layer
model.fc = nn.Linear(model.fc.in_features, 5)

# Set model to evaluation mode
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def classify_dr(image_path):
    """
    Classifies a fundus image into diabetic retinopathy categories
    using ResNet50 (PyTorch).
    """

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        outputs = model(image)
        predicted_class = torch.argmax(outputs, dim=1).item()

    return predicted_class, DR_CLASSES[predicted_class]


# Test (optional)

