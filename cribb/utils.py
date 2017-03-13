
class card:
    def __init__(self, player, masterNum, suit, cardNum):
        self.player = player
        self.masterNum = masterNum
        self.suit = suit
        self.cardNum = cardNum
        #self.face = 0
    def cardValue(self):
        if self.cardNum <= 10:
            value = self.cardNum
        else:
            value = 10
        return value



def printCard(cardObj):
    if (cardObj.cardNum < 11 and cardObj.cardNum > 1):
        print("(%s-%d) suit: %s, card: %d" % \
           (cardObj.player, cardObj.masterNum, cardObj.suit,cardObj.cardNum))
    else:
        if cardObj.cardNum == 1:
            cardName = "Ace"
        elif cardObj.cardNum == 11:
            cardName = "Jack"
        elif cardObj.cardNum == 12:
            cardName = "Queen"
        elif cardObj.cardNum == 13:
            cardName = "King"
        else:
            print("Error in card naming: %d" % cardObj.cardNum)
            return
        print("(%s-%d) suit: %s, card: %s" % \
           (cardObj.player, cardObj.masterNum, cardObj.suit, cardName))
    return
