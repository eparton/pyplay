from utils import *

#################
### GAME ########
#################
class game:
    def __init__(self):
        self.points = [0,0]
        #self.deck = deck
    def shuffle(self):
        self.deck = deck()
    def gameOver(self):
        if self.points[ME] > 120:
            return ME
        if self.points[OPP] > 120:
            return OPP
        return -1

#################
### DECK ########
#################
class deck:
    def __init__(self):
        self.cardsdealt = []

    def dealone(self, player):
        masterNum = randint(0,51)
        if masterNum in self.cardsdealt:
            altCard = self.dealone(player)
            masterNum = altCard.masterNum
        self.cardsdealt.append(masterNum)
        (suit,cardNum) = convertNumberCard(masterNum)
        cardObj = card(player,masterNum, suit, cardNum)
        cardObj.playedStatus = 0        ######### 0 == IN HAND
        return cardObj
    def display(self):
        print("remaining cards: %d\n",52-len(self.cardsdealt))



#################
### HAND ######## (cardsDealt is class, cardsDealt.handAll are the cards)
#################
class cardsDealt:
    def __init__(self,player):
        self.player=player  ## STRING
        self.handAll = []
        self.handWithCut = []
    def addCard(self,card):
        self.handAll.append(card)
    def discard(self, cardId):
        discardCard = self.handAll[cardId]
        self.handAll[cardId].playedStatus = -1 #########-1 == IN KITTEN
    def setCutCard(self, cut):
        keptCards = returnKeptCards(self.handAll)
        keptCards.append(cut)
        self.handWithCut = keptCards
    def played(self,index):
        #played is 1, discarded is -1, return true if not 0
        return (self.handAll[index].playedStatus != 0)
    def cardsInHand(self): ##count the number left without traversal?
        left = 0
        for i in range(0,HANDSIZE):
            if self.played(i) == 0:
                left += 1
        return left
    def pegOneCard(self,total):     ## returns card VALUE, if peg possible
                                    ## returns 0,          if NO peg possible
        highValue = 0
        for i in range (0,HANDSIZE):
            if (not self.played(i) \
                 and total + self.handAll[i].cardValue() <= 31):
                if self.handAll[i].cardValue() > highValue:
                    cardToPeg = self.handAll[i]
                    highValue = cardToPeg.cardValue()
        if highValue == 0:          ## No more cards to play
            return 0
        cardToPeg.playedStatus = 1             ######### 1 == PLAYED
        cardStr = cardToPeg.cardIdString()
        print("[Pegging: %d ---  %s]" % \
             (cardToPeg.cardValue(),cardStr))
        return cardToPeg.cardValue()

    def countHand(self):
        print("\n******New Hand****** COUNT ALL POINT TYPES:")
        handTotal = 0
        #print("\n\n\nActual cardsDealt:")
        handToCount = self.handWithCut
        printHand(handToCount)
        handTotal += count15s(handToCount)
        handTotal += countPairs(handToCount)
        handTotal += countRuns(handToCount)
        handTotal += countFlush(handToCount)
        handTotal += countSpJack(handToCount)
        return handTotal


#################
### CARD ########
#################
class card:
    def __init__(self, player, masterNum, suit, cardNum):
        self.player = player
        self.masterNum = masterNum
        self.suit = suit
        self.cardNum = cardNum
        self.playedStatus = 0 ######### 0 == IN HAND
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
    def cardIdString(self):
        return self.player + " --- " + self.cardName() + " of " + self.suit
    def cardJson(self):
        return "{ 'player':'" + self.player + "', " + \
                " 'suit':'"   + self.suit   + "', " + \
                " 'cardName':'"+ self.cardName() + "' }"
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

