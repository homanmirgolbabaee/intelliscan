import base64
import streamlit as st
from crewai import Agent, Crew, Task

# Define the patient inquiry data structure
class PatientInquiry:
    def __init__(self, name, age, symptoms):
        self.name = name
        self.age = age
        self.symptoms = symptoms
        self.priority = self.determine_priority()

    def determine_priority(self):
        # Simplified priority determination logic
        if "chest pain" in self.symptoms or "difficulty breathing" in self.symptoms:
            return "High"
        elif "fever" in self.symptoms or "pain" in self.symptoms:
            return "Medium"
        else:
            return "Low"

# Define agents and their roles
triage_agent = Agent(
    role="Triage Nurse",
    goal="Quickly assess the severity of patient symptoms and assign priority levels.",
    backstory="You are a Triage Nurse, responsible for initial patient assessment in the emergency room.",
    allow_delegation=False,
    verbose=True
)

doctor_agent = Agent(
    role="Emergency Room Doctor",
    goal="Diagnose and treat patients based on their symptoms and priority level.",
    backstory="You are an Emergency Room Doctor, providing critical care and medical treatment.",
    allow_delegation=False,
    verbose=True
)

support_agent = Agent(
    role="Support Staff",
    goal="Provide logistical support and manage patient information.",
    backstory="You are part of the support staff, ensuring smooth operations and accurate record-keeping.",
    allow_delegation=False,
    verbose=True
)

# Define tasks for each agent
triage_task = Task(
    description="Assess patient symptoms: {symptoms} and determine priority level.",
    expected_output="Patient {name} assigned a priority of {priority}.",
    agent=triage_agent
)

diagnosis_task = Task(
    description="Diagnose and propose treatment for patient {name} with symptoms: {symptoms}.",
    expected_output="Diagnosis and treatment plan for patient {name} with priority {priority}.",
    agent=doctor_agent
)

support_task = Task(
    description="Manage patient information: {name}, {age}, {symptoms}, {priority}.",
    expected_output="Patient information stored successfully.",
    agent=support_agent
)

# Create a crew with the defined agents and tasks
crew = Crew(
    agents=[triage_agent, doctor_agent, support_agent],
    tasks=[triage_task, diagnosis_task, support_task],
    verbose=2,
    memory=True
)

from fpdf import FPDF


def create_pdf(patient_info, result):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Emergency Room Report", 0, 1, 'C')

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Information", 0, 1)
    pdf.set_font("Arial", '', 12)
    for key, value in patient_info.items():
        pdf.multi_cell(0, 10, f"{key.capitalize()}: {value}")

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Diagnosis and Treatment Plan", 0, 1)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, result)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Patient Record", 0, 1)
    pdf.set_font("Arial", '', 12)
#    pdf.multi_cell(0, 10, record)

    return pdf.output(dest='S').encode('latin1')





# Streamlit Page
def display():


    st.title("Emergency Room AI System")
    
    st.sidebar.header("Configuration")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    
    if openai_api_key:
        st.sidebar.success("API key loaded successfully.")
    else:
        st.sidebar.error("Please enter your OpenAI API key.")
        return
    
        
    # st.title("Emergency Room AI System")
    
    st.header("Enter Patient Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    symptoms = st.text_area("Symptoms (comma-separated)")
    
    if st.button("Submit"):
        symptoms_list = [symptom.strip() for symptom in symptoms.split(',')]
        patient_inquiry = PatientInquiry(name, age, symptoms_list)
        patient_inquiry_dict = {
            "name": patient_inquiry.name,
            "age": patient_inquiry.age,
            "symptoms": patient_inquiry.symptoms,
            "priority": patient_inquiry.priority
        }

        result = crew.kickoff(inputs=patient_inquiry_dict)
        
        st.subheader("Patient Information")
        st.write(f"Name: {name}")
        st.write(f"Age: {age}")
        st.write(f"Symptoms: {', '.join(symptoms_list)}")
        st.write(f"Priority: {patient_inquiry.priority}")
        
        st.subheader("Diagnosis and Treatment Plan")
        st.write(result)
        

        # Create PDF
        pdf_bytes = create_pdf(patient_inquiry_dict, result)

        # Base64 encode the PDF for download
        b64 = base64.b64encode(pdf_bytes).decode()
        
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="patient_report.pdf">Download Report as PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
        
if __name__ == '__main__':
    display()
