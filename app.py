import streamlit as st
import os
from PIL import Image, ImageDraw
import requests
import json
import time


import os
import requests
import json

import sqlite3


def init_db():
    conn = sqlite3.connect('patient_data.db')  # This will create the database file if it does not exist
    c = conn.cursor()
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            gender TEXT,
            case_id TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    
    st.success("✅ Connected to Weaviate successfully! ")


def get_db_connection():
    conn = sqlite3.connect('patient_data.db')
    conn.row_factory = sqlite3.Row  # This enables name-based access to columns
    return conn        


def query_patient_details(case_id):
    conn = get_db_connection()
    c = conn.cursor()
    patient = c.execute('SELECT * FROM patients WHERE case_id = ?', (case_id,)).fetchone()
    conn.close()
    return patient





# Set the directory where your images are stored
image_dir = 'images'







def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
   #response = requests.post(API_URL, headers=headers, data=data)
   # return response.json()

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
        #client = connect_to_weaviate()  # Connect to Weaviate
        pass
        

    
    with st.form("patient_details_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", step=1)
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        case_id = st.text_input("Case ID")
        submit_button = st.form_submit_button("Submit")
        
    if submit_button:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO patients (first_name, last_name, age, gender, case_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, age, gender, case_id))
        conn.commit()
        conn.close()
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
    init_db()  # Initialize the database and tables

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
