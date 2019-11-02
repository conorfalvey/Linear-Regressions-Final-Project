import requests
from apscheduler.schedulers.background import BackgroundScheduler
import time

models = ["optimistic", "pessimistic", ""]
# Turn dests and origins into map to pass one data structre
dests = []
origins = []
key = "AIzaSyAHxTaivFtueStNRNX9LlDXyl_NA-JwwfQ"


def call(dest, origin, time, key):
    resps = list()
    for model in list:
        response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations={}&origins={}"
                                "&departure_time={}&traffic_model={}&key={}".format(dest, origin, time, model, key))
        resps.append(response.content)
    return resps


def routes():
    # Iterate over dests/origin map and pass to calls
    return None

def caller():
    # Interim function that clock calls
    # This calls routes and call.
    # Routes passes the current route to call as well as other params
    return None


def clock():
    scheduler = BackgroundScheduler()
    scheduler.add_job(caller, 'interval', seconds=30)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()