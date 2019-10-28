import requests
import json
import time
import re
import SID





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

def checkHongbao2(hongbaos):
    datas = []
    for hongbao in hongbaos:
        baos = []
        sid = ''
        phone = ''
        for i in range(0, len(hongbao)):
            if 'name' in hongbao[i].keys():
                if hongbao[i]['name'].find('品质') != -1 and hongbao[i]['name'].find('果蔬') == -1 and float(hongbao[i]['amount']) >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '品质' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('通用') != -1 and hongbao[i]['name'].find('果蔬') == -1 and float(hongbao[i]['amount']) >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '通用' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('王牌') != -1 and float(hongbao[i]['amount']) >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '王牌' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('果蔬商超') != -1 and float(hongbao[i]['amount']) >= 7:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '果蔬' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('下午茶') != -1 and float(hongbao[i]['amount']) >= 7:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '下午茶' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('夜宵') != -1 and float(hongbao[i]['amount']) >= 7:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '夜宵' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['amount']) + '过期' +
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
    hongbaoUrlStart = 'https://h5.ele.me/restapi/promotion/v1/users/'
    hongbaoUrlEnd = '/coupons?cart_sub_channel=alipay%3Akoubei&latitude=23.311341&longitude=113.562687'
    for sid in sids:
        try:
            headers = {
                'cookie': 'SID=' + sid,
                'user-agent': 'Mozilla/5.0 (Linux; U; Android 9; zh-CN; MI MAX 3 Build/PKQ1.190714.001) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.20.0.32 '
                              'Mobile Safari/537.36 UCBS/3.20.0.32_191012190528 NebulaSDK/1.8.100112 Nebula '
                              'AlipayDefined(nt:4G,ws:393|0|2.75) AliApp(AP/10.1.78.7000) AlipayClient/10.1.78.7000 '
                              'Language/zh-Hans useStatusBar/true isConcaveScreen/true Region/CN '

            }
            print('当前时间', time.time())
            res = requests.get(hongbaoUrlStart + SID.getUserId(sid) + hongbaoUrlEnd, headers=headers)
            # res = requests.post(tempUrl, headers=headers)
            # print(res.text)
            hongbao = json.loads(res.text)
            # if not hongbao['groups']:
            #     print('SID无效')
            # else:
            #     newSids.append('SID=' + sid)
            #     hs = []
            #     hongbao = hongbao['groups']
            #     for h in hongbao:
            #         # print(h)
            #         if float(h['amount']) > 1:
            #             hs.append(str(h['name']) + str(h['threshold']) + '-' + str(h['amount']))
            #     if len(hongbao) != 0:
            #         print('SID=' + sid + '有效,有' + str(len(hongbao)) + "个红包", hs)
            #         # 添加sid
            #         hongbao.append({'SID': sid})
            #         hongbaos.append(hongbao)

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
            time.sleep(0.5)
        except:
            continue
    # 保存有效SID
    file = open('../data/new_SID.txt', 'w')
    for line in newSids:
        file.write(str(line) + '\n')
    file.close()
    checkHongbao(hongbaos)
    # checkHongbao2(hongbaos)
    print('运行结束')


if __name__ == '__main__':
    main()

