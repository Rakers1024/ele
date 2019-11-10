import requests
import json
import time
import SID
import asyncio
import Data
import random

thread = 5  # 线程

# 位置
longitude = 113.266365
latitude = 23.17275

# 珠江新城
# longitude = 113.327721
# latitude = 23.125194


# 活动名称
# channels = ['ele_ka_wpmsj_fkp',
#             'nr_10hnshentou',
#             'mrbc_shoutao0907',
#             'cka-oct',
#             'nr_10hbshentou',
#             'nr_1111pzlm',
#             'mrbc_v2',
#             'alipay_shh_201909',
#             'bd_cps02',
#             'bd_yizhifu',
#             'bd_swuc',
#             'waimaijie_31']
# bigHongbaoChannels = [
#     'cka-oct',
#    # 'bd_yizhifu',
#    # 'bd_cps02',
#    # 'alipay_shh_201909'
# ]


# 反向地理编码
def updateGeo(sid):
    global latitude, longitude
    url = 'https://h5.ele.me/restapi/bgs/poi/reverse_geo_coding?latitude=' + str(latitude) + '&longitude=' \
          + str(longitude)
    res = requests.get(url, headers={'cookie': 'SID=' + sid})
    rep = json.loads(res.text)
    latitude = rep['latitude']
    longitude = rep['longitude']
    return rep


def getHongbao1(sid, channel,
                ua='Mozilla/5.0 (Linux; Android 9; MI MAX 3 Build/PKQ1.190714.001; wv) AppleWebKit/537.36 ('
                   'KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044904 Mobile '
                   'Safari/537.36 MMWEBID/386 MicroMessenger/7.0.7.1521(0x27000735) Process/tools NetType/4G '
                   'Language/zh_CN'):
    updateGeo(sid)
    userId = SID.getUserId(sid)
    interUrl = 'https://h5.ele.me/restapi/traffic/users/' + userId + '/lottery'
    headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
               'x-shard': 'loc=' + str(longitude) + ',' + str(latitude) + ';', }
    data = {'userId': userId, 'channel': channel, 'longitude': longitude, 'latitude': latitude}
    res = requests.post(interUrl, headers=headers, data=data)
    volume = json.loads(res.text)
    # print(volume)
    if volume['message'] == '成功':
        print('红包' + channel, str(volume['sum']['threshold']) + '-' + str(volume['sum']['amount']))
    else:
        print('红包' + channel, volume['message'])

    return volume['message']


def getHongbao2(sid,
                ua='Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.20.0.32 Mobile Safari/537.36 UCBS/3.20.0.32_191012190528 NebulaSDK/1.8.100112 Nebula AlipayDefined(nt:WIFI,ws:393|0|2.75) AliApp(AP/10.1.78.7000) AlipayClient/10.1.78.7000 Language/zh-Hans useStatusBar/true isConcaveScreen/false Region/CN'):
    url = 'https://h5.ele.me/restapi/lego/query_module_content?latitude=' + str(latitude) + '&longitude=' + str(
        longitude) + '&codes[]=module_home_coupon_popup'
    headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
               'x-shard': 'loc=' + str(longitude) + ',' + str(latitude)}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return

    volume = json.loads(res.text)
    if volume['data']:
        volume = volume['data']
        volume = volume[0]
        volume = volume['items']
        volume = volume[0]
        volume = volume['content']
        # print(volume)
        print('口碑首页红包：' + volume['title'], str(volume['discountThreshold']) + '-' + str(volume['discountAmount']))


def getHongbao3(sid,
                ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/PKQ1.190714.001 Eleme/8.26.4 Channel/xiaomi ID/1da84041-3494-3fc4-a535-3421622db4b8; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware: Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):
    startUrl = 'https://h5.ele.me/restapi/activation/api/partner/enterPlace'
    url = 'https://h5.ele.me/restapi/activation/api/chess/movePosition'
    headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
               'x-shard': 'loc=' + str(longitude) + ',' + str(latitude),
               'x-ua': 'RenderWay/H5 AppName/elmc Longitude/str(longitude) Latitude/str(latitude) DeviceId/1da84041-3494-3fc4-a535-3421622db4b8'}
    data = {"comeChannel": "app", "entrance": "app", "longitude": str(longitude), "latitude": str(latitude)}

    # 开始游戏
    requests.get(startUrl, headers=headers, data=data)

    # 跳3次
    for i in range(0, 3):
        res = requests.post(url, headers=headers, data=data)
        if res.status_code != 200:
            return

        volume = json.loads(res.text)
        print(volume['message'])
        if '没有足够的体力值' == volume['message']:
            break
        volume = volume['data']
        if volume:
            volume = volume['rewards']
            if volume and len(volume) != 0:
                volume = volume[0]
                volume = volume['chessRewards']
                volume = volume[0]
                print('双11跳一跳红包：' + volume['title'], str(volume['threshold']) + '-' + str(volume['amount']))


def getHongbao4(sid,
                ua='Rajax/1 Lenovo_L38111/Kunlun2 Android/9 Display/PKQ1.190714.001 Eleme/8.26.4 Channel/xiaomi ID/1da84041-3494-3fc4-a535-3421622db4b8; KERNEL_VERSION:4.9.112-perf+ API_Level:28 Hardware: Mozilla/5.0 (Linux; U; Android 9; zh-CN; Lenovo L38111 Build/PKQ1.190714.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.21.0.24 Mobile Safari/537.36 AliApp(ELMC/8.26.4) UCBS/2.11.1.1 TTID/offical WindVane/8.5.0,UT4Aplus/0.2.16'):
    url = 'https://h5.ele.me/restapi/traffic/berlin/issue'
    headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
               'x-shard': 'loc=' + str(longitude) + ',' + str(latitude),
               'x-ua': 'RenderWay/H5 AppName/elmc Longitude/str(longitude) Latitude/str(latitude) DeviceId/1da84041-3494-3fc4-a535-3421622db4b8'}
    data = {"activityId": "RC_1074","couponId": 365978355,"comChannel": "H5","longitude": str(longitude),"latitude": str(latitude)}

    # 开始游戏
    res = requests.post(url, headers=headers, data=data)
    print(res.text)


async def start(sid):
    try:
        # 随机切换地址
        global longitude, latitude
        lola_key = list(Data.lola.keys())[random.randint(0, len(list(Data.lola.keys())))]
        longitude = Data.lola[lola_key][0]
        latitude = Data.lola[lola_key][1]
        # longitude = Data.lola['云南'][0]
        # latitude = Data.lola['云南'][1]
        print("定位:", lola_key)
        for channel in Data.channels:
            if getHongbao1(sid, channel) == '未登录':
                return
        updateGeo(sid)
        getHongbao2(sid)
        # getHongbao3(sid)
        # getHongbao4(sid)
    except:
        print('领取出错')


def run():
    sids = SID.getSIDS('../../data/onekey/SID.txt')
    i = 0
    currentTime = time.time()
    while i < len(sids):
        loop.run_until_complete(start(sids[i]))
        i += 1
        if i % 5 == 0:
            print('领红包剩余时间：', (time.time() - currentTime) / 5 * (len(sids) - i))
            currentTime = time.time()


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    run()
