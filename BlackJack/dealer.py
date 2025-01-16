from hand import Hand

class Dealer:
    def __init__(self, saldo):
        self.saldo = saldo
        self.hand = [Hand()]

    def deal_self(self):
        hand = self.hand[0]
        while hand.get_total() < 17:
            pass


    def draw_card(self):
        pass

    def get_total(self):
        pass

    def reset_hand(self):
        pass

    def pay_money(self, money):
        pass
