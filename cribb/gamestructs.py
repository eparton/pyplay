from cardstructs import *

#################
### GAME ########
#################
class game:
    def __init__(self, numPlayers):
        self.deck = None
        self.players = []
        self.numPlayers = numPlayers
        for i in range(numPlayers):
            self.players.append(player(i))
        #self.points = [0,0]
    def shuffle(self):
        self.deck = deck()
    def gameOver(self):
        for i in range(self.numPlayers):
            if self.players[i].points > 120:
                return i
        return -1

#################
### PLAYER ######
#################
class player:
    def __init__(self,playerID):
        self.playerID = playerID
        self.points = 0
        self.hand = None


#################
### HAND ########
#################
class hand:
    def __init__(self):
        #self.player = player
        self.cards = []
    def discard(self, cardIndex):
        self.cards[cardIndex].playedStatus = -1 ## -1 -> IN KITTEN
    def cardsInHand(self): ##count the number left without traversal?
        left = 0
        for i in range(0,HANDSIZE):
            if self.cards[i].playedStatus == 0:
                left += 1
        return left

#################
### ROUND #######
#################

class round:
    def __init__(self, dealer, game):
        self.dealer = dealer
        self.game = game
        self.cutCard = None
        self.pegTotal = 0
        ##dealer a placeholder -- no initial value?
        self.currentPlayerId = dealer
        self.lastPlayer    = dealer
        self.deal()
        self.discard()
        self.setupCut()
    def deal(self):
        for player in self.game.players:
            currentHand = hand()
            print("\nHAND for %d:" % player.playerID)
            for i in range(0,HANDSIZE):
                oneCard = self.game.deck.dealone()
                currentHand.cards.append(oneCard)
                print("%s" % printCard(oneCard))
            player.hand = currentHand
        #return hands
    def setupCut(self):
        self.cutCard = self.game.deck.dealone() ##NAME OF PLAYER REMOVED IN v2
        print("\njust pulled cut card")
        print("%s" % printCard(self.cutCard))
        #self.cutCard = cutCard
    def discard(self):
        for player in self.game.players:
            player.hand.discard(0)
            player.hand.discard(1)

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
        
    def count(self):
        print("COUNT IT UP! (in construction..)\n===========")
        pointsME  = self.hands[ME].countHand()
        pointsOPP = self.hands[OPP].countHand()
        print("For the ROUND, ME scores %d and OPP scores %d" % (pointsME,pointsOPP))
        return

    def pegRound(self):
        print("\nStart pegging.. (%d was dealer)" % self.dealer.playerID)
        self.currentPlayerId = switchPlayer(self.dealer.playerID)
        print("Player now playing: %d" % self.currentPlayerId)
        while 1:
            done = 1
            for player in self.game.players:
                if player.hand.cardsInHand > 0:
                    print("(at least player #%d has cards to play)" % player.playerID)
                    done = self.pegOne(self.currentPlayerId)
                    #done = 0
            if done:
                print("NO MORE CARDS, exiting pegRound")
                return
    def pegOne(self, pID):
        for i in range(NUMPLAYERS):
            pegAttemptPlayerID = pID
            print("Continuing peg (total: %d) for player: %d" % (self.pegTotal,pegAttemptPlayerID))
            player = self.game.players[pegAttemptPlayerID]
            for card in player.hand.cards:
                print("setting up for peg attempt: %d, %d, %d" % (card.playedStatus,card.countValue(),self.pegTotal))
                cardStr = printCard(card)
                if (card.playedStatus == 0) and (card.countValue() + self.pegTotal <= 31):
                    print("->WILL PLAY: %s" % cardStr)
                    #printCard(card)
                    card.playedStatus = 1
                    self.pegTotal += card.countValue()
                    self.currentPlayerId = switchPlayer(self.currentPlayerId)
                    return 0
                    break ##so that this player doesn't play any more
                else:
                    pass
                    #print("can't play THIS card")
            print("(nothing left to play)")
            return 1

