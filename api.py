import requests
from apscheduler.schedulers.background import BackgroundScheduler
import time
import configs
import json
import datetime


models = ["optimistic", "pessimistic", "best_guess"]
routes = {"41.8839,-87.6319": "34.0537,-118.2427", "24.5551,-81.7800": "-124.635404,48.327961"}
key = configs.API_KEY
seconds = 30


def call(dest, origin):
    resps = list()
    curr = int(time.time()) + 10
    for model in models:
        response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations={}"
                                           "&origins={}&departure_time={}&traffic_model={}&key={}"
                                           .format(dest, origin, curr, model, key)).json()
        print(response)
        #print("Got results from {} to {}: {} travel time".format(response.get("origin_addresses"),
                                                                 #response.get("destination_addresses"),
                                                                 #response.get("rows")[0].get("elements")[0]
                                                                 #.get("duration").get("text")))
        resps.append(response)
    print(resps)
    return resps


def caller():
    for key, value in routes.items():
        call(key, value)


def clock():
    scheduler = BackgroundScheduler()
    scheduler.add_job(caller, 'interval', seconds = seconds)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

print("Starting Google Maps API Caller...")
print("Running {} routes every {} seconds".format(len(routes), seconds))
start = int(time.time())
clock()
end = int(time.time())
print("Total elapsed time: {}".format(str(datetime.timedelta(seconds=(end - start)))))
