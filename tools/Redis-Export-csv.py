import redis
import sys
import json

redisURL = sys.argv[1]

password, host, port = redisURL.replace(
    'redis://', '').replace('@', '|').replace(':', '|').split('|')

r = redis.Redis(host=host, password=password, port=port, ssl=True)
keys = list(r.keys())

file = './data.csv'

# Build Head

key = keys[0]
content = r.get(key).decode()
dt = eval(content)
datakeys = list(dt.keys())
head = ''
for i in datakeys:
    head += i + ','
head = head[:-1]
with open(file,'w+') as f:
    f.write(head + '\n')

for key in keys:
    value = ''
    content = r.get(key).decode()
    dt = eval(content)
    for i in dt:
        value += str(dt[i]) + ','
    value = value[:-1]
    with open(file,'a+') as f:
        f.write(value + '\n')

print('Done!')

