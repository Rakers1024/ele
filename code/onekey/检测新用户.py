import SID
import time
import requests

cookies = {}
newUserSids = []

# 通过储存的cookies获取userid
def getUserId(sid):
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


def checkNewUser(sid):
    url = 'https://h5.ele.me/restapi/eus/v2/new_user_check'
    res = requests.get(url, headers={'cookie': 'SID=' + sid})
    data = res.json()
    print(data)
    if data['is_new_user']:
        print('新用户SID='+sid)
        newUserSids.append(sid)

def saveSids(sids):
    url = '../../data/onekey/New_User_SID.txt'
    with open(url, 'w') as f:
        for sid in sids:
            f.write('SID='+sid+'\n')


if __name__ == '__main__':
    cookies = SID.readCookies()
    sids = SID.getSIDS('../../data/onekey/SID.txt')

    currentTime = time.time()
    i = 0
    for sid in sids:
        checkNewUser(sid)
        if i % 5 == 0:
            print('领红包剩余时间：', (time.time() - currentTime) / 5 * (len(sids) - i))
            currentTime = time.time()
        i += 1
    saveSids(newUserSids)
    SID.writeCookies(cookies=cookies)