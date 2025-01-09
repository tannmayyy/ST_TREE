import pandas as pd
import streamlit as st
from streamlit_condition_tree import condition_tree, config_from_dataframe

# Sample DataFrame
df = pd.DataFrame({
    'BUSINESS DATE': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01']),
    'TRADE DATE': pd.to_datetime(['2021-01-02', '2021-02-02', '2021-03-02']),
    'VALUE DATE': pd.to_datetime(['2021-01-03', '2021-02-03', '2021-03-03']),
    'PRICE': [100, 200, 300],
    'CITY': ['New York', 'Los Angeles', 'Chicago']
})

# Manually define columns based on 'Yes' or 'No'
yes_columns = ['BUSINESS DATE', 'TRADE DATE', 'VALUE DATE']
no_columns = ['PRICE', 'CITY']

# Step 1: Select columns for filtering
filter_columns = st.multiselect("Select Filters", df.columns)

# Step 2: Prepare the config for the condition tree
config_data = []
for column in filter_columns:
    if column in yes_columns:
        config_data.append({
            'label': column,
            'type': 'select',  # Dropdown for these columns
            'fieldSettings': {
                'listValues': df[column].dropna().unique().tolist()  # Automatically fill dropdown with unique values
            }
        })
    elif column in no_columns:
        config_data.append({
            'label': column,
            'type': 'text',  # Text input for these columns
            'mainWidgetProps': {
                'valuePlaceholder': 'Enter value'
            }
        })

# Step 3: Use the updated config_data with the condition_tree function
if filter_columns:  # Check if any filters are selected
    condition_tree_query = condition_tree(
        config=config_data,  # Using config_data here
        return_type='sql',
        placeholder="Add Filters",
        always_show_buttons=True
    )

    # Step 4: Display the generated SQL query
    if condition_tree_query:
        sql_query = f"SELECT * FROM your_table WHERE {condition_tree_query} LIMIT 1000"
        st.write("Generated SQL Query:")
        st.code(sql_query)
else:
    st.write("Please select filters to proceed.")
