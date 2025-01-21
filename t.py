if column in free_input_columns:
    # Add a free text input for specific columns
    config['fields'][column] = {
        'label': column,
        'type': 'text',  # Free text input
        'mainWidgetProps': {
            'valuePlaceholder': f"Enter value for {column}"
        },
    }

elif column in date_columns:
    # Add a date filter with multiple operators, including "between"
    config['fields'][column] = {
        'label': column,
        'type': 'date_range',
        'operators': ['less', 'equal', 'between', 'not_between'],
        'mainWidgetProps': {},
    }

    # Add logic for the "between" operator
    if 'between' in config['fields'][column]['operators']:
        config['fields'][column] = {
            'label': column,
            'type': 'date_range',
            'operators': ['between'],
            'mainWidgetProps': {
                'start_date': {
                    'type': 'date',
                    'label': f"Start date for {column}",
                },
                'end_date': {
                    'type': 'date',
                    'label': f"End date for {column}",
                }
            },
        }
    else:
        config['fields'][column] = {
            'label': column,
            'type': 'date',
            'operators': ['less', 'equal', 'not_between'],
            'mainWidgetProps': {
                'date': {
                    'type': 'date',
                    'label': f"Select date for {column}",
                }
            },
        }
