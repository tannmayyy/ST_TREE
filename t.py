import streamlit as st
import pandas as pd
import snowflake.connector
from streamlit_condition_tree import condition_tree, config_from_dataframe

# Load the CSV file
csv_file = "OBI Trades View Source Mapping.xlsx"
df = pd.read_excel(csv_file)

# Snowflake connection (replace with your credentials)
conn = snowflake.connector.connect(
    user="your_user",
    password="your_password",
    account="your_account",
    warehouse="your_warehouse",
    database="your_database",
    schema="your_schema",
)

# Function to fetch unique values from Snowflake for a column
def get_unique_values(selected_table, column_name):
    query = f"SELECT DISTINCT {column_name} FROM {selected_table} LIMIT 1000"
    try:
        unique_df = pd.read_sql(query, conn)
        return unique_df[column_name].dropna().unique().tolist()
    except Exception as e:
        st.warning(f"Error fetching unique values: {str(e)}")
        return []

# Prepare the configuration for Condition Tree
def prepare_config(selected_columns):
    config_dict = {}
    for col in selected_columns:
        # Check if the column is listed
        listed_value = df.loc[df["Datamart Columns"] == col, "Listed"].values[0]
        if listed_value.lower() == "yes":
            # Fetch unique values for dropdown
            unique_values = get_unique_values("configdata", col)
            config_dict[col] = {"type": "dropdown", "options": unique_values}
        else:
            # Provide an empty text input field
            config_dict[col] = {"type": "text", "placeholder": f"Enter value for {col}"}
    return config_dict

# Sidebar for category and datamart columns
categories = df.groupby("Category")["Datamart Columns"].apply(list).to_dict()
with st.sidebar:
    category_tree_items = [
        sac.TreeItem(category, children=[sac.TreeItem(column) for column in columns])
        for category, columns in categories.items()
    ]
    selected_columns = sac.tree(
        items=category_tree_items,
        label="Select Features",
        open_all=False,
        checkbox=True,
    )

# Display Condition Tree if columns are selected
if selected_columns:
    st.subheader("Add Filters")
    # Prepare config based on the selected columns
    config = prepare_config(selected_columns)
    # Generate condition tree query
    condition_tree_query = condition_tree(
        config,
        return_type="sql",
        always_show_buttons=True,
        placeholder="Add Filters",
    )
    st.write("Generated SQL Query:")
    st.code(condition_tree_query)
