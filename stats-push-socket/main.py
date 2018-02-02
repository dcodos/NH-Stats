import requests
import json
from websocket import create_connection

# base_url = 'http://localhost:38080/api?command='
#
# command_info = '{"id":1,"method":"device.list","params":[]}'
# res = requests.get(base_url + command_info)
#
# dev_info = json.loads(res.content)["devices"]
# num_devices = len(dev_info)
#
# print(dev_info)
# print(num_devices)


ws = create_connection("ws://ec2-18-216-110-114.us-east-2.compute.amazonaws.com:8888/ws")
print "Sending 'Hello, World'..."
ws.send("Hello, World")
print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()
