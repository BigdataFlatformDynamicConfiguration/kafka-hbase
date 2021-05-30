import json

res = [
    {'hs':1},
    {"fds":2},
    {"fds":32}
    ]
result = {}
idx = 0
for data in res:
    result[idx] = data
    idx += 1
print json.dumps(result)