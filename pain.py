import streamlit as st
import os
from PIL import Image

# Set the directory where your images are stored
image_dir = 'images'



import requests

API_URL = "https://api-inference.huggingface.co/models/DunnBC22/yolos-tiny-Brain_Tumor_Detection"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()








def load_images(image_dir):
    """
    Load images from the specified directory and return a list of image paths.
    """
    images = []
    for file in os.listdir(image_dir):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            images.append(os.path.join(image_dir, file))
    return images

def dummy_operation():
    """
    A dummy operation function that returns a message.
    """
    return "The button was clicked!"

def main():
    st.sidebar.title('Radiology Image Viewer Controls')
    
    # Load images
    images = load_images(image_dir)

    if images:
        # Sidebar for selecting an image
        selected_image = st.sidebar.selectbox('Select an image:', images)

        # Display the selected image in main area
        image = Image.open(selected_image)
        st.image(image, caption=os.path.basename(selected_image), width=260 )

        # Expander for image operations
        with st.expander("Image Operations"):
            if st.button('Perform Operation'):
                message = dummy_operation()
                output = query(selected_image)
                st.write(message)
                st.write(output)
    else:
        st.sidebar.error('No images found in the specified directory. Please check the directory path.')
        
    # Footer
    st.sidebar.markdown('---')
    st.sidebar.markdown('© 2024 Radiology Image Viewer')

if __name__ == '__main__':
    main()
