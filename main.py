from random import randint, shuffle#
from time import sleep
import handdetector
import os

cardvalues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['spade', 'heart', 'club', 'diamond']
suiticons = ['♤', '♡', '♧', '♢']
handtypes = ['high card', 'pair', 'two pair' ,'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush', 'royal flush']
cardexample = ['a', 'spade']

fulldeck = []
for i in range(len(cardvalues)): # Each card value
    for j in range(len(suits)): # Each suit
        fulldeck.append([cardvalues[i], suits[j]])
deck = fulldeck
shuffle(deck)

river = []
pot = 0
initialmoney = []

# Colours
reset = "\033[0m"
dim = "\033[2m" # Spades
red = "\033[31m" # Hearts
green = "\033[38;5;70m" # Clubs
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

def displaycard(card):
    if card[1] == 'spade':
        print(f"{dim}{card[0]} {suiticons[0]}{reset}")
    elif card[1] == 'heart':
        print(f"{red}{card[0]} {suiticons[1]}{reset}")
    elif card[1] == 'club':
        print(f"{green}{card[0]} {suiticons[2]}{reset}")
    elif card[1] == 'diamond':
        print(f"{orange}{card[0]} {suiticons[3]}{reset}")
    else:
        print("Suit not found")

def deckreset():
    deck = fulldeck
    shuffle(deck)

def riverreset():
    river = [deck.pop(), deck.pop(), deck.pop(), deck.pop(), deck.pop()]

def riverdisplay(riverrevealamount):
    print("River:")
    for i in range(len(river)):
        if i < riverrevealamount:
            displaycard(river[i])
    print()

def potreset():
    pot = 0

def initialmoneyreset():
    initialmoney = []
    for i in range(playernum):
        initialmoney.append(playerlist[i].money)

def decision(player):
    raiseamount = 0
    while True:
        cmd = input("Options: (Fold, Check, Raise, Cards)\n").lower()
        if cmd == 'fold':
            return cmd, raiseamount
        elif cmd == 'check':
            return cmd, raiseamount
        elif cmd == 'raise':
            if not player.checked:
                amount = input("By how much?\n")
                if amount == 'all':
                    raiseamount = player.money
                    return cmd, raiseamount
                else:
                    try:
                        raiseamount = int(amount)
                        return cmd, raiseamount
                    except:
                        print("Invalid amount")
            else:
                print("You have already checked this round, you cannot raise")
        elif cmd == 'cards':
            player.viewhand()
        else:
            print("Invalid option")

def decisionloop(player, pot, highestbid, riverrevealamount):
    print(f"Player {player.name}\nPot: {pot}\nHighest Bid: {highestbid}")
    riverdisplay(riverrevealamount)

    if not player.folded:
        choice = decision(player)
        if choice[0] == 'fold':
            player.folded = True
        elif choice[0] == 'check':
            pot += player.pay(highestbid)
            player.checked = True
        elif choice[0] == 'raise':
            highestbid = choice[1]
            pot += player.pay(highestbid)
    else:
        print(f"Player {player.name} has folded")

    return pot, highestbid

def checkcheck():
    flag = True
    for i in range(playernum):
        if not playerlist[i].checked:
            flag = False
    return flag

def checkreset():
    for i in range(playernum):
        playerlist[i].checked = False

def playersstillin():
    foldcounter = 0
    lastinid = 0
    for i in range(playernum):
        if playerlist[i].folded:
            foldcounter += 1
        else:
            lastinid = i
    return playernum - foldcounter, lastinid


# Classes

startingmoney = 40000
class Player:
    def __init__(self, newname):
        self.money = startingmoney
        self.name = newname
        self.hand = []
        self.folded = False
        self.checked = False
    def newhand(self):
        self.hand = [deck.pop(), deck.pop()]
    def resethand(self):
        self.hand = []
        self.newhand()
    def viewhand(self):
        input(f"Player {self.name} press enter to see your cards when no one else is looking\n")
        for i in range(len(self.hand)):
            displaycard(self.hand[i])
        input("\nPress enter to wipe the screen\n")
        clearscreen()
    def pay(self, amount):
        print(f"You paid {amount}")
        self.money -= amount
        return amount


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

clearscreen()


blindcounter = randint(0, playernum-1) # Player id of counter will be small blind, counter + 1 will be big blind
blindamount = 5
blindnumber = 2 # 2 blind players

# Game loop
run = True
while run:
    # Initial Setup
    riverreset()
    deckreset()
    potreset()
    initialmoneyreset()
    blindcounter %= playernum
    winnerid = None

    # Blinds
    for i in range(blindnumber):
        select = (blindcounter + i) % playernum
        pot += playerlist[select].pay(blindamount * (i + 1))

    highestbid = blindamount * blindnumber

    # Reset each player's hand and they can privately view
    for i in range(playernum):
        clearscreen()
        print("Card viewing")
        playerlist[i].resethand()
        playerlist[i].viewhand()

    for i in range(4): # 0 river, 3 river, 4 river, 5 river
        if i == 0:
            rivercounter = 0
        else:
            rivercounter = i + 2

        checkreset()
        allcheckflag = False
        counter = blindcounter + 2  # Small blind, Big blind, First player
        while not allcheckflag and winnerid is None:
            clearscreen()
            counter %= playernum  # If more than playernum counter loops back to the start
            player = playerlist[counter]

            pot, highestbid = decisionloop(player, pot, highestbid, rivercounter)

            allcheckflag = checkcheck()

            counter += 1
            input("Press enter to end turn")

            stillinresult = playersstillin()
            if stillinresult[0] == 1:
                winnerid = stillinresult[1]

        if winnerid is not None:
            break

    if winnerid is not None:
        print(f"Player {playerlist[winnerid].name} won!")
        if initialmoney[winnerid] >= pot:
            playerlist[winnerid].money += pot
        else: # Sidepot
            pass
    else:
        pass