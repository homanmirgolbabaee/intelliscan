import streamlit as st

def display():
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
