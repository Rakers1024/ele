import requests
import json
import time
import SID


class Receive(object):

    def __init__(self, longitude=113.266365, latitude=23.17275):
        self.longitude = longitude
        self.latitude = latitude

        # 领红包接口
        self.inter1Start = 'https://h5.ele.me/restapi/traffic/users/'
        self.inter1End = '/lottery'

    # 反向地理编码
    def updateGeo(self, sid):
        url = 'https://h5.ele.me/restapi/bgs/poi/reverse_geo_coding?latitude=' + str(
            self.latitude) + '&longitude=' + str(
            self.longitude)
        res = requests.get(url, headers={'cookie': 'SID=' + sid})
        # print(res.text)
        rep = json.loads(res.text)
        self.latitude = rep['latitude']
        self.longitude = rep['longitude']
        return rep

    def getHongbao1(self, sid, channel,
                    ua='Mozilla/5.0 (Linux; Android 9; MI MAX 3 Build/PKQ1.190714.001; wv) AppleWebKit/537.36 (KHTML, '
                       'like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044904 Mobile Safari/537.36 '
                       'MMWEBID/386 MicroMessenger/7.0.7.1521(0x27000735) Process/tools NetType/4G Language/zh_CN'):
        userId = SID.getUserId(sid)
        interUrl = 'https://h5.ele.me/restapi/traffic/users/' + userId + '/lottery'
        headers = {'user-agent': ua, 'cookie': 'SID=' + sid,
                   'x-shard': 'loc=' + str(self.longitude) + ',' + str(self.latitude) + ';', }
        data = {'userId': userId, 'channel': channel, 'longitude': self.longitude, 'latitude': self.latitude}

        res = requests.post(interUrl, headers=headers, data=data)
        volume = json.loads(res.text)
        if volume['message'] == '成功':
            print('红包' + channel, str(volume['sum']['threshold']) + '-' + str(volume['sum']['amount']))
        else:
            print('红包' + channel, volume['message'])


if __name__ == '__main__':
    rec = Receive()
    for sid in SID.getSIDS():
        try:
            rec.updateGeo(sid)
            rec.getHongbao1(sid, "ele_ka_wpmsj_fkp")
            rec.getHongbao1(sid, "nr_10hnshentou")
            rec.getHongbao1(sid, "mrbc_shoutao0907")
            rec.getHongbao1(sid, "cka-oct")
            rec.getHongbao1(sid, "nr_10hbshentou")
            rec.getHongbao1(sid, "nr_1111pzlm")
            rec.getHongbao1(sid, "mrbc_v2")
            rec.getHongbao1(sid, "alipay_shh_201909")
            time.sleep(0.5)
        except:
            continue
