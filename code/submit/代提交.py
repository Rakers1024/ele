import SID
import requests
import json

sid = 'Rq7ykpNf4XB8LHn6CWCPHr35HtZpbv9lYQGA'

if __name__ == "__main__":
    userID = SID.getUserId(sid)
    orderUrl = 'https://h5.ele.me/restapi/bos/v2/users/'+userID+'/orders?limit=1&offset=0'
    headers = {'cookie': 'SID=' + sid}
    res = requests.get(orderUrl, headers=headers)
    data = json.loads(res.text)
    print(data)
    shopNumber = len(data[0]['basket']['group'][0])
    group = data[0]['basket']['group'][0]
    entities = []
    for i in range(0, shopNumber):
        entities.append({
            "id": group[i]['id'],
            "sku_id": group[i]['sku_id'],
            "quantity": group[i]['quantity'],
            "name": group[i]['name'],
            "price": group[i]['price'],
            "stock": 0, # 带改
            "attrs": group[i]['attrs'],
            "weight": 1,
            "activity": [],
            "extra": {},
            "new_specs": group[i]['new_specs']
        })

    orderID = data[0]['unique_id']
    rebuyUrl = 'https://h5.ele.me/restapi/booking/v1/users/'+userID+'/orders/'+orderID+'/rebuy?geohash='
    res = requests.get(rebuyUrl, headers=headers)
    data2 = json.loads(res.text)

    for i in range(0, len(entities)):
        entities[i]['stock'] = data2['foods'][0]['stock']
    print(entities)

    # 获取地址
    addressUrl = 'https://h5.ele.me/restapi/member/v1/users/'+userID+'/addresses'
    res = requests.get(addressUrl, headers=headers)
    address = json.loads(res.text)[0]
    geohash = address['st_geohash']
    addressId = address['id']
    # print(address[])
