import pandas as pd
import streamlit as st
from streamlit_condition_tree import condition_tree, config_from_dataframe

# Sample DataFrame (replace this with actual data)
df = pd.DataFrame({
    'BUSINESS DATE': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01']),
    'TRADE DATE': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01']),
    'T_PLUS FLAG': ['Y', 'N', 'Y'],
    'VALUE DATE': pd.to_datetime(['2021-01-02', '2021-02-02', '2021-03-02']),
    'MATURITY_DATE': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01']),
    'ENTRY DATETIME': pd.to_datetime(['2021-01-01 12:00:00', '2021-02-01 12:00:00', '2021-03-01 12:00:00']),
    'CREATED_DATE': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01']),
    'PARENT TRADE ID': [101, 102, 103],
    'TRADE_ID': [201, 202, 203],
    'VERSION_ID': [301, 302, 303],
    'OTHER ID': [401, 402, 403],
    'SOURCE SYSTEM REF': ['SS1', 'SS2', 'SS3'],
    'EXTERNAL TRADE REF': ['EXT1', 'EXT2', 'EXT3'],
    'LIDK_ID': ['LID1', 'LID2', 'LID3']
})

# Define the columns that should use a dropdown (yes_columns) and those that won't (no_columns)
yes_columns = ["BUSINESS DATE", "TRADE DATE", "T_PLUS FLAG", "VALUE DATE", "MATURITY_DATE", "ENTRY DATETIME", "CREATED_DATE"]
no_columns = ["PARENT TRADE ID", "TRADE_ID", "VERSION_ID", "OTHER ID", "SOURCE SYSTEM REF", "EXTERNAL TRADE REF", "LIDK_ID"]

# Step 1: User selects the filter columns
filter_columns = st.multiselect("Select Filters", df.columns)

# Step 2: Prepare the condition tree configuration based on the selected filter columns
config_data = []

# Generate config based on selected filter columns
for column in filter_columns:
    if column in yes_columns:
        # For 'yes_columns', we provide a dropdown with unique values
        config_data.append({
            'label': column,
            'type': 'select',  # Dropdown for these columns
            'fieldSettings': {
                'listValues': df[column].dropna().unique().tolist()  # Unique values for the dropdown
            }
        })
    elif column in no_columns:
        # For 'no_columns', provide a text input (optional as per your case)
        config_data.append({
            'label': column,
            'type': 'text',  # Text input for these columns
            'mainWidgetProps': {
                'valuePlaceholder': 'Enter value'
            }
        })

# Step 3: Create the condition tree using the config data
if filter_columns:  # Ensure that filters are selected before proceeding
    condition_tree_query = condition_tree(
        config=config_data,
        return_type='sql',  # Generate SQL query from the condition tree
        always_show_buttons=True,
        placeholder="Add Filters"
    )

    # Step 4: Display the generated SQL query
    if condition_tree_query:
        sql_query = f"SELECT {', '.join(filter_columns)} FROM view_dt_test_1 WHERE {condition_tree_query}"
        st.write("Generated SQL Query:")
        st.code(sql_query)

        # Step 5: Optionally, filter the dataframe using the generated SQL query
        try:
            filtered_df = df.query(condition_tree_query)
            st.subheader("Filtered DataFrame")
            st.dataframe(filtered_df)
        except Exception as e:
            st.write(f"Error while filtering the DataFrame: {e}")
else:
    st.write("Please select filters to proceed.")
