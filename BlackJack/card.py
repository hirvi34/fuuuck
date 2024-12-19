class Card:
    """
    Represents a single playing card with a value and a suit.
    """
    def __init__(self, value: str, suit: str):
        self.value = value  # Value of the card (2-10, J, Q, K, A)
        self.suit = suit  # Suit of the card (spades, diamonds, clubs, hearts)

    def __repr__(self):
        """
        String representation of the card for display.
        """
        return f"{self.value} of {self.suit}"
