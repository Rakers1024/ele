import ELE


if __name__ == '__main__':
    queryModel = 1
    while True:
        try:
            queryModel = int(input('输入运行模式（1快速查询、2整体查询）：'))
        except:
            print('输入错误！')
            continue
        if queryModel != 1 and queryModel != 2:
            print('输入错误！')
        else:
            break
    ELE.queryFaka(queryModel=queryModel, fileName='字典0-500000.txt')
    ELE.queryHongbaos()
