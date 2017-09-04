from random import randint
import sys
ME = 0
OPP = 1
HANDSIZE = 6
NUMPLAYERS = 2

def switchPlayer(player):
    return (player + 1) % NUMPLAYERS

def printCard(cardObj):
    card = cardObj.cardId()
    #print("%s of %s" % (card['cardName'],
    #                           card['suit']))
    return card['cardName'] + " of " + card['suit']