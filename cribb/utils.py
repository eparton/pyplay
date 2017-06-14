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

#################
### COUNT LOGIC #
#################
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
    print("Start recursive check (cards left to check: %d),"\
            " compare against (baseCard): %s" % (len(cardsMaster),gloRun))
    if len(cardsMaster) == 0:
        return 1
    handId = 0
    inARow = 1
    for card in cardsMaster:
        remainingCards = list(cardsMaster) ##DEEP COPY of the hand
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


#################
### ACCESSORY ###
#################

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






#################
### PRINT #######
#################

def printCard(cardObj):
    card = cardObj.cardId()
    print("%s --- %s of %s" % (card['player'], card['cardName'],
                               card['suit']))
    return card

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
