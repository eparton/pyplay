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
        self.currentPlayerId = None
        self.lastPlayedId    = None
        self.deal()
        self.discard()
        self.setupCut()
        self.temp = {}
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
		self.lastPlayedId	 = self.dealer.playerID
		print("Player now playing: %d" % self.currentPlayerId)
		pegDone = 0
		while not pegDone:
			playedInPeg = 0
			for playerIter in range(NUMPLAYERS):
				nextToPlayId = (self.lastPlayedId + playerIter + 1) % NUMPLAYERS
				player = self.game.players[nextToPlayId]
				#print("lastPlayedId: %d, nextToPlayId: %d, playerID: %d" % \
				#	  (self.lastPlayedId,nextToPlayId, player.playerID))
				if player.hand.cardsInHand() > 0:
					#print("(at least player #%d has cards to play)" % player.playerID)
					playedInPeg = self.pegOneCheck(player.playerID) ## takes care of switching
					#return of 1 means we played a card
					if playedInPeg:
						break  ## will skip next line, otherwise execute
			if not playedInPeg:
				if self.pegTotal == 31:
					score = 2
				else:
					score = 1
				player.points += score
				print("That's 'gos' all around! Total: %d, player %d scores %d\n" % \
				     (self.pegTotal, player.playerID, score))
				#print("===> %d -- NO MORE CARDS, exiting pegRound\nRemaining cards:" % self.pegTotal)
				##TEMP DISPLAY ONLY  -- Use list compression
				for temp in self.game.players:
					for card in temp.hand.cards:
						if card.playedStatus is INHAND:
							print("Player %d leaves behind: %s" % (temp.playerID,printCard(card)))
				###################
				self.pegTotal = 0
				for player in self.game.players:
					pegDone = 1
					if player.hand.cardsInHand() > 0:
						pegDone = 0
						break
		resultsStr = "Results of round:"
		for player in self.game.players:
			resultsStr += " player " + str(player.playerID) + ": " + str(player.points)
		print(resultsStr)
		return
    def pegOne(self, card):
		card.playedStatus = PLAYED
		self.pegTotal += card.countValue()
		print("->PLAYING (player: %d): %s -- Total: %d" % \
			  (self.temp["player"].playerID,self.temp["cardStr"],self.pegTotal))
		self.lastPlayedId = self.currentPlayerId
		self.currentPlayerId = switchPlayer(self.currentPlayerId)
		return card

	#def randoPeg(self):
	
    def pegOneCheck(self, currentId):
        for i in range(NUMPLAYERS):
            pegAttemptPlayerID = (currentId + i) % NUMPLAYERS  # give fair chance starting AFTER current
            #print("Cont (total: %d) for player (started turn): %d, and player (check): %d" % \
            #      (self.pegTotal,pegAttemptPlayerID,i))
            player = self.game.players[pegAttemptPlayerID]
            for card in player.hand.cards:
                #print("setting up for peg attempt: %d, %d, %d" % (card.playedStatus,card.countValue(),self.pegTotal))
                cardStr = printCard(card)
                if (card.playedStatus == INHAND) and \
                   (card.countValue() +  self.pegTotal <= 31):
					self.temp["player"]=player
					self.temp["cardStr"]=cardStr
					card = self.pegOne(card)  # must save it back because modified status
                    ## 1 means we played a card
					return 1
                    #break ##so that this player doesn't play any more
                else:
                    pass
                    #print("can't play THIS card")
            self.currentPlayerId = switchPlayer(self.currentPlayerId)
        #print("(nothing left to play)")
        return 0
############################## NOTES #####################
"""
Final check, with only one to play, 1 is the first to attempt so gets credit
even though 0 had to come back to win the point

=======
=======
Start round 2!! (Dealer: 0)

HAND for 0:
7 of clubs
7 of hearts
6 of hearts
Queen of clubs
6 of diamonds
Queen of diamonds

HAND for 1:
2 of clubs
8 of hearts
King of diamonds
King of spades
7 of diamonds
4 of clubs

just pulled cut card
2 of spades

Start pegging.. (0 was dealer)
Player now playing: 1
->PLAYING (player: 1): King of diamonds -- Total: 10
->PLAYING (player: 0): 6 of hearts -- Total: 16
->PLAYING (player: 1): King of spades -- Total: 26
->PLAYING (player: 1): 4 of clubs -- Total: 30
That's 'gos' all around! Total: 30, player 1 scores 1

Player 0 leaves behind: Queen of clubs
Player 0 leaves behind: 6 of diamonds
Player 0 leaves behind: Queen of diamonds
Player 1 leaves behind: 7 of diamonds
->PLAYING (player: 0): Queen of clubs -- Total: 10
->PLAYING (player: 1): 7 of diamonds -- Total: 17
->PLAYING (player: 0): 6 of diamonds -- Total: 23
That's 'gos' all around! Total: 23, player 0 scores 1

Player 0 leaves behind: Queen of diamonds
->PLAYING (player: 0): Queen of diamonds -- Total: 10
That's 'gos' all around! Total: 10, player 1 scores 1
************* ^ Wrong since player 0 was the one to score
Results of round: player 0: 3 player 1: 4


"""
