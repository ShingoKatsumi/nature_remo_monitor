from remo import NatureRemoAPI
import time
import datetime

api = NatureRemoAPI('ory_at_9Oc0RqPImm2c0ea8rUyMVVqoKI5r_y3ncqF1iktEpiw.Zukn-6s28FGhwoOvbKHglBSThSQv1UaFhIkcKqfpAuo')

while True:
    # デバイス情報を取得
    devices = api.get_devices()
    #print(devices)

    if api.rate_limit.remaining>0:    
        for device in devices:
            print(device.name, str(device.newest_events['te'].val), str(device.newest_events['hu'].val) )
            print(str(api.rate_limit.limit), str(api.rate_limit.remaining),str(api.rate_limit.reset+datetime.timedelta(hours=9)))

    #待ち時間を設定
    times_remain = api.rate_limit.reset+datetime.timedelta(hours=9)-datetime.datetime.now()
    print("Waiting time:", times_remain)
    times_wait = times_remain/(api.rate_limit.remaining+1)
    print("Time to wait for the next request:", times_wait.total_seconds())
    print("Next Access time:",datetime.datetime.now()+times_wait)
    time.sleep(times_wait.total_seconds())

    if api.rate_limit.reset+datetime.timedelta(hours=9) > datetime.datetime.now():
        time.sleep((api.rate_limit.reset+datetime.timedelta(hours=9)-datetime.datetime.now()).seconds)