import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Function to generate mock software contract data
def generate_mock_software_contract_data():
    software_types = ['PowerBI', 'Excel', 'Azure', 'Dynamics', 'Teams']
    license_levels = ['Basic', 'Professional', 'Enterprise', 'Premium']
    deployment_types = ['Cloud', 'On-Premise', 'Hybrid']
    support_levels = ['Basic', 'Standard', 'Premium']
    
    data = []
    np.random.seed(42)
    
    for _ in range(200):
        entry = {
            'Software': np.random.choice(software_types),
            'License Level': np.random.choice(license_levels),
            'Deployment Type': np.random.choice(deployment_types),
            'Support Level': np.random.choice(support_levels),
            'User Count': np.random.randint(10, 1000),
            'Annual Cost': np.random.uniform(5000, 250000),
            'Contract Duration (Years)': np.random.choice([1, 2, 3, 5])
        }
        data.append(entry)
    
    return pd.DataFrame(data)

# Load Data
df = generate_mock_software_contract_data()

# Initialize session state for drill-down levels
if "selected_level" not in st.session_state:
    st.session_state.selected_level = None
if "selected_values" not in st.session_state:
    st.session_state.selected_values = {}

# Function to reset drill-down
def reset_drill():
    st.session_state.selected_level = None
    st.session_state.selected_values = {}

# Back button logic
if st.session_state.selected_level:
    if st.button("🔙 Back"):
        levels = list(st.session_state.selected_values.keys())
        if levels:
            st.session_state.selected_values.pop(levels[-1])
            if not st.session_state.selected_values:
                st.session_state.selected_level = None
        st.rerun()

# Title
st.title("🔍 Clickable 4-Level Drill-Down: Software Contracts")

# Determine the current drill-down level
if not st.session_state.selected_level:
    current_level = "Software"
    data_to_plot = df
elif "Software" in st.session_state.selected_values and "License Level" not in st.session_state.selected_values:
    current_level = "License Level"
    data_to_plot = df[df["Software"] == st.session_state.selected_values["Software"]]
elif "License Level" in st.session_state.selected_values and "Deployment Type" not in st.session_state.selected_values:
    current_level = "Deployment Type"
    data_to_plot = df[
        (df["Software"] == st.session_state.selected_values["Software"]) & 
        (df["License Level"] == st.session_state.selected_values["License Level"])
    ]
elif "Deployment Type" in st.session_state.selected_values and "Support Level" not in st.session_state.selected_values:
    current_level = "Support Level"
    data_to_plot = df[
        (df["Software"] == st.session_state.selected_values["Software"]) & 
        (df["License Level"] == st.session_state.selected_values["License Level"]) & 
        (df["Deployment Type"] == st.session_state.selected_values["Deployment Type"])
    ]
else:
    current_level = "Final"
    data_to_plot = df[
        (df["Software"] == st.session_state.selected_values["Software"]) & 
        (df["License Level"] == st.session_state.selected_values["License Level"]) & 
        (df["Deployment Type"] == st.session_state.selected_values["Deployment Type"]) & 
        (df["Support Level"] == st.session_state.selected_values["Support Level"])
    ]

# Plot the relevant data
if current_level == "Final":
    st.subheader(f"Final Level: Annual Cost Distribution for {st.session_state.selected_values}")
    fig = px.histogram(data_to_plot, x="Annual Cost", nbins=20, title="Final Annual Cost Distribution")
else:
    st.subheader(f"Click to Drill Down: {current_level}")
    fig = px.box(data_to_plot, x=current_level, y="Annual Cost", title=f"Annual Cost by {current_level}")

    # Enable click events
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig)

    # Capture Click Events
    click_data = st.session_state.get("click_data", None)
    if click_data:
        selected_value = click_data["points"][0]["x"]
        st.session_state.selected_values[current_level] = selected_value

        # Determine the next level
        levels_order = ["Software", "License Level", "Deployment Type", "Support Level"]
        current_index = levels_order.index(current_level)
        if current_index < len(levels_order) - 1:
            st.session_state.selected_level = levels_order[current_index + 1]

        st.rerun()
