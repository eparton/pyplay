#Removes "subtrahend" (S) from "message" (M), yields "remainder" (R)
HelloWorld = "****_*_*-**_*-**_---___*--_---_*-*_*-**_-**"
Help = "****_*_*-**_*--*"
#print("REMOVE: %s" % HelloWorld)
#print("FROM  : %s" % Help)

DOT   = "*"
DASH  = "-"
BLANK = "_"


class word:
    def __init__(self, content):
        self.content = content
        self.length = len(self.content)
        self.currentPos = 0
    def addLetter(self, letter):
        if len(letter) != 1:
            print("please give a single letter")
            return
        self.content += letter
        self.length += 1
        return
    def printWord(self):
        print("printing: %s (%d)" % (self.content,self.length))
        printedWord = ""
        for i in range(0,self.length):
            printedWord += ("[" + str(i) + "]" + self.content[i])
        print("printedWord: %s" % printedWord)
    def charAtPos(self, pos):
        if pos >= self.length:
            print("Indexing error!")
            return ""
        else:
            return self.content[pos]

def subtractWords(sub, mes):
    remainder = word("")
    while (mes.currentPos < mes.length):
        if comparePos(sub,mes):
            print("position %d same with position %d" %  \
                   (sub.currentPos,mes.currentPos))
            sub.currentPos += 1
            mes.currentPos += 1
        else:
            print("pos %d different with pos %d" % \
                   (sub.currentPos,mes.currentPos))
            remainder.addLetter(sub.content[sub.currentPos])
            sub.currentPos += 1
            print("remainder growing: ")
            remainder.printWord()


def comparePos(sub,mes):
    #print("(comparing %s with %s)" % 
    return (sub.charAtPos(sub.currentPos) == mes.charAtPos(mes.currentPos))
#MAIN
subtrahend = word(HelloWorld)
message = word(Help)
subtrahend.printWord()
message.printWord()

subtractWords(subtrahend, message)
