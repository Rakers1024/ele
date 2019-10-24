import requests
import json
import time
import re
import SID


def sortList1(baos):
    # ['品质31-5 过期时间2019-10-08', '果蔬39-7过期时间2019-10-08', '品质30-5 过期时间2019-10-08']
    baos = sorted(baos, key=lambda x: int(re.search("(\d+)", x.split("-")[1]).group()), reverse=True)
    return baos


def sortList2(datas):
    return sorted(datas, key=lambda x: int(re.search("(\d+)", x[50:].split("-")[1]).group()), reverse=True)


def checkHongbao(hongbaos):
    datas = []
    for hongbao in hongbaos:
        baos = []
        sid = ''
        phone = ''
        for i in range(0, len(hongbao)):
            if 'name' in hongbao[i].keys():
                if hongbao[i]['name'].find('品质') != -1 and hongbao[i]['name'].find('果蔬') == -1 and hongbao[i]['reduce_amount'] >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '品质' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('通用') != -1 and hongbao[i]['name'].find('果蔬') == -1 and hongbao[i]['reduce_amount'] >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '通用' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('王牌') != -1 and hongbao[i]['reduce_amount'] >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '王牌' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('果蔬商超') != -1 and hongbao[i]['reduce_amount'] >= 7:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '果蔬' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('下午茶') != -1 and hongbao[i]['reduce_amount'] >= 7:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '下午茶' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('夜宵') != -1 and hongbao[i]['reduce_amount'] >= 7:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '夜宵' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
            if 'SID' in hongbao[i].keys():
                sid = hongbao[i]['SID']
        if len(baos) != 0:
            baos = sortList1(baos)
            datas.append(str(phone) + '----SID=' + sid + str(baos))
            print(str(phone) + '----SID=' + sid, baos)
    # 保存有红包SID
    datas = sortList2(datas)
    file = open('../data/hongbaoSID.txt', 'w')
    for line in datas:
        file.write(str(line) + '\n')
    file.close()


def main():
    sids = SID.getSIDS()
    newSids = []
    hongbaos = []
    userIdUrl = 'https://h5.ele.me/restapi/eus/v2/current_user?info_raw={}'
    hongbaoUrlStart = 'https://h5.ele.me/restapi/promotion/v1/users/'
    hongbaoUrlEnd = '/coupons?'
    for sid in sids:
        try:
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': 'SID=' + sid,
                'referer': 'https://h5.ele.me/profile/benefit/',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) '
                              'AppleWebKit/537.36 ( '
                              'KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
                'x-shard': 'loc=0,0'
            }
            res = requests.get(userIdUrl, headers=headers)
            userId = res.text

            res = requests.get(hongbaoUrlStart + userId + hongbaoUrlEnd, headers=headers)
            hongbao = json.loads(res.text)

            if type(hongbao) != list:
                print('SID无效')
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

            # 延迟3秒
            time.sleep(0.05)
        except:
            continue
    # 保存有效SID
    file = open('../data/new_SID.txt', 'w')
    for line in newSids:
        file.write(str(line) + '\n')
    file.close()
    checkHongbao(hongbaos)
    print('运行结束')


if __name__ == '__main__':
    main()

