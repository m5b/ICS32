import json
from collections import namedtuple

# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['foo','baz'])

def create_joinmsg(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)

# Example Test
json_msg = '{"foo":"value1", "bar": {"baz": "value2"}}'
print(extract_json(json_msg))
