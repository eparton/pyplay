from random import randint

print("Starting play\n")

class deck:
    # cardsdealt = []

    def __init__(self):
        self.cardsdealt = []

    def dealone(self, player):
        masterNum = randint(0,51)
        if masterNum in self.cardsdealt:
            # print("Already here\n")
            altCard = self.dealone(player)
            masterNum = altCard.masterNum
        self.cardsdealt.append(masterNum)
        (suit,cardNum) = convertNumberCard(masterNum)
        cardObj = card(player,masterNum, suit, cardNum)
        #cardObj.number = master
        #cardObj.suit = suit
        return cardObj

    def display(self):
        print("remaining cards: %d\n",52-len(self.cardsdealt))

class card:
    def __init__(self, player, masterNum, suit, cardNum):
        self.player = player
        self.masterNum = masterNum
        self.suit = suit
        self.cardNum = cardNum
        self.face = 0

def convertNumberCard(number):
    #print("number: %d" % number)
    suitNum = number/13
    if suitNum == 0:
        suit = "clubs"
    elif suitNum == 1:
        suit = "diamonds"
    elif suitNum == 2:
        suit = "hearts"
    elif suitNum == 3:
        suit = "spades"
    else:
        print("error assigning suit")
        return (-1,-1)
    cardNumber = number % 13
    return (suit,cardNumber)

def printCard(cardObj):
    print("(%s-%d) suit: %s, card: %d" % \
           (cardObj.player, cardObj.masterNum, cardObj.suit,cardObj.cardNum))


def deal():
    handsize=6
    masterDeck = deck()
    #oneCard = card()
    player = "ME"
    for player in ("ME","OPP"):
        for i in range(0,handsize):
            oneCard = masterDeck.dealone(player)
            printCard(oneCard)
# main
deal()
print("DONE\n")
