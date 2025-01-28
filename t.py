def to_camel_case(words):
    return ''.join(word.capitalize() if i > 0 else word.lower() for i, word in enumerate(words))

# Example usage
words_list = ["allocation acc", "borrower id", "clearing house", "client region id"]

# Convert each word in the list to camel case
camel_case_list = [''.join(to_camel_case(word.split())) for word in words_list]

print(camel_case_list)
