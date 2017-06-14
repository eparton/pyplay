from cribstructs import *

print("======================\nStarting play\n=============\n")

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


        

def play():
    GAME = game()
    dealerPlayer = ME
    roundNo = 0
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
