from utils import printCard,card
from random import randint

ME = 0
OPP = 1
HANDSIZE = 6
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
class round:
    def __init__(self, hands, deck):
        self.handMe = hands[ME]
        self.handOpp = hands[OPP]
        self.cutCard = deck.dealone("CUT")
    def cut(self):
        #return deck.dealone("CUT")
        return self.cutCard
class game:
    def __init__(self, deck):
        self.points = [0,0]
        self.deck = deck
    def gameOver(self):
        if self.points[ME] > 120:
            return ME
        if self.points[OPP] > 120:
            return OPP
        return -1
#class card:
#    def __init__(self, player, masterNum, suit, cardNum):
#        self.player = player
#        self.masterNum = masterNum
#        self.suit = suit
#        self.cardNum = cardNum
#        self.face = 0

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
    cardNumber = (number % 13) +1
    return (suit,cardNumber)

def deal(masterDeck):
    handsize=6
    #masterDeck = deck()
    hands = []
    #oneCard = card()
    #player = "ME"
    for player in ("ME","OPP"):
        currentHand = hand(player)
        for i in range(0,handsize):
            oneCard = masterDeck.dealone(player)
            currentHand.addCard(oneCard)
            printCard(oneCard)
        hands.append(currentHand)
    return hands

class hand:
    def __init__(self,player):
        self.player=player
        self.cards = []
        self.playedCards = [0]*HANDSIZE
    def addCard(self,card):
        self.cards.append(card)
    def discard(self, cardId):
        discardCard = self.cards[cardId]
        print("discarding: %d" % self.cards[cardId].cardNum)
        self.playedCards[cardId] = -1
    def peg(self,total):
        for i in range (0,HANDSIZE - 2):
            if (not self.playedCards[i] \
                 and total + self.cards[i].cardValue() <= 31):
                self.playedCards[i] = 1
                print("i: %d" % i)
                #print(self.cards)
                printCard(self.cards[i])
                return self.cards[i].cardValue()
        return 0
    def printHand(self):
        for i in range(0,HANDSIZE):
            if self.playedCards[i] == -1:
                state = "discarded"
            elif self.playedCards[i] == 0:
                state = "in hand"
            elif self.playedCards[i] == 1:
                state = "played in pegging"
            else:
                print("discarding went horribly wrong")
                return
            print("%d (%s)" % (self.cards[i].cardNum, state))
def discard(round):
    round.handMe.discard(0)
    round.handMe.discard(1)
    round.handOpp.discard(0)
    round.handOpp.discard(1)
def peg(round):
    while (len(round.handMe.cards) > 0  \
           and len(round.handOpp.cards) > 0):
        total = 0
        while (total <= 31):
            print("total at while: %d" % total)
            pegCardMe = round.handMe.peg(total)
            total += pegCardMe
            print("total after Me: %d" % total)
            pegCardOpp = round.handOpp.peg(total)
            total += pegCardOpp
            if (pegCardMe == 0 and pegCardOpp == 0):
                return 0
        
    return 1
def count(round):
    return
def play():
    GAME = game(deck())
    hands = deal(GAME.deck)
    #print("gameover: %d" % GAME.gameOver())
    while (GAME.gameOver() < 0):
        print("got in while")
        oneRound = round(hands, GAME.deck)
        #cutCard = oneRound.cut(GAME.deck)
        print("cut!: ")
        printCard(oneRound.cutCard)
        discard(oneRound)
        if(not peg(oneRound)):
            print("\nCOULDN'T PEG MORE")
            print("ME hand:")
            oneRound.handMe.printHand()
            print("OPP hand:")
            oneRound.handOpp.printHand()
            break
        count(oneRound)
        break

# main
print("Starting")
play()
print("DONE\n")
