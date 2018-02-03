from flask import Flask, render_template
from pymongo import MongoClient
import requests
client = MongoClient()

db = client.mining
messages = db.messages

app = Flask(__name__)

@app.route('/')
def get_stats():
    profit_info = get_nh_profits()
    item = messages.find().sort('time', -1)[0]
    devices = item['devices']
    algorithms = item['algorithms']

    overall_btc = 0.0
    overall_usd = 0.0
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
        payrate = findpayrate(profit_info, name)
        btcPrice = getBtcPrice()

        btc_payout = payrate * float(tot_speed[0]) / 1000000000
        usd_payout = btc_payout * btcPrice
        algo['btc_payout'] = btc_payout
        algo['usd_payout'] = usd_payout

        overall_btc += btc_payout
        overall_usd += usd_payout

        algo_objects.append(algo)

    return render_template('index.html', devices = devices, algorithms = algo_objects, overall_btc = overall_btc, overall_usd = overall_usd)
    # return str(item)
    # return messages

def getBtcPrice():
    url = "https://api.gdax.com/products/BTC-USD/ticker"
    r = requests.get(url)
    btc_price = float(r.json()["price"])
    return btc_price

def findpayrate(profit_info, algo_name):
    for item in profit_info:
        if item['name'] == algo_name:
            return float(item['paying'])

def get_nh_profits():
    url = "https://api.nicehash.com/api?method=simplemultialgo.info"
    response = requests.get(url)
    try:
        nicehash_profits = response.json()["result"]["simplemultialgo"]
        return nicehash_profits
    except:
        print("uh oh")

if __name__ == "__main__":
    app.run();
