# ----------------------------------------------------
# Assignment 2: Klondike
# Purpose of code: to simulate the card game 'Klondike', for grades
# NOTE: I HAVE DONE THE CHALLENGE AND HAVE IMPLEMENTED THE ALTERNATING COLOR RULE. KEEP IN MIND IN TESTING.
# Author: Sajad Ahmadi
# Collaborators/references: nobody.
# ----------------------------------------------------
class Card:
    """
    A class to represent a card object

    Attributes
        suit : str
            string that represents the suit the card is a part of
        rank : str
            string representation of the rank of the card
        visibility : bool
            boolean value that represents whether the card is facing up or down
    """
    def __init__(self, suit, rank):
        """
        initializes the attributes of the card
        :param suit: suit of the card
        :param rank: rank of the card
        """
        self.__suit = suit
        self.__rank = rank
        self.__visible = False

    def invisibleCard(self):
        """
        communicates whether the card is facing down or up
        :return self.__visible: boolean value for whether the card is facing up or down
        """
        return self.__visible

    def faceupCard(self, visible):
        """
        method that allows us to change the visibility attribute of the card
        :param visible: boolean value that communicates if the card should be facing down or up
        """
        self.__visible = visible

    def rankCard(self):
        """
        returns the rank of the card
        :return self.__rank: string of the rank of the card
        """
        return self.__rank

    def suitCard(self):
        """
        returns suit of the card
        :return self.__suit: string of the suit of the card
        """
        return self.__suit

    def __repr__(self):
        """
        displays the card's rank, suit and visibility status in string format
        :return: string representation of the card's rank, suit and visibility
        """
        if self.__visible:
            return str(self.__rank) + str(self.__suit[0].lower()) + '+'
        else:
            return str(self.__rank) + str(self.__suit[0].lower()) + '-'

    def __str__(self):
        """
        represents the card in a string format
        :return: string representation of the card's rank and suit
        """
        if self.__visible:
            return str(self.__rank) + str(self.__suit[0].lower())
        else:
            return '??'


class Deck:
    """
    represents a deck or 'pile'

    Attributes:
        name::str
            name of the deck
        items :: list
            stack used to represent the LIFO style of the game
    """
    def __init__(self, name):
        """
        initializes a deck object
        :param name: name of the deck
        """
        self.__name = name
        self.__items = []

    def nameDeck(self):
        """
        returns name of the deck
        :return self.__name: name of the deck
        """
        return self.__name

    def sizeDeck(self):
        """
        returns size of the deck
        :return len(self.__items): length of the list of items
        """
        return len(self.__items)

    def isemptyDeck(self):
        """
        checks if the list is empty
        :return bool: returns True if deck is empty and False if it is not empty
        """
        return self.__items == []

    def pushDeck(self, card):
        """
        adds cards to the back of the deck
        :param card: card object being pushed onto the deck
        """
        self.__items.append(card)

    def popDeck(self):
        """
        removes and returns the last card in the deck
        :return: the last item in the deck
        """
        return self.__items.pop()

    def peekDeck(self):
        """
        gives a preview as to what card is on the top of the stack
        :return: last card in the stack
        """
        return self.__items[len(self.__items) - 1]

    def __repr__(self):
        """
        represents the deck with the representations of the cards
        :return: string that resembles the deck with a representation of the cards
        """
        stringRep = '[ '
        for card in self.__items[::-1]:
            stringRep += repr(card) + ' '
        return stringRep + ']'

    def __str__(self):
        """
        represents the deck in a string format with a string representation of the cards
        :return: string that resembles the list with a string representation of the cards
        """
        stringRep = '[ '
        for card in self.__items[::-1]:
            stringRep += str(card) + ' '
        return stringRep + ']'


def load(filename):
    """
    loads a saved game file
    :param filename: the name of the file to be opened
    :return decks: a dictionary containing all the decks
    """
    assert filename.endswith('.txt'), 'Invalid file type'
    file = open(filename, 'r')
    lines = file.readlines()
    decks = {}
    for line in lines:
        pile = line.strip().split('[')
        deckName = pile[0].strip()
        if deckName.startswith('PILE'):
            deckName = deckName[5]
        cardsinDeck = pile[1].strip(']').strip().split()
        newDeck = loadDecks(deckName, cardsinDeck[::-1])
        decks[deckName] = newDeck
    return decks


def loadDecks(name, cards):
    """
    loads the decks up with cards
    :param name: name of the deck
    :param cards: a list of the cards that belong to the deck
    :return pile: a Deck object with the cards loaded into it
    """
    pile = Deck(name)
    for card in cards:
        if card[1] == 's':
            suit = 'Spades'
        elif card[1] == 'd':
            suit = 'Diamonds'
        elif card[1] == 'h':
            suit = 'Hearts'
        else:
            suit = 'Clubs'
        newCard = Card(suit, card[0])
        newCard.faceupCard(card[2] == '+')
        pile.pushDeck(newCard)
    return pile


def loadBoard(decks, cheat):
    """
    prints the game board
    :param decks: dictionary of the piles or decks
    :param cheat: boolean value that specifies if cheat is enabled or not
    """
    print('Klondike!')
    for deck in decks.values():
        if len(deck.nameDeck()) == 1:
            pileRep = f'{"PILE-" + deck.nameDeck():>8} '
        else:
            pileRep = f'{deck.nameDeck().capitalize():>8} '
        if cheat:
            pileRep += repr(deck)
        else:
            pileRep += str(deck)
        print(pileRep)


def move(origin, to, decks):
    """
    moves a card from one deck to another
    :param origin: where the card is being moved FROM
    :param to: where the card is attempting to be moved TO
    :param decks: dictionary of the decks
    """
    ranks = ['K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'A']  # ranks the cards
    reds = [{'Hearts', 'Diamonds'},{'Hearts','Hearts'},{'Diamonds','Diamonds'}]  # set to prevent a red being placed on a red
    blacks = [{'Clubs', 'Spades'},{'Clubs','Clubs'},{'Spades','Spades'}]  # set to prevent a black being placed on a black
    assert to != ('Stock' or 'Discard'), 'Cannot place card in Stock and Discard piles.'
    assert not decks[origin].isemptyDeck(), 'Deck is empty'
    if to != 'suit':
        assert to in decks.keys(), 'Invalid deck'
        assert origin in decks.keys(), 'Invalid deck'
        movingCards = [decks[origin].popDeck()]
        cutoff = False
        while not decks[origin].isemptyDeck() and decks[origin].peekDeck().invisibleCard() and not cutoff:
            if decks[to].isemptyDeck():
                movingCards.append(decks[origin].popDeck())
            elif ranks.index(decks[origin].peekDeck().rankCard().upper()) < ranks.index(decks[to].peekDeck().rankCard().upper()) + 1:
                cutoff = True
            elif ranks.index(decks[origin].peekDeck().rankCard().upper()) > ranks.index(decks[to].peekDeck().rankCard().upper()) + 1:
                movingCards.append(decks[origin].popDeck())
            elif ranks.index(decks[origin].peekDeck().rankCard().upper()) == ranks.index(decks[to].peekDeck().rankCard().upper()) + 1:
                movingCards.append(decks[origin].popDeck())
                cutoff = True

        if decks[to].isemptyDeck() or movingCards[len(movingCards)-1].rankCard() == 'K':
            if movingCards[len(movingCards) - 1].rankCard() == 'K':
                assert decks[to].isemptyDeck(), 'Invalid Move'
                while movingCards:
                    decks[to].pushDeck(movingCards.pop(len(movingCards) - 1))
            # condition if the TO deck is empty and the card at the top of the stack being moves id not a King
            else:
                while movingCards:
                    decks[origin].pushDeck(movingCards.pop(len(movingCards) - 1))
                raise AssertionError('Invalid Move')
        elif ranks.index(movingCards[len(movingCards) - 1].rankCard().upper()) != ranks.index(decks[to].peekDeck().rankCard().upper()) + 1 or ({movingCards[len(movingCards) - 1].suitCard(), decks[to].peekDeck().suitCard()} in reds) or ({movingCards[len(movingCards) - 1].suitCard(), decks[to].peekDeck().suitCard()} in blacks):
            while movingCards:
                decks[origin].pushDeck(movingCards.pop(len(movingCards) - 1))
            raise AssertionError('Invalid Move')
        else:
            while movingCards:
                decks[to].pushDeck(movingCards.pop(len(movingCards) - 1))
    else:
        toDeck = decks[decks[origin].peekDeck().suitCard()]
        if decks[origin].peekDeck().rankCard() == 'A':
            toDeck.pushDeck(decks[origin].popDeck())
        else:
            assert not toDeck.isemptyDeck(), 'Invalid move'
            assert ranks.index(decks[origin].peekDeck().rankCard().upper()) == ranks.index(toDeck.peekDeck().rankCard().upper()) - 1, 'Unable to move to suit position'
            toDeck.pushDeck(decks[origin].popDeck())
    if not decks[origin].isemptyDeck():
        decks[origin].peekDeck().faceupCard(True)  # turns the next card facing up


def discard(decks):
    """
    discards 3 cards from the stock pile into the discard pile
    :param decks: dictionary of decks
    """
    assert not decks['Stock'].isemptyDeck(), 'Stock is empty and cannot be discarded'
    if decks['Stock'].sizeDeck() > 3:
        for i in range(3):
            discarded = decks['Stock'].popDeck()
            discarded.faceupCard(False)
            decks['Discard'].pushDeck(discarded)
            decks['Stock'].peekDeck().faceupCard(True)
    else:
        while decks['Stock'].sizeDeck() != 0:
            discarded = decks['Stock'].popDeck()
            discarded.faceupCard(False)
            decks['Discard'].pushDeck(discarded)


def reset(decks):
    """
    resets the cards from the discard pile back into the stock pile
    :param decks: dictionary of decks
    """
    assert decks['Stock'].isemptyDeck(), 'Stock pile is not empty yet'
    transfer = []
    while not decks['Discard'].isemptyDeck():
        transfer.append(decks['Discard'].popDeck())
    for card in transfer[::-1]:
        decks['Stock'].pushDeck(card)
    decks['Stock'].peekDeck().faceupCard(True)


def save(filename, decks):
    """
    saves the current game state into a text file
    :param filename: name of the file to write the game state to
    :param decks: dictionary of decks
    """
    assert filename.endswith('.txt'), 'Invalid filename'
    savedGame = open(filename, 'w')
    for deck in decks.keys():
        if len(decks[deck].nameDeck()) == 1:
            deckLine = f"{'PILE-' + decks[deck].nameDeck():>8} " + repr(decks[deck])
        else:
            deckLine = f"{decks[deck].nameDeck().capitalize():>8} " + repr(decks[deck])
        savedGame.write(deckLine + '\n')


def main():
    """
    runs the game
    """
    print('Welcome to Klondike!')
    play = True
    decks = {}
    while play:
        playerMove = input('Your move: ')
        print(f'Executing: {playerMove.split()}')
        if 'done' in playerMove.split():
            print('Thank you for playing')
            play = False
        elif 'load' in playerMove.split():
            try:
                decks = load(playerMove.split()[1])
            except FileNotFoundError as err:
                msg = ''.join(err.args)
                print(msg)
            except AssertionError as ex:
                msg = ''.join(ex.args)
                print(msg)
            except IndexError:
                print('Please input a valid filename')
            print(decks)
        elif 'board' in playerMove.split():
            loadBoard(decks, False)
        elif playerMove == 'cheat'.strip():
            loadBoard(decks, True)
        elif 'move' in playerMove.split():
            if len(playerMove.split()) == 3:
                playerCmd = playerMove.split(' ')
                try:
                    move(playerCmd[1].capitalize(), playerCmd[2], decks)
                except KeyError:
                    print('Those piles do not exist')
                except AssertionError as ex:
                    msg = ''.join(ex.args)
                    print(msg)
            else:
                print('Invalid Entry')
        elif 'comment' in playerMove.split():
            print(f'Comment: {" ".join(playerMove.split()[1:len(playerMove)])}')
        elif 'discard' in playerMove.split():
            try:
                discard(decks)
            except AssertionError as ex:
                msg = ''.join(ex.args)
                print(msg)
        elif playerMove == 'reset' in playerMove.split():
            try:
                reset(decks)
            except AssertionError as ex:
                msg = ''.join(ex.args)
                print(msg)
        elif 'save' in playerMove.split():
            try:
                save(playerMove.strip().split()[1], decks)
            except AssertionError as err:
                msg = ''.join(err.args)
                print(msg)
        else:
            print('Invalid input, please try again')


if __name__ == '__main__':
    main()
