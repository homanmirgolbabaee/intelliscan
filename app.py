import streamlit as st
from app_pages import home, patient_details, image_analysis, generate_report

def main():
    st.sidebar.title('Navigation 🧭')
    app_mode = st.sidebar.radio("Choose the app mode", ["Home", "Patient Details", "Image Analysis", "Generate Report"])
    
    if app_mode == "Home":
        home.display()
    elif app_mode == "Patient Details":
        patient_details.display()
    elif app_mode == "Image Analysis":
        image_analysis.display()
    elif app_mode == "Generate Report":
        generate_report.display()

if __name__ == '__main__':
    main()
