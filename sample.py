import streamlit as st
import pandas as pd

# Mock software taxonomy (simplified for visualization)
software_taxonomy = {
}

# Mock software classification output
classification_output = {
    "Virtual Machines": ["Cloud Services", "IaaS", "Compute", "Virtual Machines"],
    "Managed SQL": ["Cloud Services", "PaaS", "Databases", "Managed SQL"],
    "Payroll": ["Software Applications", "ERP", "Human Resources", "Payroll"],
    "Email Campaigns": ["Software Applications", "CRM", "Marketing", "Email Campaigns"],
}

# Streamlit UI
st.set_page_config(layout="wide")
st.title("Document Analysis and Taxonomy")

# Chat History Section
chat_history = [
    {
        "id": 1,
        "timestamp": "2025-03-02 10:00",
        "user_prompt": "Extract the contract term and payment terms from the document.",
        "system_response": "Contract Term: 12 months from effective date.\nPayment Terms: Net 30 days from invoice.",
        "citations": ["[2023, 3, 5-8]", "[2023, 4, 12-15]"],
    },
    {
        "id": 2,
        "timestamp": "2025-03-02 10:05",
        "user_prompt": "What is the total contract value and any applicable discounts?",
        "system_response": "Total Contract Value: $100,000.\nDiscount: 10% discount on orders over $50,000.",
        "citations": ["[2023, 6, 2-4]", "[2023, 7, 9-11]"],
    },
]

st.header("Chat History")
for event in chat_history:
    with st.expander(f"Query #{event['id']} ({event['timestamp']})"):
        st.markdown(f"**User Prompt:** {event['user_prompt']}")
        st.markdown(f"**System Response:** {event['system_response']}")
        st.markdown(f"**Citations:** {', '.join(event['citations'])}")

# Subtle Toggle Control
view_mode = st.radio("View Mode:", ("Tree View", "Table View"), horizontal=True)

st.header("Extracted Software Taxonomy")
st.write("Identified software components and their classifications:")

if view_mode == "Tree View":
    for product, taxonomy_path in classification_output.items():
        st.subheader(product)
        level1, level2, level3, level4 = taxonomy_path
        st.markdown(f"<ul><li><b>{level1}</b><ul><li><b>{level2}</b><ul><li><b>{level3}</b><ul><li>{level4}</li></ul></li></ul></li></ul>", unsafe_allow_html=True)
else:
    # Convert taxonomy to a structured DataFrame for Table View
    data = []
    for product, path in classification_output.items():
        data.append([product] + path)
    df = pd.DataFrame(data, columns=["Product", "Category", "Subcategory", "Type", "Detail"])
    st.dataframe(df, use_container_width=True)
