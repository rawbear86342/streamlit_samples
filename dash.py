import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Function to generate mock software contract data
def generate_mock_software_contract_data():
    software_types = ['PowerBI', 'Excel', 'Azure', 'Dynamics', 'Teams']
    license_levels = ['Basic', 'Professional', 'Enterprise', 'Premium']
    deployment_types = ['Cloud', 'On-Premise', 'Hybrid']
    
    data = []
    np.random.seed(42)
    
    for _ in range(200):
        entry = {
            'Software': np.random.choice(software_types),
            'License Level': np.random.choice(license_levels),
            'Deployment Type': np.random.choice(deployment_types),
            'User Count': np.random.randint(10, 1000),
            'Annual Cost': np.random.uniform(5000, 250000),
            'Contract Duration (Years)': np.random.choice([1, 2, 3, 5]),
            'Support Level': np.random.choice(['Basic', 'Standard', 'Premium']),
            'Implementation Complexity': np.random.choice(['Low', 'Medium', 'High'])
        }
        data.append(entry)
    
    return pd.DataFrame(data)

# Main Streamlit App
def main():
    st.title('Software Contract Analysis Dashboard')
    
    # Generate mock data
    df = generate_mock_software_contract_data()
    
    # Sidebar for Filtering
    st.sidebar.header('Filter Options')
    
    # Multiselect filters
    software_filter = st.sidebar.multiselect(
        'Select Software', 
        options=df['Software'].unique(),
        default=df['Software'].unique()
    )
    
    license_filter = st.sidebar.multiselect(
        'Select License Level', 
        options=df['License Level'].unique(),
        default=df['License Level'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        df['Software'].isin(software_filter) & 
        df['License Level'].isin(license_filter)
    ]
    
    # Pivot Table
    st.header('Interactive Pivot Table')
    
    # Available columns for pivoting
    pivot_columns_options = ['Software', 'License Level', 'Deployment Type', 'Support Level']
    
    # Prevent empty selection
    pivot_columns = st.multiselect(
        'Select Columns for Pivot', 
        options=pivot_columns_options,
        default=['Software']  # Default to at least one column
    )
    
    pivot_values = st.selectbox(
        'Select Value for Aggregation', 
        options=['Annual Cost', 'User Count', 'Contract Duration (Years)']
    )
    
    # Error handling for pivot table
    try:
        # Fallback to a default if no columns selected
        if not pivot_columns:
            pivot_columns = ['Software']
        
        pivot_table = filtered_df.pivot_table(
            values=pivot_values, 
            index=pivot_columns, 
            aggfunc=['mean', 'sum', 'count']
        )
        
        # Check if pivot table is empty
        if pivot_table.empty:
            st.warning("No data available for the selected filters.")
        else:
            st.dataframe(pivot_table)
    
    except Exception as e:
        st.error(f"Error creating pivot table: {e}")
        st.error("Please select at least one column for pivoting.")
    
    # Visualization Section
    st.header('Data Visualizations')
    
    # Ensure we have data for visualization
    if len(filtered_df) > 0:
        # Cost Distribution by Software
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Software', y='Annual Cost', data=filtered_df)
        plt.title('Annual Cost Distribution by Software')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        plt.close()
        
        # User Count Heatmap
        plt.figure(figsize=(10, 6))
        try:
            user_pivot = filtered_df.pivot_table(
                values='User Count', 
                index='License Level', 
                columns='Deployment Type', 
                aggfunc='mean'
            )
            sns.heatmap(user_pivot, annot=True, cmap='YlGnBu')
            plt.title('Average User Count by License and Deployment')
            st.pyplot(plt)
            plt.close()
        except Exception as e:
            st.error(f"Could not create heatmap: {e}")
        
        # Deployment Type Distribution
        plt.figure(figsize=(8, 6))
        deployment_counts = filtered_df['Deployment Type'].value_counts()
        plt.pie(deployment_counts, labels=deployment_counts.index, autopct='%1.1f%%')
        plt.title('Deployment Type Distribution')
        st.pyplot(plt)
        plt.close()
    else:
        st.warning("No data available for visualization after filtering.")

if __name__ == '__main__':
    main()
