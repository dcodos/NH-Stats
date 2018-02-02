import requests
import json
import websocket
import datetime

base_url = 'http://localhost:38080/api?command='

command_info = '{"id":1,"method":"device.list","params":[]}'
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
            res = requests.get(base_url + command_info)
            dev_info = json.loads(res.content)["devices"]
            num_devices = len(dev_info)

            cur_time = datetime.datetime.now()

            dev_info_message = {
            'sender': 'dan',
            'time': str(cur_time),
            'method': 'device.list',
            'message': dev_info
            }

            ws.send(json.dumps(dev_info_message))
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://ec2-18-216-110-114.us-east-2.compute.amazonaws.com:8888/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
