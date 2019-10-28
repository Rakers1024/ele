import requests
import asyncio
import json
import time
import re
import SID
import os

thread = 5  # 线程
newSids = []
hongbaos = []

rootPath = '../../data/sid/' + str(time.time()).split('.')[0]+'/'


async def getHongbaos(sid):
    global newSids, hongbaos
    hongbaoUrlStart = 'https://h5.ele.me/restapi/promotion/v1/users/'
    hongbaoUrlEnd = '/coupons?cart_sub_channel=alipay%3Akoubei&latitude=23.311341&longitude=113.562687'

    headers = {
        'cookie': 'SID=' + sid,
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI MAX 3 Build/PKQ1.190714.001) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.20.0.32 '
                      'Mobile Safari/537.36 UCBS/3.20.0.32_191012190528 NebulaSDK/1.8.100112 Nebula '
                      'AlipayDefined(nt:4G,ws:393|0|2.75) AliApp(AP/10.1.78.7000) AlipayClient/10.1.78.7000 '
                      'Language/zh-Hans useStatusBar/true isConcaveScreen/true Region/CN '
    }
    try:
        res = requests.get(hongbaoUrlStart + SID.getUserId(sid) + hongbaoUrlEnd, headers=headers)
        hongbao = json.loads(res.text)
        if type(hongbao) != list:
            print('SID=' + sid + '无效')
        else:
            newSids.append('SID=' + sid)
            hs = []
            for h in hongbao:
                if h['reduce_amount'] >= 5:
                    hs.append(h['name'] + str(h['sum_condition']) + '-' + str(h['reduce_amount']))
            if len(hongbao) != 0:
                print('SID=' + sid + '有效,有' + str(len(hongbao)) + "个红包", hs)
                # 添加sid
                hongbao.append({'SID': sid})
                hongbaos.append(hongbao)

    except:
        return


def run():
    os.mkdir(rootPath)
    startTime = time.time()
    sids = SID.getSIDS('../../data/SID.txt')
    i = 0
    while i < len(sids):
        loop.run_until_complete(getHongbaos(sids[i]))
        i += 1

    # 保存有效SID
    file = open(rootPath+'new_SID.txt', 'w')
    for line in newSids:
        file.write(str(line) + '\n')
    file.close()
    SID.checkHongbao(hongbaos, url=rootPath+'hongbaoSID.txt')
    print('运行结束，用时', time.time() - startTime)


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    run()
