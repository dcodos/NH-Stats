from flask import Flask
from pymongo import MongoClient
client = MongoClient()

db = client.mining
messages = db.messages

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stats')
def get_stats():
    item = messages.find().sort('time', -1)[0]
    return str(item)
    # return messages

if __name__ == "__main__":
    app.run();
