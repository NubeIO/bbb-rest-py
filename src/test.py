test_json_file = 'test.json'
import json

with open(test_json_file, 'r') as f:
    data = f.read()

# parse file
obj = json.loads(data)
print(obj)

rawReads = {
    "UI1": obj['UI1'],
    "UI2": obj['UI2'],
    "UI3": obj['UI3'],
    "UI4": obj['UI4'],
    "UI5": obj['UI5'],
    "UI6": obj['UI6'],
    "UI7": obj['UI7'],
}
a = 'UI1'
print(rawReads[a])
