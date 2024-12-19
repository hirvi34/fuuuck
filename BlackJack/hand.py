class Hand:
    """
    Represents a single hand of cards for a player in Blackjack.
    Manages cards, bet size, and hand state (busted, etc.).
    """
    def __init__(self, bet=0):
        self.cards = []  # List to store Card objects
        self.bet = bet  # Bet amount for this hand
        self.busted = False  # Track if the hand is busted

    def add_card(self, card):
        """
        Adds a card to the hand and checks if the hand is busted.

        :param card: Card object to add to the hand
        """
        self.cards.append(card)
        if self.get_total() > 21:
            self.busted = True



    def get_total(self):
        """
        Calculates the total value of the hand, adjusting for Aces.

        :return: Integer total value of the hand
        """
        total = 0
        aces = 0
        for card in self.cards:
            if card.value.isdigit():  # Numeric cards (2-10)
                total += int(card.value)
            elif card.value == "A":  # Aces
                total += 11
                aces += 1
            else:  # Face cards (J, Q, K)
                total += 10

        # Adjust Aces from 11 to 1 if necessary
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_busted(self):
        """
        Checks if the hand has busted (value > 21).

        :return: True if busted, False otherwise
        """
        return self.busted

    def reset(self):
        """
        Resets the hand to its initial state.
        """
        self.cards.clear()
        self.bet = 0
        self.busted = False

    def __repr__(self):
        """
        String representation of the hand.
        """
        return f"Hand({self.cards}, Bet: {self.bet}, Busted: {self.busted})"
