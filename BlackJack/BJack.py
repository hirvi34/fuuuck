﻿from cardPack import Deck

class BlackJack:
    """
    BlackJack class manages the core logic of a blackjack game.
    It handles players, the deck, and betting mechanics.
    """

    def __init__(self):
        # Dictionary to store player objects, keyed by their ID
        self.players = {}

        # Initialize a deck of cards
        self.deck = Deck()

    def add_player(self, player):
        """
        Adds a player to the game.

        :param player: Player object to add
        """
        if player.id in self.players:
            print(f"Player {player.name} is already in the game.")
        else:
            self.players[player.id] = player
            print(f"Player {player.name} has been added to the game.")

    def remove_player(self, player_id):
        """
        Removes a player from the game.

        :param player_id: ID of the player to remove
        """
        if player_id in self.players:
            del self.players[player_id]
            print(f"Player with ID {player_id} has been removed.")
        else:
            print(f"No player with ID {player_id} found.")

    def start_game(self):
        """
        Starts the game by shuffling the deck and dealing two cards to each hand of every player.
        """
        self.deck.shuffle()

        # Deal two cards to each player's initial hand
        for player in self.players.values():
            for hand in player.hands:
                hand.reset()  # Reset the hand to start fresh
                player.draw_card(self.deck, 2, hand_index=player.hands.index(hand))
                print(f"{player.name}'s Hand: {hand.cards} (Total: {hand.get_total()})")

    def add_pot(self, player_id, bet_amount, hand_index =0):
        """
        Adds a player's bet for their initial hand.

        :param hand_index: index of a hand
        :param player_id: ID of the player
        :param bet_amount: Bet amount for the player's hand
        """
        player = self.players[player_id]

        if bet_amount > player.saldo:
            print("Insufficient funds for this bet.")
            return

        if hand_index < 0 or hand_index >= len(player.hands):
            print(f"Invalid hand index. Player {player.name} has {len(player.hands)} hands.")
            return

        player.add_money(-bet_amount)
        player.hands[hand_index].bet = bet_amount
        print(f"{player.name} placed a bet of {bet_amount} on their first hand.")

    def double(self, player_id, hand_index=0):
        pass

    def split(self, player_id, hand_index=0):
        pass

    def hit(self, player_id, hand_index=0):
        pass

    def stay(self, player_id, hand_index=0):
        pass

    def sum_of_hands(self, player_id):
        """
        Displays the total values of all hands for a specific player.

        :param player_id: ID of the player
        :return: List of totals for each hand
        """
        player = self.players[player_id]
        totals = [hand.get_total() for hand in player.hands]
        return totals