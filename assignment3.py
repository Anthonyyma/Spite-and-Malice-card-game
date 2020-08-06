# import the classes
from SpiteAndMalice import Card, PlayStack, Hand
from lectureStructures import Queue, Stack

# import the functions
from SpiteAndMalice import shuffle, displayGame, getDecision, getDiscard, getPlayCard, choosePlayStack, checkForZero, onlyZeros, replenishHand, checkWin


def main():
    """
    Main function that controls the flow of the game
    """
    # the shoe that holds all of the cards used while playing
    shoe = Queue()

    # a list that holds all of the finished play stacks
    removedCards = []
    removedTimes = 0

    # player 1's hand
    p1h = Hand()

    # player 1's goal stack
    p1g = Stack()

    # player 2's hand
    p2h = Hand()

    # player 2's goal stack
    p2g = Stack()

    # initialize 120 cards into the show
    for i in range(10):
        for j in range(0, 10):
            shoe.enqueue(Card(j))
    for i in range(20):
        shoe.enqueue(Card(-1))

    # shuffle the shoe
    shoe = shuffle(shoe)

    # add cards to both players hand
    for i in range(5):
        p1h.add(shoe.dequeue())
        p2h.add(shoe.dequeue())
    p1h.sort()
    p2h.sort()

    # add cards to both players goal stack
    for i in range(15):
        p1g.push(shoe.dequeue())
        p2g.push(shoe.dequeue())

    # create the play stacks
    ps1 = PlayStack()
    ps2 = PlayStack()
    ps3 = PlayStack()
    ps4 = PlayStack()
    pslist = [ps1, ps2, ps3, ps4]

    # create each players discard stacks
    p1d1 = Stack()
    p1d2 = Stack()
    p1d3 = Stack()
    p1d4 = Stack()
    p1dlist = [p1d1, p1d2, p1d3, p1d4]
    p2d1 = Stack()
    p2d2 = Stack()
    p2d3 = Stack()
    p2d4 = Stack()
    p2dlist = [p2d1, p2d2, p2d3, p2d4]

    # create list of each players stacks
    p1Cards = [p1h, p1g, p1dlist]
    p2Cards = [p2h, p2g, p2dlist]

    ############STARTING THE GAME##############
    continueGame = True

    # peek the top card of both players. player with the higher card goes first. player 1 goes first if they are the same
    if ((p2g.peek().getValue() > p1g.peek().getValue()) and (p1g.peek().getValue() != -1)) or (
            (p2g.peek().getValue() == -1) and (p1g.peek().getValue() != -1)):
        turn = 2
    else:
        turn = 1

    while continueGame:
        validPos = False
        validPile = False
        validPlayCard = True

        # display the current status of the game
        displayGame(p1Cards, p2Cards, pslist)

        # ask the player if they want to play or discard
        decision = getDecision(turn)

        # let the player discard only if they do not have a zero
        while decision == 'X' and not checkForZero(turn, p1Cards, p2Cards) or onlyZeros(turn, p1Cards, p2Cards):
            discarding = True

            # if the player only has zeros then they pass without discarding anything
            if onlyZeros(turn, p1Cards, p2Cards):
                emptyStacks = False
                pile = 1
                while not emptyStacks and pile < 5:
                    if str(eval('ps' + str(pile))) == '||':
                        emptyStacks = True
                    else:
                        pile += 1
                        if not emptyStacks:
                            if (turn + 1) % 2 == 0:
                                turn = 2
                            else:
                                turn = 1

            # run if the player chooses to discard a card
            if discarding:
                discarding = False
                validDiscard = False

                # ask for a card to discard until a valid one is chosen
                while not validDiscard:
                    pos, pile = getDiscard()

                    # check if trying to discard a zero
                    if pos != 'g':
                        currentCard = eval('p' + str(turn) + pos[:1]).pop(int(pos[-1:]) - 1)
                        if currentCard.getValue() == 0:
                            print('Error: Cannot discard a zero')
                        else:
                            validDiscard = True
                        eval('p' + str(turn) + pos[:1]).add(currentCard)
                        eval('p' + str(turn) + pos[:1]).sort()
                    else:
                        currentCard = eval('p' + str(turn) + pos[:1]).peek()
                        if currentCard.getValue() == 0:
                            print('Error: Cannot discard a zero')
                        else:
                            validDiscard = True
                # add the discarded card to a discard pile and pass the turn to the next player
                if pos != 'g':
                    eval('p' + str(turn) + 'd' + str(pile)).push(eval('p' + str(turn) + pos[:1]).pop(int(pos[-1:]) - 1))
                else:
                    eval('p' + str(turn) + 'd' + str(pile)).push(eval('p' + str(turn) + pos[:1]).pop())
                if (turn + 1) % 2 == 0:
                    turn = 2
                else:
                    turn = 1

                # player draws cards until they have 5 cards in their hand
                replenishHand(turn, shoe, p1h, p2h)

                displayGame(p1Cards, p2Cards, pslist)

                decision = getDecision(turn)

        # if the player has a 0 then make them play it first if possible
        if checkForZero(turn, p1Cards, p2Cards):
            # check if there is an empty play stack
            try:
                for i in range(1, 5):
                    eval('ps' + str(i)).peekValue()
            except:
                # get players decision
                while not validPos or not validPile:
                    pos = getPlayCard()
                    pile = choosePlayStack()

                    # check if the chosen card is a zero
                    if pos[:1] == 'g':
                        if eval('p' + str(turn) + 'g').peek().getFace() == '0':
                            chosenCard = eval('p' + str(turn) + 'g')
                            validPos = True
                        else:
                            print('Must play a 0')
                    elif pos[:1] == 'h':
                        selectCard = eval('p' + str(turn) + 'h').pop(int(pos[-1:]) - 1)
                        if selectCard.getValue() == 0:
                            chosenCard = selectCard
                            validPos = True
                        else:
                            eval('p' + str(turn) + 'h').add(selectCard)
                            eval('p' + str(turn) + 'h').sort()
                            print('Must play a 0')
                    elif pos[:1] == 'd':
                        if eval('p' + str(turn) + 'd' + pos[-1:]).peek().getValue() == 0:
                            chosenCard = eval('p' + str(turn) + 'd' + pos[-1:]).peek()
                            validPos = True
                        else:
                            print('Must play a 0')
                    if eval('p' + str(turn) + 'h').size() <= 0:
                        replenishHand(turn, shoe, p1h, p2h)

                    # check if the targeted stack is empty
                    if str(eval('ps' + str(pile))) == '||':
                        validPile = True

        # condition for if the player does not have a zero
        else:
            while not validPile:

                pos = getPlayCard()

                pile = choosePlayStack()
                # check if the chosen card can be legally played
                try:
                    if pos[:1] == 'g':

                        # checks if the chosen card is a joker and assigns it accordingly
                        if eval('p' + str(turn) + 'g').peek().getFace() == '*':
                            if str(eval('ps' + str(pile))) == '||':
                                eval('p' + str(turn) + 'g').peek().assign(0)
                            else:
                                eval('p' + str(turn) + 'g').peek().assign(eval('ps' + str(pile)).peekValue() + 1)
                            chosenCard = eval('p' + str(turn) + 'g').pop()
                            validPile = True

                        # checks if the chosen card is being played on a stack that has its previous card on top
                        elif eval('p' + str(turn) + 'g').peek().getValue() == eval('ps' + str(pile)).peekValue() + 1:
                            chosenCard = eval('p' + str(turn) + 'g').pop()
                            validPile = True
                        else:
                            print('Invalid Stack')
                    elif pos[:1] == 'h':

                        # checks if the chosen card is a joker and assigns it accordingly
                        selectCard = eval('p' + str(turn) + 'h').pop(int(pos[-1:]) - 1)
                        if selectCard.getFace() == '*':
                            if str(eval('ps' + str(pile))) == '||':
                                selectCard.assign(0)
                            else:
                                selectCard.assign(eval('ps' + str(pile)).peekValue() + 1)
                            chosenCard = selectCard
                            validPile = True

                        # checks if the chosen card is being played on a stack that has its previous card on top
                        elif selectCard.getValue() == eval('ps' + str(pile)).peekValue() + 1:
                            chosenCard = selectCard
                            validPile = True
                        else:
                            eval('p' + str(turn) + 'h').add(selectCard)
                            eval('p' + str(turn) + 'h').sort()
                            print('Invalid Stack')
                    elif pos[:1] == 'd':

                        # checks if the chosen card is being played on a stack that has its previous card on top
                        if eval('p' + str(turn) + 'd' + pos[-1:]).peek().getFace() == '*':
                            if str(eval('ps' + str(pile))) == '||':
                                eval('p' + str(turn) + 'd' + pos[-1:]).peek().assign(0)
                            else:
                                eval('p' + str(turn) + 'd' + pos[-1:]).peek().assign(
                                    eval('ps' + str(pile)).peekValue() + 1)
                            chosenCard = eval('p' + str(turn) + 'd' + pos[-1:]).pop()
                            validPile = True

                        # checks if the chosen card is being played on a stack that has its previous card on top
                        elif eval('p' + str(turn) + 'd' + pos[-1:]).peek().getValue() == eval(
                                'ps' + str(pile)).peekValue() + 1:
                            chosenCard = eval('p' + str(turn) + 'd' + pos[-1:]).pop()
                            validPile = True
                        else:
                            print('Invalid Stack')
                # deal with exception raised if playing to an invalid stack
                except Exception as x:
                    print(x)
                    if pos[:1] == 'h':
                        eval('p' + str(turn) + 'h').add(selectCard)
                        eval('p' + str(turn) + 'h').sort()
                        validPile = True
                        validPlayCard = False

        # runs only if a card is legally played
        if validPlayCard:

            # checks if a stack has become full
            removeList = eval('ps' + str(pile)).playCard(chosenCard)

            # if a stack is full then clear it and put it aside
            if removeList:
                removedCards.append(removeList)
                removedTimes += 1

                # when 5 stacks have been filled the cards put aside are shuffled and put back into the back of the shoe
                if removedTimes == 5:
                    shuffle(removedCards)
                    for i in removedCards:
                        if i == '*':
                            shoe.enqueue(Card(-1))
                        else:
                            shoe.enqueue(Card(int(i)))

            # check if the current player has won
            if checkWin(turn, p1g, p2g):
                continueGame = False

    print('Player', str(turn), 'wins!')


main()
