import json

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

with open(f'AAA.json', 'w') as json_file:
  json.dump(x, json_file)
# the result is a JSON string:
print(y)
