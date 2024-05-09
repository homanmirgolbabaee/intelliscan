import streamlit as st
from utils.image_processing import load_images, draw_boxes
import os 

def display():
    st.title("Image Analysis 🔍")
    images = load_images()
    if images:
        selected_image = st.selectbox('Select an image:', images)
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Original Image")
            st.image(selected_image, caption=os.path.basename(selected_image), use_column_width=True)
        
        if st.button('Perform Analysis 🔎'):
            # Example placeholder functionality
            boxes = [(50, 50, 150, 150)]  # Placeholder for actual analysis results
            image_with_boxes = draw_boxes(selected_image, boxes)
            with col2:
                st.write("Analysis Result")
                st.image(image_with_boxes, caption="Analysis Result", use_column_width=True)
    else:
        st.error("No images found in the specified directory. Please check the directory path. ⚠️")
