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
### Doesn't work if the first card in the run is after the others!!
def runsUtil(wholeHand, cardsMaster, currentHighest):
    if len(cardsMaster) == 0:
        return 1
    handId = 0
    inARow = 1
    for card in cardsMaster:
        remainingCards = list(cardsMaster) ##DEEP COPY of the hand
        if len(remainingCards) <= handId:  ## Finished checking hand
            break
        #print("  %d checked as the next in run (needed to match %d)" % \
        #        (card.cardNum,gloRun + 1))
        #if it is a run, add to the row# and recheck with
        # new card and card removed from hand
        #if card.cardNum == gloRun + 1:
        if card.cardNum == currentHighest + 1:
            print("****************RRRRRUN of %s following %d" % \
                    (card.cardIdString(),currentHighest))
            currentHighest += 1
            #remainingCards = list(wholeHand) ##DEEP COPY of the hand
            del remainingCards[handId] ## delete matched card
            inARow = runsUtil(wholeHand, remainingCards, currentHighest) + 1
        #else: ## Not a run, check on!
        #if not a run, don't increase row # and recheck with SAME base
        # but hand with card removed
        handId += 1
    return inARow
def countRuns(hand):
    print("Counting points from runs..")
    inARow = runsUtil(hand, hand[1:], hand[0].cardNum)
    if inARow >= 3:
        print("FOUND %d IN A ROW!!" % inARow)
        if inARow >= INAROWMIN:
            sys.exit()
        return inARow
    return 0
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
