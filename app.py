import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

import json
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration to wide mode
st.set_page_config(layout="wide")
# Custom CSS for controlling sidebar width
st.markdown(
    """
    
    <style>
        [data-testid="stSidebar"] {
            min-width: 300px;  /* Adjust this value */
            max-width: 350px;
        }
    
    * Style for menu tab */
    div[data-baseweb="tab-list"] button {
        font-size: 22px !important; /* Larger font size */
        font-weight: bold !important;
        padding: 12px 24px !important; /* Better spacing */
        border: none !important;
        background-color: #f8f9fa !important; /* Subtle background */
        color: #333 !important; /* Darker text for contrast */
        border-radius: 8px 8px 0 0 !important; /* Rounded top corners */
    }
    
    /* Active tab styling */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.9) !important; /* Subtle white for active tab */
        border-bottom: 3px solid #007BFF !important; /* Highlight active tab */
    }
    
    /* Style for contract details panel */
    .contract-details {
        font-size: 18px !important;
        background: white !important;
        padding: 20px !important;
        border-radius: 8px !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
        margin-top: -2px !important; /* Seamless connection with tabs */
    }
    
    
    
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
    <style>
        .top-bar {
            background-color: #1E1E2E;
            padding: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
        }
        .top-bar img {
            height: 40px;
        }
        .top-bar h1 {
            color: white;
            font-size: 20px;
            margin: 0;
            padding-left: 10px;
        }
    </style>
    <div class="top-bar">
        <img src="https://via.placeholder.com/100x40" alt="AI Contracts">
        <h1>AI Contract Manager</h1>
    </div>
    <br><br><br>  <!-- Add spacing so content doesn't get hidden under the fixed bar -->
""", unsafe_allow_html=True)

# Contract data as a single inline JSON payload
contract_data_json = '''
{
  "contracts": [
    {
      "Contract ID": "C-0",
      "Client Name": "Alpha Corp",
      "Contract Amount ($)": 50000,
      "Status": "Active",
      "Priority": "High",
      "Contract Type": "Service",
      "Department": "Legal",
      "Start Date": "2024-01-01",
      "End Date": "2025-01-01",
      "Last Modified": "2024-01-25",
      "Signed By": "J. Smith",
      "Description": "This contract agreement outlines the terms and conditions between the two parties involved. The agreement is binding and subject to the laws of the state.",
      "Timeline": [
        {"date": "2024-01-15", "event": "Contract created by J. Smith"},
        {"date": "2024-01-20", "event": "Contract reviewed by Legal Department"},
        {"date": "2024-01-25", "event": "Contract sent to client for approval"},
        {"date": "2024-01-30", "event": "Contract signed by all parties"}
      ]
    },
    {
      "Contract ID": "C-1",
      "Client Name": "Beta Ltd",
      "Contract Amount ($)": 120000,
      "Status": "Pending",
      "Priority": "Critical",
      "Contract Type": "Licensing",
      "Department": "Finance",
      "Start Date": "2024-02-15",
      "End Date": "2025-02-15",
      "Last Modified": "2024-02-10",
      "Signed By": "A. Johnson",
      "Description": "The parties agree to the stipulated payment terms and delivery conditions. Any disputes arising shall be resolved through arbitration.",
      "Timeline": [
        {"date": "2024-02-01", "event": "Contract created by A. Johnson"},
        {"date": "2024-02-05", "event": "Contract reviewed by Finance Department"},
        {"date": "2024-02-08", "event": "Contract sent to client for approval"},
        {"date": "2024-02-10", "event": "Awaiting client signature"}
      ]
    },
    {
      "Contract ID": "C-2",
      "Client Name": "Gamma Inc",
      "Contract Amount ($)": 75000,
      "Status": "Under Review",
      "Priority": "Medium",
      "Contract Type": "Partnership",
      "Department": "Operations",
      "Start Date": "2024-03-10",
      "End Date": "2025-03-10",
      "Last Modified": "2024-03-05",
      "Signed By": "M. Williams",
      "Description": "Confidentiality clauses apply to all aspects of this contract. Breach of confidentiality will result in penalties as per section 5.3 of this document.",
      "Timeline": [
        {"date": "2024-03-01", "event": "Contract created by M. Williams"},
        {"date": "2024-03-03", "event": "Contract submitted for internal review"},
        {"date": "2024-03-05", "event": "Revisions requested by legal team"},
        {"date": "2024-03-08", "event": "Currently under review"}
      ]
    },
    {
      "Contract ID": "C-3",
      "Client Name": "Delta LLC",
      "Contract Amount ($)": 98000,
      "Status": "Completed",
      "Priority": "Low",
      "Contract Type": "Employment",
      "Department": "HR",
      "Start Date": "2024-04-20",
      "End Date": "2025-04-20",
      "Last Modified": "2024-04-22",
      "Signed By": "R. Jones",
      "Description": "This employment contract outlines the responsibilities and compensation package for the specified role. All parties have agreed to the terms.",
      "Timeline": [
        {"date": "2024-04-10", "event": "Contract template created by HR"},
        {"date": "2024-04-15", "event": "Terms negotiated with candidate"},
        {"date": "2024-04-18", "event": "Final draft approved by management"},
        {"date": "2024-04-22", "event": "Contract signed by all parties"}
      ]
    },
    {
      "Contract ID": "C-4",
      "Client Name": "Epsilon Group",
      "Contract Amount ($)": 65000,
      "Status": "Renewed",
      "Priority": "Medium",
      "Contract Type": "Vendor",
      "Department": "IT",
      "Start Date": "2024-05-05",
      "End Date": "2025-05-05",
      "Last Modified": "2024-05-02",
      "Signed By": "D. Brown",
      "Description": "This vendor agreement includes service level agreements and performance metrics. The contract has been renewed for an additional year with updated terms.",
      "Timeline": [
        {"date": "2024-04-15", "event": "Renewal discussion initiated"},
        {"date": "2024-04-22", "event": "New terms proposed by vendor"},
        {"date": "2024-04-28", "event": "Terms negotiated and finalized"},
        {"date": "2024-05-02", "event": "Renewal contract signed"}
      ]
    },
    {
      "Contract ID": "C-5",
      "Client Name": "Zeta Systems",
      "Contract Amount ($)": 82000,
      "Status": "Active",
      "Priority": "High",
      "Contract Type": "Lease",
      "Department": "Marketing",
      "Start Date": "2024-06-12",
      "End Date": "2025-06-12",
      "Last Modified": "2024-06-15",
      "Signed By": "L. Davis",
      "Description": "This lease agreement covers the terms for equipment and space rental. The agreement includes maintenance and support provisions.",
      "Timeline": [
        {"date": "2024-06-01", "event": "Lease requirements specified"},
        {"date": "2024-06-08", "event": "Property inspection completed"},
        {"date": "2024-06-10", "event": "Terms negotiated with property owner"},
        {"date": "2024-06-15", "event": "Lease agreement finalized and signed"}
      ]
    },
    {
      "Contract ID": "C-6",
      "Client Name": "Eta Networks",
      "Contract Amount ($)": 110000,
      "Status": "Pending",
      "Priority": "Critical",
      "Contract Type": "Service",
      "Department": "Operations",
      "Start Date": "2024-07-08",
      "End Date": "2025-07-08",
      "Last Modified": "2024-07-05",
      "Signed By": "J. Smith",
      "Description": "This service contract outlines the maintenance and support requirements for network infrastructure. The contract is awaiting final approval.",
      "Timeline": [
        {"date": "2024-07-01", "event": "Service requirements documented"},
        {"date": "2024-07-03", "event": "Proposal received from service provider"},
        {"date": "2024-07-05", "event": "Contract draft created and reviewed"},
        {"date": "2024-07-07", "event": "Awaiting executive approval"}
      ]
    },
    {
      "Contract ID": "C-7",
      "Client Name": "Theta Digital",
      "Contract Amount ($)": 45000,
      "Status": "Active",
      "Priority": "Medium",
      "Contract Type": "Licensing",
      "Department": "Legal",
      "Start Date": "2024-08-22",
      "End Date": "2025-08-22",
      "Last Modified": "2024-08-25",
      "Signed By": "A. Johnson",
      "Description": "This licensing agreement covers the use of proprietary software and technology. The agreement includes usage limitations and support terms.",
      "Timeline": [
        {"date": "2024-08-10", "event": "Licensing requirements specified"},
        {"date": "2024-08-15", "event": "Terms proposed and negotiated"},
        {"date": "2024-08-20", "event": "Legal review completed"},
        {"date": "2024-08-25", "event": "Agreement signed by all parties"}
      ]
    },
    {
      "Contract ID": "C-8",
      "Client Name": "Iota Solutions",
      "Contract Amount ($)": 93000,
      "Status": "Under Review",
      "Priority": "High",
      "Contract Type": "Partnership",
      "Department": "Finance",
      "Start Date": "2024-09-15",
      "End Date": "2025-09-15",
      "Last Modified": "2024-09-10",
      "Signed By": "M. Williams",
      "Description": "This partnership agreement outlines the profit sharing and collaborative efforts between parties. Several clauses are currently under review.",
      "Timeline": [
        {"date": "2024-09-01", "event": "Partnership framework established"},
        {"date": "2024-09-05", "event": "Initial draft created"},
        {"date": "2024-09-08", "event": "Finance team identified concerns"},
        {"date": "2024-09-10", "event": "Revisions in progress"}
      ]
    },
    {
      "Contract ID": "C-9",
      "Client Name": "Kappa Tech",
      "Contract Amount ($)": 78000,
      "Status": "Completed",
      "Priority": "Low",
      "Contract Type": "Vendor",
      "Department": "IT",
      "Start Date": "2024-10-01",
      "End Date": "2025-10-01",
      "Last Modified": "2024-10-05",
      "Signed By": "R. Jones",
      "Description": "This vendor agreement specifies the delivery of IT hardware and implementation services. The contract has been fully executed.",
      "Timeline": [
        {"date": "2024-09-20", "event": "Vendor requirements specified"},
        {"date": "2024-09-25", "event": "Vendor selected after evaluation"},
        {"date": "2024-09-30", "event": "Contract terms negotiated"},
        {"date": "2024-10-05", "event": "Contract signed and implementation begun"}
      ]
    }
  ]
}
'''

# Parse the JSON data
contract_data = json.loads(contract_data_json)

# Initialize session state to store selection
if 'selected_contract_id' not in st.session_state:
    st.session_state.selected_contract_id = None

def show_contract_details(contract_id):
    st.session_state.selected_contract_id = contract_id

# Convert JSON to DataFrame for display
df = pd.DataFrame(contract_data["contracts"])

# Streamlit UI
st.title("Contract Management Dashboard")

# This sidebar content changes based on the active tab
with st.sidebar:
    if st.session_state.active_tab == "Contracts":
        st.write("### Filter Contracts")
        client_filter = st.text_input("Search Client", "")
        status_filter = st.selectbox("Status", ["All", "Active", "Pending", "Under Review", "Completed", "Renewed"])
        type_filter = st.selectbox("Contract Type", ["All", "Service", "Licensing", "Partnership", "Employment", "Vendor", "Lease"])
        min_amount, max_amount = st.slider("Contract Amount Range ($)", 0, 200000, (0, 200000))
        
        # Apply Sidebar Filters
        filtered_df = df[
            (df["Client Name"].str.contains(client_filter, case=False, na=False) if client_filter else True) &
            (df["Status"] == status_filter if status_filter != "All" else True) &
            (df["Contract Type"] == type_filter if type_filter != "All" else True) &
            (df["Contract Amount ($)"] >= min_amount) & (df["Contract Amount ($)"] <= max_amount)
        ]
    else:  # Data Insights tab
        st.write("### Data Insights Options")
        contracts_df = pd.json_normalize(contract_data['contracts'])

        # Sidebar Filters
        status_filter = st.sidebar.multiselect('Select Status', options=contracts_df['Status'].unique(), default=contracts_df['Status'].unique())
        department_filter = st.sidebar.multiselect('Select Department', options=contracts_df['Department'].unique(), default=contracts_df['Department'].unique())
        priority_filter = st.sidebar.multiselect('Select Priority', options=contracts_df['Priority'].unique(), default=contracts_df['Priority'].unique())

        # Apply filters to DataFrame
        filtered_df = contracts_df[
            contracts_df['Status'].isin(status_filter) &
            contracts_df['Department'].isin(department_filter) &
            contracts_df['Priority'].isin(priority_filter)
        ]

# Create tabs
tabs = st.tabs(["Contracts", "📊 Contract Data Insights"])
# Tab 1: Contract Management Grid View
with tabs[0]:
    # Create two columns for layout: contracts list on left, details on right
    left_col, right_col = st.columns([7, 4])
    with left_col:    
        # Display column headers
        header_cols = st.columns([1, 2.5, 1.5, 1.2, 1.2, 1.5, 1.5, 1])
        with header_cols[0]:
            st.write("**ID**")
        with header_cols[1]:
            st.write("**Client**")
        with header_cols[2]:
            st.write("**Amount**")
        with header_cols[3]:
            st.write("**Status**")
        with header_cols[4]:
            st.write("**Type**")
        with header_cols[5]:
            st.write("**Start Date**")
        with header_cols[6]:
            st.write("**End Date**")
        with header_cols[7]:
            st.write("")
        
        st.divider()
        
        # Display rows
        for i, row in df.iterrows():
            cols = st.columns([1, 2.5, 1.5, 1.2, 1.2, 1.5, 1.5, 1])
            with cols[0]:
                st.write(f"**{row['Contract ID']}**")
            with cols[1]:
                st.write(row['Client Name'])
            with cols[2]:
                st.write(f"${row['Contract Amount ($)']:,}")
            with cols[3]:
                # Color code the status
                status = row['Status']
                if status == "Active":
                    st.markdown(f"<span style='color:green'>{status}</span>", unsafe_allow_html=True)
                elif status == "Pending":
                    st.markdown(f"<span style='color:orange'>{status}</span>", unsafe_allow_html=True)
                elif status == "Under Review":
                    st.markdown(f"<span style='color:blue'>{status}</span>", unsafe_allow_html=True)
                elif status == "Completed":
                    st.markdown(f"<span style='color:gray'>{status}</span>", unsafe_allow_html=True)
                elif status == "Renewed":
                    st.markdown(f"<span style='color:purple'>{status}</span>", unsafe_allow_html=True)
                else:
                    st.write(status)
            with cols[4]:
                st.write(row['Contract Type'])
            with cols[5]:
                st.write(row['Start Date'])
            with cols[6]:
                st.write(row['End Date'])
            with cols[7]:
                st.button(f"...", key=f"btn_{row['Contract ID']}", 
                        on_click=show_contract_details, 
                        args=(row['Contract ID'],))
            st.divider()

    # Display selected contract details in the right column
    with right_col:
        st.write("### Selected Contract Details")
        if st.session_state.selected_contract_id:
            # Find the selected contract in the original JSON data
            selected_contract = next(
                (contract for contract in contract_data["contracts"] 
                if contract["Contract ID"] == st.session_state.selected_contract_id),
                None
            )
            
            if selected_contract:
                # Display contract header with status indicator
                status = selected_contract['Status']
                status_color = "green" if status == "Active" else "orange" if status == "Pending" else "blue" if status == "Under Review" else "gray" if status == "Completed" else "purple"
                st.markdown(f"<h3>{selected_contract['Contract ID']} - {selected_contract['Client Name']} <span style='color:{status_color}'>({status})</span></h3>", unsafe_allow_html=True)
                
                # Create three columns for key details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Contract Amount:**")
                    st.write(f"${selected_contract['Contract Amount ($)']:,}")
                    
                    st.write("**Department:**")
                    st.write(selected_contract['Department'])
                
                with col2:
                    st.write("**Start Date:**")
                    st.write(selected_contract['Start Date'])
                    
                    st.write("**Contract Type:**")
                    st.write(selected_contract['Contract Type'])
                
                with col3:
                    st.write("**End Date:**")
                    st.write(selected_contract['End Date'])
                    
                    st.write("**Priority:**")
                    priority = selected_contract['Priority']
                    priority_color = "red" if priority == "Critical" else "orange" if priority == "High" else "blue" if priority == "Medium" else "green"
                    st.markdown(f"<span style='color:{priority_color}'>{priority}</span>", unsafe_allow_html=True)
                
                # Additional metadata
                st.write("**Last Modified:**", selected_contract['Last Modified'])
                st.write("**Signed By:**", selected_contract['Signed By'])
                
                # Description section
                st.write("### Description")
                st.write(selected_contract['Description'])
                
                # Add action buttons
                #st.write("### Actions")
                #action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                #with action_col1:
                #    st.button("Edit Contract", key="edit_btn")
                #with action_col2:
                #    st.button("Download PDF", key="download_btn")
                #with action_col3:
                #    st.button("Renew Contract", key="renew_btn")
                #with action_col4:
                #    st.button("Archive", key="archive_btn")
                
                # Add a timeline section using the timeline data from JSON
                st.write("### Timeline")
                for event in selected_contract["Timeline"]:
                    st.write(f"**{event['date']}:** {event['event']}")

                if st.button("🚀 Publish Data"):
                    st.success(f"{selected_contract['Contract ID']}  has been published successfully!")

        else:
            st.info("Select a contract to view details")
with tabs[1]:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Contracts by Status
    sns.countplot(data=df, x="Status", ax=axes[0], palette="Set2")
    axes[0].set_title("Contracts by Status")

    # Contract Amount by Department
    sns.barplot(data=df, x="Department", y="Contract Amount ($)", ax=axes[1], palette="Blues")
    axes[1].set_title("Contract Amount by Department")

    # Priority Distribution
    sns.countplot(data=df, x="Priority", ax=axes[2], palette="coolwarm")
    axes[2].set_title("Priority Distribution")

    st.pyplot(fig)
