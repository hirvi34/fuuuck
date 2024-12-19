import itertools
import random
from card import Card


class Deck:
    """
    Represents a deck of playing cards. Handles shuffling, drawing,
    resetting, and recycling cards.
    """

    def __init__(self):
        # Initialize the deck with all possible cards (52 cards total)
        num = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        symbol = ["spades", "diamonds", "clubs", "hearts"]
        self.cards = [Card(value, suit) for value, suit in itertools.product(num, symbol)]

        # A pile to hold discarded cards
        self.discard_pile = []

        # Shuffle the deck on initialization
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def draw(self):
        """
        Draws a card from the deck. If the deck is empty, raises an error.

        :return: Card object drawn from the deck
        """
        if not self.cards:
            raise ValueError("Deck is empty")
        card = self.cards.pop()  # Remove the top card
        self.discard_pile.append(card)  # Move it to the discard pile
        return card

    def add_card(self, card):
        """
        Adds a valid card back to the deck.

        :param card: Card object to add
        """
        if card not in itertools.product(
                ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"],
                ["spades", "diamonds", "clubs", "hearts"]
        ):
            raise ValueError("Invalid card.")
        self.cards.append(card)

    def reset(self):
        """
        Resets the deck to its full 52-card state and shuffles it.
        """
        self.cards = [
            Card(value, suit)
            for value, suit in itertools.product(
                ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"],
                ["spades", "diamonds", "clubs", "hearts"]
            )
        ]
        self.discard_pile.clear()  # Clear the discard pile
        self.shuffle()

    def remaining_cards(self):
        """
        Returns the number of remaining cards in the deck.

        :return: Integer count of remaining cards
        """
        return len(self.cards)

    def recycle_discard_pile(self):
        """
        Recycles the discard pile back into the deck and shuffles it.
        Raises an error if the discard pile is empty.
        """
        if not self.discard_pile:
            raise ValueError("No cards in the discard pile to recycle.")
        self.cards.extend(self.discard_pile)
        self.discard_pile.clear()
        self.shuffle()
