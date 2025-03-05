import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Function to generate mock software contract data
def generate_mock_software_contract_data():
    software_types = ['PowerBI', 'Excel', 'Azure', 'Dynamics', 'Teams', 'SharePoint']
    license_levels = ['Basic', 'Professional', 'Enterprise', 'Premium']
    deployment_types = ['Cloud', 'On-Premise', 'Hybrid']
    support_levels = ['Basic', 'Standard', 'Premium']
    complexity_levels = ['Low', 'Medium', 'High']
    
    data = []
    np.random.seed(42)
    
    for _ in range(500):  # Increased data points for more robust analysis
        entry = {
            'Software': np.random.choice(software_types),
            'License Level': np.random.choice(license_levels),
            'Deployment Type': np.random.choice(deployment_types),
            'User Count': np.random.randint(10, 1000),
            'Annual Cost': np.random.uniform(5000, 250000),
            'Contract Duration (Years)': np.random.choice([1, 2, 3, 5]),
            'Support Level': np.random.choice(support_levels),
            'Implementation Complexity': np.random.choice(complexity_levels)
        }
        data.append(entry)
    
    return pd.DataFrame(data)

# Main Streamlit App
def main():
    st.set_page_config(layout="wide")
    st.title('Microsoft Software Contract Analysis Dashboard')
    
    # Generate mock data
    df = generate_mock_software_contract_data()
    
    # Create columns for filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        software_filter = st.multiselect(
            'Select Software', 
            options=df['Software'].unique(),
            default=df['Software'].unique(),
            key='software_select'
        )
    
    with col2:
        license_filter = st.multiselect(
            'Select License Level', 
            options=df['License Level'].unique(),
            default=df['License Level'].unique(),
            key='license_select'
        )
    
    with col3:
        deployment_filter = st.multiselect(
            'Select Deployment Type', 
            options=df['Deployment Type'].unique(),
            default=df['Deployment Type'].unique(),
            key='deployment_select'
        )
    
    with col4:
        support_filter = st.multiselect(
            'Select Support Level', 
            options=df['Support Level'].unique(),
            default=df['Support Level'].unique(),
            key='support_select'
        )
    
    # Apply filters
    filtered_df = df[
        df['Software'].isin(software_filter) & 
        df['License Level'].isin(license_filter) & 
        df['Deployment Type'].isin(deployment_filter) & 
        df['Support Level'].isin(support_filter)
    ]
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(['Pivot Analysis', 'Visualizations', 'Detailed Data'])
    
    with tab1:
        st.header('Pivot Table Analysis')
        
        # Pivot Table Configuration
        pivot_columns = st.multiselect(
            'Select Columns for Pivot', 
            options=['Software', 'License Level', 'Deployment Type', 'Support Level'],
            default=['Software', 'License Level'],
            key='pivot_columns'
        )
        
        pivot_values = st.selectbox(
            'Select Value for Aggregation', 
            options=['Annual Cost', 'User Count', 'Contract Duration (Years)'],
            key='pivot_values'
        )
        
        # Error handling for pivot table
        try:
            pivot_table = filtered_df.pivot_table(
                values=pivot_values, 
                index=pivot_columns, 
                aggfunc=['mean', 'sum', 'count']
            )
            
            st.dataframe(pivot_table)
        except Exception as e:
            st.error(f"Error creating pivot table: {e}")
    
    with tab2:
        st.header('Data Visualizations')
        
        # Create visualization columns
        vis_col1, vis_col2 = st.columns(2)
        
        with vis_col1:
            # Cost Distribution by Software
            plt.figure(figsize=(10, 6))
            sns.boxplot(x='Software', y='Annual Cost', data=filtered_df)
            plt.title('Annual Cost Distribution by Software')
            plt.xticks(rotation=45)
            st.pyplot(plt)
            plt.close()
        
        with vis_col2:
            # Deployment Type Distribution
            plt.figure(figsize=(8, 6))
            deployment_counts = filtered_df['Deployment Type'].value_counts()
            plt.pie(deployment_counts, labels=deployment_counts.index, autopct='%1.1f%%')
            plt.title('Deployment Type Distribution')
            st.pyplot(plt)
            plt.close()
        
        # Heatmap
        plt.figure(figsize=(12, 6))
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
    
    with tab3:
        st.header('Detailed Contract Data')
        st.dataframe(filtered_df)
        
        # Summary Statistics
        st.subheader('Summary Statistics')
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            st.metric("Total Contracts", len(filtered_df))
            st.metric("Average Annual Cost", f"${filtered_df['Annual Cost'].mean():,.2f}")
        
        with col_stats2:
            st.metric("Total Users", filtered_df['User Count'].sum())
            st.metric("Average Contract Duration", f"{filtered_df['Contract Duration (Years)'].mean():.2f} Years")

if __name__ == '__main__':
    main()
