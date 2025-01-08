import streamlit as st
import pandas as pd
import snowflake.connector
from streamlit_condition_tree import condition_tree
from streamlit_antd_components import TreeItem

def preview_filtered_data(selected_table):
    sql_query = ""

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=
    )

    # Query Snowflake
    sql_query = f"SELECT * FROM OBI.MISDBO.{selected_table} LIMIT 25"
    df = pd.read_sql(sql_query, conn)

    # Convert columns to categorical for unique values
    for col in df.columns:
        df[col] = pd.Categorical(df[col])

    # Sidebar: Load CSV file
    with st.sidebar:
        csv_file = "C:/Users/choudhta/streamlit/Source_mapping.csv"
        source_df = pd.read_csv(csv_file)

        # Group by categories
        categories = (
            source_df.groupby("Category")["Datamart Columns"]
            .apply(list)
            .to_dict()
        )

        # Create a tree structure
        category_tree_items = [
            TreeItem(category, children=[TreeItem(column) for column in columns])
            for category, columns in categories.items()
        ]

        # Display the tree structure
        selected_columns = st.tree(
            items=category_tree_items,
            label="Select Features",
            open_all=False,
            checkbox=True,
        )

    # If columns are selected
    if selected_columns:
        cols = st.columns(len(selected_columns))
        st.write("Selected Columns:", selected_columns)

        for i, column in enumerate(selected_columns):
            with cols[i]:
                st.metric(
                    label=f"{column}",
                    value=f"Unique count: {df[column].nunique()}",
                    delta=None,
                )

    # Multiselect for filters
    filter_columns = st.multiselect("Select Filters", source_df["Datamart Columns"])
    st.write("Filters Selected:", filter_columns)

    # Prepare config for condition_tree
    try:
        config = {col: {"type": "dropdown", "options": df[col].unique().tolist()} for col in filter_columns}
    except KeyError as e:
        st.warning("A selected column is not found in the data. Please check the column name.")

    # Render condition tree
    condition_tree_query = condition_tree(
        config,
        return_type="sql",
        placeholder="Add Filters",
        always_show_buttons=True,
    )

    # Generate the SQL query
    sql_query = f"SELECT {', '.join(selected_columns)} FROM {selected_table}"
    if condition_tree_query:
        sql_query += f" WHERE {condition_tree_query} LIMIT 100000"

    st.write("Generated SQL Query:")
    st.code(sql_query)

    return selected_columns, sql_query
