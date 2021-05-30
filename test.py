import requests
import json

URL = 'http://34.64.94.147:2000/row-list'
data = {'param1': 'value1', 'param2': 'value'} 
data = json.dumps(data)

# data = 'hello'
res = requests.post(URL, data=data)
