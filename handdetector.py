cardvalues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
suits = ['spade', 'heart', 'club', 'diamond']
handtypes = ['high card', 'pair', 'two pair' ,'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush', 'royal flush']
#cardexample = ['a', 'spade']

def sorthand(hand): # Sorts hand by card value, lowest to highest
    sortedhand = []
    for i in range(len(hand)):
        smallestindex = 12 # Ace index
        foundindex = 0
        for j in range(len(hand)):
            index = cardvalues.index(hand[j][0])
            if index < smallestindex:
                smallestindex = index
                foundindex = j
        sortedhand.append(hand.pop(foundindex))
    return sortedhand

def subtractlists(biglist, smalllist): # Remove all elements in small list from big list
    smalllist = smalllist[:]
    finallist = []
    for i in range(len(biglist)):
        indexflag = True
        for j in range(len(smalllist)):
            if biglist[i] == smalllist[j]:
                indexflag = False
                smalllist[j] = None
        if indexflag:
            finallist.append(biglist[i])
    return finallist

def straightdetect(sortedcardlist):
    tophand = [sortedcardlist[0]]
    straightcounter = 1
    for i in range(1, len(sortedcardlist)):
        if cardvalues.index(sortedcardlist[i][0]) - cardvalues.index(sortedcardlist[i - 1][0]) == 1:
            straightcounter += 1
            tophand.append(sortedcardlist[i])
        elif straightcounter < 5:  # Only reset if previous detection wasn't a full straight
            straightcounter = 1
            tophand = [sortedcardlist[i]]

    if straightcounter < 5 and sortedcardlist[-1][0] == 'a':  # Possible wraparound straight
        for i in range(5 - straightcounter):
            if sortedcardlist[i][0] == cardvalues[i]:  # If first cards are, 2, 3, 4, etc
                straightcounter += 1
                tophand.append(sortedcardlist[i])

    if straightcounter > 5:  # Cut the list to top 5 cards
        if 'a' in tophand and tophand[-1] != 'a':  # If ace in hand but not final then it is a wraparound straight
            tophand = tophand[:5]  # Right end is cut off for wraparound
        else:
            tophand = tophand[-5:]  # Left end is cut off for normal straight
        straightcounter = 5

    if straightcounter == 5:
        return True, tophand
    else:
        return False, []

def detectpokerhand(hand): # Parameter of 7 cards list
    # Return: type of hand, cards in the scoring hand, remaining cards
    handtype = 'high card'
    tophand = []
    remainingcards = []
    spadelist = []
    heartlist = []
    clublist = []
    diamondlist = []

    for i in range(len(hand)):
        match hand[i][1]:
            case 'spade':
                spadelist.append(hand[i])
            case 'heart':
                heartlist.append(hand[i])
            case 'club':
                clublist.append(hand[i])
            case 'diamond':
                diamondlist.append(hand[i])
            case _:
                print("Invalid card")

    suitlists = [sorthand(spadelist), sorthand(heartlist), sorthand(clublist), sorthand(diamondlist)]
    sortedcardlist = sorthand(suitlists[0] + suitlists[1] + suitlists[2] + suitlists[3])
    cardnumbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(sortedcardlist)):
        cardnumbers[cardvalues.index(sortedcardlist[i][0])] += 1

    # Flush detection
    for i in range(len(suitlists)):
        if len(suitlists[i]) >= 5:
            # Straight detection
            straightflushresult = straightdetect(suitlists[i])
            if not straightflushresult[0]:
                handtype = 'flush'
            else:
                tophand = straightflushresult[1]
                if tophand[-1][0] == 'a':
                    handtype = 'royal flush'
                else:
                    handtype = 'straight flush'
                remainingcards = subtractlists(sortedcardlist, tophand)
                return handtype, tophand, remainingcards # Royal/straight flush are top hands so will instantly return

    # Non-flush hands
    toppairid = None
    secondpairid = None
    toptripleid = None
    flushflag = False
    if handtype == 'flush':
        flushflag = True

    for i in range(len(cardnumbers)):
        if cardnumbers[i] == 4:
            handtype = 'four of a kind'
            tophand = []
            remainingcards = []
            for card in sortedcardlist:
                if card[0] == cardvalues[i]:
                    tophand.append(card)
                else:
                    remainingcards.append(card)
            return handtype, tophand, remainingcards # Past flush checks, so 4 of a kind is always highest with no flush
        elif cardnumbers[i] == 3:
            toptripleid = i
        elif cardnumbers[i] == 2:
            if toppairid != None: # If there is already a pair
                secondpairid = toppairid
            toppairid = i # Will always be overwritten by higher pair

    # Flush
    if (toptripleid is None or toppairid is None) and flushflag:
        handtype = 'flush'
        print(tophand)
        remainingcards = subtractlists(sortedcardlist, tophand)
        return handtype, tophand, remainingcards  # Top hand and remaining cards are already set
    # Full house
    elif toptripleid is not None and toppairid is not None:
        handtype = 'full house'
        tophand = []
        remainingcards = []
        for card in sortedcardlist:
            if card[0] == cardvalues[toptripleid] or card[0] == cardvalues[toppairid]:
                tophand.append(card)
            else:
                remainingcards.append(card)
        return handtype, tophand, remainingcards  # Full house is next highest hand so will return here

    tophand = []
    remainingcards = []

    # Straight detection
    straightresult = straightdetect(sortedcardlist)
    if straightresult[0]:
        handtype = 'straight'
        tophand = straightresult[1]
        remainingcard = subtractlists(sortedcardlist, tophand)
        return handtype, tophand, remainingcards


    # Final hands

    tophand = []
    remainingcards = []

    # Three of a kind
    if toptripleid != None:
        handtype = 'three of a kind'
        for card in sortedcardlist:
            if card[0] == cardvalues[toptripleid]:
                tophand.append(card)
            else:
                remainingcards.append(card)
    # Two pair
    elif secondpairid != None:
        handtype = 'two pair'
        for card in sortedcardlist:
            if card[0] == cardvalues[toppairid] or card[0] == cardvalues[secondpairid]:
                tophand.append(card)
            else:
                remainingcards.append(card)
    # Pair
    elif toppairid != None:
        handtype = 'pair'
        for card in sortedcardlist:
            if card[0] == cardvalues[toppairid]:
                tophand.append(card)
            else:
                remainingcards.append(card)
    # High card
    else:
        handtype = 'high card'
        tophand.append(sortedcardlist[-1])
        for i in range(len(sortedcardlist)-1):
            remainingcards.append(sortedcardlist[i])

    return handtype, tophand, remainingcards



#testhand = [['a', 'spade'], ['2', 'spade'], ['7', 'spade'], ['j', 'spade'], ['8', 'spade'], ['q', 'spade'], ['k', 'spade']]
#print(testhand)
#print(detectpokerhand(testhand))