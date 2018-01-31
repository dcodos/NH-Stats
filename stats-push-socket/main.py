import requests

base_url = "http://localhost:38080/api?command="

command_info = '{"id":1, "method":info, "params":[]}'
res = requests.get(base_url + command_info)
print(res.content)
