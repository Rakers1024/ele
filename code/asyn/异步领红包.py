import requests
import json
import SID
import asyncio

thread = 5  # 线程

# 位置
longitude = 113.266365
latitude = 23.17275

# 活动名称
channels = ['ele_ka_wpmsj_fkp',
            'nr_10hnshentou',
            'mrbc_shoutao0907',
            'cka-oct',
            'nr_10hbshentou',
            'nr_1111pzlm',
            'mrbc_v2',
            'alipay_shh_201909',
            'bd_cps02',
            'bd_yizhifu',
            'bd_swuc',
            'waimaijie_31']
bigHongbaoChannels = [
    'cka-oct',
    'bd_yizhifu',
    'bd_cps02',
    'alipay_shh_201909'
]


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
    if volume['message'] == '成功':
        print('红包' + channel, str(volume['sum']['threshold']) + '-' + str(volume['sum']['amount']))
    else:
        print('红包' + channel, volume['message'])

    return volume['message']


async def start(sid):
    for channel in bigHongbaoChannels:
       # print('时间', time.time())
        if getHongbao1(sid, channel) == '未登录':
            return


def run():
    # sids = SID.getSIDS('../../data/SID.txt')
    sids = SID.getSIDS('../../data/onekey/SID.txt')
    index = 0
    while index < len(sids):
            loop.run_until_complete(start(sids[index]))
            index += 1


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    run()
