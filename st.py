import streamlit as st

# Example columns
free_input_columns = ["name", "description"]
date_columns = ["created_date", "updated_date"]

# Configuration dictionary
config = {'fields': {}}

# Streamlit app
st.title("Streamlit Condition Tree Example")

# Select a column for demonstration
column = st.selectbox("Select a column", free_input_columns + date_columns)

# Implement the condition tree
if column in free_input_columns:
    # Free text input
    config['fields'][column] = {
        'label': column,
        'type': 'text',  # Free text input
        'mainWidgetProps': {
            'valuePlaceholder': f"Enter value for {column}"
        },
    }
    st.text_input(f"Enter value for {column}")

elif column in date_columns:
    # Date filter with operators
    config['fields'][column] = {
        'label': column,
        'type': 'date_range',
        'operators': ['less', 'equal', 'between'],
        'mainWidgetProps': {},
    }

    # Operator selection
    selected_operator = st.selectbox(f"Select operator for {column}", config['fields'][column]['operators'])

    # Logic for specific operators
    if selected_operator == "between":
        start_date = st.date_input(f"Select start date for {column}")
        end_date = st.date_input(f"Select end date for {column}")
        config['fields'][column]['mainWidgetProps'] = {
            'start_date': start_date,
            'end_date': end_date,
        }
        st.write(f"Selected range: {start_date} to {end_date}")
    else:
        single_date = st.date_input(f"Select date for {column}")
        config['fields'][column]['mainWidgetProps'] = {
            'date': single_date,
        }
        st.write(f"Selected date: {single_date}")

# Display the configuration
st.subheader("Generated Configuration")
st.json(config)
