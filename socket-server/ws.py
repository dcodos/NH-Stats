import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()

db = client.mining
messages = db.messages

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new connection')

    def on_message(self, message):
        # print 'message received:  %s' % json.loads(message)
        mes = json.loads(message)
        time = mes['time']
        mes['time'] = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        result = messages.insert_one(mes)
        print("Message logged")
        # print(result)
        # self.write_message(message)

    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
    (r'/ws', WSHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
