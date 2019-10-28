import requests

url = 'https://h5.ele.me/restapi/booking/v1/carts/checkout'
datas = {"restaurant_id":"E4530637603165996875","entities":[[{"id":1790850103,"sku_id":"100000120439026324","quantity":2,"name":"培根烤盘+1份米","price":12,"stock":9961,"attrs":[],"weight":1,"activity":[],"extra":{},"new_specs":[]}]],"entities_with_ingredient":[[]],"packages":[[]],"geohash":"ww0gsy3hywgh","come_from":"mobile","deliver_time":"","paymethod_id":1,"address_id":2500692872141687,"address_select_by":"user","sig":"c279cef05dcfb15374269bc6d5091f67","hongbao_sn":"","hongbao_action":0,"merchant_coupon_action":1,"merchant_coupon_id":"","user_id":4799808994,"tying_entities":[],"is_ant_diamond_vip":0,"is_pintuan":'null',"cinema_deliver_info":'null',"scene_id":-1,"wechat_unionid":"","hongpon_entities":[],"is_ninja":0,"sub_channel":""}

headers = {
'cookie': 'SID=' + 'Av7OueRoqLeSiF46RaI4LfGfRtm59GWneYyQ',
}

res = requests.post(url, data=datas)
print(res)
print(res.text)
