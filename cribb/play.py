from gamestructs import *
from cardstructs import *

print("======================\nStarting play\n=============\n")


    

        

def play():
    GAME = game(NUMPLAYERS)
    dealerID = ME
    roundNo = 0
    while (GAME.gameOver() < 0):
        print("\n\n\n=======\n=======\nStart round %d!! (Dealer: %s)" % \
            (roundNo,dealerID))
        GAME.shuffle()
        #hands = deal(GAME.deck, GAME.numPlayers)

        oneRound = round(GAME.players[dealerID], GAME)
        oneRound.pegRound()
        #oneRound.count()
        dealerID = switchPlayer(dealerID)
        #dealerPlayer = switchPlayer(dealerPlayer)

        NUMBEROFROUNDS = 2
        roundNo += 1
        if roundNo > NUMBEROFROUNDS:
            break
    print("GAME ENDED, player %d wins!" % GAME.gameOver())
# main
play()
