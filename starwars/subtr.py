import sys

HelloWorld = "****_*_*-**_*-**_---___*--_---_*-*_*-**_-**"
Help = "****_*_*-**_*--*"

#DOT   = "*"
#DASH  = "-"
#BLANK = "_"
SYMBOLS = {}
SYMBOLS['DOT']  = "*"
SYMBOLS['DASH'] = "-"
SYMBOLS['BLANK']= "_"
REVSYM = {}
REVSYM['*'] = "DOT"
REVSYM['-'] = "DASH"
REVSYM['_'] = "BLANK"

class letter:
    def __init__(self, letter, position):
        self.letter = letter
        self.position = position

class word:
    def __init__(self, content):
        self.rawPayload = content
        self.length = len(content)
        self.letters = []
        self.ingest()
    def ingest(self):
        self.wordArray = []
        for pos in range(self.length):
            #self.wordArray[pos] = self.rawPayload[pos]
            tempLetter = letter(self.rawPayload[pos], pos)
            self.letters.append(tempLetter)
            if len(self.letters) != pos + 1:
                print("HUGE ACCOUNTING ERROR! QUIT\n")
                sys.exit()
        print("DONE INGESTION")
        #print(self.letters)
        for eachL in self.letters:
            print("%d position: %s" % (eachL.position, eachL.letter))

#main
parentWord = word(HelloWorld)
print("END")
