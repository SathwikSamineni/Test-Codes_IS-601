import json

# open file
content = None
with open('example_orders.json') as f:
    content = f.read()
if content is not None:
    # load JSON data
    content = json.loads(content)
else:
    print("Error: Unable to open file")
    exit()
# extract content

items = []
orders = []
customers = []
for order in content:
    customers.append({
        "name": order["customer"]["name"],
        "phone": order["customer"]["phone"]
    })
    items = items | order["items"]
    customer = order["name"]
    orders.append({
        "customer":customer, 
        "items":[x["name"] for x in order["items"]]
        })
    # if order["name"] in orders:
    #     orders[order["name"]] |= order["items"]
    # else:
    #     orders[order["name"]] = order["items"]

# create tables


    
    
