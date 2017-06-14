from utils import *
from random import randint
import sys

ME = 0
OPP = 1
INAROWMIN = 5
NUMBEROFDRAWS = 10000
HANDSIZE = 6
HAND6 = 6
HAND5WITHCUT = 5
HAND4WITHOUTCUT = 4
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
        self.total = 0
        ##dealer a placeholder -- no initial value?
        self.currentPlayer = dealer
        self.lastPlayer    = dealer
        self.discard()
        self.setupCut(deck)
    def setupCut(self, deck):
        cutCard = deck.dealone("CUT") ##NAME OF PLAYER
        print("just pulled cut card")
        printCard(cutCard)
        self.hands[ME].setCutCard(cutCard)
        self.hands[OPP].setCutCard(cutCard)
    #def cut(self):
    #    return self.cutCard
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
        print("Final total: %d (play again?)" % self.total)
        
    def pegRound(self):
        self.currentPlayer = switchPlayer(self.dealer) #NON dealer starts pegging
        self.lastPlayer = self.currentPlayer
        while(self.hands[ME].cardsInHand() or self.hands[OPP].cardsInHand()):
            self.total = 0
            print("\nSTART PEG (start player: %s)" % pName(self.currentPlayer))
            while (self.total <= 31):
                if self.total == 31:
                    print("THIRTYONE exactly for %s"% pName(self.lastPlayer))
                    self.endCount()
                    break
                pegCard = self.hands[self.currentPlayer].pegOneCard(self.total)

                if (pegCard): #played something
                    self.cardPlayed(pegCard)
                else:
                    print("No play possible for player: %s"  % pName(self.currentPlayer))
                    if self.currentPlayer is not self.lastPlayer: #still give lP chance to play
                        self.currentPlayer = switchPlayer(self.currentPlayer)
                        continue
                    elif self.currentPlayer is self.lastPlayer: #Other player already known: NO CARDS
                        #None played by %s, COUNT OVER % (self.lastPlayer)
                        self.endCount()
                        break
                    else:
                        print("\n\nNEVER HERE\n\n\n\n\n\n\n\n")
        print("exiting peg>>>>>>>>\n\n")
        return 1
    def count(self):
        print("COUNT IT UP! (in construction..)\n===========")
        pointsME  = self.hands[ME].countHand()
        pointsOPP = self.hands[OPP].countHand()
        print("For the ROUND, ME scores %d and OPP scores %d" % (pointsME,pointsOPP))
        return
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
    hands = []
    for player in ("ME","OPP"):
        currentHand = cardsDealt(player)
        print("HAND for %s:" % player)
        for i in range(0,handsize):
            oneCard = masterDeck.dealone(player)
            currentHand.addCard(oneCard)
            printCard(oneCard)
        hands.append(currentHand)
    return hands

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

def returnKeptCards(hand):
    keptCards = []
    for card in hand:
        if card.playedStatus >= 0: #if NOT discarded KITTEN
            keptCards.append(card)
    ##HARD CODED CONSTANT, NEVER CHANGES:
    if len(keptCards) != HAND4WITHOUTCUT:
        print("ERROR in returnKeptCards")
        sys.exit()
    return keptCards
        
def count15s(hand):
    print("Counting points from 15s..")
    cardValues = []
    for card in hand:
        #if card.playedStatus >= 0: #if NOT discarded KITTEN
        cardValues.append(card.cardValue())
    print(cardValues)
    #myReturn = subsetsum(cardValues, 15)
    #print("OUT with myReturn (bool), got: %r" % myReturn)
    myReturn2 = subset2(cardValues, len(cardValues), "", 15, 0)
    print("OUT with myReturn2, got %d fifteens" % myReturn2)
    return myReturn2
        
def countPairs(hand):
    print("Counting points from pairs..")
    return 0
gloRun=0
def runsUtil(cardsMaster, baseCard):
    global gloRun
    #print("In runsUtil len(cardsMaster):%d, baseCard#: %s" % (len(cardsMaster),gloRun))
    print("Start recursive check (cards left to check: %d),"\
            " compare against (baseCard): %s" % (len(cardsMaster),gloRun))
    if len(cardsMaster) == 0:
        return 1
    handId = 0
    #remainingCards = list(cardsMaster) ##DEEP COPY of the hand
    inARow = 1
    for card in cardsMaster:
        remainingCards = list(cardsMaster) ##DEEP COPY of the hand
        #print("\nProcessing %s, hand:" % card.cardIdString())              ##DEBUG
        #printHand(cardsMaster)        ##DEBUG
        #print("remainingCards:")           ##DEBUG
        #printHand(remainingCards)          ##DEBUG
        #print(" ")                    ##DEBUG
        if len(remainingCards) <= handId:
            ## Finished checking hand, since handId iterator reched len(remainingCards)
            break
        print("  %d checked as the next in run (needed to match %d)" % \
                (card.cardNum,gloRun + 1))
        #if it is a run, add to the row# and recheck with
        # new card and card removed from hand
        if card.cardNum == gloRun + 1:
            print("****************RRRRRUN of %s following %d" % \
                    (card.cardIdString(),gloRun))
            gloRun += 1
            cardInARow = card
            del remainingCards[handId]
            inARow = runsUtil(remainingCards, cardInARow) + 1
        #else: ## Not a run, check on!
        #if not a run, don't increase row # and recheck with SAME base
        # but hand with card removed
        handId += 1
    #print("inARow==> %d" % inARow)
    return inARow
def countRuns(hand):
    global gloRun
    print("Counting points from runs..")
    #print("Hand size (in countRuns): %d" % len(hand[1:]))
    gloRun=hand[0].cardNum
    inARow = runsUtil(hand[1:], hand[0])
    print("FOUND %d IN A ROW!!" % inARow)
    if inARow >= INAROWMIN:
        sys.exit()
    return inARow
def countFlush(hand):
    print("Counting points from flush..")
    return 0
def countSpJack(hand):
    print("Counting points from spJack..")
    return 0

def printHand(hand):
    for card in hand:
        if card.playedStatus == -1:
            state = "discarded KITTEN"
        elif card.playedStatus == 0:
            state = "in hand"
        elif card.playedStatus == 1:
            state = "pegged"
        else:
            print("discarding went horribly wrong")
            return
        print("%s (%s)" % (card.cardJson(), state))
def subsetsum(array, num):
        if num == 0 or num < 1:
            return None
        elif len(array) == 0:
            return None
        else:
            if array[0] == num:
                return [array[0]]
            else:
                with_v = subsetsum(array[1:],(num - array[0])) 
                if with_v:
                    return [array[0]] + with_v
                else:
                    return subsetsum(array[1:],num)
def subset2(list, n, subset, sum, occurs):
    if sum == 0:
        print subset
        return 1
    if n == 0:
        return 0
    if list[n-1] <= sum:
        occurs += subset2(list, n-1, subset, sum, occurs)
        occurs += subset2(list, n-1, subset+`list[n-1]`+" ", sum-list[n-1], occurs)
    else:
        occurs += subset2(list, n-1, subset, sum, occurs)
    return occurs
def pName(player):
    if player:
        return "OPP"
    return "ME"
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
        print("\n\n\n=======\n=======\nStart round %d!! (Dealer: %s)" % \
              (roundNo,pName(dealerPlayer)))
        GAME.shuffle()
        hands = deal(GAME.deck)

        oneRound = round(dealerPlayer,hands, GAME.deck)
        oneRound.pegRound()
        oneRound.count()
        dealerPlayer = switchPlayer(dealerPlayer)
        roundNo += 1
        #if roundNo > 2:
        if roundNo > NUMBEROFDRAWS:
            break

# main
play()
