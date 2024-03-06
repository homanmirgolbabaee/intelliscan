import streamlit as st
import os
from PIL import Image
from PIL import Image, ImageDraw
# Set the directory where your images are stored
image_dir = 'images'



import requests
import json

BRAIN_HEADER = st.secrets["brain_api"]

API_URL = "https://api-inference.huggingface.co/models/DunnBC22/yolos-tiny-Brain_Tumor_Detection"
headers = {"Authorization": BRAIN_HEADER}



def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()





def draw_boxes(image_path, boxes):
    """
    Draw rectangles on the image for each box in boxes.
    """
    with Image.open(image_path) as im:
        draw = ImageDraw.Draw(im)
        for box in boxes:
            xmin, ymin, xmax, ymax = box
            draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="red", width=3)
        return im



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
    return "Analysis Started ..."

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
                # Extract bounding box coordinates from the output
                boxes = []
                if output:
                    for result in output:
                        box = result.get("box", {})
                        xmin, ymin, xmax, ymax = box.get("xmin"), box.get("ymin"), box.get("xmax"), box.get("ymax")
                        boxes.append((xmin, ymin, xmax, ymax))


               # Draw boxes on the image
                if boxes:
                    image_with_boxes = draw_boxes(selected_image, boxes)
                    st.image(image_with_boxes, caption=os.path.basename(selected_image), use_column_width=True)
                else:
                    # Display the original selected image in main area if there are no boxes
                    image = Image.open(selected_image)
                    st.image(image, caption=os.path.basename(selected_image), width=260)


                # Write output to JSON file
                with open('output.json', 'w') as f:
                    json.dump(output, f)
                
                    
    else:
        st.sidebar.error('No images found in the specified directory. Please check the directory path.')
        
    # Footer
    st.sidebar.markdown('---')
    st.sidebar.markdown('© 2024 Radiology Image Viewer')

if __name__ == '__main__':
    main()
