import streamlit as st

# Define category mappings with new names
categories = {
    "Customer Info": ["Customer_ID", "Customer_Name"],
    "Transaction Details": ["Transaction_ID", "Order_ID", "Payment_Mode", "Invoice_No"],
    "Product Data": ["Product_ID", "Category", "Sub_Category", "Brand", "Description"],
    "Financial Records": ["Account_No", "Balance", "Credit_Score"],
    "Company Profiles": ["Company_ID", "Company_Name", "Sector"],
    "Employee Data": ["Employee_ID", "User_Name", "Role", "Department"],
    "Vendor Details": ["Vendor_ID", "Vendor_Name", "Location", "Contact"]
}

# Mapping of join conditions with changed table names
join_conditions = {
    "Financial Records": {"Account_No": "Customer Info.Customer_ID"},
    "Company Profiles": {"Company_ID": "Financial Records.Account_No"},
    "Employee Data": {"Employee_ID": "Company Profiles.Company_ID"},
    "Vendor Details": {"Vendor_ID": "Product Data.Product_ID"}
}

# Sidebar selection
selected_columns = []
selected_views = set()

st.sidebar.header("Select Features")
for category, columns in categories.items():
    with st.sidebar.expander(category):
        selected = st.multiselect(f"Select {category} Columns", columns)
        if selected:
            selected_columns.extend(selected)
            selected_views.add(category)

# Construct SQL Query
base_table = "view_transaction_summary"
sql_query = f"SELECT {', '.join(selected_columns)} FROM {base_table}"
joins = []

for view in selected_views:
    if view in join_conditions:
        for col in categories[view]:
            if col in selected_columns and col in join_conditions[view]:
                join_condition = join_conditions[view][col]
                join_table = join_condition.split(".")[0]
                joins.append(f"INNER JOIN {join_table} ON {view}.{col} = {join_condition}")

if joins:
    sql_query += " " + " ".join(joins)

sql_query += " WHERE transaction_date BETWEEN 'start_date_str' AND 'end_date_str'"

st.text_area("Generated SQL Query:", sql_query)
