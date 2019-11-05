import requests
from apscheduler.schedulers.background import BackgroundScheduler
import time
import configs
import datetime
import pg8000

models = ["optimistic", "pessimistic", "best_guess"]
routes = {"41.8839,-87.6319": "34.0537,-118.2427", "24.5551,-81.7800": "47.6062,-122.3321"}
api_key = configs.API_KEY
seconds = 30


def db_insert(curr_time, route, model, distance, duration_text, duration, duration_traffic_text, duration_traffic):
    cursor.execute("INSERT INTO maps (time, route, model, distance, durationText, duration, durationTrafficText, "
                   "durationTraffic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                   (curr_time, route, model, distance, duration_text, duration,
                    duration_traffic_text, duration_traffic))
    print("Values added to database at {}".format(curr_time))


def call(dest, origin):
    resps = list()
    if dest == list(routes.keys())[0]:
        curr_route = 0
    else:
        curr_route = 1
    curr = int(time.time()) + 10
    for model in models:
        response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations={}"
                                "&origins={}&departure_time={}&traffic_model={}&key={}"
                                .format(dest, origin, curr, model, api_key)).json()
        if response is not None:
            db_insert(curr, curr_route, model, response.get("rows")[0].get("elements")[0].get("distance").get("value"),
                      response.get("rows")[0].get("elements")[0].get("duration").get("text"),
                      response.get("rows")[0].get("elements")[0].get("duration").get("value"),
                      response.get("rows")[0].get("elements")[0].get("duration_in_traffic").get("text"),
                      response.get("rows")[0].get("elements")[0].get("duration_in_traffic").get("value"))


def caller():
    for key, value in routes.items():
        call(key, value)


def clock():
    scheduler = BackgroundScheduler()
    scheduler.add_job(caller, 'interval', seconds=seconds)
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
print("Opening connection to datbase...")
conn = pg8000.connect(user=configs.DB_USER, password=configs.DB_PASSWORD)
cursor = conn.cursor()
print("Successfully connected to database")
start = int(time.time())
clock()
end = int(time.time())
print("Total elapsed time: {}".format(str(datetime.timedelta(seconds=(end - start)))))
conn.commit()
