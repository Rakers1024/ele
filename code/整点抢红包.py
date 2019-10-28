import requests
import json
import time
import SID

timeInfoUrl = 'https://h5.ele.me/restapi/member/v1/sign_in/limit/hongbao/info?channel='
interUrlStart = 'https://h5.ele.me/restapi/member/v1/users/'
interUrlEnd = '/sign_in/limit/hongbao'


def getTimeInfo():
    res = requests.get(timeInfoUrl)
    data = json.loads(res.text)
    print('当前时间:', data['current_at'])
    print('系统时间:', time.time())
    print('下一个领红包时间:', data['next_begin_at'])
    return data['next_begin_at']

def checkTime(startTime):
    return time.time() >= startTime


def start(sid):
    url = interUrlStart + SID.getUserId(sid) + interUrlEnd
    headers = {'cookie': 'SID=' + sid}
    res = requests.post(url, headers=headers, data='channel=')
    print(res.text)


if __name__ == '__main__':
    startTime = getTimeInfo()
    print('运行抢红包中...')
    while True:
        if checkTime(startTime):
            for sid in SID.getSIDS():
                print('当前SID='+str(sid))
                start(sid)
            print('抢红包结束')
            exit(0)
