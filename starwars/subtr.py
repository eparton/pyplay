from wordStructs import *


def startCompare(comparison):
    parent = comparison.parentWord
    child = comparison.childWord
    if child.length > parent.length:
        print("Subtraction word too large! Quitting\n")
        sys.exit()
    #for pos in range(parent.length):
    count = 0
    for letterCompare in child.letters:
        print("position: %d" % count)
        #if pos >= child.length:
        #    break
        #if parent.letters[pos].letter == child.letters[pos].letter:
        if letterCompare.letter == parent.letters[count].letter:
            print("MATCH at position %d for symbol %s" % (count, parent.letters[count].letter))
        else:
            print("%s does not match %s" % (parent.letters[count].letter,child.letters[count].letter))
        count = count + 1

def main():
    print("first word:   %s" % HelloWorld)
    print("secondt word: %s" % Help)

    parentWord = word(HelloWorld)
    childWord  = word(Help)
    firstCompare = comparePair(parentWord, childWord)
    print("END")
    startCompare(firstCompare)

main()
