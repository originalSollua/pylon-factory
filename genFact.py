# genFact
# try to make random facts
import random

def partA():
    partAL = [
            'Did you know that',
            'Have you considered that',
            'Interestingly, ',
            'You might not know it but',
            'This might surprise you, but',
            'Here is a hot tip:',
            'Not everyone knows this, but',
            'Einstine once said',
            'Bill Nye says that',
            'I saw on the news that',
            'I just found out that',
            'I just checked my magic 8 ball and saw that',
            'Grumbo did the mole dance and he says',
            "I'll have you know that"
            ]
    return random.choice(partAL)

def partB():
    partBL = [
            'agile is',
            'the moon is actually',
            'cows are',
            'javascript is',
            'Earth could be',
            'nanobots are',
            'memes are',
            'science is',
            'the cake is',
            'old tires are',
            'the code for this bot can be',
            '3D printers are',
            'the tree gators are',
            'the Glorious Haskell Compiler is',
            'kids these days are',
            'Chris Perkins is',
            'the Sun is'
            ]
    return random.choice(partBL)

def partC():
    partCL = [
            'slang for some really offensive terms',
            'made of cheese',
            'composed mostly of hot gas',
            'a dumpster that is also on fire',
            'a way to drink coffee faster',
            'a lie',
            'de wey',
            'restless',
            'a replacement for Bender',
            'confirmed by Mythbusters',
            'one of the Mario Bros',
            'the next game getting ported to the Switch',
            'a deadly laser',
            'starting to gain traction',
            'addicted to smartphones',
            "could afford a house by now if it weren't for all that avacado toast",
            'a kind and merciful DM',
            'a show you did not know was on Netflix'
            ]

    return random.choice(partCL)
def get():
    return partA()+" "+partB()+" "+partC()

