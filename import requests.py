from remo import NatureRemoAPI
import time
import datetime

api = NatureRemoAPI('ory_at_9Oc0RqPImm2c0ea8rUyMVVqoKI5r_y3ncqF1iktEpiw.Zukn-6s28FGhwoOvbKHglBSThSQv1UaFhIkcKqfpAuo')
time_updated_old = ""

#初回アクセス時はリセットタイミングまで待機する
try:
    devices = api.get_devices()
except:
    print("Initial wait until rate limit reset ")
    time.sleep(900)

if api.rate_limit.remaining == 30:
    pass
else:
    print("Initial wait until rate limit reset at", api.rate_limit.reset+datetime.timedelta(hours=9))
    time.sleep((api.rate_limit.reset+datetime.timedelta(hours=9)-datetime.datetime.now()).seconds)

while True:
    # デバイス情報を取得
    devices = api.get_devices()
    print("----------")
    #print(devices)

    if api.rate_limit.remaining>1:
        for device in devices:
            print(device.name, str(device.newest_events['te'].val), str(device.newest_events['hu'].val) )
            print(str(api.rate_limit.limit), str(api.rate_limit.remaining),str(api.rate_limit.reset+datetime.timedelta(hours=9)))

    time_updated = devices[0].newest_events['te'].created_at+datetime.timedelta(hours=9)
    print("time_updated:", time_updated)
    #正常に更新されているので次の更新を待つ
    if time_updated_old != "" and api.rate_limit.remaining>1:
        print("Updated:", time_updated)
        time_updated_old = time_updated
        time.sleep(900)
    #正常に更新されていないので更新を急かす
    else:
        print("Not updated:", time_updated)
        #待ち時間を設定
        times_remain = api.rate_limit.reset+datetime.timedelta(hours=9)-datetime.datetime.now()
        print("Waiting time:", times_remain)
        times_wait = times_remain/(api.rate_limit.remaining)
        print("Time to wait for the next request:", times_wait.total_seconds())
        print("Next Access time:",datetime.datetime.now()+times_wait)
        time.sleep(max(0, times_wait.total_seconds()))

    if api.rate_limit.remaining <= 1:
        # レート制限のリセットを待機
        if api.rate_limit.reset+datetime.timedelta(hours=9) > datetime.datetime.now() and api.rate_limit.remaining == 1:
            print("Rate limit exceeded. Waiting until reset at", api.rate_limit.reset+datetime.timedelta(hours=9))
            time.sleep((api.rate_limit.reset+datetime.timedelta(hours=9)-datetime.datetime.now()).seconds)

    time_updated_old = time_updated
    print("go to next step")