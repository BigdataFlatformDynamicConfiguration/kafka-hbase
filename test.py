import requests
import json

URL = 'http://34.64.94.147:2000/row-list'
# data = {'param1': 'value1', 'param2': 'value'} 

data = {"table_name" : "my-topic11", "data" : [{"cf1:col1" : "1","cf1:col2" : "2",},{"cf1:col1" : "3","cf1:col2" : "4",}]}
# {
#   "table_name" : "my-topic11",
#   "data" : 
#   [
#     {
#       "cf1:col1" : "1",
#       "cf1:col2" : "2",
#     },
#     {
#       "cf1:col1" : "3",
#       "cf1:col2" : "4",
#     }
#   ]
# }


# res = requests.post(URL, data=json.dumps(data))
res = requests.post(URL, json=data)
print(res.text)
