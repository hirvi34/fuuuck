from hand import Hand

class Player:
    """
    Represents a player in the game. Manages their hand, balance, and betting.
    """
    id_counter = 1  # Class-level counter to assign unique player IDs

    def __init__(self, name, saldo):
        self.id = Player.id_counter
        Player.id_counter += 1
        self.name = name
        self.saldo = saldo  # Player's balance
        self.hands = [Hand()]  # List of Hand objects

    def draw_card(self, deck, num=1, hand_index=0):
        """
        Draws cards for the specified hand.

        :param deck: Deck object to draw cards from
        :param num: Number of cards to draw
        :param hand_index: Index of the hand to add cards to
        """
        for _ in range(num):
            if deck.remaining_cards() > 0:
                card = deck.draw()
                self.hands[hand_index].add_card(card)
            else:
                print("No more cards in the deck.")
                break

    def add_hand(self, bet=0):
        """
        Adds a new hand to the player's list of hands with an optional bet.

        :param bet: Bet amount for the new hand
        :return: Index of the new hand
        """
        new_hand = Hand(bet)
        self.hands.append(new_hand)
        return len(self.hands) - 1

    def delete_hand(self, hand_index):
        """
        Deletes a specific hand by index.

        :param hand_index: The index of the hand to delete.
        """
        if hand_index < 0 or hand_index >= len(self.hands):
            raise IndexError("Invalid hand index.")
        if len(self.hands) == 1:
            print("for safety purposes plz dont delete last hand")
        else:
            del self.hands[hand_index]

    def reset_hands(self):
        """
        Resets the player's hands for a new game.
        Keeps only the first hand and clears its state.
        """
        # Clear all hands except the first one
        while len(self.hands) > 1:
            self.hands.pop(len(self.hands)-1)  # Always delete the last hand for simplicity

        # Reset the first hand
        self.hands[0].reset()

    def add_money(self, amount):
        """
        Updates the player's balance.

        :param amount: Amount to add (negative for deductions)
        """
        if self.saldo + amount < 0:
            raise ValueError("Insufficient funds.")
        self.saldo += amount

    def show_hands(self):
        """
        Displays all the player's hands.

        :return: String representation of the player's hands
        """
        return [str(hand) for hand in self.hands]


    def bet(self, bet_amount):
        """
        Places a bet by deducting from the player's balance.

        :param bet_amount: Amount to bet
        :return: Bet amount if valid, -1 if the bet is invalid
        """
        if bet_amount > self.saldo:
            print("Insufficient funds for this bet.")
            return -1
        elif bet_amount <= 0:
            print("Bet amount must be greater than zero.")
            return -1
        else:
            self.saldo -= bet_amount
            return bet_amount
