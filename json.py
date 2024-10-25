import json

EXAMPLE_JSON_STRING = '{ "eggs": 2.25, "milk": 2.50, "cheese": 3.00 }'
EXAMPLE_PYTHON_DICT = {
  "waffles": 5.00,
  "cereal": 6.00,
  "oatmeal": 3.00,
}



dict_result = json.loads(EXAMPLE_JSON_STRING) 
print(dict_result)

json_result = json.dumps(EXAMPLE_PYTHON_DICT) 
print(json_result)

with open("example.json") as f: 
    dict_result = json.load(f)

with open("example.json") as f: 
    json.dump(EXAMPLE_PYTHON_DICT, f)