from utils import *

#################
### DECK ########
#################
class deck:
    def __init__(self):
        self.cardsdealt = []

    def dealone(self):
        masterNum = randint(0,51)
        #masterNum += 1
        if masterNum in self.cardsdealt:
            altCard = self.dealone()
            masterNum = altCard.masterNum
        self.cardsdealt.append(masterNum)
        #(suit,cardNum) = convertNumberCard(masterNum)
        cardObj = card(masterNum)
        cardObj.playedStatus = 0        ######### 0 == IN HAND
        return cardObj
    def display(self):
        print("remaining cards: %d\n",52-len(self.cardsdealt))



#################
### MASTERCARD ##
#################
class card:
    #def __init__(self, player, masterNum):
    def __init__(self, masterNum):
        #self.player = player
        self.masterNum = masterNum
        self.playedStatus = 0 ######### 0 == IN HAND
                              ######### 1 == PLAYED
                              #########-1 == IN KITTEN
        #self.initCard()
    #def initCard(self):
    def suit(self):
        suitNum = self.masterNum / 13
        if suitNum == 0:
            return "clubs"
        elif suitNum == 1:
            return "diamonds"
        elif suitNum == 2:
            return "hearts"
        elif suitNum == 3:
            return "spades"
        else:
            print("error assigning suit")
            return -1
    def num(self):
        return (self.masterNum % 13) +1
    def countValue(self):
        num = self.num()
        if num <= 10:
            return num
        else:
            return 10
    def cardId(self):
        return {'suit' : self.suit(),
                'cardNumber':self.num(), 
                'cardName' : self.name() }
#    def cardIdString(self):
#        return self.player + " --- " + self.name() + " of " + self.suit()
#    def cardJson(self):
#        return "{ 'player':'" + self.player + "', " + \
#                " 'suit':'"   + self.suit()   + "', " + \
#                " 'cardName':'"+ self.name() + "' }"
    def name(self):
        num = self.num()
        if num == 1:
            cardName = "Ace"
        elif num == 11:
            cardName = "Jack"
        elif num == 12:
            cardName = "Queen"
        elif num == 13:
            cardName = "King"
        else:
            cardName = str(num)
        return cardName
