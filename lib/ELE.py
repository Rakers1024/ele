from bs4 import BeautifulSoup
import requests
import asyncio
import time
import FaKa
import json
import SID

onekeyRootPath = '../../data/onekey/'
sidPath = onekeyRootPath + 'SID.txt'

newSids = []
hongbaos = []

# 保存sid对应的位置等信息，以备下次领取
cookies = {}

def queryFaka(queryModel=1, fileName='numbers.txt'):
    timek = 100
    loop = asyncio.get_event_loop()
    if queryModel == 1:
        numbers = FaKa.getNumbers(onekeyRootPath+'save_numbers.txt')
        timek = 100
    else:
        numbers = FaKa.getNumbers(onekeyRootPath+fileName)
        timek = 1000
    i = 0
    currentTime = time.time()
    while i < len(numbers):
        loop.run_until_complete(searchCard(numbers[i], queryModel=queryModel))
        i += 1
        if i % timek == 0:
            print('查卡平均剩余时间：', (time.time() - currentTime)/timek*(len(numbers)-i))
            currentTime = time.time()


# 查询红包
def queryHongbaos():
    global cookies
    cookies = SID.readCookies()
    loop = asyncio.get_event_loop()
    startTime = time.time()
    sids = SID.getSIDS(sidPath)
    i = 0
    currentTime = time.time()
    while i < len(sids):
        loop.run_until_complete(getHongbaos(sids[i]))
        i += 1
        if i % 10 == 0:
            print('查红包平均剩余时间：', (time.time() - currentTime)/10*(len(sids)-i))
            currentTime = time.time()

    # 保存有效SID
    file = open(onekeyRootPath + 'save_SID.txt', 'w')
    for line in newSids:
        file.write(str(line) + '\n')
    file.close()
    SID.checkHongbao(hongbaos, url=onekeyRootPath + 'hongbaoSID_'+str(time.time()).split('.')[0]+'.txt')
    print('运行结束，用时', time.time() - startTime)
    SID.writeCookies(cookies=cookies)

def writeFile(lis):
    with open(sidPath, 'a') as f:
        for line in lis:
            try:
                f.write(str(line) + '\n')
            except:
                continue


# 有卡的保存记录以备下次查询
def writeNumber(number, isRun=True):
    if isRun:
        with open(onekeyRootPath + 'save_numbers.txt', 'a') as f:
            f.write(number + '\n')


# 定义异步函数,查卡
async def searchCard(number, queryModel=1):
    url = 'http://www.bxfaka.com/orderquery2?st=contact&kw=' + str(number)
    try:
        res = requests.get(url, timeout=5)
    except:
        try:
            res = requests.get(url, timeout=5)
        except:
            return
    if res.status_code == 200:
        cardInfo = []
        soup = BeautifulSoup(res.text, 'html5lib')
        for link in soup.select('.QueTab tr b'):
            if link.text.find('订单未付款') < 0 and link.text.find('您的当前IP') < 0 and link.text.find('该订单有取卡密码') < 0:
                cardInfo.append(link.text)
        if len(cardInfo) != 0:
            if queryModel == 1:
                writeNumber(number, isRun=False)
            else:
                writeNumber(number)
            print(cardInfo)
        else:
            pass
        writeFile(cardInfo)
    else:
        print('请求失败', res.status_code)


async def getHongbaos(sid):
    global newSids, hongbaos, cookies
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
    if sid not in cookies:
        cookies[sid] = {}
    if 'userId' in cookies[sid]:
        userId = cookies[sid]['userId']
        # 为0说明是已经登记得已失效得sid，故结束
        if userId == '0':
            return
    else:
        userId = SID.getUserId(sid)
        cookies[sid]['userId'] = userId
    try:
        res = requests.get(hongbaoUrlStart + userId + hongbaoUrlEnd, headers=headers)
        hongbao = json.loads(res.text)
        if type(hongbao) != list:
            print('SID=' + sid + '无效')
        else:
            newSids.append('SID=' + sid)
            hs = []
            for h in hongbao:
                if h['reduce_amount'] >= 5:
                    hs.append(h['name'] + str(h['sum_condition']) + '-' + str(h['reduce_amount']))
            if len(hs) != 0:
                hs = SID.sortList1(hs)
            if len(hongbao) != 0:
                print('SID=' + sid + '有效,有' + str(len(hongbao)) + "个红包", hs)
                # 添加sid
                hongbao.append({'SID': sid})
                hongbaos.append(hongbao)

    except:
        return
