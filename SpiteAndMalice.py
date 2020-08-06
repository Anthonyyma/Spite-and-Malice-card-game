import random
from lectureStructures import Queue


class Card:
    def __init__(self, value):
        self.__value = value
        if self.__value != -1:
            self.__face = str(self.__value)
        else:
            self.__face = '*'

    def assign(self, value):
        """
        Assigns new value to card if face is '*'
        """
        assert value in range(0, 10) or value == -1, 'Error: Invalid value'
        try:
            if self.getFace() != '*':
                # raises exception if trying to assign value to a non-joker card
                raise Exception
        except AssertionError:
            raise
        except:
            print('Error: Can not change the value of card')

        else:
            # assign joker card to new value
            self.__value = value

    def getValue(self):
        """
        Returns the value of a card
        """
        return self.__value

    def getFace(self):
        """
        Returns the face of a card
        """
        return self.__face

    def __str__(self):
        """
        Generates a string for the card class
        """
        return '[' + self.__face + ']'

    def __repr__(self):
        """
        Generates a repr for the card class
        """
        return self.__str__() + '.' + str(self.__value)


class PlayStack:
    def __init__(self, ):
        self.cards = []

    def peekValue(self):
        """
        Returns the value of the card on top of self.cards
        """
        try:
            return self.cards[-1:][0].getValue()
        except:
            raise Exception('Error: No cards in the playing stack')

    def peekFace(self):
        """
        Returns the face of the card on top of self.cards
        """
        try:
            return self.cards[-1:].getFace()
        except:
            raise Exception('Error: No cards in the playing stack')

    def playCard(self, card):
        """
        Pushes a card on top of the cards stack
        """
        validPlay = False
        # check is the cards stack is empty
        if not self.cards:
            # play the card if the card has a value of zero
            if card.getValue() == 0:
                self.cards.append(card)
                validPlay = True
            else:
                raise Exception('Error: Card rejected')
        else:
            # only add the card to the cards stack if the card on top is of lower value
            if self.cards[-1:][0].getValue() < card.getValue():
                self.cards.append(card)
                validPlay = True
            else:
                raise Exception('Error: Card rejected')

        # if the card played is a 9 then empty the stack and returns a list of the card faces
        if card.getValue() == 9 and validPlay:
            currentCards = []
            for i in self.cards:
                # get a list of the card faces to return
                currentCards.append(i.getFace())
            self.cards = []
            return currentCards
        else:
            return []

    def __str__(self):
        """
        Generates a string for the play stack class
        """
        string = ''
        for i in self.cards:
            string += '[' + str(i.getValue()) + ']'
        return '|' + string + '|'


class Hand:
    def __init__(self):
        self.__hand = []

    def sort(self):
        """
        Sorts the cards in creasing order by value
        """
        self.__hand.sort(key=lambda x: x.getValue())

    def pop(self, i=-1):
        """
        Returns and removes the card at position i
        """
        assert self.__hand != []
        if i == -1:
            return self.__hand.pop()
        else:
            return self.__hand.pop(i)

    def index(self, v):
        """
        Returns the index of the first card with value v
        """
        index = 0
        found = False
        for i in self.__hand:
            if i.getValue() == v:
                found = True
            else:
                index += 1
        if found:
            return index
        else:
            # return an index of -1 if the value is not found
            return -1

    def check0(self):
        """
        Returns the index of the first card in the hand
        """
        index = 0
        found = False
        for i in self.__hand:
            if i.getValue() == 0:
                found = True
            else:
                index += 1
        if found:
            return index
        else:
            # return an index of -1 if there are no zeros
            return -1

    def size(self):
        """
        Returns the number of cards in the hand
        """
        return len(self.__hand)

    def add(self, cardList):
        """
        Adds Cards in the cardList to the hand
        """
        assert len(self.__hand) + 1 <= 5
        self.__hand.append(cardList)

    def __str__(self):
        """
        Generates a string for the hand class
        """
        string = ''
        for i in self.__hand:
            string += str(i)
        return '[' + string + ']'


def shuffle(cardList):
    """
    Puts the given list of cards into ascending order
    """
    shuffledList = []
    shuffledQueue = Queue()

    # dequeues all of the cards and puts them into a list
    while not cardList.isEmpty():
        shuffledList.append(cardList.dequeue())

    # randomly pop cards from the list and enqueue them into a queue
    while len(shuffledList) > 0:
        shuffledQueue.enqueue(shuffledList.pop(random.randint(0, len(shuffledList) - 1)))
    return shuffledQueue


def displayGame(p1Cards, p2Cards, pslist):
    """
    Displays all of the stacks to the screen
    """
    # display player 1's stacks
    print('-' * 50)
    print('Player 1 Hand', str(p1Cards[0]))
    for i in range(1, 5):
        if p1Cards[2][i - 1].isEmpty():
            print('Player 1 Discard', str(i) + ':', str(p1Cards[2][i - 1]))
        else:
            print('Player 1 Discard', str(i) + ':', '[' + str(p1Cards[2][i - 1].peek().getValue()) + ']')
    print('Player 1 Goal', p1Cards[1].peek(), p1Cards[1].size(), 'cards left')
    print()

    # display the play stacks
    for i in range(1, 5):
        print('Play Stack', str(i) + ':', str(pslist[i - 1]))
    print()

    # display player 2's stacks
    print('Player 2 Hand', str(p2Cards[0]))
    for i in range(1, 5):
        if p2Cards[2][i - 1].isEmpty():
            print('Player 2 Discard', str(i) + ':', str(p2Cards[2][i - 1]))
        else:
            print('Player 2 Discard', str(i) + ':', '[' + str(p2Cards[2][i - 1].peek().getValue()) + ']')
    print('Player 2 Goal', p2Cards[1].peek(), p2Cards[1].size(), 'cards left')


def getDecision(turn):
    """
    Get input from player of whether they want to play or discard
    """
    print('-' * 50)
    decision = input('Player' + str(turn) + ', choose action: P (play) or X (discard/end turn): ')[:1].upper()
    while decision not in ['P', 'X']:
        print('Invalid Input')
        decision = input('Player' + str(turn) + ', choose action: P (play) or X (discard/end turn): ')[:1].upper()

    return decision


def getDiscard():
    """
    Get input of which card they want to discard
    """
    # get the position of the card they want to discard
    pos = input('Discard from where: hi = hand at position i (1-5); g = goal: ').lower()
    while pos[:1] not in ['h', 'g'] or pos[:1] == 'h' and int(pos[-1:]) not in range(1, 6):
        print('Invalid Input')
        pos = input('Discard from where: hi = hand at position i (1-5); g = goal: ').lower()

    # get the discard pile they want to discard to
    pile = int(input('Which Discard Pile are you targeting (1-4)?: '))
    while pile not in range(1, 5):
        print('Invalid Input')
        pile = input('Which Discard Pile are you targeting (1-4)?: ')

    return (pos, pile)


def getPlayCard():
    """
    Get input for which card they want to play
    """
    # get the position of the card they want to play
    pos = input('Play from where: hi = hand at position i (1-5); g = goal; dj = discard pile j (1-4)?: ').lower()
    while pos[:1] not in ['h', 'g', 'd'] or (pos[:1] == 'h' and int(pos[-1:]) not in range(1, 6)) or (
            pos[:1] == 'd' and int(pos[-1:]) not in range(1, 5)):
        print('Invalid Input')
        pos = input('Play from where: hi = hand at position i (1-5); g = goal; dj = discard pile j (1-4)?: ').lower()

    return pos


def choosePlayStack():
    """
    Ask the player which play stack they want to play on
    """
    # get the play stack that they want to play to
    pile = int(input('Which play stack are you targeting (1-4)?: '))
    while pile not in range(1, 5):
        print('Invalid Input')
        pile = input('Which play stack are you targeting (1-4)?: ')

    return int(pile)


def checkForZero(turn, p1Cards, p2Cards):
    """
    Checks if the player has any playable jokers in any of their piles
    """
    # checks the players hand for zeros
    if eval('p' + str(turn) + 'Cards' + '[0]').check0() != -1:
        return True

    # checks the players goal stack for a zero on top
    elif eval('p' + str(turn) + 'Cards' + '[1]').peek().getValue() == 0:
        return True

    # checks the players discard stacks for zeros on top
    else:
        for i in range(1, 5):
            if not eval('p' + str(turn) + 'Cards' + '[2]')[i - 1].isEmpty():
                if eval('p' + str(turn) + 'Cards' + '[2]')[i - 1].peek().getValue() == 0:
                    return True
    return False


def onlyZeros(turn, p1Cards, p2Cards):
    """
    Check if the player only has zeros in their piles
    """
    # checks the players hand has only zeros
    if eval('p' + str(turn) + 'Cards' + '[0]').check0() != -1:

        # checks if the players goal stack has a zero on top
        if eval('p' + str(turn) + 'Cards' + '[1]').peek().getValue() == 0:

            # checks if the players discard stacks either are empty or only have zeros on top
            for i in range(1, 5):
                if eval('p' + str(turn) + 'Cards' + '[2]')[i - 1].isEmpty():
                    pass
                else:
                    if eval('p' + str(turn) + 'Cards' + '[2]')[i - 1].peek().getValue() == 0:
                        pass
                    else:
                        return False
            return True
    return False


def replenishHand(turn, shoe, p1h, p2h):
    """
    player draws cards from the shoe until they have 5 cards in their hand
    """
    # add cards from the shoe to the hand until the hand has 5 cards
    while eval('p' + str(turn) + 'h').size() < 5:
        eval('p' + str(turn) + 'h').add(shoe.dequeue())
    eval('p' + str(turn) + 'h').sort()


def checkWin(turn, p1g, p2g):
    """
    Checks if the current player has won the game
    """
    # check if the players goal stack is empty
    if eval('p' + str(turn) + 'g').isEmpty():
        return True
    else:
        return False
