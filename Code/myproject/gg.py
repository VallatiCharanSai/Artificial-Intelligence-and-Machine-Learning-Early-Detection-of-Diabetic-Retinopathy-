import torch
from torchvision import transforms
from PIL import Image

def predict_image(image_path, 
                  model_path="dr_model.pt", 
                  class_names=None, 
                  device=None):
    """
    Predicts the class of an image using a trained ResNet50 model (.pt full model checkpoint)
    using PyTorch 2.6+ with weights_only=False.
    """
    class_labels = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative']
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ========== LOAD FULL MODEL ==========
    model = torch.load(model_path, map_location=device, weights_only=False)  # bypass safe globals
    model.eval()
    model.to(device)

    # ========== IMAGE PREPROCESSING ==========
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    # ========== PREDICTION ==========
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        pred_class = predicted.item()

    if class_names:
        return class_names[pred_class]
    return pred_class,class_labels[pred_class]


# ================== USAGE ==================
if __name__ == "__main__":
    test_image_path = "test_dr_image.jpg"  # Replace with your test image path
    prediction = predict_image(test_image_path, model_path="dr_model.pt")
    print(f"Predicted Class: {prediction}")
