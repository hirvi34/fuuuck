import unittest
from cardPack import Deck
from card import Card
from player import Player
from hand import Hand
from BJack import BlackJack
class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Sets up the test environment."""
        self.player = Player(name="Alice", saldo=100)

    def test_draw_card(self):
        """Tests drawing cards for a player."""
        deck = Deck()
        initial_card_count = len(self.player.hands[0].cards)
        self.player.draw_card(deck, 2)
        self.assertEqual(len(self.player.hands[0].cards), initial_card_count + 2)

    def test_add_hand(self):
        """Tests adding a new hand to the player."""
        hand_index = self.player.add_hand(bet=20)
        self.assertEqual(len(self.player.hands), 2)
        self.assertEqual(self.player.hands[hand_index].bet, 20)

    def test_delete_hand(self):
        """Tests deleting a hand from the player."""
        self.player.add_hand()
        self.player.delete_hand(1)
        self.assertEqual(len(self.player.hands), 1)

    def test_reset_hands(self):
        """Tests resetting the player's hands."""
        self.player.add_hand()
        self.player.reset_hands()
        self.assertEqual(len(self.player.hands), 1)
        self.assertEqual(len(self.player.hands[0].cards), 0)

    def test_add_money(self):
        """Tests updating the player's balance."""
        self.player.add_money(50)
        self.assertEqual(self.player.saldo, 150)
        self.player.add_money(-30)
        self.assertEqual(self.player.saldo, 120)
        with self.assertRaises(ValueError):
            self.player.add_money(-200)

    def test_bet(self):
        """Tests placing a bet."""
        bet_amount = self.player.bet(50)
        self.assertEqual(bet_amount, 50)
        self.assertEqual(self.player.saldo, 50)
        invalid_bet = self.player.bet(200)
        self.assertEqual(invalid_bet, -1)

class TestHand(unittest.TestCase):

    def setUp(self):
        """Sets up the test environment."""
        self.hand = Hand(bet=10)

    def test_add_card(self):
        """Tests adding a card to the hand."""
        card = Card("10", "hearts")
        self.hand.add_card(card)
        self.assertIn(card, self.hand.cards)

    def test_get_total(self):
        """Tests calculating the total value of the hand."""
        self.hand.cards = [Card("10", "hearts"), Card("A", "spades")]
        self.assertEqual(self.hand.get_total(), 21)
        self.hand.cards.append(Card("5", "diamonds"))
        self.assertEqual(self.hand.get_total(), 16)

    def test_is_busted(self):
        """Tests if the hand is busted."""
        self.hand.cards = [Card("10", "hearts"), Card("K", "spades"), Card("2", "diamonds")]
        self.hand.get_total()  # Update the busted state
        self.assertTrue(self.hand.is_busted())

    def test_reset(self):
        """Tests resetting the hand."""
        self.hand.cards = [Card("10", "hearts"), Card("5", "spades")]
        self.hand.reset()
        self.assertEqual(len(self.hand.cards), 0)
        self.assertEqual(self.hand.bet, 0)
        self.assertFalse(self.hand.busted)

class TestDeck(unittest.TestCase):

    def setUp(self):
        """Sets up the test environment."""
        self.deck = Deck()

    def test_shuffle(self):
        """Tests shuffling the deck."""
        initial_order = list(self.deck.cards)
        self.deck.shuffle()
        self.assertNotEqual(initial_order, self.deck.cards)

    def test_draw(self):
        """Tests drawing a card from the deck."""
        initial_size = len(self.deck.cards)
        card = self.deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.deck.cards), initial_size - 1)

    def test_recycle_discard_pile(self):
        """Tests recycling the discard pile back into the deck."""
        card = self.deck.draw()
        self.deck.discard_pile.append(card)
        self.deck.recycle_discard_pile()
        self.assertIn(card, self.deck.cards)
        self.assertEqual(len(self.deck.discard_pile), 0)

    def test_reset(self):
        """Tests resetting the deck to its full state."""
        self.deck.draw()  # Remove a card
        self.deck.reset()
        self.assertEqual(len(self.deck.cards), 52)
        self.assertEqual(len(self.deck.discard_pile), 0)

class TestBlackJack(unittest.TestCase):
    def setUp(self):
        """Sets up the test environment."""
        self.game = BlackJack()
        self.player = Player(name="Alice", saldo=200)
        self.game.add_player(self.player)

    def test_add_player(self):
        """Tests adding a player to the game."""
        new_player = Player(name="Bob", saldo=300)
        self.game.add_player(new_player)
        self.assertIn(2, self.game.players)
        self.assertEqual(self.game.players[2].name, "Bob")

    def test_remove_player(self):
        """Tests removing a player from the game."""
        self.game.remove_player(1)
        self.assertNotIn(1, self.game.players)

    def test_start_game(self):
        """Tests starting the game and dealing initial cards."""
        self.game.start_game()
        for player in self.game.players.values():
            for hand in player.hands:
                self.assertEqual(len(hand.cards), 2)

    def test_add_pot(self):
        """Tests adding a bet to a player's hand."""
        self.game.add_pot(player_id=1, bet_amount=50)
        self.assertEqual(self.player.saldo, 150)
        self.assertEqual(self.player.hands[0].bet, 50)

    def test_add_pot_insufficient_funds(self):
        """Tests adding a bet with insufficient funds."""
        self.game.add_pot(player_id=1, bet_amount=250)
        self.assertEqual(self.player.saldo, 200)
        self.assertEqual(self.player.hands[0].bet, 0)

    def test_double(self):
        """Tests doubling a player's bet and drawing a card."""
        self.game.add_pot(player_id=1, bet_amount=50)
        self.game.double(player_id=1, hand_index=0)
        self.assertEqual(self.player.hands[0].bet, 100)
        self.assertEqual(self.player.saldo, 100)
        self.assertEqual(len(self.player.hands[0].cards), 3)

    def test_double_insufficient_funds(self):
        """Tests doubling a bet with insufficient funds."""
        self.game.add_pot(player_id=1, bet_amount=150)
        self.game.double(player_id=1, hand_index=0)
        self.assertEqual(self.player.hands[0].bet, 150)
        self.assertEqual(self.player.saldo, 50)
        self.assertEqual(len(self.player.hands[0].cards), 2)

    def test_split_successful(self):
        """Tests a successful split."""
        self.player.hands[0].add_card(Card("8", "hearts"))
        self.player.hands[0].add_card(Card("8", "diamonds"))
        self.player.hands[0].bet = 50
        self.game.split(player_id=1, hand_index=0)

        self.assertEqual(len(self.player.hands), 2)
        self.assertEqual(len(self.player.hands[0].cards), 2)
        self.assertEqual(len(self.player.hands[1].cards), 2)
        self.assertEqual(self.player.hands[0].bet, 50)
        self.assertEqual(self.player.hands[1].bet, 50)
        self.assertEqual(self.player.saldo, 100)

    def test_split_invalid_conditions(self):
        """Tests split failure due to invalid conditions."""
        self.player.hands[0].add_card(Card("8", "hearts"))
        self.player.hands[0].add_card(Card("9", "diamonds"))  # Non-matching cards
        self.player.hands[0].bet = 50
        self.game.split(player_id=1, hand_index=0)

        self.assertEqual(len(self.player.hands), 1)
        self.assertEqual(len(self.player.hands[0].cards), 2)

    def test_hit(self):
        """Tests hitting (drawing a card) for a player's hand."""
        self.game.hit(player_id=1, hand_index=0)
        self.assertEqual(len(self.player.hands[0].cards), 1)

    def test_sum_of_hands(self):
        """Tests calculating the total values of all hands for a player."""
        self.player.hands[0].add_card(Card("10", "hearts"))
        self.player.hands[0].add_card(Card("A", "spades"))
        totals = self.game.sum_of_hands(player_id=1)
        self.assertEqual(totals, [21])

if __name__ == "__main__":
    unittest.main()
