class card:
    def __init__(self, player, masterNum, suit, cardNum):
        self.player = player
        self.masterNum = masterNum
        self.suit = suit
        self.cardNum = cardNum
        #self.playedStatus = 0 ######### 0 == IN HAND
                              ######### 1 == PLAYED
                              #########-1 == IN KITTEN
    def cardValue(self):
        if self.cardNum <= 10:
            value = self.cardNum
        else:
            value = 10
        return value
    def cardId(self):
        return {'player':self.player,
                'suit' : self.suit,
                'cardNumber':self.cardNum, 
                'cardName' : self.cardName() }
    def cardName(self):
        if self.cardNum == 1:
            cardName = "Ace"
        elif self.cardNum == 11:
            cardName = "Jack"
        elif self.cardNum == 12:
            cardName = "Queen"
        elif self.cardNum == 13:
            cardName = "King"
        else:
            cardName = str(self.cardNum)
        return cardName

# FORMAT of dictionary for a card:
# cardDict = {'player': 1, 'suit': 'hearts',
#             'cardNumber': 2, 'cardName': '2'}
def printCard(cardObj):
    #if (cardObj.cardNum < 11 and cardObj.cardNum > 1):
    #    print("(%s-%d) suit: %s, card: %d" % \
    #       (cardObj.player, cardObj.masterNum, cardObj.suit,cardObj.cardNum))
    #else:
    card = cardObj.cardId()
    print("%s --- %s of %s" % (card['player'], card['cardName'],
                               card['suit']))
    return card

def convertNumberCard(number):
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
    cardNumber = (number % 13) +1
    return (suit,cardNumber)


