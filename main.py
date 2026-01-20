from random import randint, shuffle
import handdetector
import os

cardvalues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
suits = ['spade', 'heart', 'club', 'diamond']
suiticons = ['♤', '♡', '♧', '♢']
handtypes = ['high card', 'pair', 'two pair' ,'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush', 'royal flush']
cardexample = ['a', 'spade']

fulldeck = []
for i in range(len(cardvalues)): # Each card value
    for j in range(len(suits)): # Each suit
        fulldeck.append([cardvalues[i], suits[j]])
deck = shuffle(fulldeck)

# Colours
reset = "\033[0m"
dim = "\033[2m" # Spades
red = "\033[31m" # Hearts
green = "\033[28;5;22m" # Clubs
orange = "\033[38;5;214m" # Diamonds

# Subroutins
# Hand detection imported from handdetector.py

def intinputvalidate(prompt, lower, upper):
    while True:
        try:
            temp = int(input(prompt))
            if lower != -1 and upper != -1:
                if temp < lower or temp > upper:
                    1 / 0
                else:
                    return temp
            else:
                return temp
        except Exception:
            print("Invalid input")

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear') # Wipe terminal

def displaynames():
    print(f"All {len(playernamelist)} players:")
    for name in playernamelist:
        print(name)
    print() # Leaves whitespace after names are displayed

def draw():
    return deck.pop()


# Classes

startingmoney = 40000
class Player:
    def __init__(self, newname):
        self.money = startingmoney
        self.name = newname
        self.hand = []
    def newhand(self):
        self.hand = [draw(), draw()]
    def resethand(self):
        self.hand = []


playerlist = []
playernamelist = []
devmode = False

while True:
    newplayername = input("Input player name: (Input '0' once all players are in or '-1' to reset all names)\n")
    if newplayername == '0':
        if len(playernamelist) >= 3:
            displaynames()
            allplayernamesconfirm = intinputvalidate("Is this all players? (1=Yes, 0=No, add more)\n", 0, 1)
            if allplayernamesconfirm:
                break
        else:
            print("You must have at least 3 players to play")
    elif newplayername == '-1':
        playernamelist = []
        print("All names reset, please input all player names again")
    else:
        if newplayername not in playernamelist:
            print(f"Name: {newplayername}")
            playernamelist.append(newplayername)
            if newplayername == '`dev`':
                print("devmode activated")
                devmode = True
        else:
            print("Name is already taken")

playernum = len(playernamelist)

# Player Instantiation

for i in range(playernum):
    playerlist.append(Player(playernamelist[i]))

