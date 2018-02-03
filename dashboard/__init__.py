from flask import Flask, render_template
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
    devices = item['devices']
    algorithms = item['algorithms']

    algo_objects = []
    for algo in algorithms:
        name = algo['name']
        workers = algo['workers']
        tot_speed = [0,0]
        worker_objects = []
        for worker in workers:
            device_id = worker['device_id']
            speed = worker['speed']
            tot_speed[0] += speed[0]
            tot_speed[1] += speed[1]

            found = False
            for idx, worker2 in enumerate(worker_objects):
                device_id2 = worker2['device_id']
                if device_id == device_id2:
                    found = True
                    new_worker = worker2
                    new_worker['speed'][0] += speed[0]
                    new_worker['speed'][1] += speed[1]
                    worker_objects[idx] = new_worker

            if not found:
                new_worker = {}
                new_worker['device_id'] = device_id
                new_worker['speed'] = speed
                worker_objects.append(new_worker)

        algo['workers'] = worker_objects
        algo['total_speed'] = tot_speed
        algo_objects.append(algo)


    return render_template('index.html', devices = devices, algorithms = algo_objects)
    # return str(item)
    # return messages

if __name__ == "__main__":
    app.run();
