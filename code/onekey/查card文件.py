import re

def readCard(file):
    data = []
    with open(file, 'r') as f:
        for line in f.readlines():
            data.append(line.strip('\n'))
    return data

if __name__ == '__main__':
    data = readCard(file='../../data/onekey/card.txt')
    for line in data:
        # print(re.match('[A-Z0-9]{15}', line))
        if re.findall('^卡号：[A-Z0-9]{16}$', line):
            print(re.findall('^卡号：([A-Z0-9]{16})$', line)[0])



