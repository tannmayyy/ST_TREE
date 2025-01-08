import pandas as pd
import streamlit as st
from streamlit_antd_components import condition_tree

# Load CSV configuration
df_config = pd.read_csv("source_mapping.csv")  # Adjust the path as needed

# Example DataFrame for demo (replace with actual data from Snowflake)
# df = pd.read_sql("SELECT * FROM your_table", conn)

# Step 1: Identify columns that need dropdown or text input
column_filters = {row['Datamart Columns']: 'dropdown' if row['Listed'].lower() == 'yes' else 'text'
                  for _, row in df_config.iterrows()}

# Step 2: Select columns to filter
filter_columns = st.multiselect("Select Filters", column_filters.keys())

# Step 3: Prepare configuration for condition_tree
config_data = []
for column in filter_columns:
    filter_type = column_filters[column]
    if filter_type == 'dropdown':
        unique_values = df[column].dropna().unique()  # Get unique values from the column
        config_data.append({'column': column, 'filter_type': 'dropdown', 'options': unique_values})
    else:
        config_data.append({'column': column, 'filter_type': 'text'})

# Step 4: Generate condition tree and SQL query
condition_tree_query = condition_tree(
    config=config_data,
    return_type='sql',
    placeholder="Add Filters",
    always_show_buttons=True
)

# Step 5: Display generated SQL query
if condition_tree_query:
    sql_query = f"SELECT * FROM your_table WHERE {condition_tree_query} LIMIT 1000"
    st.write("Generated SQL Query:")
    st.code(sql_query)
