
cards = []
def readFile(url='../../data/onekey/card.txt'):
    global cards
    with open(url, 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            cards.append(line)
    cards = set(cards)
    print('共'+str(len(cards))+'张卡')


def filterEmail():
    mCards = []
    for card in cards:
        if card.find('----') != -1:
            nn = card.split('----')
            if len(nn[1]) == 6:
                print(card)



if __name__ == '__main__':
    readFile()
    # print(cards)
    filterEmail()