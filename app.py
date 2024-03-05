import streamlit as st
import torch
from monai.networks.nets import DenseNet121
from monai.transforms import Compose, LoadImage, EnsureChannelFirst, ScaleIntensity, ToTensor
from PIL import Image
import io
import numpy as np


def main():
    # Define the transformation pipeline
    transform = Compose([
        LoadImage(image_only=True),
        EnsureChannelFirst(),
        ScaleIntensity(),
        ToTensor()
    ])

    # Load your trained model
    model = DenseNet121(spatial_dims=2, in_channels=1, out_channels=6)  # Adjust `out_channels` as per your setup
    model_path = 'best_metric_model.pth'  # Ensure this path is correct
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    # Streamlit interface for file upload
    st.title('Medical Image Classification')

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    def predict(image):
        """
        Function to predict the class of the image
        """
        # Pre-process the image and add batch dimension
        img = transform(image)
        img = torch.unsqueeze(img, 0)
        
        with torch.no_grad():
            preds = model(img)
            # Assuming your model outputs raw logits
            predicted_scores = torch.softmax(preds, dim=1)
            predicted_class = predicted_scores.argmax(dim=1).item()
            confidence = predicted_scores[0, predicted_class].item()
            return predicted_class, confidence

    if uploaded_file is not None:
        # Convert the file to an image
        image = Image.open(uploaded_file).convert('L')  # Convert to grayscale
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("Classifying...")
        label, confidence = predict(np.array(image))
        # TODO: Convert `label` to the actual class name if you have a mapping
        st.write(f"Prediction: {label} with confidence {confidence:.2f}")

# Run the app
if __name__ == '__main__':
    main()
