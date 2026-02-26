#Convert from JSON to Python:
import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])



#Convert from Python to JSON:
# a Python object (dict):
f = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
g = json.dumps(f)

# the result is a JSON string:
print(g)