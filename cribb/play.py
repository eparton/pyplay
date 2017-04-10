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
    def cut(self):
        return self.cutCard
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
    def peg(self,total):
        highValue = 0
        #pegCardId = 0
        for i in range (0,HANDSIZE):
            if (not self.played(i) \
                 and total + self.cards[i].cardValue() <= 31):
                if self.cards[i].cardValue() > highValue:
                    cardToPeg = self.cards[i]
                    highValue = cardToPeg.cardValue()
        if highValue == 0:
            print("(no more high card %s)" % self.player)
            return 0
        cardToPeg.playedStatus = 1             ######### 1 == PLAYED
        cardStr = cardToPeg.cardIdString()
        print("Pegging: %d ---  %s" % \
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
        return "ME"
    return "OPP"
def discard(round):
    round.hands[ME].discard(0)
    round.hands[ME].discard(1)
    round.hands[OPP].discard(0)
    round.hands[OPP].discard(1)
def pegRound(round):
    player = switchPlayer(round.dealer) #NON dealer starts pegging
    lastPlayer = player
    #while (len(round.hands[ME].cards) > 0  \
    #       and len(round.hands[OPP].cards) > 0):
    while(round.hands[ME].cardsInHand() or round.hands[OPP].cardsInHand()):
        total = 0
        print("\nSTART PEG (start player: %s)" % pName(player))
        while (total <= 31):
            #pegCard = 0
            #print("starttotal (pl: %d): %d" % (player,total))
            pegCard = round.hands[player].peg(total)
            if (pegCard): #played something
                total += pegCard
                #print("(%d) played %d - total peg play: %d" % (player, pegCard,total))
                #print("player %d left: %d" %(player,round.hands[player].cardsInHand()))
                lastPlayer = player
                player = switchPlayer(player)
                print("  %d  <peg card played>" % total)
            #if (pegCard == 0):
            else:
                
                if total == 0: #nothing more to play
                    print("NOTHIGN MORE TO PLAY")
                    return 0
                elif player is not lastPlayer: #still give lP chance to play
                    print("give %s another chance" % pName(lastPlayer))
                    player = switchPlayer(player)
                    continue
                else:
                    if total == 31:
                        print("THIRTYONE exactly for %s"% pName(lastPlayer))
                    print("---------------")
                    round.hands[ME].printHand()
                    round.hands[OPP].printHand()
                    print("ENDING PLAYER: %s" % pName(lastPlayer))
                    #if (player == lastPlayer):
                    #    print("%s got a chance to play twice!\n\n\n\n"\
                    #           % pName(player))
                    player = switchPlayer(player)
                    print("(final %d) play again?"%total)
                    break
                    #return 0
            #else:
                #player = switchPlayer(player)
    print("exiting peg>>>>>>>>\n\n")
    return 1
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
        discard(oneRound)
        if(not pegRound(oneRound)):
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
