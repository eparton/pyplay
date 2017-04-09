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
    def __init__(self, dealer, hands, deck):
        self.dealer = dealer
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
    def played(self,index):
        #played is 1, discarded is -1, return true if not 0
        return (self.playedCards[index] != 0)
    def cardsInHand(self):
        left = 0
        for i in range(0,HANDSIZE):
            if self.played(i) == 0:
                left += 1
        return left
    def peg(self,total):
        highCard = 0
        pegCardId = 0
        for i in range (0,HANDSIZE):
            if (not self.played(i) \
                 and total + self.cards[i].cardValue() <= 31):
				if self.cards[i].cardValue() > highCard:
					pegCardId = i
					highCard = self.cards[i].cardValue()
        if highCard == 0:
            print("(no more high card)\n")
            return 0
        self.playedCards[pegCardId] = 1
        print("playing Id (i): %d" % pegCardId)
                #print(self.cards)
        printCard(self.cards[pegCardId])
        return self.cards[pegCardId].cardValue()
        #return 0
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
        player = round.dealer
        while (total <= 31):
            pegCardMe = 0
            pegCardOpp = 0
            print("total at while: %d" % total)
            if (player == ME):
                pegCardMe = round.handMe.peg(total)
                total += pegCardMe
                print("total after Me: %d" % total)
                print("player %d left: %d" %(player,round.handMe.cardsInHand()))
            else:
                pegCardOpp = round.handOpp.peg(total)
                total += pegCardOpp
                print("total after Opp: %d" % total)
                print("player %d left: %d" %(player,round.handOpp.cardsInHand()))
            player = switchPlayer(player)
            if (pegCardMe == 0 and pegCardOpp == 0):
                if total == 0: #nothing more to play
                    return 0
                else:
                    print("Got to a count of %d, play again!"%total)
                    return 0
    return 1
def count(round):
    print("COUNT IT UP! (nothing yet)")
    return
def switchPlayer(dealerPlayer):
    return not dealerPlayer
def play():
    GAME = game(deck())
    hands = deal(GAME.deck)
    dealerPlayer = ME
    #print("gameover: %d" % GAME.gameOver())
    while (GAME.gameOver() < 0):
        print("start a round, dealer: %d\n" % dealerPlayer)
        oneRound = round(dealerPlayer,hands, GAME.deck)
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
        dealerPlayer = switchPlayer()
        break

# main
print("Starting")
play()
print("DONE\n")
