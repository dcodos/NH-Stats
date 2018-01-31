import requests
import json

base_url = 'http://localhost:38080/api?command='

command_info = '{"id":1,"method":"device.list","params":[]}'
res = requests.get(base_url + command_info)

dev_info = json.loads(res.content)["devices"]
num_devices = len(dev_info)

print(dev_info)
print(num_devices)
