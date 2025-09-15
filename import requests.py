from remo import NatureRemoAPI
import time
import datetime
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import japanize_matplotlib

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

# データ保存用リスト
time_list = []
device_name_lists = []
temp_lists = [[] for i in range(len(devices))]
hum_lists = [[] for i in range(len(devices))]

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
    print("latest_time_updated:", time_updated)
    #正常に更新されているので次の更新を待つ
    if time_updated_old != "" and api.rate_limit.remaining>1:
        print("data_Updated_at:", time_updated)
        time_updated_old = time_updated
        print("Next Access time:",datetime.datetime.now()+datetime.timedelta(seconds=300))
        time.sleep(300)

    #正常に更新されていないので更新を急かす
    else:
        print("data_Not_updated_at:", time_updated)
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

    try:
        plt.cla()
        plt.close()
    except:
        pass

    #グラフ描画
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.set_ylabel('Temperature (°C)')
    ax2.set_ylabel('Humidity (%)')
    ax1.set_xlabel('Time')
    ax1.set_title('Temperature and Humidity Over Time')

    time_list.append(datetime.datetime.now())

    for device in devices:
        device_name_lists.append(device.name)
        temp_lists[devices.index(device)].append(device.newest_events['te'].val)
        hum_lists[devices.index(device)].append(device.newest_events['hu'].val)        
        if len(time_list) > 50:  # データポイントが50を超えたら最初のデータを削除
            del time_list[0]
            for row in temp_lists:
                del row[0]
            for row in hum_lists:
                del row[0]
        ax1.plot(time_list, temp_lists[devices.index(device)], label='Temp_'+device.name, color=plt.get_cmap('tab10')(devices.index(device)), linestyle='solid', marker='o')
        ax2.plot(time_list, hum_lists[devices.index(device)], label='Humid_'+device.name, color=plt.get_cmap('tab10')(devices.index(device)), linestyle='dotted', marker='x')
        # 凡例をまとめて表示
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
    
    ax1.legend(h1 + h2, l1 + l2, loc='upper left')
    
    fig.autofmt_xdate()  # x軸の日時ラベルを自動で回転
    formatter = matplotlib.dates.DateFormatter('%H:%M')
    locator = matplotlib.dates.MinuteLocator(interval=10)
    ax1.xaxis.set_major_locator(locator)
    ax1.xaxis.set_major_formatter(formatter)

    ax1.set_xlim([min(time_list), max(time_list)])
    ax1.set_ylim([min(min(temp_lists))-1, max(max(temp_lists))+1])
    ax2.set_ylim([min(min(hum_lists))-5, max(max(hum_lists))+5])

    matplotlib.pyplot.rcParams['font.size'] = 10
    fig.subplots_adjust(left=0.25, right=0.95, top=0.9, bottom=0.15)

    ax2.spines['left'].set_position(('axes', -0.2))
    ax2.yaxis.set_ticks_position('left') 
    ax2.yaxis.set_label_position('left') 
    plt.pause(10)  # グラフを更新

    print("go to next step")