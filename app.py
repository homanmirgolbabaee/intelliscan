import streamlit as st
import os
from PIL import Image, ImageDraw
import requests
import json
import time



## @@@ Weaviate Setup @@@

import weaviate
import weaviate.classes as wvc
import os
import requests
import json
from weaviate.schema import Schema


WCS_API_KEY = st.secrets["WCS_API_KEY"]
WCS_CLUSTER_URL= st.secrets["WCS_CLUSTER_URL"]
OPENAI_APIKEY=st.secrets["OPENAI_APIKEY"]



import weaviate
from weaviate import Client
from weaviate.util import generate_uuid5

def connect_to_weaviate():
    """
    Connect to the Weaviate instance using Streamlit secrets or environment variables.
    """
    client = weaviate.connect_to_wcs(
        cluster_url=st.secrets["WCS_CLUSTER_URL"],
        auth_credentials=weaviate.auth.AuthApiKey(st.secrets["WCS_API_KEY"]),
        headers={
            "X-OpenAI-Api-Key": st.secrets["OPENAI_APIKEY"]
        },
        skip_init_checks=True
    )
    
    try:
          
        #patient_fn = client.collections.create(
        #name="first_name",
        #vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        #generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries
        #)
        #patient_ln = client.collections.create(
        #name="last_name",
        #vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        #generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries            
        #)
        #patient_age = client.collections.create(
        #name="age",
        #vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        #generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries            
        #)
        #patient_case_id = client.collections.create (
        #name="case_id",
        #vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        #generative_config=wvc.config.Configure.Generative.openai()  # Ensure the `generative-openai` module is used for generative queries       
        #)

    
        pass
        
    finally:
        pass
    
    
    st.success("✅ Connected to Weaviate successfully! ")
    
    return client


        




def create_patient_schema(client):
    """
    Create the 'Patient' schema in Weaviate.
    """
    schema = {
        "classes": [{
            "class": "Patient",
            "description": "A class to store patient details",
            "properties": [
                {
                    "name": "first_name",
                    "dataType": ["string"],
                    "description": "The first name of the patient",
                    # Additional configuration for vectorization can be added here
                },
                {
                    "name": "last_name",
                    "dataType": ["string"],
                    "description": "The last name of the patient",
                    # Additional configuration for vectorization can be added here
                },
                {
                    "name": "age",
                    "dataType": ["string"],
                    "description": "The age of the patient",
                    # Additional configuration for validation or other purposes can be added here
                },
                {
                    "name": "case_id",
                    "dataType": ["string"],
                    "description": "The unique case ID for the patient",
                    # Additional configuration for unique constraints can be added here if supported
                }
            ],
            "vectorizer": "text2vec-openai",
            # Add generative module configuration if needed
        }]
    }
    client.schema.delete_all()  # Caution: This deletes the existing schema. Use with care.
    client.schema.create(schema)







# Set the directory where your images are stored
image_dir = 'images'
brain_url = st.secrets["brain_url"]
# Use Streamlit secrets for API header
BRAIN_HEADER = st.secrets["brain_api"]
API_URL = brain_url
headers = {"Authorization": BRAIN_HEADER}








def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def draw_boxes(image_path, boxes):
    with Image.open(image_path) as im:
        draw = ImageDraw.Draw(im)
        for box in boxes:
            xmin, ymin, xmax, ymax = box
            draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="red", width=3)
        return im

def load_images(image_dir):
    images = []
    for file in os.listdir(image_dir):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            images.append(os.path.join(image_dir, file))
    return images

def app_home():
    st.title("Radiology Image Viewer 🏠")
    st.markdown("Welcome to the Radiology Image Viewer. Select an option from the left sidebar to begin.")

                

            


def app_patient_details():
    st.title("Patient Details 📝")
    
    client = None  # Initialize client to None

    if st.button("Patient Database"):
        client = connect_to_weaviate()  # Connect to Weaviate
        

    
    with st.form("patient_details_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", step=1)
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        case_id = st.text_input("Case ID")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            
            client = connect_to_weaviate()

            patients_obj= {
                "first_name": first_name,
                "last_name": last_name,
                "age": str(age),
                "case_id" : float(case_id)
            }
            patients = client.collections.get("Patient")
            patients.data.insert(patients_obj)  # This uses batching under the hood
            
            st.success(f"Patient Details Saved: {first_name} 💾 ! ")






def app_image_analysis():
    st.title("Image Analysis 🔍")
    images = load_images(image_dir)
    if images:
        selected_image = st.selectbox('Select an image:', images)

        # Create two columns for displaying images side by side
        col1, col2 = st.columns(2)

        with col1:
            st.write("Original Image")
            image = Image.open(selected_image)
            st.image(image, caption=os.path.basename(selected_image), use_column_width=True)

        # Perform analysis and display results in the second column
        if st.button('Perform Analysis 🔎'):
            output = query(selected_image)
            if isinstance(output, list):
                boxes = []
                for result in output:
                    # Ensure each result is a dictionary and has a "box" key
                    if isinstance(result, dict) and "box" in result:
                        box = result["box"]
                        xmin, ymin, xmax, ymax = box.get("xmin"), box.get("ymin"), box.get("xmax"), box.get("ymax")
                        boxes.append((xmin, ymin, xmax, ymax))
                if boxes:
                    image_with_boxes = draw_boxes(selected_image, boxes)
                    with col2:
                        st.write("Analysis Result")
                        st.image(image_with_boxes, caption="Analysis Result", use_column_width=True)
                else:
                    with col2:
                        st.write("Analysis Result")
                        st.write("No significant findings.")
            else:
                st.error("Unexpected response format. Please check the API response. ❗")
    else:
        st.error("No images found in the specified directory. Please check the directory path. ⚠️")


def app_generate_report():
    st.title("Generate Report 📊")
    case_id = st.text_input("Case ID", "Enter Case ID here...")
    findings = st.text_area("Findings", "Describe the findings here...")
    conclusion = st.text_area("Conclusion", "Enter the conclusion here...")
    if st.button("Generate Report 📄"):
        st.success("Report generated successfully for Case ID: " + case_id + " 🎉")
        st.markdown("### Findings")
        st.write(findings)
        st.markdown("### Conclusion")
        st.write(conclusion)

def main():
    st.sidebar.title('Navigation 🧭')
    app_mode = st.sidebar.radio("Choose the app mode",
                                ["Home", "Patient Details", "Image Analysis", "Generate Report"])
    if app_mode == "Home":
        app_home()
    elif app_mode == "Patient Details":
        app_patient_details()
    elif app_mode == "Image Analysis":
        app_image_analysis()
    elif app_mode == "Generate Report":
        app_generate_report()

    # Footer
    st.sidebar.markdown('---')
    st.sidebar.markdown('© 2024 Radiology Image Viewer IntelliScan Inc. 🧠')

if __name__ == '__main__':
    main()
