import requests
import json
import websocket
import datetime

base_url = 'http://localhost:38080/api?command='

command_device_list = '{"id":1,"method":"device.list","params":[]}'
command_device_info = '{{"id":1,"method":"device.get","params":["{0}"]}}'
command_algorithm_list = '{"id":1,"method":"algorithm.list","params":[]}'
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while True:
            res = requests.get(base_url + command_device_list)
            all_dev_info = json.loads(res.content)["devices"]

            device_ids = []
            for item in all_dev_info:
                device_id = item["device_id"]
                device_ids.append(int(device_id))

            all_devices = []
            for dev in device_ids:
                res = requests.get(base_url + command_device_info.format(str(dev)))
                device_info = json.loads(res.content)
                all_devices.append(device_info)

            cur_time = datetime.datetime.now()

            # dev_info_message = {
            # 'sender': 'dan',
            # 'time': str(cur_time),
            # 'type': 'devices',
            # 'message': all_devices
            # }

            # ws.send(json.dumps(dev_info_message))

            res = requests.get(base_url + command_algorithm_list)
            all_algo_info = json.loads(res.content)["algorithms"]
            algo_message = {
            'sender': 'dan',
            'time': str(cur_time),
            'type': 'all',
            'devices': all_devices,
            'algorithms': all_algo_info
            }
            ws.send(json.dumps(algo_message))
            time.sleep(30)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://ec2-18-216-164-213.us-east-2.compute.amazonaws.com/:8888/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
