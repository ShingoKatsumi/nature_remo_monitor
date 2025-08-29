from remo import NatureRemoAPI
import time
import datetime

api = NatureRemoAPI('ory_at_9Oc0RqPImm2c0ea8rUyMVVqoKI5r_y3ncqF1iktEpiw.Zukn-6s28FGhwoOvbKHglBSThSQv1UaFhIkcKqfpAuo')
devices = api.get_devices()
print(devices)

while True:
    while api.rate_limit.remaining>0:
        for device in devices:
            print(device.name, str(device.newest_events['te'].val), str(device.newest_events['hu'].val) )
            print(str(api.rate_limit.limit), str(api.rate_limit.remaining),str(api.rate_limit.reset+datetime.timedelta(hours=9)))
        time.sleep(1)

    if str(api.rate_limit.reset+datetime.timedelta(hours=9)) > datetime.now():
        time.sleep((api.rate_limit.reset+datetime.timedelta(hours=9)-datetime.datetime.now()).seconds)
