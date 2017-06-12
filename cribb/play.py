from utils import *
from random import randint

ME = 0
OPP = 1
HANDSIZE = 6
print("==========================\nStarting play\n=============\n")

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
class round:
    def __init__(self, dealer, hands, deck):
        self.dealer = dealer
        self.hands = hands
        self.cutCard = deck.dealone("CUT-------------->") ##NAME OF PLAYER
        self.total = 0
        self.currentPlayer = dealer ##dealer a placeholder -- no initial value?
        self.lastPlayer    = dealer ##dealer a placeholder -- no initial value?
    def cut(self):
        return self.cutCard
    def discard(self):
        self.hands[ME].discard(0)
        self.hands[ME].discard(1)
        self.hands[OPP].discard(0)
        self.hands[OPP].discard(1)
    def cardPlayed(self, cardValue):
        self.total += cardValue
        #print("(%s) played %d - total peg play: %d" % (pName(player), pegCard,self.total))
        #print("player %d left: %d" %(player,self.hands[player].cardsInHand()))
        self.lastPlayer = self.currentPlayer
        self.currentPlayer = switchPlayer(self.currentPlayer)
        print("  %d  <peg card %d played>" % (self.total, cardValue))
        return cardValue
    def endCount(self):
        self.currentPlayer = switchPlayer(self.lastPlayer)
        print("ENDING PLAYER: %s" % pName(self.lastPlayer))
        print("Final total: %d (play again?)\n" % self.total)
        
    def pegRound(self):
        self.currentPlayer = switchPlayer(self.dealer) #NON dealer starts pegging
        self.lastPlayer = self.currentPlayer
        while(self.hands[ME].cardsInHand() or self.hands[OPP].cardsInHand()):
            self.total = 0
            print("\nSTART PEG (start player: %s)" % pName(self.currentPlayer))
            while (self.total <= 31):
                # FIRST CHECK IF 31, IN WHICH CASE POINTS GIVEN AND PLAYER CHANGED
                if self.total == 31:
                    print("THIRTYONE exactly for %s"% pName(self.lastPlayer))
                    self.endCount()
                    break
                pegCard = self.hands[self.currentPlayer].pegOneCard(self.total)

                if (pegCard): #played something
                    self.cardPlayed(pegCard)
                else:
                    print("No play possible for player: %s"  % pName(self.currentPlayer))
                    #if self.total == 0: #nothing more to play
                    #    #print("NOTHIGN MORE TO PLAY AT ALL!")
                    #    return 0
                    if self.currentPlayer is not self.lastPlayer: #still give lP chance to play
                        #print("give %s another chance" % pName(self.lastPlayer))
                        self.currentPlayer = switchPlayer(self.currentPlayer)
                        continue
                    elif self.currentPlayer is self.lastPlayer: #Other player already known: NO CARDS
                        #print("None played by %s, COUNT OVER" % pName(self.lastPlayer))
                        self.endCount()
                        break
                    else:
                        print("\n\nNEVER HERE\n\n\n\n\n\n\n\n")
        print("exiting peg>>>>>>>>\n\n")
        return 1
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

def deal(masterDeck):
    handsize=6
    #masterDeck = deck()
    hands = []
    #oneCard = card()
    #player = "ME"
    for player in ("ME","OPP"):
        currentHand = hand(player)
        print("\nHAND for %s:" % player)
        for i in range(0,handsize):
            oneCard = masterDeck.dealone(player)
            currentHand.addCard(oneCard)
            printCard(oneCard)
        hands.append(currentHand)
    return hands

class hand:
    def __init__(self,player):
        self.player=player  ## STRING
        self.cards = []
        #self.playedCards = [0]*HANDSIZE
    def addCard(self,card):
        self.cards.append(card)
    def discard(self, cardId):
        discardCard = self.cards[cardId]
        self.cards[cardId].playedStatus = -1 #########-1 == IN KITTEN
        #print("discarding: %d" % self.cards[cardId].cardNum)
        #self.playedCards[cardId] = -1
    def played(self,index):
        #played is 1, discarded is -1, return true if not 0
        return (self.cards[index].playedStatus != 0)
        #return (self.playedCards[index] != 0)
    def cardsInHand(self): ##count the number left without traversal?
        left = 0
        for i in range(0,HANDSIZE):
            if self.played(i) == 0:
                left += 1
        return left
    def pegOneCard(self,total):     ## returns card VALUE, if peg possible
                                    ## returns 0,          if NO peg possible
        highValue = 0
        #pegCardId = 0
        for i in range (0,HANDSIZE):
            if (not self.played(i) \
                 and total + self.cards[i].cardValue() <= 31):
                if self.cards[i].cardValue() > highValue:
                    cardToPeg = self.cards[i]
                    highValue = cardToPeg.cardValue()
        if highValue == 0:
            #print("(no more high card %s)" % self.player)
            return 0
        cardToPeg.playedStatus = 1             ######### 1 == PLAYED
        cardStr = cardToPeg.cardIdString()
        print("[Pegging: %d ---  %s]" % \
             (cardToPeg.cardValue(),cardStr))
        #printCard(self.cards[pegCardId])
        return cardToPeg.cardValue()
    def printHand(self):
        print("%s PEGGING HAND UPDATE:" % self.player)
        for i in range(0,HANDSIZE):
            #if self.playedCards[i] == -1:
            if self.cards[i].playedStatus == -1:
                state = "discarded KITTEN"
            #elif self.playedCards[i] == 0:
            elif self.cards[i].playedStatus == 0:
                state = "in hand"
            #elif self.playedCards[i] == 1:
            elif self.cards[i].playedStatus == 1:
                state = "played in pegging"
            else:
                print("discarding went horribly wrong")
                return
            print("%s (%s)" % (self.cards[i].cardJson(), state))
def pName(player):
    if player:
        return "OPP"
    return "ME"
def count(round):
    print("===========\nCOUNT IT UP! (nothing yet)\n==========")
    return
def switchPlayer(dealerPlayer):
    return not dealerPlayer
def play():
    #GAME = game(deck())
    GAME = game()
    #hands = deal(GAME.deck)
    dealerPlayer = ME
    roundNo = 0
    #print("gameover: %d" % GAME.gameOver())
    while (GAME.gameOver() < 0):
        print("\nstart round %d, dealer: %s" %(roundNo,pName(dealerPlayer)))
        GAME.shuffle()
        hands = deal(GAME.deck)

        oneRound = round(dealerPlayer,hands, GAME.deck)
        #cutCard = oneRound.cut(GAME.deck)
        #print("cut!: ")
        printCard(oneRound.cutCard)
        oneRound.discard()
        if(not oneRound.pegRound()):
            print("\n********NNOOO*********COULDN'T PEG MORE")
            print("ME hand:")
            oneRound.hands[ME].printHand()
            print("OPP hand:")
            oneRound.hands[OPP].printHand()
        #else:
        #    print("should never get here, delete evntually")
        count(oneRound)
        dealerPlayer = switchPlayer(dealerPlayer)
        roundNo += 1
        if roundNo > 2:
            break

# main
play()
