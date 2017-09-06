from random import randint
import sys
ME = 0
OPP = 1
HANDSIZE = 6
NUMPLAYERS = 2

INKITTEN = -1
INHAND   = 0
PLAYED   = 1

def switchPlayer(player):
    return (player + 1) % NUMPLAYERS

def printCard(cardObj):
    card = cardObj.cardId()
    #print("%s of %s" % (card['cardName'],
    #                           card['suit']))
    return card['cardName'] + " of " + card['suit']

def evaluateHand(hand, cut):
	if cut == None:
		print("just hand of 4 here")
		pt15s = hand.count15s()
	else:
		print("eval with cut: %s" % printCard(cut))