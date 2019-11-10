import requests
import Data
import re


def getSIDS(url='../data/SID.txt', otherUrl='../../data/onekey/card.txt'):
    # 读取文件SID
    # txt = '../data/SID.txt'
    sids = []
    cards = []
    with open(url, encoding='gbk') as f:
        for line in f.readlines():
            if line.find('SID=') != -1:
                start = line.find('SID=') + 4
                #             print(line[start:start+36])
                sids.append(line[start:start + 36])
            elif line.find('COM') == -1:
                cards.append(line)
    # 保存其他卡
    print(cards)
    with open(otherUrl, 'w', encoding='gbk') as f:
        for line in list(set(cards)):
            f.write(str(line))
    # 去重
    sids = list(set(sids))
    print('共', len(sids), '个SID')
    return sids


def getUserId(sid):
    userIdUrl = 'https://h5.ele.me/restapi/eus/v2/current_user?info_raw={}'
    res = requests.get(userIdUrl, headers={'cookie': 'SID=' + sid})
    if res.status_code == 200:
        return res.text
    else:
        return ''


# 行排序
def sortList1(baos):
    # ['品质31-5 过期时间2019-10-08', '果蔬39-7过期时间2019-10-08', '品质30-5 过期时间2019-10-08']
    return sorted(baos, key=lambda x: int(re.search("(\\d+)", x.split("-")[1]).group()), reverse=True)


# 列排序
def sortList2(datas):
    return sorted(datas, key=lambda x: int(re.search("(\\d+)", x[50:].split("-")[1]).group()), reverse=True)


def checkHongbao2(hongbaos, url='../data/hongbaoSID.txt'):
    datas = []
    for hongbao in hongbaos:
        baos = []
        sid = ''
        phone = ''
        for i in range(0, len(hongbao)):
            if 'name' in hongbao[i].keys():
                if hongbao[i]['name'].find('品质') != -1 and hongbao[i]['name'].find('果蔬') == -1 and hongbao[i][
                    'reduce_amount'] >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '品质' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('通用') != -1 and hongbao[i]['name'].find('果蔬') == -1 and hongbao[i][
                    'reduce_amount'] >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '通用' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
                        hongbao[i]['end_date'])
                elif hongbao[i]['name'].find('心意') != -1 and hongbao[i]['reduce_amount'] >= 5:
                    if 'variety' in hongbao[i].keys():
                        if 'phone' in hongbao[i]['variety'].keys():
                            phone = hongbao[i]['variety']['phone']
                    baos.append(
                        '心意' + str(hongbao[i]['sum_condition']) + '-' + str(hongbao[i]['reduce_amount']) + '过期' +
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
    file = open(url, 'w')
    for line in datas:
        file.write(str(line) + '\n')
    file.close()

#替换红包名字
def replaceName(name):
    if name in Data.replace:
        return Data.replace[name]
    return name


def checkHongbao(hongbaos, url='../data/hongbaoSID.txt', filters=Data.filters):
    print(filters)
    datas = []
    datas_fruits = []
    datas_limits = []
    for hongbao in hongbaos:
        baos = []
        # 水果红包
        fruits = []
        #有限制
        limits = []

        sid = ''
        phone = ''
        for i in range(0, len(hongbao)):
            if 'name' in hongbao[i].keys():
                if hongbao[i]['reduce_amount'] > 5 or (hongbao[i]['reduce_amount'] == 5 and (
                        hongbao[i]['sum_condition'] < 15 or not hongbao[i]['sum_condition'])):
                    if 'description_map' in hongbao[i].keys():
                        # 排除商家红包
                        if '13' not in hongbao[i]['description_map']:
                            # 排除水果卷
                            if '果蔬' not in hongbao[i]['name'] and '水果' not in hongbao[i]['name']:
                                bao = replaceName(str(hongbao[i]['name'])) + str(hongbao[i]['sum_condition']) + '-' + str(
                                    hongbao[i]['reduce_amount'])
                                if bao not in filters:
                                    if '8' in hongbao[i]['description_map']:
                                        limits.append(bao + '['+hongbao[i]['description_map']['8']+']过期' + hongbao[i]['end_date'])
                                    elif '7' in hongbao[i]['description_map']:
                                        limits.append(bao + '[' + hongbao[i]['description_map']['7'] + ']过期' + hongbao[i]['end_date'])
                                    else:
                                        baos.append(bao + '过期' + hongbao[i]['end_date'])
                            # 水果卷另外放
                            else:
                                fruits.append(replaceName(str(hongbao[i]['name'])) + str(hongbao[i]['sum_condition']) + '-' + str(
                                    hongbao[i]['reduce_amount']) + '过期' + hongbao[i]['end_date'])

                if 'variety' in hongbao[i].keys():
                    if 'phone' in hongbao[i]['variety'].keys():
                        phone = hongbao[i]['variety']['phone']

            if 'SID' in hongbao[i].keys():
                sid = hongbao[i]['SID']
        if len(baos) != 0:
            baos = sortList1(baos)
            datas.append(str(phone) + '----SID=' + sid + del0(str(baos)))
            print(str(phone) + '----SID=' + sid, baos)

        if len(fruits) != 0:
            fruits = sortList1(fruits)
            datas_fruits.append(str(phone) + '----SID=' + sid + del0(str(fruits)))
            print(str(phone) + '----SID=' + sid, fruits)

        if len(limits) != 0:
            limits = sortList1(limits)
            datas_limits.append(str(phone) + '----SID=' + sid + del0(str(limits)))
            print(str(phone) + '----SID=' + sid, limits)

    # 保存有红包SID
    datas = sortList2(datas)
    datas_fruits = sortList2(datas_fruits)
    datas_limits = sortList2(datas_limits)
    # file = open(url, 'w')
    # for line in datas:
    #     file.write(str(line) + '\n')
    # file.close()
    with open(url, 'w') as f:
        f.write("吃吃吃合集:\n")
        for line in datas:
            f.write(str(line) + '\n')

        f.write("\n\n\n\n有限制合集:\n")
        for line in datas_limits:
            f.write(str(line) + '\n')

        f.write("\n\n\n\n果蔬合集:\n")
        for line in datas_fruits:
            f.write(str(line) + '\n')


# 删除.0
def del0(s):
    return str(s).replace(old='.0', new='')
