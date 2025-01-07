import streamlit as st
import pandas as pd
import snowflake.connector
from streamlit_antd_components import config_from_dataframe, condition_tree

# Snowflake connection details
SNOWFLAKE_ACCOUNT = "your_account"
SNOWFLAKE_USER = "your_username"
SNOWFLAKE_PASSWORD = "your_password"
SNOWFLAKE_WAREHOUSE = "your_warehouse"
SNOWFLAKE_DATABASE = "your_database"
SNOWFLAKE_SCHEMA = "your_schema"
SNOWFLAKE_TABLE = "your_table"

# Function to fetch unique values for a selected column
def fetch_unique_values_from_snowflake(column_name):
    ctx = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    query = f"SELECT DISTINCT {column_name} FROM {SNOWFLAKE_TABLE}"
    result = ctx.cursor().execute(query).fetchall()
    ctx.close()
    return [row[0] for row in result]  # Extract unique values

# Load your CSV file
csv_file = "path_to_your_csv_file.csv"  # Replace with your file path
df = pd.read_csv(csv_file)

# Get unique datamart column names from the CSV
datamart_columns = df["Datamart Columns"].unique()

# Multiselect widget for column selection
filter_columns = st.multiselect("Select Filters", options=datamart_columns)

# Fetch unique values from Snowflake for the selected column
if filter_columns:
    selected_column = filter_columns[0]  # Assume single selection for simplicity
    unique_values = fetch_unique_values_from_snowflake(selected_column)
    
    # Display unique values in a dropdown or other widget
    selected_value = st.selectbox(f"Unique values for {selected_column}", options=unique_values)
    
    # Display the selected value
    if selected_value:
        st.write(f"You selected: {selected_value}")
    
    # Optionally build SQL query with selected value
    sql_query = f"SELECT * FROM {SNOWFLAKE_TABLE} WHERE {selected_column} = '{selected_value}'"
    st.code(sql_query, language="sql")
