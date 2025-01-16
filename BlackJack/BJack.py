from cardPack import Deck
from helper import hand_index_check, money_check, split_check


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

        if not money_check(bet_amount, player):
            return

        if not hand_index_check(hand_index, player):
            return

        player.add_money(-bet_amount)
        player.hands[hand_index].bet = bet_amount
        print(f"{player.name} placed a bet of {bet_amount}.")

    def double(self, player_id, hand_index=0):
        """
        Doubles players bet and draws card automatically.

        :param hand_index: index of a hand
        :param player_id: ID of the player
        """
        player = self.players[player_id]

        if not money_check(player.hands[hand_index].bet, player):
            return

        if not hand_index_check(hand_index, player):
            return

        player.add_money(-player.hands[hand_index].bet)
        player.hands[hand_index].bet *= 2
        player.draw_card(self.deck, 1, hand_index)

    def split(self, player_id, hand_index=0):
        player = self.players[player_id]

        if split_check(player, hand_index):
            pass

        if not money_check(player.hands[hand_index].bet, player):
            return

        if not hand_index_check(hand_index, player):
            return

        player.add_money(-player.hands[hand_index].bet)

        new_hand = player.add_hand(player.hands[hand_index].bet)

        move_card = player.hands[hand_index].cards.pop(1)
        player.hands[new_hand].add_card(move_card)

        player.draw_card(self.deck, 1, hand_index)
        player.draw_card(self.deck, 1, move_card)

    def hit(self, player_id, hand_index=0):
        player = self.players[player_id]
        player.draw_card(self.deck, 1, hand_index)
        if player.hands.is_busted:
            player.hands.busted = True

    def stay(self, player_id, hand_index=0):
        player = self.players[player_id]

        if player.hands.is_busted:
            player.hands.busted = True

    def sum_of_hands(self, player_id):
        """
        Displays the total values of all hands for a specific player.

        :param player_id: ID of the player
        :return: List of totals for each hand
        """
        player = self.players[player_id]
        totals = [hand.get_total() for hand in player.hands]
        return totals
