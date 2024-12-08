import json

# Load the JSON file
with open('example_orders.json', 'r') as file:
    data = json.load(file)

# Print the JSON data in a readable format
print(json.dumps(data, indent=4))
