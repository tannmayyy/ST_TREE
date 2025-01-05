import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# Load your CSV file
csv_file = "path_to_your_csv_file.csv"  # Replace with your file path
df = pd.read_csv(csv_file)

# Group the DataFrame by category and get the datamart columns for each category
categories = df.groupby("category")["datamart"].apply(list).to_dict()

with st.sidebar:
    # Create TreeItems for each category and its associated datamart columns
    category_tree_items = [
        sac.TreeItem(category, children=[sac.TreeItem(column) for column in columns])
        for category, columns in categories.items()
    ]

    # Display the tree structure in the sidebar
    selected_columns = sac.tree(
        items=category_tree_items,
        label="Select Features",
        open_all=False,
        checkbox=True,
    )

# Display selected columns (optional)
if selected_columns:
    st.write("Selected Columns:", selected_columns)
