import requests
import json
import time
import SID
import asyncio
import Data
import random
import re
import ELE


# 位置
longitude = 113.266365
latitude = 23.17275


# 储存当前领取的红包
hongbaos = []

# 保存sid对应的位置等信息，以备下次领取
cookies = {}

# 反向地理编码
def updateGeo(sid):
    global latitude, longitude
    # 随机定位
    index = random.randint(0, len(Data.lola))
    lola_key = '同上'
    if index >= 0 and index < len(Data.lola):
        lola_key = list(Data.lola.keys())[index]
        print(lola_key)
        if lola_key in Data.lola:
            longitude = Data.lola[lola_key][0]
            latitude = Data.lola[lola_key][1]
    url = 'https://h5.ele.me/restapi/bgs/poi/reverse_geo_coding?latitude=' + str(latitude) + '&longitude=' \
          + str(longitude)
    res = requests.get(url, headers={'cookie': 'SID=' + sid})
    rep = json.loads(res.text)
    latitude = rep['latitude']
    longitude = rep['longitude']
    return rep


def getHongbao1(sid, channel, ua='Mozilla/5.0 (Linux; Android 9; MI MAX 3 Build/PKQ1.190714.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044904 Mobile Safari/537.36 MMWEBID/386 MicroMessenger/7.0.7.1521(0x27000735) Process/tools NetType/4G Language/zh_CN', loc=['广州']):
    # 随机切换地址
    global longitude, latitude
    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        if userId == '0':
            return
    else:
        userId = SID.getUserId(sid)
        cookies[sid]['userId'] = userId
    # if channel not in cookies[sid]:
    #     cookies[sid][channel] = {}
    # if 'longitude' in cookies[sid][channel] and 'latitude' in cookies[sid][channel]:
    #     longitude = cookies[sid]['longitude']
    #     latitude = cookies[sid]['latitude']
    # else:
    index = random.randint(0, len(loc))
    lola_key = '同上'
    if index >= 0 and index < len(loc):
        lola_key = loc[index]
        if lola_key in loc:
            longitude = Data.lola[lola_key][0]
            latitude = Data.lola[lola_key][1]
            # print("定位:", lola_key)


    interUrl = 'https://h5.ele.me/restapi/traffic/users/' + userId + '/lottery'
    headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
               'x-shard': 'loc=' + str(longitude) + ',' + str(latitude) + ';', }
    data = {'userId': userId, 'channel': channel, 'longitude': longitude, 'latitude': latitude}
    res = requests.post(interUrl, headers=headers, data=data)
    volume = json.loads(res.text)
    # print(volume)
    if volume['message'] == '成功':
        if 'data' in volume:
            for hb in volume['data']:
                try:
                    hongbao = str(hb['title'])+str(hb['threshold'])+'-'+str(hb['amount'])
                    print(lola_key+'红包' + channel, hongbao)
                    if int(hb['amount']) > 5:
                        hongbaos.append(hongbao)
                    cookies[sid][channel] = {'longitude': longitude, 'latitude': latitude}
                except:
                    print('领取出错')
        # hongbao = str(volume['sum']['threshold']) + '-' + str(volume['sum']['amount'])
        # print(lola_key+'红包' + channel, hongbao)
        # if hongbao.find('.0') >= 0 and hongbao.find('-1.0') == -1 and hongbao != '':
        #     hongbaos.append(hongbao)
    else:
        hongbao = volume['message']
        print(lola_key+'红包' + channel, hongbao)


def getHongbao2(sid, ua='Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190302.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.20.0.32 Mobile Safari/537.36 UCBS/3.20.0.32_191012190528 NebulaSDK/1.8.100112 Nebula AlipayDefined(nt:WIFI,ws:393|0|2.75) AliApp(AP/10.1.78.7000) AlipayClient/10.1.78.7000 Language/zh-Hans useStatusBar/true isConcaveScreen/true Region/CN'):
    global longitude, latitude, cookies
    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        if userId == '0':
            return
    if 'longitude' in cookies[sid] and 'latitude' in cookies[sid]:
        longitude = cookies[sid]['longitude']
        latitude = cookies[sid]['latitude']
    url = 'https://h5.ele.me/restapi/lego/query_module_content?latitude=' + str(latitude) + '&longitude=' + str(
        longitude) + '&codes[]=module_home_coupon_popup'
    headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
               'x-shard': 'loc=' + str(longitude) + ',' + str(latitude)}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        volume = json.loads(res.text)
        if volume['data']:
            volume = volume['data']
            volume = volume[0]
            volume = volume['items']
            volume = volume[0]
            volume = volume['content']
            # print(volume)
            hongbao = str(volume['title'] + volume['discountThreshold']) + '-' + str(volume['discountAmount'])
            print('口碑首页红包：' + hongbao)
            hongbaos.append(hongbao)
            cookies[sid]['口碑首页红包'] = {'longitude': longitude, 'latitude': latitude}

# 这是饿了么客户端首页得红包
def getHongbao3(sid, ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/Z6Lite_MIUI1_V11.0.3.0_YouLinw_191105 Eleme/8.26.4 Channel/xiaomi ID/a78ab0ea-70c2-3500-badc-e1218a28b714; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware:ba3232802c95d8f316278ecd188ed3e3 Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190302.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):

    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        if userId == '0':
            return
    else:
        userId = SID.getUserId(sid)
        cookies[sid]['userId'] = userId
    if '饿了么首页红包' in cookies[sid]:
        geohash = cookies[sid]['饿了么首页红包']['geohash']
    else:
        rep = updateGeo(sid)
        geohash = rep['geohash']
    url = 'https://restapi.ele.me/marketing/v5/users/'+userId+'/startup_hongbao'
    headers = {
        'user-agent': ua,
        'cookie': 'SID=' + sid,
        'x-shard': 'loc=' + str(longitude) + ',' + str(latitude),
        'x-deviceinfo': 'aW1laTo4NjUxNjYwMjAyMDAxNzkgc2VyaWFsOjAwNjA0ZTg1IGFuZHJvaWRfaWQ6MzE0NmViMzBmZDI5ZmNlZSBicmFuZDp4aWFvbWkgbW9kZWw6aG1fbm90ZV8xbHRlIG5ldHdvcmtPcGVyYXRvcjo0NjAwMCBtYWNBZGRyZXNzOjAwXzgxXzY3XzRkXzk1X2YxIG5ldFR5cGU6V0lGSSBzaW1TZXJpYWxOdW1iZXI6ODk4NjAwMjI2NjU5ODY4MTU1Njggc2ltU3RhdGU6NSBsYXRpdHVkZTozOS45MTYyOTQ5MjQ5MTQ4NCBsb25naXR1ZGU6MTE2LjQxMDM0MzkwNzc3MzUgY2lkOjMyMzA1IGxhYzoxMDI4IHdpZmlMaXN0OjAwXzgxX2YxXzRkX2RiXzk1IGhhdmVCbHVldG9vdGg6dHJ1ZSB0cmFja19pZDogbWVtb3J5OjUxOSBlbmVyZ3lfcGVyY2VudDoxMDAgZmlyc3Rfb3BlbjoxNTcyNDQzMjcxIGxhc3Rfb3BlbjoxNTczOTY2NDQ5IG5ldF90eXBlOldJRkkgaGFyZHdhcmVfaWQ6OWFmYTM4Nzk5NzY2MmFkYTgyYjAzYjgwYTE2N2EzZDc='}
    data = {"geohash": geohash}
    res = requests.post(url, headers=headers, data=data)
    data = json.loads(res.text)
    if 'hongbao_list' in data and len(data['hongbao_list']) != 0:
        for d in data['hongbao_list']:
            try:
                hongbao = str(d['hongbao_name'])+str(d['sum_condition'])+'-'+str(d['amount'])
                hongbaos.append(hongbao)
                print('首页红包'+hongbao)
                cookies[sid]['饿了么首页红包'] = {'geohash':geohash, 'longitude': longitude, 'latitude': latitude}

            except:
                print('领取错误')


# 已过期
# def getHongbao3(sid,
#                 ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/PKQ1.190714.001 Eleme/8.26.4 Channel/xiaomi ID/1da84041-3494-3fc4-a535-3421622db4b8; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware: Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):
#     startUrl = 'https://h5.ele.me/restapi/activation/api/partner/enterPlace'
#     url = 'https://h5.ele.me/restapi/activation/api/chess/movePosition'
#     headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
#                'x-shard': 'loc=' + str(longitude) + ',' + str(latitude),
#                'x-ua': 'RenderWay/H5 AppName/elmc Longitude/str(longitude) Latitude/str(latitude) DeviceId/1da84041-3494-3fc4-a535-3421622db4b8'}
#     data = {"comeChannel": "app", "entrance": "app", "longitude": str(longitude), "latitude": str(latitude)}
#
#     # 开始游戏
#     requests.get(startUrl, headers=headers, data=data)
#
#     # 跳3次
#     for i in range(0, 3):
#         res = requests.post(url, headers=headers, data=data)
#         if res.status_code != 200:
#             return
#
#         volume = json.loads(res.text)
#         print(volume['message'])
#         if '没有足够的体力值' == volume['message']:
#             break
#         volume = volume['data']
#         if volume:
#             volume = volume['rewards']
#             if volume and len(volume) != 0:
#                 volume = volume[0]
#                 volume = volume['chessRewards']
#                 volume = volume[0]
#                 print('双11跳一跳红包：' + volume['title'], str(volume['threshold']) + '-' + str(volume['amount']))
#
# # 已过期
# def getHongbao4(sid,
#                 ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/PKQ1.190714.001 Eleme/8.26.4 Channel/xiaomi ID/1da84041-3494-3fc4-a535-3421622db4b8; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware: Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):
#     url = 'https://h5.ele.me/restapi/traffic/berlin/issue'
#     headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
#                'x-shard': 'loc=' + str(longitude) + ',' + str(latitude),
#                'x-ua': 'RenderWay/H5 AppName/elmc Longitude/str(longitude) Latitude/str(latitude) DeviceId/1da84041-3494-3fc4-a535-3421622db4b8'}
#     data = {"activityId": "RC_1074","couponId": 365978355,"comChannel": "H5","longitude": str(longitude),"latitude": str(latitude)}
#
#     # 开始游戏
#     res = requests.post(url, headers=headers, data=data)
#     print(res.text)
#
# # 自动双11抽奖
# def getHongbao5(sid,
#                 ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/PKQ1.190714.001 Eleme/8.26.4 Channel/xiaomi ID/1da84041-3494-3fc4-a535-3421622db4b8; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware: Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):
#     userId = SID.getUserId(sid)
#     hongbaoInfoUrl = 'https://h5.ele.me/restapi/traffic/lottery/my/info?activityCode=10164&uid=' + userId + '&longitude=' + str(
#         longitude) + '&latitude=' + str(latitude)
#     headers = {
#         'cookie': 'SID=' + sid
#     }
#     res = requests.get(hongbaoInfoUrl, headers=headers)
#     data = json.loads(res.text)
#     if 'data' in data.keys():
#         count = int(data['data']['game']['count'])
#     else:
#         count = 0
#     print('当前SID=' + sid)
#     for i in range(count):
#         try:
#             url = 'https://h5.ele.me/restapi/traffic/lottery/draw'
#             data = {"activityCode": 10164, "uid": userId, "longitude": str(longitude), "latitude": str(latitude)}
#             res = requests.post(url, headers=headers, data=data)
#             data2 = json.loads(res.text)
#             if data2['data']:
#                 if data2['msg'] == '中奖啦':
#                     print(data2['msg'])
#                     print(data2['data'])
#         except:
#             continue
#             # print(res.text)

# 游戏等活动
def getHongbao6(sid, ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/PKQ1.190714.001 Eleme/8.26.4 Channel/xiaomi ID/1da84041-3494-3fc4-a535-3421622db4b8; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware: Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):
    global cookies
    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        if userId == '0':
            return
    else:
        userId = SID.getUserId(sid)
        cookies[sid]['userId'] = userId
    try:
        url = 'https://h5.ele.me/restapi/traffic/lottery/draw'
        headers = {
                    'cookie': 'SID=' + sid
                }
        data = {"activityCode": 10258, "uid": userId, "longitude": str(longitude), "latitude": str(latitude)}
        res = requests.post(url, headers=headers, data=data)
        data2 = json.loads(res.text)
        if data2['data']:
            if data2['msg'] == '中奖啦':
                print('1当前sid='+sid)
                print(data2['msg'])
                print(data2['data'])
                # cookies[sid]['draw'] = {'userId': userId, 'channel': '饿了么首页红包', 'longitude': longitude, 'latitude': latitude}

        data = {"activityCode": 10223, "uid": userId, "longitude": str(longitude), "latitude": str(latitude)}
        res = requests.post(url, headers=headers, data=data)
        data2 = json.loads(res.text)
        if data2['data']:
            if data2['msg'] == '中奖啦':
                print('2当前sid=' + sid)
                print(data2['msg'])
                print(data2['data'])

        data = {"activityCode": 10271, "uid": userId, "longitude": str(longitude), "latitude": str(latitude)}
        res = requests.post(url, headers=headers, data=data)
        data2 = json.loads(res.text)

        if data2['data']:
            if data2['msg'] == '中奖啦':
                print('2当前sid=' + sid)
                print(data2['msg'])
                print(data2['data'])
    except:
        print('领取出错')
            # print(res.text)


def getHongbao7(sid):
    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        if userId == '0':
            return
    url = "https://h5.ele.me/pizza/star.epic/v1/scratchcard/drawlottery"
    headers = {
        "cookie": "SID=" + sid,
        "User-Agent":"Rajax/1 Lenovo_L38111/kunlun2 Android/9 Display/Z6Lite_H2OS_9.0.7_YouLinw_190813 Eleme/8.27.4 Channel/liulanqi ID/4cbabd1d-7963-348e-906b-c0e40de554c7; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware:c6edf20593ab62b8617ae85c336f7b88 Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.180716.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.27.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16",
        "x-shard":"loc=113.56410272419453,23.31278594210744"
    }
    data = {
        "userAgent": "Rajax/1 Lenovo_L38111/kunlun2 Android/9 Display/Z6Lite_H2OS_9.0.7_YouLinw_190813 Eleme/8.27.4 Channel/liulanqi ID/4cbabd1d-7963-348e-906b-c0e40de554c7; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware:c6edf20593ab62b8617ae85c336f7b88 Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.180716.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.27.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16",
        "latitude": "23.31278594210744", "longitude": "113.56410272419453", "userId": userId, "activityId": "8",
        "deviceId": "4cbabd1d-7963-348e-906b-c0e40de554c7"}
    res = requests.post(url, headers, data)
    print(res.text)



# 签到
def signIn(sid, ua='Mozilla/5.0 (Linux; Android 9; Lenovo L38111 Build/PKQ1.190302.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/992 MMWEBSDK/191001 Mobile Safari/537.36 MMWEBID/386 MicroMessenger/7.0.8.1540(0x27000833) Process/tools NetType/WIFI Language/zh_CN ABI/arm64'):
    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        if userId == '0':
            return
    else:
        userId = SID.getUserId(sid)
        cookies[sid]['userId'] = userId

    url = 'https://h5.ele.me/restapi/member/v2/users/'+userId+'/sign_in'
    url2 = url+'/daily/prize'
    headers = {
        'user-agent': ua,
        'cookie': 'SID=' + sid,
        'x-shard': 'loc=' + str(longitude) + ',' + str(latitude)
    }
    data = {"channel": "alipay","captcha_code": "","source": "wechat","longitude": str(longitude),"latitude": str(latitude)}
    data2 = {"channel": "alipay","index": random.randint(0, 2),"longitude": str(longitude),"latitude": str(latitude)}
    res = requests.post(url, headers=headers, data=data)
    if len(res.json()) == 0:
        for i in range(2):
            res = requests.post(url2, headers=headers, data=data2)
        hbs = res.json()
        for hb in hbs:
            if hb['status'] == 1:
                hongbao = str(hb['prizes'][0]['name'])+str(hb['prizes'][0]['sum_condition'])+'-'+str(hb['prizes'][0]['amount'])
                print("签到红包"+hongbao)
                if int(hb['prizes'][0]['amount']) > 5:
                    hongbaos.append(hongbao)
                cookies[sid]['签到红包'] = {'longitude': longitude, 'latitude': latitude}
    # 注释以下可以加快速度
    # res = requests.get('https://h5.ele.me/restapi/member/v1/users/'+userId+'/sign_in/info?longitude='+str(longitude)+'&latitude='+str(latitude), headers=headers)
    # tm = res.json()
    # if 'statuses' in tm:
    #     print('当前签到第'+str(sum(tm['statuses']))+'天')


# 第一次执行为覆盖
writeType = 'w'
def saveLog(name):
    global writeType
    with open(ELE.onekeyRootPath+'领红包日志.txt', writeType) as f:
        f.write('\n\n'+str(name)+'\n')
        for line in hongbaos:
            try:
                f.write(str(line) + '\n')
            except:
                continue
    writeType = 'a'



# 这个是循环sid领取
async def start(sid):
    try:
        getHongbao2(sid)
        getHongbao3(sid)
        # getHongbao7(sid)
        # getHongbao6(sid)
        # signIn(sid)
    except:
        print('领取出错')


# 这个是循环channels的sid领取channel
def channelStart(channel, sids):
    global hongbaos
    hongbaos = []
    i = 0
    currentTime = time.time()
    for sid in sids:
        try:
            getHongbao1(sid=sid, channel=channel['channel'], loc=channel['loc'])
            i += 1
            hongbaos = sorted(hongbaos, key=lambda x: int(re.search("(\\d+)", x.split("-")[0]).group()), reverse=True)
            hongbaos = sorted(hongbaos, key=lambda x: int(re.search("(\\d+)", x.split("-")[1]).group()), reverse=True)
            if i % 5 == 0:
                print('领红包剩余时间：', (time.time() - currentTime) / 5 * (len(sids) - i))
                currentTime = time.time()
                print(hongbaos)
        except:
            print('领取出错')
    saveLog(channel['channel'])


def run(h=0, m=0, isChannel=True):
    time.sleep(3600 * h + 60 * m)
    global hongbaos, cookies
    cookies = SID.readCookies()
    sids = SID.getSIDS('../../data/onekey/SID.txt')
    i = 0
    if isChannel:
        for channel in Data.channels:
            channelStart(channel, sids)
    currentTime = time.time()
    hongbaos = []
    while i < len(sids):
        loop.run_until_complete(start(sids[i]))
        i += 1
        hongbaos = sorted(hongbaos, key=lambda x: int(re.search("(\\d+)", x.split("-")[0]).group()), reverse=True)
        hongbaos = sorted(hongbaos, key=lambda x: int(re.search("(\\d+)", x.split("-")[1]).group()), reverse=True)
        if i % 5 == 0:
            print('领红包剩余时间：', (time.time() - currentTime) / 5 * (len(sids) - i))
            currentTime = time.time()
            print(hongbaos)
    saveLog('首页红包')
    SID.writeCookies(cookies=cookies)
    # 开始查询红包
    ELE.queryFaka(queryModel=1, fileName='numbersQQ.txt')
    ELE.queryHongbaos()
#


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    run(0, 0, isChannel=True)