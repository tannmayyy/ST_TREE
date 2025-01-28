def to_pascal_case_with_underscore(words):
    words = words.lower()  # Convert to lowercase first
    parts = words.split('_')  # Split the string by underscores
    pascal_case = '_'.join(part.capitalize() for part in parts)  # Capitalize each part and join with underscores
    return pascal_case  # Return the result with the first letter capitalized

# Example usage
words_list = ["ALLOCATIONACC", "BORROWER_ID", "TRADE_STATUS", "EVENT_TYPE"]

# Convert each word in the list to Pascal Case with underscores
pascal_case_list = [to_pascal_case_with_underscore(word) for word in words_list]

print(pascal_case_list)
