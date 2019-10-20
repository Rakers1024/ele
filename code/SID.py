import requests


def getSIDS():
    # 读取文件SID
    txt = '../data/SID.txt'
    sids = []
    with open(txt, encoding='utf-8') as f:
        for line in f.readlines():
            if line.find('SID=') != -1:
                start = line.find('SID=') + 4
                #             print(line[start:start+36])
                sids.append(line[start:start + 36])
    # 去重
    sids = list(set(sids))
    return sids


def getUserId(sid):
    userIdUrl = 'https://h5.ele.me/restapi/eus/v2/current_user?info_raw={}'
    return requests.get(userIdUrl, headers={'cookie': 'SID=' + sid}).text
