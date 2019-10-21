import requests
import time
import SID


def unBindWeibo(sid):
    unBindUrl = 'https://mainsite-restapi.ele.me/eus/v2/users/' + SID.getUserId(sid) + '/sns'
    return requests.delete(unBindUrl, headers={'cookie': 'SID=' + sid}, json={'sns_type': 1}).status_code


if __name__ == '__main__':
    for sid in SID.getSIDS():
        if unBindWeibo(sid) == 200:
            print("SID=%s,解绑微博成功！" % sid)
        else:
            print("SID=%s,解绑微博失败！" % sid)
        time.sleep(0.5)  # 500毫秒一次
    print("运行结束")
