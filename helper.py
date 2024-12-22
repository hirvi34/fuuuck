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