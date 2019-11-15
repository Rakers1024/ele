import re


def setNumbers(lis, url='../../data/card/numbers.txt'):
    with open(url, 'w') as f:
        for l in lis:
            f.write(l + '\n')
        # for i in range(999999):
        #     f.write(str(i)+'\n')


def getNumbers(url='../../data/card/qq.txt'):
    numbers = []
    with open(url, encoding='utf-8') as f:
        for line in f.readlines():
            matchObj = re.match('(\\d+)', line)
            # matchObj = re.match('^(\\d+)', line)
            if matchObj:
                number = matchObj.group()
                if number and len(number) > 4:
                    numbers.append(number)
    numbers = list(set(numbers))
    print('共%d个测试项' % len(numbers))
    # lis = list(set(numbers))
    # # setNumbers(lis)
    return list(set(numbers))
