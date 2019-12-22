import requests
import SID
sid = 'YJyGZDNCpYhu5oHAmcrWeibnPoLF3AftYidA'
userId = SID.getUserId(sid)
orderId = '3053856883698367732'
url = 'https://restapi.ele.me/bos/v1/users/'+userId+'/orders/'+orderId+'?latitude=24.305599&longitude=113.566253'
headers = {
    'cookie': 'SID=' + sid,
    'X-Shard': 'eosid='+orderId+';loc=113.566253,24.305599'
}

res = requests.post(url, headers=headers)
print(res)
print(res.text)
