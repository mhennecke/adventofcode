import os

from functools import cmp_to_key
from collections import Counter

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


card_order = "AKQT98765432J"
card_pos = {c: p for (p, c) in enumerate(card_order)}


def read_data(file_name: str) -> list[tuple[str, int]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            d = line.strip().split(' ')
            data.append((d[0], int(d[1])))
    return data


def compare_hands(h1: tuple[str, int], h2: tuple[str, int]):
    h1c = h1[0]
    h2c = h2[0]
    h1_t = hand_type(h1c)
    h2_t = hand_type(h2c)
    if h1_t != h2_t:
        return h1_t - h2_t
    else:
        for i in range(len(h1c)):
            if h1c[i] == h2c[i]:
                if i < len(h1c):
                    continue
            else:
                return card_order.find(h2c[i]) - card_order.find(h1c[i])
        return 0


def hand_type(hand: str) -> float:
    # 5: Five of a kind, where all five cards have the same label: AAAAA
    # 4: Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    # 3.5: Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    # 3: Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    # 2: Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    # 1: One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    # 0: High card, where all cards' labelslabels are distinct: 23456

    temp_hand = hand.replace('J', '')
    temp_cards = Counter(temp_hand)
    best_replacement = temp_cards.most_common(1)
    if best_replacement:
        hand = hand.replace('J', best_replacement[0][0])
    else:
        # all Jacks
        pass

    cards = Counter(hand)
    top_cards = cards.most_common(2)
    occ = top_cards[0][1]
    occ_next = top_cards[1][1] if len(top_cards) == 2 else 0

    if occ == 5 or occ == 4:
        return occ
    elif occ == 3 and occ_next == 2:
        return 3.5
    elif occ == 3:
        return 3
    elif occ == 2 and occ_next == 2:
        return 2
    elif occ == 2:
        return 1
    elif occ == 1:
        return 0
    else:
        raise ValueError()


def total_bids(hands: list[tuple[str, int]]) -> int:
    hands.sort(key=cmp_to_key(compare_hands))
    [print(f'{i:<3} {c[0]} {(i + 1) * c[1]}') for i, c in enumerate(hands)]
    return sum([(i + 1) * h[1] for i, h in enumerate(hands)])


test_data = read_data(test_input_file)
assert hand_type(test_data[0][0]) == 1
assert hand_type(test_data[1][0]) == 4
assert hand_type(test_data[2][0]) == 2
assert hand_type(test_data[3][0]) == 4
assert hand_type(test_data[4][0]) == 4
assert hand_type('JJJJJ') == 5
assert hand_type('3J3JJ') == 5
assert hand_type('22422') == 4
assert compare_hands(('25J4J', 0), ('Q3QQ4', 0)) < 0
assert compare_hands(('22K2K', 0), ('Q3QQ4', 0)) > 0
assert compare_hands(('K2K2K', 0), ('K3KK3', 0)) < 0
assert compare_hands(('KK22K', 0), ('K3KK3', 0)) > 0
assert compare_hands(('JJJJJ', 0), ('Q3QQ4', 0)) > 0
assert compare_hands(('33332', 0), ('2AAAA', 0)) > 0
assert compare_hands(('77888', 0), ('77788', 0)) > 0
assert compare_hands(('23456', 0), ('23457', 0)) < 0
assert compare_hands(('J4444', 0), ('8JJJJ', 0)) < 0
assert compare_hands(('J4444', 0), ('KJJJJ', 0)) < 0

assert total_bids(test_data) == 5905

data = read_data(input_file)
print(total_bids(data))
