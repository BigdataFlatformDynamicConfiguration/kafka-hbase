import requests

URL = 'http://34.64.94.147:2000/row-list'
data = {'param1': 'value1', 'param2': 'value'} 
res = requests.post(URL, data=data)
