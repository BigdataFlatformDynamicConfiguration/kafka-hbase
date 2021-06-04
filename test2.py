import requests
import json

URL = 'http://34.64.120.158:2000/put-row'
# data = {'param1': 'value1', 'param2': 'value'} 

# data = {"table_name" : "my-topic11", "data" : [{"cf1:col1" : "5","cf1:col2" : "6",},{"cf1:col1" : "7","cf1:col2" : "8",}]}
data = {"table_name" : "my-topic11", "datalist" : [{"rowkey":"3", "data": {"cf1:col1" : "1","cf1:col2" : "2",}},{"rowkey":"4", "data": {"cf1:col1" : "3","cf1:col2" : "4",}}]}
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
