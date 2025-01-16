


def hand_index_check(hand_index, player):
    if hand_index < 0 or hand_index >= len(player.hands):
        print(f"Invalid hand index for {player.name}. Player has {len(player.hands)} hands.")
        return False
    return True

def money_check(bet_amount, player):
    if bet_amount > player.saldo:
        print("insufficient funds")
        return False
    return True

def split_check(player, hand_index):
    if len(player.hands[hand_index].cards)>2:
        print("hand too large")
        return False
    if player.hands[hand_index].get_value(0) == player.hands[hand_index].get_value(1):
        print("different value pair")
        return False
    return True