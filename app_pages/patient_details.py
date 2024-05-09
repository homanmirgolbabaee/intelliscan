import streamlit as st

from utils.database import insert_patient_details, query_patient_details
def display():
    st.title("Patient Details 📝")
    with st.form("patient_details_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", step=1)
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        case_id = st.text_input("Case ID")
        submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        insert_patient_details(first_name, last_name, age, gender, case_id)
        st.success(f"Patient Details Saved: {first_name} 💾 ! ")
