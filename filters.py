# Ensure 'Date' column is properly parsed
data["Date"] = pd.to_datetime(data["Date"], errors='coerce')

st.title("Tableau-Style Dynamic Filters")

# Sidebar for Filters
st.sidebar.header("Filters")

filters = {}

for col in data.columns:
    st.sidebar.markdown(f"**{col}**")  # Display column header
    
    if data[col].dtype == "object":  # Text columns
        unique_values = sorted(data[col].dropna().unique().tolist())
        unique_values.insert(0, "All")  # Add "All" option
        selected_values = st.sidebar.multiselect(f"Select {col}", unique_values, default="All")
        filters[col] = unique_values[1:] if "All" in selected_values else selected_values
    
    elif pd.api.types.is_numeric_dtype(data[col]):  # Numeric columns
        min_val, max_val = int(data[col].min()), int(data[col].max())
        filters[col] = st.sidebar.slider(f"Select {col} Range", min_val, max_val, (min_val, max_val))
    
    elif pd.api.types.is_datetime64_any_dtype(data[col]):  # Date columns
        if data[col].notna().sum() > 0:  # Ensure valid dates exist
            min_date, max_date = data[col].min().date(), data[col].max().date()
            date_range = st.sidebar.date_input(f"Select {col} Range", [min_date, max_date])
            
            # Convert Python date to Pandas timestamp to avoid comparison errors
            filters[col] = [pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])] if isinstance(date_range, list) and len(date_range) == 2 else None

# Apply Filters
filtered_data = data.copy()

for col, value in filters.items():
    if col in data.columns and pd.api.types.is_datetime64_any_dtype(data[col]) and value is not None:  # Date range filter
        filtered_data = filtered_data[
            (filtered_data[col] >= value[0]) & (filtered_data[col] <= value[1])
        ]
    elif isinstance(value, tuple):  # Numeric slider range
        filtered_data = filtered_data[
            (filtered_data[col] >= value[0]) & 
            (filtered_data[col] <= value[1])
        ]
    elif isinstance(value, list) and data[col].dtype == "object":  # Multi-select text filter
        filtered_data = filtered_data[filtered_data[col].isin(value)]
