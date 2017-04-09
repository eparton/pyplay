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
        #self.handMe = hands[ME]
        #self.handOpp = hands[OPP]
        self.hands = hands
        self.cutCard = deck.dealone("CUT")
    def cut(self):
        #return deck.dealone("CUT")
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
            print("(no more high card)")
            return 0
        self.playedCards[pegCardId] = 1
        #print("playing Id (%d): %d" % (pegCardId,self.cards[pegCardId].cardValue()))
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
    round.hands[ME].discard(0)
    round.hands[ME].discard(1)
    round.hands[OPP].discard(0)
    round.hands[OPP].discard(1)
def peg(round):
    player = switchPlayer(round.dealer) #NON dealer starts pegging
    lastPlayer = player
    #while (len(round.hands[ME].cards) > 0  \
    #       and len(round.hands[OPP].cards) > 0):
    while(round.hands[ME].cardsInHand() or round.hands[OPP].cardsInHand()):
        total = 0
        while (total <= 31):
            #pegCard = 0
            print("starttotal (pl: %d): %d" % (player,total))
            pegCard = round.hands[player].peg(total)
            if (pegCard): #played something
                total += pegCard
                print("(%d) played %d - total peg play: %d" % (player, pegCard,total))
                #print("player %d left: %d" %(player,round.hands[player].cardsInHand()))
                lastPlayer = player
                player = switchPlayer(player)
            #if (pegCard == 0):
            else:
                
                if total == 0: #nothing more to play
                    print("NOTHIGN MORE TO PLAY")
                    return 0
                elif player is not lastPlayer: #still give lP chance to play
                    print("give %d another chance" % lastPlayer)
                    player = switchPlayer(player)
                    continue
                else:
                    print("Got to a count of %d, play again!"%total)
                    print("---------------")
                    round.hands[ME].printHand()
                    round.hands[OPP].printHand()
                    print("ENDING PLAYER: %d\n\n" % lastPlayer)
                    player = switchPlayer(player)
                    break
                    #return 0
            #else:
                #player = switchPlayer(player)
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
        print("\nstart round %d, dealer: %d" % (roundNo,dealerPlayer))
        GAME.shuffle()
        hands = deal(GAME.deck)

        oneRound = round(dealerPlayer,hands, GAME.deck)
        #cutCard = oneRound.cut(GAME.deck)
        print("cut!: ")
        printCard(oneRound.cutCard)
        discard(oneRound)
        if(not peg(oneRound)):
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
print("Starting")
play()
print("DONE\n")
