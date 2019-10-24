import requests
import json
import SID

hongbaoUrlStart = 'https://h5.ele.me/restapi/promotion/v1/users/'
hongbaoUrlEnd = '/coupons?'

if __name__ == '__main__':
    sid = 'HBSPtHUyluguLgEAN1af7vqiZrnqIxT3VJpw'
    userId = SID.getUserId(sid)
    res = requests.get(hongbaoUrlStart + userId + hongbaoUrlEnd, headers={'cookie': 'SID=' + sid})
    hongbaos = json.loads(res.text)

    for hongbao in hongbaos:
        print(hongbao['name'])
        print('来源', hongbao['h5_scheme'])
        print(str(hongbao['sum_condition'])+'-'+str(hongbao['reduce_amount']))
        print('=================================================')