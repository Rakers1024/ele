from bs4 import BeautifulSoup
import requests
import asyncio
import time
import FaKa
import json
import os

rootPath = '../../data/card/cards/'+str(time.time()).split('.')[0]+'/'
runModel = 1

def writeFile(lis):
    with open(rootPath+'card.txt', 'a') as f:
        for line in lis:
            try:
                f.write(str(line) + '\n')
            except:
                continue


# 有卡的保存记录以备下次查询
def writeNumber(number, isRun=True):
    if isRun:
        with open('../../data/card/new_number.txt', 'a') as f:
            f.write(number + '\n')


# 定义异步函数
async def searchCard(number):

    url = 'http://www.bxfaka.com/orderquery2?st=contact&kw=' + str(number)
    try:
        res = requests.get(url, timeout=5)
    except:
        try:
            res = requests.get(url, timeout=5)
        except:
            return
    if res.status_code == 200:
        cardInfo = []
        soup = BeautifulSoup(res.text, 'html5lib')
        for link in soup.select('.QueTab tr b'):
            if link.text.find('订单未付款') < 0 and link.text.find('您的当前IP') < 0 and link.text.find('该订单有取卡密码') < 0:
                cardInfo.append(link.text)
        if len(cardInfo) != 0:
            if runModel == 1:
                writeNumber(number, isRun=False)
            else:
                writeNumber(number)
            print(cardInfo)
        else:
            pass
        writeFile(cardInfo)
    else:
        print('请求失败', res.status_code)


def saveData(line):
    # dict = {'line': line, 'path': rootPath}
    with open('../../data/card/historyData.json', 'w') as f:
        f.write(str(json.dumps({'line': line, 'path': rootPath})))


def getHistoryData(numberLength):
    global rootPath
    url = '../../data/card/historyData.json'
    if os.path.exists(url):
        with open(url, 'r') as f:
            line = f.readline()
            if line:
                dict = json.loads(line)
                line = int(dict['line'])
                # 创建新的目录跑
                if line + 1000 > numberLength:
                    os.mkdir(rootPath)
                    return 0
                else:
                    rootPath = dict['path']
                    if not os.path.exists(rootPath):
                        os.mkdir(rootPath)
                return line
            else:
                return 0
    else:
        return 0


def run():
    global runModel
    numbers = []
    while True:
        try:
            runModel = int(input('输入运行模式（1快速查询、2整体查询）：'))
        except:
            print('输入错误！')
            continue
        if runModel == 1:
            numbers = FaKa.getNumbers(url='../../data/card/new_number.txt')
            break
        elif runModel == 2:
            numbers = FaKa.getNumbers()
            break
        else:
            print('输入错误！')
    historyLine = getHistoryData(len(numbers))

    FaKa.setNumbers(numbers, url=rootPath+'numbers.txt')

    print('当前开始位置:', historyLine)
    while historyLine < len(numbers):
        loop.run_until_complete(searchCard(numbers[historyLine]))
        historyLine += 1
        if historyLine % 100 == 0:
            saveData(historyLine)
            if historyLine % 1000 == 0:
                print(historyLine)


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    startTime = time.time()
    run()
    print('运行结束,用时', time.time() - startTime)
